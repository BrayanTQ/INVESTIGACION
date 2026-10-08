from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .constants import ORBITAS_VALIDAS, RESOLUCION_METROS


@dataclass(frozen=True)
class SearchConfig:
    aoi: dict[str, Any]
    fecha_inicio: str
    fecha_fin: str
    orbita: str = "AMBAS"
    max_resultados: int = 20
    escala_m: int = RESOLUCION_METROS

    def validate(self) -> "SearchConfig":
        fi = datetime.strptime(self.fecha_inicio, "%Y-%m-%d")
        ff = datetime.strptime(self.fecha_fin, "%Y-%m-%d")
        if fi > ff:
            raise ValueError("La fecha de inicio no puede ser posterior a la fecha final.")
        if self.orbita not in ORBITAS_VALIDAS:
            raise ValueError(f"Órbita inválida: {self.orbita}. Use {ORBITAS_VALIDAS}.")
        if self.max_resultados <= 0:
            raise ValueError("max_resultados debe ser mayor que 0.")
        if self.escala_m <= 0:
            raise ValueError("escala_m debe ser mayor que 0.")
        if not isinstance(self.aoi, dict) or "tipo" not in self.aoi:
            raise ValueError("La configuración AOI debe incluir el campo 'tipo'.")
        return self


def cargar_config(path: str | Path) -> SearchConfig:
    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    aoi = dict(data["aoi"])
    if str(aoi.get("tipo", "")).lower() == "geojson" and "archivo" in aoi:
        ap = Path(aoi["archivo"])
        if not ap.is_absolute():
            aoi["archivo"] = str((path.parent / ap).resolve())
    cfg = SearchConfig(
        aoi=aoi,
        fecha_inicio=data["fecha_inicio"],
        fecha_fin=data["fecha_fin"],
        orbita=str(data.get("orbita", "AMBAS")).upper(),
        max_resultados=int(data.get("max_resultados", 20)),
        escala_m=int(data.get("escala_m", RESOLUCION_METROS)),
    )
    return cfg.validate()
