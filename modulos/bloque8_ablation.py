# ==========================================================
# BLOQUE 8 - ABLACIÓN / REDUCCIÓN DE TÓPICOS
# ==========================================================

def ablar_topicos(topic_model, textos, embeddings, verbose=False):
    """
    Aplica reducción de tópicos usando BERTopic.
    Retorna:
        - modelo_reducido
        - info_reduccion: {"antes": X, "despues": Y}
    """
    if topic_model is None:
        print("[ERROR] No se recibió un modelo BERTopic válido.")
        return None, None

    try:
        if verbose:
            print("\n[INFO] Iniciando reducción de tópicos con BERTopic...")

        # Cantidad original de tópicos
        topicos_antes = len(topic_model.get_topics())

        # Reducción de tópicos (versión nueva de BERTopic)
        modelo_reducido = topic_model.reduce_topics(
            docs=textos,
            nr_topics="auto"
        )

        topicos_despues = len(modelo_reducido.get_topics())

        if verbose:
            print("[INFO] Reducción completada exitosamente.")
            print(f"[INFO] Tópicos antes: {topicos_antes}")
            print(f"[INFO] Tópicos después: {topicos_despues}")

        info = {
            "antes": topicos_antes,
            "despues": topicos_despues
        }

        return modelo_reducido, info

    except Exception as e:
        print(f"[ERROR] Falló la ablación de tópicos: {e}")
        return None, None
