import json
import time
import subprocess
import requests
from datetime import datetime

LOG_PATH = "var/log/cowrie/cowrie.json"
CEREBRO_URL = "http://IP_DE_TU_SERVIDOR:5000/estimular"  # ajustar a tu red
ALERTAS_PATH = "var/log/cowrie/alertas_criticas.log"

PICKLE_PATH = "/ruta/a/cowrie/data/fs.pickle"  # ajustar a tu instalacion
DECOY_DIR = "/ruta/a/honeypot/decoy_content"   # ajustar a tu instalacion

DECOYS = [
    ("/root/backup_credenciales.txt", f"{DECOY_DIR}/backup_credenciales_alto.txt"),
    ("/root/claves_ssh.txt", f"{DECOY_DIR}/claves_ssh_alto.txt"),
    ("/root/db_produccion.sql", f"{DECOY_DIR}/db_produccion_alto.sql"),
]

decoys_activados = False

UMBRAL_ALERTA = 0.70
UMBRAL_CRITICO = 0.80

def clasificar_comando(comando):
    c = comando.lower().strip()

    if any(p in c for p in ["sudo", "su -", "su root", "chmod 777", "chown root"]):
        return "acceso_root"
    if any(p in c for p in ["wget", "curl", "scp", "nc ", "netcat"]):
        return "descarga_payload"
    if any(p in c for p in ["rm -rf", "rm -r", "dd if=", "mkfs", "> /dev/", ":(){ :|:& };:"]):
        return "comando_destructivo"
    if any(p in c for p in ["nmap", "masscan", "ping -f", "netstat", "ss -"]):
        return "escaneo_puertos"
    if any(p in c for p in ["cat ", "less ", "more ", "vi ", "nano ", "open("]):
        return "archivo_abierto"

    return "comando_simple"

def estimular_cerebro_remoto(tipo_evento):
    try:
        resp = requests.post(CEREBRO_URL, json={"tipo_evento": tipo_evento}, timeout=180)
        return resp.json()
    except Exception as e:
        print(f"    [!] Error contactando al cerebro: {e}")
        return None

def registrar_alerta(session, ip, comando, tipo, panico, nivel):
    linea = (f"{datetime.now().isoformat()} | {nivel} | sesion={session} | "
             f"ip={ip} | comando={comando!r} | tipo={tipo} | panico={panico:.3f}\n")
    with open(ALERTAS_PATH, "a") as f:
        f.write(linea)

def mostrar_alerta(nivel, session, ip, comando, panico):
    if nivel == "CRITICO":
        borde = "=" * 60
        print(f"\n{borde}")
        print(f"!!! ALERTA CRITICA !!!  panico={panico:.3f}")
        print(f"IP: {ip}  |  Sesion: {session}")
        print(f"Comando: {comando}")
        print(f"{borde}\n")
    else:
        print(f"    [ALERTA] Nivel elevado ({panico:.3f}) - IP: {ip} - revisar sesion {session}\n")

def activar_senuelos():
    global decoys_activados
    if decoys_activados:
        return
    for ruta_virtual, archivo_local in DECOYS:
        subprocess.run(
            ["fsctl", PICKLE_PATH, f"load {ruta_virtual} {archivo_local}"],
            capture_output=True
        )
    decoys_activados = True
    print("    >>> Senuelos de alto perfil activados en el sistema de archivos.\n")

def seguir_log(path):
    with open(path, "r") as f:
        f.seek(0, 2)
        while True:
            linea = f.readline()
            if not linea:
                time.sleep(0.5)
                continue
            yield linea

def main():
    print(f">>> Vigilando {LOG_PATH}...")
    print(f">>> Cerebro en: {CEREBRO_URL}")
    print(f">>> Alertas se guardan en: {ALERTAS_PATH}")
    print(">>> Esperando actividad del atacante...\n")

    ip_por_sesion = {}

    for linea in seguir_log(LOG_PATH):
        try:
            evento = json.loads(linea)
        except json.JSONDecodeError:
            continue

        eventid = evento.get("eventid", "")
        session = evento.get("session", "")

        if eventid == "cowrie.session.connect":
            ip = evento.get("src_ip", "?")
            ip_por_sesion[session] = ip
            print(f">>> Nueva conexion desde {ip}\n")

        elif eventid == "cowrie.login.success":
            user = evento.get("username", "?")
            pwd = evento.get("password", "?")
            print(f">>> Login exitoso: {user}/{pwd}\n")

        elif eventid == "cowrie.command.input":
            comando = evento.get("input", "").strip()
            if not comando:
                continue
            ip = ip_por_sesion.get(session, "?")
            tipo = clasificar_comando(comando)

            print(f"[{session[:8]}] Comando: {comando!r} -> tipo: {tipo}")
            resultado = estimular_cerebro_remoto(tipo)

            if resultado:
                panico = resultado.get("panico", 0)
                print(f"    Nivel de panico: {panico:.3f}  "
                      f"(GF: {resultado['gf_derecha_hz']:.1f}/{resultado['gf_izquierda_hz']:.1f} Hz)")

                if panico >= UMBRAL_CRITICO:
                    mostrar_alerta("CRITICO", session[:8], ip, comando, panico)
                    registrar_alerta(session[:8], ip, comando, tipo, panico, "CRITICO")
                    activar_senuelos()
                elif panico >= UMBRAL_ALERTA:
                    mostrar_alerta("ELEVADO", session[:8], ip, comando, panico)
                    registrar_alerta(session[:8], ip, comando, tipo, panico, "ELEVADO")
                else:
                    print()

if __name__ == "__main__":
    main()
