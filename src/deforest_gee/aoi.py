from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def validar_aoi_spec(spec: dict[str, Any]) -> dict[str, Any]:
    tipo = str(spec.get("tipo", "")).lower()
    if tipo == "punto_radio":
        lat = float(spec["latitud"])
        lon = float(spec["longitud"])
        radio = float(spec["radio_km"])
        if not -90 <= lat <= 90:
            raise ValueError("Latitud fuera de rango.")
        if not -180 <= lon <= 180:
            raise ValueError("Longitud fuera de rango.")
        if radio <= 0:
            raise ValueError("radio_km debe ser mayor que 0.")
    elif tipo == "bbox":
        oeste = float(spec["oeste"])
        sur = float(spec["sur"])
        este = float(spec["este"])
        norte = float(spec["norte"])
        if oeste >= este or sur >= norte:
            raise ValueError("Bounding box inválido.")
    elif tipo == "geojson":
        archivo = Path(spec["archivo"])
        if not archivo.exists():
            raise FileNotFoundError(f"No existe el GeoJSON: {archivo}")
    else:
        raise ValueError("AOI no soportado. Use punto_radio, bbox o geojson.")
    return spec


def cargar_geojson(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("type") == "Feature":
        return data["geometry"]
    if data.get("type") == "FeatureCollection":
        features = data.get("features") or []
        if len(features) != 1:
            raise ValueError("Para esta versión, un FeatureCollection debe contener exactamente 1 geometría.")
        return features[0]["geometry"]
    return data


def aoi_to_ee(spec: dict[str, Any], ee):
    validar_aoi_spec(spec)
    tipo = spec["tipo"].lower()
    if tipo == "punto_radio":
        punto = ee.Geometry.Point([float(spec["longitud"]), float(spec["latitud"])])
        return punto.buffer(float(spec["radio_km"]) * 1000)
    if tipo == "bbox":
        return ee.Geometry.Rectangle([
            float(spec["oeste"]), float(spec["sur"]),
            float(spec["este"]), float(spec["norte"]),
        ])
    geom = cargar_geojson(spec["archivo"])
    return ee.Geometry(geom)
