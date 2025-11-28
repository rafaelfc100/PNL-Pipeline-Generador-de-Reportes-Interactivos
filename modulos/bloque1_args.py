# modulos/bloque1_args.py
import argparse
import os

def validar_archivo(archivo):
    """Valida que el archivo exista físicamente."""
    if not os.path.exists(archivo):
        raise argparse.ArgumentTypeError(f"El archivo '{archivo}' no existe.")
    return archivo

def crear_parser():
    parser = argparse.ArgumentParser(
        description="Script de análisis de texto con preprocesamiento, nubes de palabras, n-gramas, LDA, UMAP y reporte interactivo."
    )

    parser.add_argument(
        '--archivo', '-a',
        type=validar_archivo,
        required=True,
        help='Ruta del archivo CSV que contiene los textos a analizar.'
    )

    parser.add_argument(
        '--columnas', '-c',
        nargs='+',
        required=True,
        help='Nombre(s) de la(s) columna(s) que contienen el texto.'
    )

    parser.add_argument(
        '--paleta', '-p',
        type=int,
        choices=range(1, 6),
        default=1,
        help=(
            'Selecciona paleta de colores para los gráficos:\n'
            '1 = Clásica\n'
            '2 = Cálida\n'
            '3 = Fría\n'
            '4 = Alto contraste\n'
            '5 = Daltónicos (colorblind-friendly)'
        )
    )

    parser.add_argument(
        '--idioma', '-l',
        type=str,
        choices=['es', 'en', 'fr', 'pt', 'multi'],
        default='es',
        help='Idioma principal de los textos (es/en/fr/pt/multi).'
    )

    parser.add_argument(
        '--titulo', '-t',
        type=str,
        default="Reporte de análisis de texto",
        help='Título principal del reporte HTML generado.'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='count',
        default=0,
        help='Aumenta nivel de detalle (-v, -vv, -vvv).'
    )

    return parser
