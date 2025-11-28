# PNL-Pipeline-Generador-de-Reportes-Interactivos
Pipeline de Análisis de Texto en Python que automatiza el flujo de trabajo completo: desde el preprocesamiento, pasando por análisis descriptivo (Nubes de Palabras, N-gramas) y Modelado de Tópicos (BERTopic) . El proceso incluye reducción de dimensionalidad UMAP , detección de outliers  y finaliza con un informe HTML interactivo.
Este proyecto implementa un pipeline completo de análisis de texto, dividido en bloques independientes que trabajan de forma secuencial:

lectura de datos,

preprocesamiento,

vectorización,

entrenamiento de modelos clásicos,

evaluación y métricas.

Todo el sistema fue diseñado para ser fácil de ejecutar desde la terminal, usando argumentos y archivos de prueba incluidos en el repositorio.

El objetivo principal es contar con un flujo reproducible, modular y entendible que permita analizar datos textuales desde cero.

🚀 Funcionalidades principales
📥 Entrada del sistema

El programa toma como entrada un archivo .csv y una columna que contiene los textos.
Los parámetros se manejan desde la terminal mediante argparse.

Ejemplo general (incluido en commands.txt):

python main.py --input "data/ejemplo.csv" --columna "texto"

🔧 Bloque 1 – Manejo de argumentos

Este módulo define todos los parámetros que el usuario puede activar:

ruta del CSV

nombre de la columna de texto

opción para activar el preprocesamiento

tipo de vectorización

modelo de clasificación

modo verboso

Los argumentos permiten combinar distintos flujos sin modificar el código.

🧹 Bloque 2 – Carga de archivos

Incluye funciones para:

leer CSV con codificaciones variadas

validación de columnas

limpieza básica del dataset (NaN, espacios, textos vacíos)

El bloque siempre regresa un DataFrame limpio y listo para procesar.

✏️ Bloque 3 – Preprocesamiento de texto

Aquí se realiza el tratamiento del texto antes de vectorizarlo.
Tu implementación incluye:

✔️ Conversión a minúsculas
✔️ Eliminación de signos, números y URLs
✔️ Normalización de espacios
✔️ Tokenización por expresiones regulares
✔️ Stopwords personalizadas
✔️ Lematización sencilla opcional

El resultado final queda en una columna llamada:

texto_procesado

🔢 Bloque 4 – Vectorización

Se implementaron tres métodos clásicos:

Bag of Words

TF–IDF

CountVectorizer

Cada uno puede activarse desde la línea de comandos.

El vector resultante se usa directamente por los clasificadores.

🤖 Bloque 5 – Clasificadores

Incluyes el entrenamiento de varios modelos clásicos:

Regresión logística

Naive Bayes

SVM lineal

Árbol de decisión

KNN

Cada modelo genera:

matriz de confusión

accuracy

reporte de clasificación

Los resultados se imprimen en consola.

📄 Bloque 6 – Ejecución orquestada (main.py)

Este archivo une todos los bloques y ejecuta el pipeline completo:

Leer argumentos

Cargar CSV

Preprocesar texto

Vectorizar

Entrenar modelo

Mostrar métricas

El flujo es completamente automático.

📁 Estructura del proyecto
data/
    ejemplo.csv
    comandos_de_prueba.txt   # ejecutables que usa el proyecto
modulos/
    bloque1_args.py
    bloque2_carga.py
    bloque3_preproc.py
    bloque4_vectorizacion.py
    bloque5_modelos.py
main.py
README.md

📦 Requisitos y versiones usadas

Estas son las versiones reales que anotaste en tu archivo commands.txt:

Python 3.13
numpy 2.1.1
pandas 2.2.2
scikit-learn 1.5.0
nltk 3.9


(Si deseas agrego más versiones o verifico las que tienes instaladas.)

📂 Archivo ejecutable: commands_example.txt

Incluye ejemplos listos para correr:

python main.py --input "data/ejemplo.csv" --columna "texto" --modelo "svm"
python main.py --input "data/ejemplo.csv" --columna "comentario" --preprocesar 1 --vector "tfidf"
python main.py --input "data/otra.csv" --columna "review" --modelo "logreg"

👨‍💻 Autor

Alejandro Frías Cortéz — Proyecto académico de procesamiento de lenguaje natural en Python.
