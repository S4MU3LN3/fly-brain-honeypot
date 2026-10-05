from model import run_exp
from model import default_params as params
import utils as utl
from brian2 import ms
import random
import string

CONFIG = {
    'path_res'  : './results/eventos',
    'path_comp' : './Completeness_783.csv',
    'path_con'  : './Connectivity_783.parquet',
    'n_proc'    : 1,
}

ID_GF_DERECHA = 720575940632499757
ID_GF_IZQUIERDA = 720575940622838154

GF_MAX_HZ = 193.0
MAX_NEURONAS_TOTAL = 260

def _cargar_ids(path):
    with open(path, encoding='utf-8') as f:
        return [int(x) for x in f.read().strip().split(',') if x.strip()]

NEU_LC4 = _cargar_ids('root_ids_cell_type_LC4.txt')
NEU_LPLC2 = _cargar_ids('root_ids_cell_type_LPLC2.txt')

EVENTO_A_FRACCION = {
    'comando_simple':      0.05,
    'archivo_abierto':     0.15,
    'escaneo_puertos':     0.30,
    'comando_destructivo': 0.60,
    'descarga_payload':    0.80,
    'acceso_root':         1.00,
}

def _id_experimento():
    return 'evt_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

def estimular_cerebro(tipo_evento, n_run=1, t_run_ms=300):
    fraccion = EVENTO_A_FRACCION.get(tipo_evento, 0.10)

    n_lc4 = max(1, int(len(NEU_LC4) * fraccion))
    n_lplc2 = max(1, int(len(NEU_LPLC2) * fraccion))
    neuronas = NEU_LC4[:n_lc4] + NEU_LPLC2[:n_lplc2]

    if len(neuronas) > MAX_NEURONAS_TOTAL:
        neuronas = neuronas[:MAX_NEURONAS_TOTAL]

    params['n_run'] = n_run
    params['t_run'] = t_run_ms * ms

    exp_name = _id_experimento()
    run_exp(exp_name=exp_name, neu_exc=neuronas, params=params, force_overwrite=True, **CONFIG)

    df_spike = utl.load_exps([f"{CONFIG['path_res']}/{exp_name}.parquet"])
    df_rate, _ = utl.get_rate(df_spike, t_run=params['t_run'], n_run=params['n_run'])

    gf_d = df_rate.loc[ID_GF_DERECHA, exp_name] if ID_GF_DERECHA in df_rate.index else 0.0
    gf_i = df_rate.loc[ID_GF_IZQUIERDA, exp_name] if ID_GF_IZQUIERDA in df_rate.index else 0.0
    tasa_promedio = (gf_d + gf_i) / 2

    panico = min(tasa_promedio / GF_MAX_HZ, 1.5)

    return {
        'tipo_evento': tipo_evento,
        'neuronas_excitadas': len(neuronas),
        'gf_derecha_hz': gf_d,
        'gf_izquierda_hz': gf_i,
        'panico': round(panico, 3),
    }


if __name__ == '__main__':
    import sys
    evento = sys.argv[1] if len(sys.argv) > 1 else 'comando_simple'
    print(f">>> Probando evento: {evento}")
    resultado = estimular_cerebro(evento)
    print(resultado)
