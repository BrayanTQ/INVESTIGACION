def parsear_seleccion(texto: str, total: int) -> list[int]:
    texto = texto.strip().lower()
    if total < 0:
        raise ValueError("total inválido")
    if texto in {"todos", "all"}:
        return list(range(total))
    indices = []
    vistos = set()
    for bloque in texto.split(","):
        bloque = bloque.strip()
        if not bloque:
            continue
        if "-" in bloque:
            a, b = bloque.split("-", 1)
            inicio, fin = int(a), int(b)
            if inicio > fin:
                raise ValueError(f"Rango inválido: {bloque}")
            nums = range(inicio, fin + 1)
        else:
            nums = [int(bloque)]
        for n in nums:
            if n < 1 or n > total:
                raise ValueError(f"Índice fuera de rango: {n}. Total disponible: {total}.")
            idx = n - 1
            if idx not in vistos:
                vistos.add(idx)
                indices.append(idx)
    if not indices:
        raise ValueError("No se seleccionó ninguna escena.")
    return indices
