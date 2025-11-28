import matplotlib
matplotlib.use("Agg")  # <- backend sin GUI, estable

from modulos.bloque1_args import crear_parser
from modulos.bloque2_carga import cargar_csv
from modulos.bloque3_preproc import preprocesar_textos
from modulos.bloque4_wordcloud import generar_wordcloud
from modulos.bloque5_ngrams import generar_ngramas
from modulos.bloque6_embeddings import generar_embeddings
from modulos.bloque7_bertopic import modelado_topicos_bertopic
from modulos.bloque8_ablation import ablar_topicos
from modulos.bloque9_visualizacion import visualizar_topicos
from modulos.bloque10_html import generar_html_salida
from modulos.bloque11_outliers import detectar_outliers, extraer_textos_outliers

import os

def main():
    # ================= BLOQUE 1: Argumentos =================
    parser = crear_parser()
    args = parser.parse_args()

    PALETAS = {
        1: "viridis",
        2: "autumn",
        3: "winter",
        4: "cubehelix",
        5: "tab20"
    }

    paleta = PALETAS.get(args.paleta, "viridis")


    if args.verbose:
        print("\n[INFO] === Iniciando Script de Análisis de Texto ===")
        print(f"[INFO] Archivo: {args.archivo}")
        print(f"[INFO] Columnas: {args.columnas}")
        print(f"[INFO] Paleta seleccionada: {paleta}")
        print(f"[INFO] Idioma: {args.idioma}")

    # ================= BLOQUE 2: Cargar CSV =================
    df = cargar_csv(args.archivo, args.columnas, verbose=args.verbose)
    if df is None:
        print("[ERROR] No se pudo cargar el CSV.")
        return

    if args.verbose:
        print("\n=== Vista previa del DataFrame ===")
        print(df.head())

    # ================= PREPROCESAMIENTO =================
    textos_limpios, tokens_por_doc = preprocesar_textos(
        df["texto"], idioma=args.idioma, verbose=args.verbose
    )

    # ================= NUBE DE PALABRAS =================
    ruta_nube = generar_wordcloud(textos_limpios, paleta=paleta, verbose=args.verbose)

    # ================= N-GRAMAS =================
    ruta_bi = generar_ngramas(textos_limpios, n=2, nombre="bigramas", paleta=paleta)
    ruta_tri = generar_ngramas(textos_limpios, n=3, nombre="trigramas", paleta=paleta)

    # ================= EMBEDDINGS =================
    embeddings = generar_embeddings(textos_limpios, verbose=args.verbose)

    # ================= BERTopic =================
    resultados_bertopic = modelado_topicos_bertopic(
        textos_limpios=textos_limpios,
        idioma=args.idioma,
        verbose=args.verbose
    )
    modelo_bertopic = resultados_bertopic["topic_model"]

    # ================= Extraer tópicos originales =================
    topicos_antes = modelo_bertopic.get_topics()

    # ================= ABLACIÓN DE TÓPICOS =================
    modelo_reducido, info_ablation = ablar_topicos(
        topic_model=modelo_bertopic,
        textos=textos_limpios,
        embeddings=embeddings,
        verbose=args.verbose
    )
    modelo_a_usar = modelo_reducido if modelo_reducido else modelo_bertopic

    # ================= Extraer tópicos reducidos =================
    topicos_reducidos = modelo_a_usar.get_topics()

    # ================= VISUALIZACIÓN UMAP =================
    os.makedirs("salidas", exist_ok=True)
    ruta_umap = "salidas/umap_plot.html"

    fig_html = visualizar_topicos(
        modelo=modelo_a_usar,
        textos_limpios=textos_limpios,
        embeddings=embeddings,
        verbose=args.verbose,
        titulo="Tópicos (UMAP 2D)",
        return_fig=True,
        paleta=paleta
    )

    with open(ruta_umap, "w", encoding="utf-8") as f:
        f.write(fig_html)

    # ================= OUTLIERS =================
    outliers_idx = detectar_outliers(embeddings, porcentaje=0.05, verbose=args.verbose)
    textos_outliers = extraer_textos_outliers(df, outliers_idx, max_ejemplos=5)

    if args.verbose:
        for i, t in enumerate(textos_outliers, 1):
            print(f"[OUTLIER {i}] {t[:200]}...")

    # ================= RUTAS PARA HTML =================
    rutas = {
        "nube": ruta_nube,
        "bigramas": ruta_bi,
        "trigramas": ruta_tri,
        "umap": ruta_umap,
        "outliers": textos_outliers,
        "topic_model": modelo_a_usar,
        "info_ablation": info_ablation,
        "topicos_antes": topicos_antes,        # <-- agregado
        "topicos_reducidos": topicos_reducidos # <-- agregado

        
        
    }

    # ================= HTML FINAL =================
    config = {
        "archivo": args.archivo,
        "idioma": args.idioma,
        "paleta": paleta,
        "titulo": args.titulo
    }

    generar_html_salida(config, rutas)

if __name__ == "__main__":
    main()
