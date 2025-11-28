# bloque9_visualizacion.py

import plotly.express as px
import pandas as pd
import umap
import matplotlib.cm as cm
import matplotlib.colors as mcolors

def convertir_colormap_a_hex(nombre, n=20):
    """Convierte un colormap de Matplotlib en colores hexadecimales para Plotly."""
    cmap = cm.get_cmap(nombre, n)
    return [mcolors.to_hex(cmap(i)) for i in range(cmap.N)]


def visualizar_topicos(modelo, textos_limpios, embeddings,
                       verbose=False, titulo="Visualización de Tópicos",
                       return_fig=False, paleta="Blues"):
    """
    Visualiza los tópicos con UMAP usando Plotly.
    Si return_fig=True, regresa el div HTML para usarlo en el reporte.
    """

    if verbose:
        print("\n[INFO] Generando visualización avanzada de tópicos...")

    # Obtener tópicos desde el modelo
    topics, probs = modelo.transform(textos_limpios)

    df_viz = pd.DataFrame({
        "Documento": textos_limpios,
        "Topico": topics
    })

    # ----------- 🔥 CONFIGURACIÓN DE UMAP 🔥 -------------
    reducer = umap.UMAP(
        n_neighbors=15,
        min_dist=0.1,
        metric="cosine",
        random_state=42
    )

    X_2d = reducer.fit_transform(embeddings)
    df_viz["x"] = X_2d[:, 0]
    df_viz["y"] = X_2d[:, 1]

    # ---------------- PALETAS ----------------
    PALETAS = {
        1: "viridis",      # clásica
        2: "autumn",       # cálida
        3: "winter",       # fría
        4: "cubehelix",    # alto contraste
        5: "tab20"         # daltónicos
    }

    # Elegir colormap real
    cmap_name = paleta  # ya viene como string correcto
    # Convertir a colores hex para Plotly
    colores = convertir_colormap_a_hex(cmap_name, n=30)


    # Crear gráfica Plotly
    fig = px.scatter(
        df_viz,
        x="x",
        y="y",
        color="Topico",
        hover_data=["Documento"],
        title=titulo,
        width=900,
        height=600,
        color_discrete_sequence=colores
    )

    # Si se quiere para HTML → devolver código HTML
    if return_fig:
        return fig.to_html(full_html=True)

    # Caso normal: mostrar en pantalla
    fig.show()

    if verbose:
        print("[OK] Visualización generada con Plotly.")
