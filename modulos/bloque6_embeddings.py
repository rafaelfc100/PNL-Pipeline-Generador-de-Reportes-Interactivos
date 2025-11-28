# modulos/bloque6_embeddings.py

from sentence_transformers import SentenceTransformer

def generar_embeddings(textos_limpios, modelo="sentence-transformers/paraphrase-multilingual-mpnet-base-v2", verbose=False):
    """
    Genera embeddings vectoriales para cada documento usando un modelo de SentenceTransformers.
    
    Parámetros:
        textos_limpios : lista de strings ya preprocesados
        modelo : nombre del modelo pre-entrenado
        verbose : imprime información extra
    
    Retorna:
        embeddings : matriz (list of lists) con un vector por documento
    """

    if verbose:
        print("\n[INFO] Cargando modelo de embeddings...")
        print(f"[INFO] Modelo: {modelo}")

    # Cargar modelo solo una vez
    embedder = SentenceTransformer(modelo)

    if verbose:
        print("[INFO] Generando embeddings...")

    embeddings = embedder.encode(textos_limpios, show_progress_bar=verbose)

    if verbose:
        print(f"[INFO] Embeddings generados: {len(embeddings)} documentos.")
        print(f"[INFO] Dimensión del vector: {len(embeddings[0])}")

    return embeddings
