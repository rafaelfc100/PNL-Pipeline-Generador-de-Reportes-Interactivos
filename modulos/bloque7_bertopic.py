# bloque7_bertopic.py

from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import umap
import hdbscan

def modelado_topicos_bertopic(textos_limpios,
                              idioma="es",
                              n_dim=10,
                              min_cluster_size=10,
                              verbose=False):
    """
    Modelado de tópicos con BERTopic + Embeddings + UMAP + HDBSCAN.

    Parámetros:
        textos_limpios: lista de textos preprocesados
        idioma: modelo de embeddings ("es" usa Distiluse-base-multilingual)
        n_dim: dimensiones UMAP
        min_cluster_size: parámetro para HDBSCAN
        verbose: imprimir detalles
    
    Retorna:
        - modelo BERTopic
        - topicos
        - probabilidades
        - embeddings
        - topicos_reducidos
        - probs_reducidos
    """

    if verbose:
        print("\n[INFO] Iniciando Bloque 7: Modelado de Tópicos con BERTopic...")

    # ===== 1. Modelo de embeddings =====
    if idioma == "es":
        emb_model = SentenceTransformer("sentence-transformers/distiluse-base-multilingual-cased-v2")
    else:
        emb_model = SentenceTransformer("all-MiniLM-L6-v2")

    if verbose:
        print("[INFO] Generando embeddings...")

    embeddings = emb_model.encode(textos_limpios, show_progress_bar=verbose)

    # ===== 2. Reducción dimensional UMAP =====
    if verbose:
        print("[INFO] Aplicando UMAP a 10 dimensiones...")

    umap_model = umap.UMAP(
        n_components=n_dim,
        n_neighbors=15,
        min_dist=0.0,
        metric="cosine"
    )

    # ===== 3. Clustering con HDBSCAN =====
    if verbose:
        print("[INFO] Aplicando HDBSCAN...")

    hdbscan_model = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        metric='euclidean',
        cluster_selection_method='eom',
        prediction_data=True,
        core_dist_n_jobs=1
    )

    # ===== 4. BERTopic =====
    topic_model = BERTopic(
        language="multilingual",
        embedding_model=emb_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        verbose=verbose
    )

    if verbose:
        print("[INFO] Entrenando BERTopic...")

    topics, probs = topic_model.fit_transform(textos_limpios, embeddings)

    if verbose:
        print("[INFO] Tópicos generados correctamente:")
        print(topic_model.get_topic_info())

    # ===== 5. Reducción de tópicos (ABLACIÓN) =====
    if verbose:
        print("[INFO] Iniciando reducción de tópicos con BERTopic...")

    try:
        reduced_topics, reduced_probs = topic_model.reduce_topics(
            textos_limpios,
            nr_topics=None     # ← reducción automática
        )
        if verbose:
            print("[OK] Tópicos reducidos correctamente.")

    except Exception as e:
        reduced_topics = None
        reduced_probs = None
        if verbose:
            print(f"[ERROR] Falló la ablación de tópicos: {e}")

    return {
        "topic_model": topic_model,
        "topics": topics,
        "probabilidades": probs,
        "embeddings": embeddings,
        "reduced_topics": reduced_topics,
        "reduced_probabilities": reduced_probs
    }
