import os
import re
from datetime import datetime

from src.constants import *
from src.Images import *
from src.Logic import *
from API import *


def Escribir(Aux, TimeList):
    with open(f'docs/Results_{Aux}.csv', 'w') as f:
        for elemento in TimeList:
            f.write(elemento + '\n')

def TestFun():
    TimeList = []
    Count = 0
    Name = 0
    for i in os.listdir('input_folder_ingles'):
        Init = datetime.now()
        Last = int(re.findall(r'\d+', i)[0])
        Loc = f'input_folder_ingles/{i}'
        print(f'Leyendo {Loc}')
        process_file([Loc,1,Last, 'spa'])
        End = datetime.now()
        Aux = f'{Last},{End-Init}'
        TimeList.append(Aux)    
        Count+=1
        Name+=1
        if Count == 5:
            Escribir(Name, TimeList)
            TimeList = []
            Count = 0
    

#Probar una cosa
def Init():
    Loc = "input_folder/input_5.pdf"
    Init = 1
    Last = 4
    #'spa' de español 
    #'eng' de inglés
    Idioma = 'spa'
    return process_file([Loc,Init,Last, Idioma])
    



#Codigo para ejecutar programa en consola
if __name__ == '__main__':
    #TestFun()
    print(Init())

