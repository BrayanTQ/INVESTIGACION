from __future__ import annotations

import shutil
import subprocess


def detectar_gpt() -> str | None:
    return shutil.which("gpt") or shutil.which("gpt.exe")


def ejecutar_grafo(graph_xml: str, parametros: dict[str, str] | None = None) -> int:
    gpt = detectar_gpt()
    if not gpt:
        raise RuntimeError("No se encontró SNAP GPT en PATH.")
    cmd = [gpt, graph_xml]
    for k, v in (parametros or {}).items():
        cmd.append(f"-P{k}={v}")
    return subprocess.run(cmd, check=False).returncode
