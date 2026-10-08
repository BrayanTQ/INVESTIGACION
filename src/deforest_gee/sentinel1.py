from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Any

from .aoi import aoi_to_ee
from .constants import COLECCION_SENTINEL1, MODO_INSTRUMENTO, RESOLUCION_METROS
from .config import SearchConfig


def construir_coleccion(ee, cfg: SearchConfig):
    region = aoi_to_ee(cfg.aoi, ee)
    fecha_fin_exclusiva = (datetime.strptime(cfg.fecha_fin, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    col = (
        ee.ImageCollection(COLECCION_SENTINEL1)
        .filterBounds(region)
        .filterDate(cfg.fecha_inicio, fecha_fin_exclusiva)
        .filter(ee.Filter.eq("instrumentMode", MODO_INSTRUMENTO))
        .filter(ee.Filter.eq("resolution_meters", RESOLUCION_METROS))
        .filter(ee.Filter.listContains("transmitterReceiverPolarisation", "VV"))
        .filter(ee.Filter.listContains("transmitterReceiverPolarisation", "VH"))
    )
    if cfg.orbita == "ASCENDENTE":
        col = col.filter(ee.Filter.eq("orbitProperties_pass", "ASCENDING"))
    elif cfg.orbita == "DESCENDENTE":
        col = col.filter(ee.Filter.eq("orbitProperties_pass", "DESCENDING"))
    return col.sort("system:time_start")


def _iso_utc(ms: int | float | None) -> str | None:
    if ms is None:
        return None
    return datetime.fromtimestamp(float(ms) / 1000, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def obtener_resultados(ee, cfg: SearchConfig) -> list[dict[str, Any]]:
    col = construir_coleccion(ee, cfg).limit(cfg.max_resultados)
    info = col.getInfo()
    salida = []
    for feature in info.get("features", []):
        props = feature.get("properties", {})
        salida.append({
            "ee_id": feature.get("id"),
            "system_index": props.get("system:index"),
            "fecha_hora_utc": _iso_utc(props.get("system:time_start")),
            "plataforma": props.get("platform_number"),
            "modo": props.get("instrumentMode"),
            "producto": props.get("productType"),
            "resolucion_m": props.get("resolution_meters"),
            "polarizaciones": props.get("transmitterReceiverPolarisation"),
            "orbita": props.get("orbitProperties_pass"),
            "orbita_absoluta": props.get("orbitNumber_start"),
            "orbita_relativa": props.get("relativeOrbitNumber_start"),
            "mission_data_take_id": props.get("missionDataTakeID"),
        })
    return salida
