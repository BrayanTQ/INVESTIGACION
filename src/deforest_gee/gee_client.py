from __future__ import annotations

import os


def importar_ee():
    try:
        import ee
    except ImportError as exc:
        raise RuntimeError(
            "No está instalada la API de Google Earth Engine. Ejecute: python -m pip install -e ."
        ) from exc
    return ee


def autenticar():
    ee = importar_ee()
    ee.Authenticate()


def inicializar(project_id: str | None = None):
    ee = importar_ee()
    project_id = project_id or os.getenv("GEE_PROJECT_ID")
    if not project_id:
        raise ValueError(
            "Debe indicar --proyecto o definir la variable de entorno GEE_PROJECT_ID."
        )
    ee.Initialize(project=project_id)
    return ee


def diagnostico(project_id: str) -> dict:
    ee = inicializar(project_id)
    # Una operación mínima para comprobar inicialización y acceso al catálogo.
    n = ee.ImageCollection("COPERNICUS/S1_GRD").limit(1).size().getInfo()
    return {"project_id": project_id, "earth_engine": "OK", "catalogo_sentinel1": int(n) >= 0}
