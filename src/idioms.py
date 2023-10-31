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
        final_result = []
        szigriszt_values = []
        fernandez_huerta_values = []
        mu_legibility_values = []
        total_words = 0
        total_phrases = 0
        total_syllables = 0
        for index, pharagraph in enumerate(pharagraphs):
            tokenized_pharagraph = nlp(pharagraph)
            letters_counter = get_letters_per_word(tokenized_pharagraph)
            word_counter = calculate_words(tokenized_pharagraph)
            phrases_counter = calculate_phrases(tokenized_pharagraph.sents)
            syllables_counter = calculate_syllables(tokenized_pharagraph)
            
            total_words += word_counter
            total_phrases += phrases_counter
            total_syllables += syllables_counter
            
            perspicuity_values = {'words': word_counter, 'phrases': phrases_counter, 'syllables':syllables_counter, 'letters': letters_counter, 'Three_sillabls_words':0 }            
            result = calculate_perspicuitySPA(perspicuity_values)
            sigrizt_result = result[SIGRISZPAZOS]
            fernandez_result = result[FERNANDEZHUERTA]
            mu_result = result[MULEGIBILITY]
            
            Value = f'{index}{csvSeparator}{sigrizt_result}{csvSeparator}{fernandez_result}{csvSeparator}{mu_result}'
            
            final_result.append({ **dict(zip(Text.split(';'), Value.split(';'))), **perspicuity_values, 'letters': sum(letters_counter) })
            szigriszt_values.append(sigrizt_result)
            fernandez_huerta_values.append(fernandez_result)
            mu_legibility_values.append(mu_result)
        #Crea el json
        json = {}
        json["Parrafo"] = len(final_result)
        json["words"] = total_words
        json["phrases"] = total_phrases
        json["syllables"] = total_syllables
        json[f'{SIGRISZPAZOS_TEXT}_{INFLESZ_TEXT}'] = str(calculate_average(szigriszt_values))
        json[FERNANDEZHUERTA_TEXT] = str(calculate_average(fernandez_huerta_values))
        json[MULEGIBILITY_VAR_TEXT] = str(calculate_average(mu_legibility_values))
        json["paragraphInfo"] = final_result 
        return json

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
        final_result = []
        flesh_values = []
        fog_values = []
        smog_values = []
        total_words = 0
        total_phrases = 0
        total_syllables = 0
        for index, pharagraph in enumerate(pharagraphs):
            tokenized_pharagraph = nlp(pharagraph)
            letters_counter = get_letters_per_word(tokenized_pharagraph)
            word_counter = calculate_words(tokenized_pharagraph)
            phrases_counter = calculate_phrases(tokenized_pharagraph.sents)
            syllables_counter = calculate_syllables_eng(tokenized_pharagraph)
            syllables_three_counter = calculate_three_syllables(tokenized_pharagraph)
            
            total_words += word_counter
            total_phrases += phrases_counter
            total_syllables += syllables_counter
            
            perspicuity_values = {'words': word_counter, 'phrases': phrases_counter, 'syllables':syllables_counter, 'letters': letters_counter ,'Three_sillabls_words':syllables_three_counter}
            result = calculate_perspicuityENG(perspicuity_values)
            flesh_result = result[FLESH]
            fog_result = result[FOG]
            smog_result = result[SMOG]
            
            Value = f'{index}{csvSeparator}{flesh_result}{csvSeparator}{fog_result}{csvSeparator}{smog_result}'
            
            final_result.append({ **dict(zip(Text.split(';'), Value.split(';'))), **perspicuity_values, 'letters': sum(letters_counter) })
            flesh_values.append(flesh_result)
            fog_values.append(fog_result)
            smog_values.append(smog_result)
        #Crea el json
        json = {}
        json["Parrafo"] = len(final_result)
        json["words"] = total_words
        json["phrases"] = total_phrases
        json["syllables"] = total_syllables
        json[FLESH_TEXT] = str(calculate_average(flesh_values)),
        json[FOG_TEXT] = str(calculate_average(fog_values))
        json[SMOG_TEXT] = str(calculate_average(smog_values))
        json["paragraphInfo"] = final_result 
        return json
    

def calculate_average(data: list[float]) -> float:
    average = sum(data) / len(data)
    return round(average, 2)