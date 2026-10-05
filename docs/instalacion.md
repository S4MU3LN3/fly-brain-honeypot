# Instalación

## 1. El modelo del conectoma (Shiu et al.)

Este proyecto depende de [Drosophila_brain_model](https://github.com/philshiu/Drosophila_brain_model), el repositorio que acompaña el paper de Shiu et al. (2023), *A leaky integrate-and-fire computational model based on the connectome of the entire adult Drosophila brain*. No se incluye en este repo por su tamaño (los datos de conectividad pesan varios cientos de MB) y porque tiene su propia licencia.

```bash
git clone https://github.com/philshiu/Drosophila_brain_model
cd Drosophila_brain_model
```

Copia los archivos de este repo (`cerebro/*.py`) dentro de esa carpeta, junto a `model.py` y `utils.py`.

## 2. IDs de neuronas LC4 y LPLC2

Descarga las listas de IDs desde [FlyWire Codex](https://codex.flywire.ai/app/search):

1. Busca `cell_type == LC4`, exporta los Cell IDs como `root_ids_cell_type_LC4.txt`
2. Busca `cell_type == LPLC2`, exporta como `root_ids_cell_type_LPLC2.txt`
3. Coloca ambos archivos junto a `cerebro_mosca.py`

## 3. Dependencias de Python

```bash
pip install -r cerebro/requirements.txt
```

Nota: Brian2 funciona mucho más rápido con un compilador de C++ instalado (Cython). En Windows, instala "Microsoft C++ Build Tools" con la carga de trabajo "Desarrollo para el escritorio con C++". Sin esto, el sistema funciona pero cada simulación puede tardar varias veces más.

## 4. Calibración (opcional, recomendado la primera vez)

```bash
cd Drosophila_brain_model
python calibracion.py
```

Esto corre tres niveles de estímulo (nulo, débil, fuerte) y muestra la tasa de disparo de la Giant Fiber en cada uno. Ajusta `GF_MAX_HZ` en `cerebro_mosca.py` según el resultado "fuerte" si tu máquina da valores distintos a los documentados.

## 5. Levantar el servidor del cerebro

```bash
python servidor_cerebro.py
```

Por defecto escucha en el puerto 5000. Anota la IP de esta máquina (`ipconfig` en Windows, `ip addr` en Linux) para configurarla en el traductor.

## 6. Cowrie (el honeypot)

Ver [cowrie.org/docs](https://docs.cowrie.org/) para la instalación oficial, o:

```bash
python3 -m venv cowrie-env
source cowrie-env/bin/activate
pip install cowrie
cowrie init
cowrie start
```

Cowrie requiere un entorno tipo Unix. En Windows, usa WSL2.

## 7. Configurar y correr el traductor

Edita `honeypot/traductor.py` y actualiza `CEREBRO_URL` con la IP del servidor del cerebro (paso 5).

```bash
pip install requests
python3 traductor.py
```
