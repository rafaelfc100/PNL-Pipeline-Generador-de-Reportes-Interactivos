# ==========================================================
# BLOQUE 10 - GENERA HTML FINAL DEL REPORTE
# ==========================================================

import base64
import os

def encode_image(path):
    """Convierte una imagen en base64 para incrustarla en HTML."""
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        print(f"[WARNING] No se pudo cargar la imagen {path}: {e}")
        return None


def generar_html_salida(config, rutas):
    """
    Genera un archivo HTML final con diseño profesional.
    """

    # ================= Extraer imágenes en base64 =================
    img_wc = encode_image(rutas.get("nube"))
    img_bi = encode_image(rutas.get("bigramas"))
    img_tri = encode_image(rutas.get("trigramas"))

    # ================= Extraer información de ablación =================
    info_ablation = rutas.get("info_ablation", None)
    topicos_antes = rutas.get("topicos_antes", {})
    topicos_reducidos = rutas.get("topicos_reducidos", {})

    # ================= Tópicos originales =================
    html_topics_originales = """
    <h2 class='section-title'>Tópicos Generados por BERTopic</h2>
    <div class='cards-container'>
    """

    for topic_id, words in topicos_antes.items():
        if topic_id == -1:
            continue
        lista = ", ".join([w for w, _ in words[:10]])
        html_topics_originales += f"""
            <div class='card'>
                <h3>Tópico {topic_id}</h3>
                <p>{lista}</p>
            </div>
        """

    html_topics_originales += "</div>"

    # ================= Tópicos reducidos =================
    html_topics_reducidos = ""

    if info_ablation:
        html_topics_reducidos += f"""
        <h2 class='section-title'>Ablación de Tópicos</h2>

        <div class='info-box'>
            <p><b>Tópicos antes de reducción:</b> {info_ablation['antes']}</p>
            <p><b>Tópicos después de reducción:</b> {info_ablation['despues']}</p>
        </div>

        <h2 class='section-title'>Tópicos Reducidos</h2>
        <div class='cards-container'>
        """

        for topic_id, words in topicos_reducidos.items():
            if topic_id == -1:
                continue
            lista = ", ".join([w for w, _ in words[:10]])
            html_topics_reducidos += f"""
            <div class='card'>
                <h3>Tópico {topic_id}</h3>
                <p>{lista}</p>
            </div>
            """

        html_topics_reducidos += "</div>"

    # ================= Construcción del HTML =================
    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{config.get("titulo", "Reporte de Análisis")}</title>

        <style>
            body {{
                font-family: Arial, Helvetica, sans-serif;
                margin: 0;
                background: #f7f7f7;
                color: #333;
                line-height: 1.6;
            }}

            header {{
                background: #2c3e50;
                color: white;
                padding: 25px;
                text-align: center;
            }}

            .container {{
                width: 85%;
                margin: auto;
                padding: 20px 0;
            }}

            .section-title {{
                margin-top: 40px;
                border-left: 6px solid #2980b9;
                padding-left: 10px;
                font-size: 26px;
                color: #2c3e50;
            }}

            img {{
                display: block;
                margin: 20px auto;
                max-width: 100%;
                border-radius: 8px;
                box-shadow: 0 0 8px rgba(0,0,0,0.15);
            }}

            hr {{
                border: 0;
                height: 1px;
                background: #ccc;
                margin: 40px 0;
            }}

            .cards-container {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }}

            .card {{
                background: white;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                transition: transform 0.2s;
            }}

            .card:hover {{
                transform: translateY(-5px);
            }}

            .info-box {{
                background: #dff0ff;
                padding: 15px;
                border-left: 5px solid #2980b9;
                border-radius: 5px;
                margin-bottom: 20px;
            }}

            ol li {{
                margin-bottom: 10px;
            }}

            footer {{
                margin-top: 40px;
                background: #2c3e50;
                color: white;
                text-align: center;
                padding: 15px;
            }}
        </style>
    </head>

    <body>

        <header>
            <h1>{config.get("titulo", "Reporte de Análisis")}</h1>
            <p>Archivo analizado: <b>{config.get("archivo")}</b></p>
            <p>Idioma: {config.get("idioma")} ─ Paleta: {config.get("paleta")}</p>
        </header>

        <div class="container">

            <h2 class='section-title'>Nube de Palabras</h2>
            {'<img src="data:image/png;base64,' + img_wc + '">' if img_wc else '<p>[Imagen no disponible]</p>'}

            <h2 class='section-title'>Bigrams</h2>
            {'<img src="data:image/png;base64,' + img_bi + '">' if img_bi else '<p>[Imagen no disponible]</p>'}

            <h2 class='section-title'>Trigrams</h2>
            {'<img src="data:image/png;base64,' + img_tri + '">' if img_tri else '<p>[Imagen no disponible]</p>'}

            {html_topics_originales}

            {html_topics_reducidos}

            <h2 class='section-title'>Outliers detectados</h2>
            <ol>
            {''.join([f'<li>{t}</li>' for t in rutas.get('outliers', [])])}
            </ol>

            <h2 class='section-title'>UMAP (2D) - Representación de Tópicos</h2>
            {open(rutas.get("umap"), "r", encoding="utf-8", errors="ignore").read() if rutas.get("umap") else "<p>[UMAP no disponible]</p>"}

        </div>

        <footer>
            Reporte generado automáticamente ─ {config.get("titulo")}
        </footer>

    </body>
    </html>
    """

    # Guardar HTML
    output = "salidas/reporte_final.html"
    os.makedirs("salidas", exist_ok=True)

    with open(output, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n[OK] Reporte HTML generado en: {output}")
