import es_core_news_sm
import spacy
from src.constants import *
from src.pdf import *
from src.perspicuity import *
from src.Results import *
from src.Text import *
import spacy


def Spa():
    nlp = es_core_news_sm.load()
    with open(OUTPUT_FILE, "a", encoding="utf-8") as text_file:
        pharagraphs = []
        raw_file = open(OUTPUT_TEXT, "r", encoding="utf-8")
        Lines = raw_file.readlines()
        refined_text = refine_text(Lines)
        pharagraphs = refined_text.split('@')
        pharagraphs = list(filter(None, pharagraphs))
        csvSeparator = ";"
        Value = ''
        Text = 'Parrafo'+csvSeparator+SIGRISZPAZOS_TEXT+'_'+INFLESZ_TEXT+csvSeparator+FERNANDEZHUERTA_TEXT+csvSeparator+MULEGIBILITY_VAR_TEXT
        for index, pharagraph in enumerate(pharagraphs):
            tokenized_pharagraph = nlp(pharagraph)
            letters_counter = get_letters_per_word(tokenized_pharagraph)
            word_counter = calculate_words(tokenized_pharagraph)
            phrases_counter = calculate_phrases(tokenized_pharagraph.sents)
            syllables_counter = calculate_syllables(tokenized_pharagraph)
            perspicuity_values = {'words': word_counter, 'phrases': phrases_counter, 'syllables':syllables_counter, 'letters': letters_counter, 'Three_sillabls_words':0 }            
            result = calculate_perspicuitySPA(perspicuity_values)   
            Value = str(index) + csvSeparator + str(result[SIGRISZPAZOS])  + csvSeparator + str(result[FERNANDEZHUERTA])+ csvSeparator + str(result[MULEGIBILITY])
        if Value == '':
            Value = '0;0;0;0'
        #Crea el json
        jsonFile = dict(zip(Text.split(';'), Value.split(';')))
        return jsonFile


#El resultado ingles se espera que retorne un json
def Eng():
    nlp = spacy.load("en_core_web_sm")
    with open(OUTPUT_FILE, "a", encoding="utf-8") as text_file:
        pharagraphs = []
        raw_file = open(OUTPUT_TEXT, "r", encoding="utf-8")
        Lines = raw_file.readlines()
        refined_text = refine_text(Lines)
        pharagraphs = refined_text.split('@')
        pharagraphs = list(filter(None, pharagraphs))
        csvSeparator = ";"

        Text = 'Parrafo'+csvSeparator+FLESH_TEXT+csvSeparator+FOG_TEXT+csvSeparator+SMOG_TEXT
        Value = ''
        for index, pharagraph in enumerate(pharagraphs):
            tokenized_pharagraph = nlp(pharagraph)
            letters_counter = get_letters_per_word(tokenized_pharagraph)
            word_counter = calculate_words(tokenized_pharagraph)
            phrases_counter = calculate_phrases(tokenized_pharagraph.sents)
            syllables_counter = calculate_syllables_eng(tokenized_pharagraph)
            syllables_three_counter = calculate_three_syllables(tokenized_pharagraph)
            perspicuity_values = {'words': word_counter, 'phrases': phrases_counter, 'syllables':syllables_counter, 'letters': letters_counter ,'Three_sillabls_words':syllables_three_counter}
            result = calculate_perspicuityENG(perspicuity_values)
            Value = str(index) + csvSeparator + str(result[FLESH]) + csvSeparator + str(result[FOG]) + csvSeparator + str(result[SMOG])


        if Value == '':
            Value = '0;0;0;0'
        #Crea el json
        jsonFile = dict(zip(Text.split(';'), Value.split(';')))
        return jsonFile