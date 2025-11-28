# ==========================================================
# BLOQUE 11 - DETECCIÓN Y VISUALIZACIÓN DE OUTLIERS
# ==========================================================

import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA

def detectar_outliers(embeddings, porcentaje=0.05, verbose=0):
    """
    Detecta outliers en embeddings de textos usando Isolation Forest.
    - porcentaje: proporción de puntos a considerar outliers
    """
    clf = IsolationForest(contamination=porcentaje, random_state=42)
    preds = clf.fit_predict(embeddings)  # -1 = outlier, 1 = normal
    
    outliers_idx = np.where(preds == -1)[0]
    if verbose:
        print(f"[INFO] Se detectaron {len(outliers_idx)} outliers de {len(embeddings)} textos.")
    return outliers_idx


def graficar_outliers(embeddings, outliers_idx, ruta_salida="output/outliers.png"):
    """
    Grafica outliers usando PCA 2D.
    """
    pca = PCA(n_components=2)
    coords = pca.fit_transform(embeddings)
    
    plt.figure(figsize=(8,6))
    plt.scatter(coords[:,0], coords[:,1], c='blue', alpha=0.5, label='Normal')
    if len(outliers_idx) > 0:
        plt.scatter(coords[outliers_idx,0], coords[outliers_idx,1], c='red', label='Outliers')
    plt.legend()
    plt.title("Outliers detectados (PCA 2D)")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    os.makedirs("output", exist_ok=True)
    plt.savefig(ruta_salida, dpi=300, bbox_inches="tight")
    plt.close()
    if ruta_salida:
        print(f"[INFO] Outliers graficados en {ruta_salida}")
    return ruta_salida


def extraer_textos_outliers(df, outliers_idx, max_ejemplos=10):
    """
    Devuelve una lista de los textos que fueron detectados como outliers.
    """
    textos = []
    for idx in outliers_idx[:max_ejemplos]:
        textos.append(df.iloc[idx]['texto'])
    return textos
