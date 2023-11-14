import os
import matplotlib
import matplotlib.pyplot as plt
import pytesseract
from src.constants import *
from PIL import Image
from pdf2image import convert_from_path
from src.perspicuity import *
from multiprocessing import Pool
import fitz


number_pages = 0
Idioma = ''


def deletePlot():
    try:
        os.remove('docs/plot-FernandezHuerta-hist.png')
        os.remove('docs/plot-MuLegibility-hist.png')
        os.remove('docs/plot-resByParagraph.png')
        os.remove('docs/plot-SzigrisztPazos-hist.png')
    except Exception as e:
        return None

def ReadPDF(Pdf, First, Last):
    pdf_doc  = fitz.open(Pdf)
    Aux =1
    for pg in range(First-1, Last):
        page = pdf_doc[pg]
        pix = page.get_pixmap(alpha=False)
        img_bytes = pix.samples

        img = Image.frombytes('RGB', (pix.width, pix.height), img_bytes)
        img = img.convert('L')
        img.save(f'docs/plt-pagina_{Aux}.jpg')
        Aux+=1


def Binarizacion(i):
    file_name = define_file_name(i[0])
    text = str(pytesseract.image_to_string(Image.open(DOCS_ROUTE+'plt-'+file_name),config='-c page_separator='' '))
    text = text.replace('-\n', '')
    
    open(OUTPUT_TEXT, "a", encoding="utf-8").write(text)

#La imagen se convierte primero a escala de grises y luego se binariza para obtener mejores resultados
def refine_image(Lista):
    Aux = []
    var = 1
        
    for i in range(len(Lista)):
        Aux.append(var)
        Binarizacion([var])
        var+=1
    open(OUTPUT_TEXT, "a", encoding="utf-8").close()

#Se crea la imagen binarizada y se guarda. La imagen en escala de grises se desecha 
def plot_image(plot_configs, binary_otsu):
    matplotlib.rcParams['font.size'] = 12
    mult=5
    plt.figure(figsize=((int)(plot_configs['width']/plot_configs['dpi'])*mult, (int)(plot_configs['height']/plot_configs['dpi'])*mult))
    plt.imshow(binary_otsu, cmap=plt.cm.gray)
    plt.axis('off')
    plt.savefig(plot_configs['file_path'], bbox_inches='tight')
    plt.cla()
    plt.close()

def define_file_name(number): 
    return 'pagina_'+ str(number) + '.jpg'

def define_file_path(file_name):
    return DOCS_ROUTE+file_name

#Elimina las imagenes originales, a las que no se les ha aplicado ningún algoritmo de procesamiento de imágenes
def delete_files(first_page, last_page):
    global number_pages
    number_pages = number_pages
    for i in range(1, last_page-first_page+2):
        file_name = define_file_name(i)
        file_path = define_file_path(file_name)
        try:
            #os.remove(file_path)
            os.remove(DOCS_ROUTE+'plt-'+file_name)
        except Exception as e:
            continue