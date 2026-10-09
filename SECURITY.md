# Seguridad

## Credenciales y secretos

Nunca publiques en GitHub contraseñas, tokens de NASA Earthdata, archivos `.netrc` / `_netrc`, archivos `.env` con valores reales ni credenciales incluidas directamente en el código.

Reglas del proyecto:

1. Mantener el repositorio **privado** mientras el equipo investigador valida el flujo de adquisición.
2. Usar variables de entorno como `EARTHDATA_TOKEN` o un archivo netrc del usuario.
3. No guardar credenciales dentro de archivos Python, JSON, BAT, Markdown o ejemplos de configuración.
4. No subir a GitHub los productos Sentinel-1 descargados. La carpeta `downloads/` está excluida mediante `.gitignore`.
5. Antes de cada `git push`, ejecutar `git status` y revisar los archivos que serán publicados.

## Reporte de vulnerabilidades o exposición de credenciales

Si se detecta una credencial publicada accidentalmente:

1. revocar inmediatamente el token o cambiar la contraseña;
2. informar al responsable del repositorio;
3. retirar el secreto del historial de Git;
4. revisar accesos y actividad reciente;
5. documentar el incidente sin volver a copiar el secreto.

No publiques credenciales reales dentro de una incidencia (Issue).
