# modulos/bloque4_wordcloud.py

import os
from wordcloud import WordCloud

# paletas de colores según número
PALETAS = {
    1: "viridis",      # clásica
    2: "autumn",       # cálida
    3: "winter",       # fría
    4: "cubehelix",    # alto contraste
    5: "tab20"         # daltónicos
}

def generar_wordcloud(textos_limpios, paleta=1, verbose=0):
    """Genera y guarda una nube de palabras a partir del texto procesado."""

    if verbose:
        print("[INFO] Generando nube de palabras...")

    # Unir todos los textos
    texto_unido = " ".join(textos_limpios)

    # Obtener nombre de colormap según número
    colormap = paleta

    wc = WordCloud(
        width=1600,
        height=900,
        background_color="white",
        colormap=colormap,
        collocations=False
    ).generate(texto_unido)

    os.makedirs("output", exist_ok=True)
    ruta_salida = "output/nube.png"
    wc.to_file(ruta_salida)

    if verbose:
        print(f"[INFO] Nube de palabras guardada en: {ruta_salida}")

    return ruta_salida
