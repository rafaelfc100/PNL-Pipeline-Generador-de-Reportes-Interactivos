# PNL-Pipeline-Generador-de-Reportes-Interactivos
Pipeline de Análisis de Texto en Python que automatiza el flujo de trabajo completo: desde el preprocesamiento, pasando por análisis descriptivo (Nubes de Palabras, N-gramas) y Modelado de Tópicos (BERTopic) . El proceso incluye reducción de dimensionalidad UMAP , detección de outliers  y finaliza con un informe HTML interactivo.

# PNL-Pipeline-Generador-de-Reportes-Interactivos
Pipeline completo de Análisis de Texto en Python que automatiza todo el flujo de trabajo: desde la carga y preprocesamiento de datos, generación de nubes de palabras y n-gramas, embeddings vectoriales, reducción dimensional, clustering y modelado de tópicos con BERTopic, hasta producir un informe HTML interactivo.

Este proyecto está organizado en bloques modulares, cada uno encargado de una etapa del procesamiento.

---

## Estructura del Proyecto

---

## **Descripción de cada bloque**

### 🔹 **Bloque 1 — Argumentos CLI (`bloque1_args.py`)**
Define los argumentos del programa:
- Ruta del CSV
- Columnas a analizar
- Paleta de colores
- Idioma
- Título del reporte
- Verbose para depuración  
Incluye validación de archivo y ayuda interactiva.

---

### 🔹 **Bloque 2 — Carga de Datos (`bloque2_carga.py`)**
Funciones para:
- Cargar el CSV con soporte UTF-8 / ISO-8859-1
- Unir varias columnas de texto si es necesario
- Validar columnas existentes
- Limpiar filas vacías

Retorna un DataFrame con una única columna: `texto`.

---

### 🔹 **Bloque 3 — Preprocesamiento (`bloque3_preproc.py`)**
Incluye:
- Limpieza inicial del texto
- Lematización con spaCy
- Stopwords del idioma elegido
- Eliminación de acentos
- Conversión a tokens  
Produce:
- `textos_limpios`
- `tokens_por_doc`

---

### 🔹 **Bloque 4 — WordCloud (`bloque4_wordcloud.py`)**
Genera una nube de palabras con:
- Paletas configurables
- Guardado automático en `output/nube.png`

---

### 🔹 **Bloque 5 — N-gramas (`bloque5_ngrams.py`)**
Generación de:
- Bigramas
- Trigramas  
Incluye:
- Filtro de stopwords
- Selección de top n-gramas
- Gráfica en PNG con la paleta seleccionada
- - Guardado automático en `output/trigrama.png`
  - - Guardado automático en `output/bigrama.png`

---

### 🔹 **Bloque 6 — Embeddings (`bloque6_embeddings.py`)**
Crea vectores de embeddings utilizando:

Incluye información de debug:
- Número de documentos
- Dimensionalidad del vector

---

### 🔹 **Bloque 7 — Modelado de Tópicos (BERTopic) (`bloque7_bertopic.py`)**
Implementa el pipeline completo:
1. **Embeddings**
2. **UMAP** para reducción
3. **HDBSCAN** para clustering
4. **BERTopic** para extracción de temas

Devuelve un diccionario con:
- Modelo BERTopic
- Tópicos originales
- Probabilidades
- Embeddings

---

### **🔹 BLOQUE 8 — Ablación de tópicos**
Reduce tópicos usando:
- reducción de dimensionalidad  
- eliminación de temas irrelevantes
- reducción o depuración de tópicos usando las herramientas internas de BERTopic

Devuelve modelo reducido + estadísticas.

---

### **🔹 BLOQUE 9 — Visualización (UMAP + Plotly)**  
Convierte colormaps de Matplotlib a HEX.  
Genera **visualización interactiva** UMAP 2D.  
Crea un archivo HTML embebible.

---

### **🔹 BLOQUE 10 — Generación del HTML final**
Construye un **reporte web profesional**, con:

- WordCloud  
- Bigrams y trigrams  
- Tópicos originales  
- Tópicos reducidos  
- Outliers  
- UMAP interactivo  

Todo embebido sin rutas externas.

---

### **🔹 BLOQUE 11 — Outliers**
Usa Isolation Forest + PCA para detectar y graficar textos atípicos.

---

### **🔹 main.py**
Integra todo el pipeline y:
1. Ejecuta cada bloque  
2. Guarda todas las imágenes  
3. Genera el HTML final  
4. Imprime avances si `--verbose` está activado  

---

## 🛠️ **Requisitos y Versiones Recomendadas**

Para evitar errores con BERTopic, HDBSCAN y UMAP, se recomienda usar **estas versiones fijas**:

```txt
pandas==2.2.2
numpy==1.26.4
scikit-learn==1.3.2
matplotlib==3.8.0
seaborn==0.13.2
wordcloud==1.9.3
nltk==3.8.1
spacy==3.7.2
umap-learn==0.5.4
hdbscan==0.8.33
bertopic==0.16.0
plotly==5.22.0
python-dateutil==2.9.0.post0
```
Salida final
```
El sistema genera:
/salidas/
 ├── nube_palabras.png
 ├── bigramas.png
 ├── trigramas.png
 ├── umap_plot.html
 ├── reporte_final.html   ← ARCHIVO PRINCIPAL
```



