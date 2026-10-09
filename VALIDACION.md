# Validación técnica

Validado para la versión 0.1.1:

- compilación de módulos Python;
- pruebas unitarias;
- generación de AOI por punto+radio;
- generación de BBOX;
- validación de configuración y fechas;
- normalización de órbitas en español e inglés;
- selección de escenas por `todos`, índice, lista y rango;
- escritura y lectura de manifiestos;
- construcción del perfil fijo Sentinel-1;
- ayuda de la CLI en español;
- alias de comandos en español e inglés.

Comandos de validación local:

```bash
python -m compileall -q src
pytest
PYTHONPATH=src python -m deforest_s1 --help
PYTHONPATH=src python -m deforest_s1 diagnostico --help
PYTHONPATH=src python -m deforest_s1 buscar --help
PYTHONPATH=src python -m deforest_s1 descargar --help
```

## Validaciones que requieren red y credenciales reales

El entorno de construcción no puede completar por sí solo estas pruebas de aceptación:

- búsqueda real en el catálogo Sentinel-1 de ASF;
- descarga autenticada con NASA Earthdata.

Estas pruebas deben ejecutarse en la estación de trabajo del proyecto mediante:

```bash
deforest-s1 diagnostico
deforest-s1 buscar --configuracion config/search.example.json
deforest-s1 descargar --manifiesto outputs/ARCHIVO.json --seleccionar 1 --directorio-salida downloads --autenticacion token
```

La aceptación final de una versión destinada a producción debe registrar fecha, equipo utilizado, versión de Python, versión de `asf-search`, consulta ejecutada y nombre exacto de la escena descargada.
