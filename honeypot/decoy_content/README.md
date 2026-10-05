# decoy_content

Contenido de los archivos señuelo que ve el atacante dentro del honeypot.

Cada señuelo tiene dos versiones:
- `*_bajo.txt` / `*_bajo.sql`: contenido inicial, poco interesante. Es lo que ve el atacante antes de que el sistema detecte una amenaza seria.
- `*_alto.txt` / `*_alto.sql`: contenido que `traductor.py` carga en caliente (vía `fsctl load`) cuando el nivel de pánico cruza el umbral crítico.

Todos los datos (claves, contraseñas, hashes) son **ficticios e inválidos a propósito** — tienen el formato correcto para ser creíbles, pero no funcionan si alguien intenta usarlos.
