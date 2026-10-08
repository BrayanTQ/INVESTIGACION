from __future__ import annotations

from pathlib import Path


def entrenar_random_forest(csv_path: str | Path, etiqueta: str, modelo_salida: str | Path):
    try:
        import joblib
        import pandas as pd
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import classification_report
        from sklearn.model_selection import train_test_split
    except ImportError as exc:
        raise RuntimeError(
            "Faltan dependencias ML. Instale: python -m pip install -e \".[ml]\""
        ) from exc

    df = pd.read_csv(csv_path)
    if etiqueta not in df.columns:
        raise ValueError(f"No existe la columna etiqueta '{etiqueta}'.")
    X = df.drop(columns=[etiqueta]).select_dtypes(include="number")
    y = df[etiqueta]
    if X.empty:
        raise ValueError("No existen columnas numéricas para entrenar.")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y if y.nunique() > 1 else None
    )
    model = RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    reporte = classification_report(y_test, pred, output_dict=False, zero_division=0)
    modelo_salida = Path(modelo_salida)
    modelo_salida.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "features": list(X.columns)}, modelo_salida)
    return reporte
