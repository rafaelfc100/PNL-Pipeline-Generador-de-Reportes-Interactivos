# modulos/bloque2_carga.py
import pandas as pd

def cargar_csv(ruta, columnas, verbose=0):
    """
    Carga un CSV, valida columnas y regresa un DataFrame con una sola columna 'texto'.
    """

    if verbose:
        print(f"[INFO] Cargando archivo: {ruta}")

    try:
        df = pd.read_csv(ruta, encoding="utf-8")
    except UnicodeDecodeError:
        if verbose:
            print("[WARN] Error UTF-8, intentando ISO-8859-1...")
        df = pd.read_csv(ruta, encoding="ISO-8859-1")

    # Validar columnas
    for col in columnas:
        if col not in df.columns:
            raise ValueError(
                f"La columna '{col}' no existe en el archivo. "
                f"Columnas disponibles: {list(df.columns)}"
            )

    if verbose:
        print(f"[INFO] Columnas encontradas: {columnas}")

    # Si hay varias columnas, se concatenan
    if len(columnas) > 1:
        df["texto"] = df[columnas].astype(str).agg(" ".join, axis=1)
        if verbose:
            print("[INFO] Varias columnas unidas en 'texto'")
    else:
        df["texto"] = df[columnas[0]].astype(str)

    # Elimina filas vacías
    df = df[df["texto"].str.strip().astype(bool)]

    if verbose:
        print(f"[INFO] Registros cargados: {len(df)}")

    return df[["texto"]]
