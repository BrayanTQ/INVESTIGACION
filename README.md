# Deforest S1 Acquisition

Herramienta de línea de comandos para **buscar y descargar productos Sentinel-1** destinados al proyecto de investigación sobre predicción de la deforestación amazónica mediante imágenes satelitales e inteligencia artificial.

## 1. Alcance actual

Esta versión resuelve únicamente la **adquisición de datos Sentinel-1**.

Perfil fijo de búsqueda:

- Misión: **Sentinel-1**
- Sensor: SAR
- Modo: **IW**
- Producto / nivel: **GRD_HD**
- Polarización: **VV+VH**
- Órbita: BOTH, ASCENDING o DESCENDING
- Área de interés: punto + radio, bounding box, GeoJSON Polygon o WKT
- Rango temporal: fecha inicial y final

El código **no usa Copernicus Data Space**. La consulta y descarga de productos Sentinel-1 se realiza mediante **ASF DAAC / NASA Earthdata** usando el paquete oficial `asf-search`.

> Nota conceptual: Sentinel-1 es la misión/satélite que adquiere los datos. Un programa no se conecta directamente al satélite; consulta un archivo de distribución que almacena y sirve los productos Sentinel-1.

## 2. Qué hace el software

1. Valida el entorno.
2. Construye el área de interés.
3. Busca únicamente productos Sentinel-1 compatibles con el perfil fijo.
4. Presenta los resultados por línea de comandos.
5. Guarda un manifiesto JSON reproducible de la búsqueda.
6. Permite elegir qué escenas descargar.
7. Resuelve nuevamente las escenas exactas por `sceneName` antes de la descarga.
8. Se autentica contra NASA Earthdata mediante token, credenciales o netrc.
9. Descarga a la carpeta indicada por el investigador.

La organización científica definitiva de los productos descargados se diseñará en una etapa posterior. En esta versión, `--output-dir` indica únicamente el destino físico de descarga.

---

## 3. Requisitos

- Windows 10/11, Linux o macOS
- Python **3.10 o superior**
- Internet
- Cuenta de NASA Earthdata para realizar descargas
- Git, si se desea colaborar mediante GitHub

Dependencia principal fijada para reproducibilidad:

```text
asf-search==14.0.3
```

---

## 4. Instalación rápida en Windows

Abra CMD o PowerShell dentro de la carpeta del repositorio.

### Opción A — automática

Ejecute:

```cmd
scripts\setup_windows.bat
```

### Opción B — manual

```cmd
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Después debe funcionar:

```cmd
deforest-s1 --help
```

También puede ejecutarse sin instalar el comando global del entorno:

```cmd
python -m deforest_s1 --help
```

---

## 5. Primera comprobación

```cmd
deforest-s1 doctor
```

El comando informa:

- versión del proyecto;
- versión instalada de `asf-search`;
- perfil Sentinel-1 fijo;
- estado de disponibilidad del servicio ASF.

`doctor` necesita Internet, pero no necesita descargar escenas.

---

## 6. Primera búsqueda recomendada

El repositorio incluye:

```text
config/search.example.json
```

Contenido inicial:

```json
{
  "aoi": {
    "type": "point_radius",
    "lat": -12.60,
    "lon": -69.20,
    "radius_km": 10
  },
  "start_date": "2025-01-01",
  "end_date": "2025-03-31",
  "orbit": "BOTH",
  "max_results": 20
}
```

Ejecute:

```cmd
deforest-s1 buscar --configuracion config\search.example.json
```

El programa mostrará los resultados y generará automáticamente un manifiesto en `outputs/`.

Ejemplo:

```text
outputs/busqueda_sentinel1_20261008_130000.json
```

Ese manifiesto conserva la consulta y la identidad de las escenas encontradas.

---

## 7. Búsqueda sin archivo de configuración

También puede introducir todo por línea de comandos:

```cmd
deforest-s1 buscar --lat -12.60 --lon -69.20 --radio-km 10 --inicio 2025-01-01 --fin 2025-03-31 --orbita AMBAS --max-resultados 20
```

### Solo órbita ascendente

```cmd
deforest-s1 buscar --lat -12.60 --lon -69.20 --radio-km 10 --inicio 2025-01-01 --fin 2025-03-31 --orbita ASCENDENTE --max-resultados 20
```

### Solo órbita descendente

```cmd
deforest-s1 buscar --lat -12.60 --lon -69.20 --radio-km 10 --inicio 2025-01-01 --fin 2025-03-31 --orbita DESCENDENTE --max-resultados 20
```

### Bounding box

```cmd
deforest-s1 buscar --bbox -69.40 -12.80 -69.00 -12.40 --inicio 2025-01-01 --fin 2025-03-31 --max-resultados 20
```

### GeoJSON Polygon

```cmd
deforest-s1 buscar --geojson ruta\aoi.geojson --inicio 2025-01-01 --fin 2025-03-31 --max-resultados 20
```

---

## 8. Descargar escenas

La descarga se realiza a partir de un manifiesto de búsqueda. Esto hace que el proceso sea más trazable que volver a elegir productos manualmente.

### Descargar solo el primer resultado

```cmd
deforest-s1 descargar --manifiesto outputs\busqueda_sentinel1_XXXXXXXX_XXXXXX.json --seleccionar 1 --directorio-salida downloads --autenticacion token
```

### Descargar 1, 3 y 5

```cmd
deforest-s1 descargar --manifiesto outputs\busqueda_sentinel1_XXXXXXXX_XXXXXX.json --seleccionar 1,3,5 --directorio-salida downloads --autenticacion token
```

### Descargar del 1 al 5

```cmd
deforest-s1 descargar --manifiesto outputs\busqueda_sentinel1_XXXXXXXX_XXXXXX.json --seleccionar 1-5 --directorio-salida downloads --autenticacion token
```

### Descargar todos

```cmd
deforest-s1 descargar --manifiesto outputs\busqueda_sentinel1_XXXXXXXX_XXXXXX.json --seleccionar todos --directorio-salida downloads --autenticacion token
```

### Dos descargas paralelas

```cmd
deforest-s1 descargar --manifiesto outputs\busqueda_sentinel1_XXXXXXXX_XXXXXX.json --seleccionar todos --directorio-salida downloads --autenticacion token --processes 2
```

Para una primera prueba se recomienda **una sola escena y un solo proceso**.

---

## 9. Autenticación NASA Earthdata

### Recomendado para el equipo: token por variable de entorno

CMD:

```cmd
set EARTHDATA_TOKEN=PEGAR_TOKEN_AQUI
```

Después:

```cmd
deforest-s1 descargar --manifiesto outputs\archivo.json --seleccionar 1 --directorio-salida downloads --autenticacion token
```

El token no debe aparecer en código, configuraciones ni commits.

### Credenciales solicitadas interactivamente

```cmd
deforest-s1 descargar --manifiesto outputs\archivo.json --seleccionar 1 --directorio-salida downloads --autenticacion credenciales
```

El programa solicitará usuario y contraseña; la contraseña se oculta.

### netrc

`asf-search` también puede utilizar credenciales netrc del usuario:

```cmd
deforest-s1 descargar --manifiesto outputs\archivo.json --seleccionar 1 --directorio-salida downloads --autenticacion netrc
```

Cada investigador debe usar **sus propias credenciales**.

---

## 10. Estructura del repositorio

```text
deforest-s1-acquisition/
│
├── README.md
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── .gitignore
├── .env.example
├── SECURITY.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── NOTICE.md
├── VALIDACION.md
│
├── src/
│   └── deforest_s1/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── aoi.py
│       ├── config.py
│       ├── asf_client.py
│       ├── display.py
│       ├── manifest.py
│       └── selection.py
│
├── config/
│   └── search.example.json
│
├── tests/
│   ├── test_aoi.py
│   ├── test_config.py
│   ├── test_manifest.py
│   └── test_selection.py
│
├── scripts/
│   ├── setup_windows.bat
│   ├── test_windows.bat
│   └── example_search_windows.bat
│
├── docs/
│   ├── ARQUITECTURA.md
│   ├── INSTALACION_Y_COMANDOS.md
│   ├── COLABORACION_GITHUB.md
│   ├── ACCESOS_Y_ROLES_GITHUB.md
│   ├── ENTREGA_INVESTIGADORES.md
│   └── DECISIONES_TECNICAS.md
│
├── .github/
│   ├── pull_request_template.md
│   ├── workflows/
│   │   └── tests.yml
│   └── ISSUE_TEMPLATE/
│       ├── config.yml
│       ├── reporte_error.md
│       └── solicitud_mejora.md
│
├── outputs/
│   └── .gitkeep
│
└── downloads/
    └── .gitkeep
```

---

## 11. Pruebas

Instale dependencias de desarrollo:

```cmd
python -m pip install -e ".[dev]"
```

Ejecute:

```cmd
pytest
```

Las pruebas unitarias no necesitan descargar imágenes.

La prueba real de conectividad se realiza con:

```cmd
deforest-s1 doctor
```

La prueba real completa debe hacerse con:

1. `buscar`;
2. revisar el manifiesto;
3. `descargar --seleccionar 1`;
4. verificar que el ZIP Sentinel-1 se haya descargado correctamente.

---

## 12. Documentación oficial de referencia

- Paquete Python ASF Search: https://docs.asf.alaska.edu/asf_search/
- Parámetros de búsqueda: https://docs.asf.alaska.edu/asf_search/searching/
- Downloads/authentication: https://docs.asf.alaska.edu/asf_search/downloading/
- NASA Earthdata Login: https://urs.earthdata.nasa.gov/

---

## 13. Estado

Versión: `0.1.1`

Estado recomendado del repositorio: **privado / investigación interna** hasta que los investigadores principales definan publicación, licencia y política institucional de datos/código.


## Idioma del repositorio

La documentación, plantillas de GitHub y mensajes visibles de la CLI están redactados en español. Se conservan alias y algunos identificadores técnicos en inglés para compatibilidad con bibliotecas, GitHub y versiones anteriores.

Para definir permisos del equipo, revisar `docs/ACCESOS_Y_ROLES_GITHUB.md`.
