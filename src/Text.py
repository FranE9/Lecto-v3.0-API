import re
from src.constants import *
from syltippy import syllabize
from src.perspicuity import *
from src.pdf import *
import syllables

#Devuelve el texto depurado 
def refine_text(Lines):
    raw_text = extract_file_text(Lines)
    return substract_from_text(raw_text)

#Junta todas las líneas de un texto en una sola variable
def extract_file_text(Lines):
    text_raw = ''
    for line in Lines:
        text_raw += line
    return text_raw

#Limpia el texto usando expresiones regulares
def substract_from_text(raw_text):
    raw_text = re.sub(r'[0-9]+([\.\,\+\-\*\/][0-9]+)*(%*)', '', raw_text)
    raw_text = re.sub(r'@', '', raw_text)
    raw_text = re.sub(r'(\.|\!|\?|\:)[\r\n\v\f][\r\n\v\f ]+', r'\1@', raw_text)
    raw_text = re.sub(r'(\[[ \t]*\])*(\([ \t]*\))*(\{[ \t]*\})*', '', raw_text)
    raw_text = re.sub(r'([ \t][ \t]+)', ' ', raw_text)
    raw_text = raw_text.encode("latin-1","ignore").decode("latin-1")
    refined_text = re.sub(r'[\r\n\t\v\f]+', ' ', raw_text)
    return refined_text

#Cuenta la cantidad de frases en un párrafo  
def calculate_phrases(phrases): 
    counter = 0
    
    for phrase in phrases:
        counter += 1
    return counter

#Cuenta la cantidad de palabras en un párrafo
def calculate_words(words):
    counter = 0
    
    for word in words:
        if word.pos_ != "PUNCT" and word.pos_ != "SYM":
            counter += 1
    return counter

#Cuenta la cantidad de sílabas en un párrafo
def calculate_syllables(words):
    syllables_counter = 0
    for word in words:
        if word.pos_ != "PUNCT" and word.pos_ != "SYM":
            syllables_counter += get_word_syllables(word)
    return syllables_counter

def calculate_syllables_eng(words):
    syllables_counter = 0
    for word in words:
        if word.pos_ != "PUNCT" and word.pos_ != "SYM":
            syllables_counter += get_word_syllables_eng(word)
    return syllables_counter

def calculate_three_syllables(words):
    syllables3_counter = 0
    for word in words:
        if word.pos_ != "PUNCT" and word.pos_ != "SYM":
            if((get_word_syllables_eng(word))>=3):
                syllables3_counter=syllables3_counter+1
    return syllables3_counter

#Extrae las sílabas de cada palabra
def get_word_syllables(word):
    syllables, stress = syllabize(u'{}'.format(word.text))
    return len(syllables)

def get_word_syllables_eng(word):
    words= str(word)
    syllabless = syllables.estimate(words)
    return syllabless

#Cuenta las letras en una palabra
def get_letters_per_word(words):
    letters_counter = []
    for word in words:
        if word.pos_ != "PUNCT" and word.pos_ != "SYM":
            letters_counter.append(len(word))
    
    return letters_counter

#Evalúa las fórmulas de perspicuidad con los datos obtenidos y obtiene los resultados
def calculate_perspicuitySPA(perspicuity_values):
    return {
        SIGRISZPAZOS: round(SzigrisztPazos(perspicuity_values).calculate(),2),    
        FERNANDEZHUERTA: round(FernandezHuerta(perspicuity_values).calculate(),2),
        MULEGIBILITY: round(MuLegibility(perspicuity_values).calculate(),2)
    }

#Formulas en ingles
def calculate_perspicuityENG(perspicuity_values):
    return {
        FLESH: round(Flesch(perspicuity_values).calculate(),2),
        SMOG: round(Smog(perspicuity_values).calculate(),2),
        FOG: round(Fog(perspicuity_values).calculate(),2)
    }

#Limpia los archivos TXT
def clean_file():
    open(OUTPUT_TEXT, "w", encoding="utf-8").close()
    open(OUTPUT_FILE, "w", encoding="utf-8").close()