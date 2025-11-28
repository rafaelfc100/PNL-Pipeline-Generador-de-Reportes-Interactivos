# modulos/bloque5_ngrams.py

import os
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from modulos.bloque3_preproc import cargar_stopwords

# Paletas de colores según número
PALETAS = {
    1: "viridis",
    2: "autumn",
    3: "winter",
    4: "cubehelix",
    5: "tab20"
}

def generar_ngramas(textos, n=2, nombre="ngramas", top=10, idioma="es", paleta=1):
    """
    Genera bigramas o trigramas:
    - Usa textos preprocesados
    - Stopwords según idioma (ES, EN, FR, PT)
    - Solo los 'top' n-gramas
    - Graficar con la paleta elegida
    """

    print(f"[INFO] Generando {nombre} (n={n})...")

    # Stopwords según idioma
    stopwords_local = cargar_stopwords(idioma)

    # Vectorizador limitado a ngramas útiles
    vectorizer = CountVectorizer(
        ngram_range=(n, n),
        analyzer="word",
        max_features=5000
    )

    X = vectorizer.fit_transform(textos)
    vocab = vectorizer.get_feature_names_out()
    counts = X.sum(axis=0).A1

    # Filtrar n-gramas que contengan stopwords
    def contiene_stopword(ngram):
        return any(p in stopwords_local for p in ngram.split())

    freq_filtrado = [(ng, c) for ng, c in zip(vocab, counts) if not contiene_stopword(ng)]

    # Top N
    top_n = sorted(freq_filtrado, key=lambda x: x[1], reverse=True)[:top]

    if not top_n:
        print(f"[WARN] No se encontraron {nombre} después de filtrar stopwords.")
        return None

    etiquetas = [x[0] for x in top_n]
    valores = [x[1] for x in top_n]

    # Obtener nombre de colormap según número
    cmap = paleta  

    # Graficar
    plt.figure(figsize=(10, 5))
    plt.barh(etiquetas, valores, color=plt.cm.get_cmap(cmap)(0.7))
    plt.xlabel("Frecuencia")
    plt.title(f"Top {top} {nombre}")
    plt.gca().invert_yaxis()

    os.makedirs("output", exist_ok=True)
    ruta = f"output/{nombre}.png"
    plt.savefig(ruta, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"[INFO] {nombre.capitalize()} guardados en: {ruta}")
    return ruta
