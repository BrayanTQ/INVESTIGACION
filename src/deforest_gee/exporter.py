from __future__ import annotations

import re
from typing import Any

from .aoi import aoi_to_ee
from .constants import BANDAS_EXPORTACION
from .selection import parsear_seleccion


def _nombre_seguro(texto: str) -> str:
    texto = re.sub(r"[^A-Za-z0-9_.-]+", "_", texto)
    return texto[:100]


def iniciar_exportaciones(
    ee,
    manifiesto: dict[str, Any],
    seleccion: str,
    carpeta_drive: str,
    escala_m: int | None = None,
    max_pixels: float = 1e13,
) -> list[dict[str, Any]]:
    resultados = manifiesto.get("resultados", [])
    indices = parsear_seleccion(seleccion, len(resultados))
    aoi_spec = manifiesto["consulta"]["aoi"]
    region = aoi_to_ee(aoi_spec, ee)
    escala = int(escala_m or manifiesto["consulta"].get("escala_m", 10))

    tareas = []
    for idx in indices:
        escena = resultados[idx]
        ee_id = escena.get("ee_id")
        if not ee_id:
            raise ValueError(f"La escena {idx+1} no contiene ee_id.")
        nombre = _nombre_seguro(escena.get("system_index") or f"sentinel1_{idx+1}")
        image = ee.Image(ee_id).select(list(BANDAS_EXPORTACION)).clip(region)
        task = ee.batch.Export.image.toDrive(
            image=image,
            description=f"S1_{nombre}",
            folder=carpeta_drive,
            fileNamePrefix=nombre,
            region=region,
            scale=escala,
            maxPixels=max_pixels,
            fileFormat="GeoTIFF",
        )
        task.start()
        status = task.status()
        tareas.append({
            "indice": idx + 1,
            "ee_id": ee_id,
            "system_index": escena.get("system_index"),
            "task_id": status.get("id"),
            "state": status.get("state"),
            "carpeta_drive": carpeta_drive,
            "archivo": nombre,
        })
    return tareas


def listar_tareas(ee, limite: int = 50) -> list[dict[str, Any]]:
    salida = []
    for task in ee.batch.Task.list()[:limite]:
        st = task.status()
        salida.append({
            "id": st.get("id"),
            "state": st.get("state"),
            "description": st.get("description"),
            "error_message": st.get("error_message"),
        })
    return salida
