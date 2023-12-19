import es_core_news_sm
import spacy
from src.constants import *
from src.pdf import *
from src.perspicuity import *
from src.Results import *
from src.Text import *
# NO DELETE
import spacy_fastlang


def WriteResults():
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("language_detector")
    raw_file = open(OUTPUT_TEXT, "r", encoding="utf-8")
    Lines = raw_file.readlines()
    refined_text = refine_text(Lines)
    pharagraphs = refined_text.split('@')
    pharagraphs = list(filter(None, pharagraphs))
    language =  nlp(pharagraphs[0])._.language
    model = nlp if language == "en" else es_core_news_sm.load()
    final_result = []
    value = ''
    csvSeparator = ";"
    spanish_text = f'Parrafo{csvSeparator}{SIGRISZPAZOS_TEXT}_{INFLESZ_TEXT}{csvSeparator}{FERNANDEZHUERTA_TEXT}{csvSeparator}{MULEGIBILITY_VAR_TEXT}'
    english_text = f'Parrafo{csvSeparator}{FLESH_TEXT}{csvSeparator}{FOG_TEXT}{csvSeparator}{SMOG_TEXT}'
    total_values = {"words": 0, "syllables": 0, "phrases": 0 }
    spa_values = {"szigriszt": [], "fernandez_huerta": [], "mu_legibility": []}
    eng_values = {"flesh": [], "fog": [], "smog": []}

    for index, pharagraph in enumerate(pharagraphs):
        tokenized_pharagraph = model(pharagraph)
        letters_counter = get_letters_per_word(tokenized_pharagraph)
        word_counter = calculate_words(tokenized_pharagraph)
        phrases_counter = calculate_phrases(tokenized_pharagraph.sents)
        syllables_counter = calculate_syllables_eng(tokenized_pharagraph) if language == "en" else calculate_syllables(tokenized_pharagraph)
        syllables_three_counter = calculate_three_syllables(tokenized_pharagraph) if language == "en" else 0
        total_values["words"] += word_counter
        total_values["phrases"] += phrases_counter
        total_values["syllables"] += syllables_counter
        perspicuity_values = {'words': word_counter, 'phrases': phrases_counter, 'syllables':syllables_counter, 'letters': letters_counter, 'Three_sillabls_words': syllables_three_counter }  
        result = calculate_perspicuitySPA(perspicuity_values) if language == "es" else calculate_perspicuityENG(perspicuity_values)
        
        if language == "es":
            sigrizt_result = result[SIGRISZPAZOS]
            fernandez_result = result[FERNANDEZHUERTA]
            mu_result = result[MULEGIBILITY]
            spa_values["szigriszt"].append(sigrizt_result)
            spa_values["fernandez_huerta"].append(fernandez_result)
            spa_values["mu_legibility"].append(mu_result)
            value = f'{index}{csvSeparator}{sigrizt_result}{csvSeparator}{fernandez_result}{csvSeparator}{mu_result}'
        else:
            flesh_result = result[FLESH]
            fog_result = result[FOG]
            smog_result = result[SMOG]
            eng_values["flesh"].append(flesh_result)
            eng_values["fog"].append(fog_result)
            eng_values["smog"].append(smog_result)
            value = f'{index}{csvSeparator}{flesh_result}{csvSeparator}{fog_result}{csvSeparator}{smog_result}'

        Text = spanish_text if language == "es" else english_text
        final_result.append({ **dict(zip(Text.split(';'), value.split(';'))), **perspicuity_values, 'letters': sum(letters_counter), "content": pharagraph })

    values = spa_values if language == "es" else eng_values
    return GenerateJson(language, total_values, values, final_result)
    
def GenerateJson(language, total_values, values, result):
    json = {}
    json["Parrafo"] = len(result)
    json["words"] = total_values["words"]
    json["phrases"] = total_values["phrases"]
    json["syllables"] = total_values["syllables"]
    json["paragraphInfo"] = result 
    json["language"] = language

    if language == "es":
        json[f'{SIGRISZPAZOS_TEXT}_{INFLESZ_TEXT}'] = str(calculate_average(values["szigriszt"] or []))
        json[FERNANDEZHUERTA_TEXT] = str(calculate_average(values["fernandez_huerta"] or []))
        json[MULEGIBILITY_VAR_TEXT] = str(calculate_average(values["mu_legibility"] or []))
    else:
        json[FLESH_TEXT] = str(calculate_average(values["flesh"] or []))
        json[FOG_TEXT] = str(calculate_average(values["fog"] or []))
        json[SMOG_TEXT] = str(calculate_average(values["smog"] or []))
    return json

def calculate_average(data: list[float]) -> float:
    average = sum(data) / len(data)
    return round(average, 2)