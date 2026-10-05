# cerebro-mosca-miel-olla

fly-brain-honeypot es un honeypot SSH (Cowrie) cuyo nivel de alerta lo calcula un conectoma real de Drosophila simulado con Brian2. Cada comando del atacante estimula el circuito de huida de la mosca (LC4/LPLC2 → Giant Fiber), y la respuesta decide alertas y señuelos.

## Qué es esto

Un honeypot SSH normal (basado en [Cowrie](https://github.com/cowrie/cowrie)) conectado a una simulación del conectoma completo de *Drosophila melanogaster* (~139,000 neuronas, ~50 millones de sinapsis, datos de [FlyWire](https://flywire.ai/), simulados con [Brian2](https://brian2.readthedocs.io/)).

Cuando un atacante ejecuta un comando en el honeypot, el sistema estimula el circuito visual de detección de amenazas de la mosca (neuronas **LC4** y **LPLC2**), cuya señal se propaga por el conectoma real hasta la **Giant Fiber**, la neurona que dispara el reflejo de huida en una mosca de verdad. La tasa de disparo resultante se convierte en un "nivel de pánico" (0 a 1) que decide:

- Cuándo generar una alerta
- Cuándo el sistema de archivos falso cambia su contenido hacia señuelos más convincentes (credenciales falsas, claves SSH falsas, dumps de base de datos falsos)

## Qué usamos vs. qué construimos

**Cowrie** aporta el honeypot SSH en sí: la terminal simulada, el sistema de archivos falso, el registro de comandos. Existe de forma independiente desde hace más de una década.

Este proyecto agrega:

- El motor de decisión biológico (`cerebro/cerebro_mosca.py`, expuesto como API HTTP con `cerebro/servidor_cerebro.py`)
- El traductor que conecta los eventos de Cowrie con esa simulación (`honeypot/traductor.py`)
- La lógica de señuelos adaptativos que modifica el contenido del sistema de archivos en caliente según el nivel de pánico

## Estado del proyecto

El circuito biológico (LC4/LPLC2 → Giant Fiber) está validado contra la literatura científica publicada ([Shiu et al., *Nature*](https://www.biorxiv.org/content/10.1101/2023.05.02.539144v1)) — la simulación reproduce el comportamiento esperado del circuito real.

**No está demostrado** que este enfoque sea más eficaz como mecanismo de engaño que un sistema de reglas simple. No se ha corrido el experimento comparativo (cerebro vs. tabla de reglas, con atacantes reales). Este es un proyecto de exploración de ingeniería y neurociencia computacional aplicada a seguridad, no un producto de seguridad probado.

## Arquitectura
