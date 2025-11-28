# modulos/bloque3_preproc.py

import re
import nltk
from nltk.corpus import stopwords
import spacy
import unicodedata

# Descargar stopwords si falta
nltk.download('stopwords', quiet=True)

# Cargar modelo spaCy solo una vez
try:
    nlp = spacy.load("es_core_news_sm")
except:
    raise RuntimeError(
        "Error: falta el modelo de spaCy.\n"
        "Instálalo con:\n\n"
        "python -m spacy download es_core_news_sm"
    )
stopwords_espanol_custom = {
    'de','la','que','el','en','y','a','los','del','se','las','por','un','para','con','no','una',
    'su','al','lo','como','mas','pero','sus','le','ya','o','este','si','porque','esta','entre',
    'cuando','muy','sin','sobre','tambien','me','hasta','hay','donde','quien','desde','todo',
    'nos','durante','todos','uno','les','ni','contra','otros','ese','eso','ante','ellos','e',
    'esto','mi','antes','algunos','que','unos','yo','otro','otras','otra','el','tanto','esa',
    'estos','mucho','quienes','nada','muchos','cual','poco','ella','estar','estas','algunas',
    'algo','nosotros','mi','mis','tu','te','ti','tu','tus','ellas','nosotras','vosotros',
    'vosotras','os','mio','mia','mios','mias','tuyo','tuya','tuyos','tuyas','suyo','suya',
    'suyos','suyas','nuestro','nuestra','nuestros','nuestras','vuestro','vuestra','vuestros',
    'vuestras','esos','esas','estoy','estas','esta','estamos','estais','estan','este','estes',
    'estemos','esteis','esten','estare','estaras','estara','estaremos','estareis','estaran',
    'estaria','estarias','estariamos','estariais','estarian','estaba','estabas','estabamos',
    'estabais','estaban','estuve','estuviste','estuvo','estuvimos','estuvisteis','estuvieron',
    'estuviera','estuvieras','estuvieramos','estuvierais','estuvieran','estuviese','estuvieses',
    'estuviesemos','estuvieseis','estuviesen','estando','estado','estada','estados','estadas',
    'estad','he','has','ha','habemos','habeis','han','haya','hayas','hayamos','hayais','hayan',
    'habre','habras','habra','habremos','habreis','habran','habria','habrias','habriamos',
    'habriais','habrian','habia','habias','habiamos','habiais','habian','hube','hubiste','hubo',
    'hubimos','hubisteis','hubieron','hubiera','hubieras','hubieramos','hubierais','hubieran',
    'hubiese','hubieses','hubiesemos','hubieseis','hubiesen','habiendo','habido','habida',
    'habidos','habidas','soy','eres','es','somos','sois','son','sea','seas','seamos','seais',
    'sean','sere','seras','sera','seremos','sereis','seran','seria','serias','seriamos',
    'seriais','serian','era','eras','eramos','erais','eran','fui','fuiste','fue','fuimos',
    'fuisteis','fueron','fuera','fueras','fueramos','fuerais','fueran','fuese','fueses',
    'fuesemos','fueseis','fuesen','siendo','sido','sed','tengo','tienes','tiene','tenemos',
    'teneis','tienen','tenga','tengas','tengamos','tengais','tengan','tendre','tendras',
    'tendra','tendremos','tendreis','tendran','tendria','tendrias','tendriamos','tendriais',
    'tendrian','tenia','tenias','teniamos','teniais','tenian','tuve','tuviste','tuvo',
    'tuvimos','tuvisteis','tuvieron','tuviera','tuvieras','tuvieramos','tuvierais',
    'tuvieran','tuviese','tuvieses','tuviesemos','tuvieseis','tuviesen','teniendo','tenido',
    'tenida','tenidos','tenidas','tened','lugar','ser','ver'
}

def quitar_acentos(txt):
    """Elimina acentos después de lematizar."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', txt)
        if unicodedata.category(c) != 'Mn'
    )


def cargar_stopwords(idioma):
    """Cargar stopwords en el idioma elegido."""
    try:
        return set(stopwords.words({
            "es": "spanish",
            "en": "english",
            "fr": "french",
            "pt": "portuguese"
        }.get(idioma, "spanish")))
    except:
        return set()


def limpiar_texto(texto):
    """Limpieza básica previa a spaCy."""
    texto = texto.lower()
    texto = re.sub(r"http\S+|www\S+", "", texto)       # quitar URLs
    texto = re.sub(r"[^a-záéíóúñü ]", " ", texto)      # dejar solo letras
    texto = re.sub(r"\s+", " ", texto).strip()         # limpiar espacios
    return texto


def preprocesar_textos(textos, idioma="es", verbose=0):
    """
    Preprocesa texto usando:
    - limpieza
    - spaCy para lematización
    - eliminación de stopwords
    - eliminación de acentos (final)
    """
    if verbose:
        print("[INFO] Iniciando preprocesamiento con lematización...")

    stop = cargar_stopwords(idioma)

    textos_limpios = []
    tokens_por_doc = []

    for t in textos:

        t_original = t
        t = limpiar_texto(t)

        # Procesar con spaCy
        doc = nlp(t)
        tokens = []

        for token in doc:

            # ignorar stopwords y tokens muy cortos
            if token.text in stop:
                continue
            if len(token.text) <= 2:
                continue

            # Lema (forma base)
            lemma = token.lemma_.lower()

            # Eliminar acentos
            lemma = quitar_acentos(lemma)

            # ignorar tokens inútiles
            if len(lemma) <= 2:
                continue

            tokens.append(lemma)

        textos_limpios.append(" ".join(tokens))
        tokens_por_doc.append(tokens)

    if verbose:
        print("[INFO] Preprocesamiento terminado.")
        print("[INFO] Ejemplo antes:", textos[0][:120])
        print("[INFO] Ejemplo después:", textos_limpios[0][:120])

    return textos_limpios, tokens_por_doc
