import json
from src.constants import *
from src.Images import *
from src.pdf import *
from src.perspicuity import *
from src.Results import *
from src.Text import *
from src.idioms import *
from fastapi import HTTPException
import os 
import datetime
import asyncio


current_date = ''

def CreateRange(Param):
    Lista = []
    for i in range(Param[1],Param[2]+1):
        Lista.append(i)  
    return Lista


#Función principal que maneja todo el flujo del programa
def process_file(Param):
    print(f"Init time: {str(datetime.datetime.now())}")
    #Limpia archivos auxiliares TXT
    clean_file()
    #Obtiene conteo desde donde comenzar a contar en PDF
    Lista = CreateRange(Param)

    #Crea imagenes PDF
    #await asyncio.to_thread(ReadPDF, Param[0], Param[1], Param[2])
    ReadPDF(Param[0], Param[1], Param[2])

    #Binarizacion y extraccion de texto de pdf
    #await asyncio.to_thread(refine_image, Lista)

    refine_image(Lista)
    # Param[3] = Idioma

    #Borra imagenes creadas de PDF
    delete_files(Param[1], Param[2])
    #await asyncio.to_thread(delete_files, Param[1], Param[2])

    #Escribe resultados 
    return WriteResults()
    #return asyncio.to_thread(WriteResults)

def languageValidation(idioma):
    return idioma != "es" and idioma != "en"

def pageValidation(num1,num2):
    if num1 and num2 > 0:
        return num1>num2
    else:
        return False

def DeletePDF(Loc):
    os.remove(Loc)


def process_text(Text):
    try:
        #Limpia archivos auxiliares TXT
        clean_file()
        #Pasa el texto en el output_text
        open(OUTPUT_TEXT, "a", encoding="utf-8").write(Text)
        return WriteResults()
    except:
        raise HTTPException(status_code=400, detail=f"Ingrese un texto más largo")


def FindTicket(ticket):
    try:
        with open(f'src/Files/Results/{ticket}.json', 'r') as f:
            #contenido = f.read().replace('\\','') 
            return json.load(f)
    except:
            Var = os.listdir('src/Files/Results/')
            Var.remove('file.txt')
            files ="Ninguno" if Var == None else Replace_TXT(Var)

            raise HTTPException(status_code=400, detail=f"Los resultados no están aún o se digitó mal el ticket, los resultados disponible son: {files}")
            return {"ticket": f"{ticket}"}
    
def CreateTicketResult(Path, result):
    #chars = '{/}"'
    #my_str = json.dumps(result).translate(str.maketrans('', '', chars))
    my_json = json.dumps(result) if result != {} else "El OCR no detectó alguna palabra."
    with open(Path, "w") as archivo:
        archivo.write(my_json)
        

def Replace_TXT(List):
    New_List = []
    for i in List:
        New_List.append(i.replace('.json', ''))
    return New_List


def Validation_Result():
    Var = os.listdir('src/Files/Results/')
    Var.remove('file.txt')
    if len(Var) >= 10:
        for i in Var:
            os.remove(f"src/Files/Results/{i}")

def Create_Result(List):
    print('Running main function')
    try:
    #Inicializando variables
        Source = List[0]
        num1 = List[1]
        num2 = List[2]
        Ticket = List[3]
        Idioma = List[5]
        NameFile = List[6]
        Results = process_file([Source, num1, num2, Idioma])
        DeletePDF(Source)
        #Casteando dict a str
        #my_str = json.dumps(Results)
        #Result_Path = f"src/Files/Results/{Ticket}.txt"
        Result_Path = f"src/Files/Results/{Ticket}.json"
        #CreateTicketResult(Result_Path, my_str)
        Results['Init_Date'] = str(datetime.datetime.now())
        Results['Name_File'] = NameFile
        Results['Idioma'] = Idioma

        CreateTicketResult(Result_Path, Results)
        print('Finish json results')
        print(f"End time: {str(datetime.datetime.now())}")
    except Exception as e:
        print(f'{e}')
        try:
            DeletePDF(Source)
        except:
            pass
        return {"Error a la hora de procesar PDF o número de páginas colocadas no existe"}
    

def ValidacionPaginas(num1, num2, source):
    # Abre el archivo PDF en modo lectura
    with fitz.open(source) as doc:
        # Obtiene el número de páginas del PDF
        num_paginas = len(doc)
    if num1>num_paginas or num2>num_paginas:
        return True
    return False


def CalculateEstimatedTime(num1, num2,source) -> tuple[str, int]:
    X = num2-num1
    Y = round(0.39846153846153837*X -0.21999999999999859,0)
    if Y >=60.0:
        min = round(Y/60,0)
        seg = Y-min*60
        return f"{min} min con {seg} s", Y
    return f"{Y} segundos", Y