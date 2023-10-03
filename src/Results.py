import matplotlib.pyplot as plt
from src.constants import *
from src.perspicuity import *
from src.pdf import *

current_date = ''


def sort_formulas_results(formulas):
    return sorted(formulas, key=lambda x: float(x["indice_perspicuidad"]), reverse=True)
#Obtiene el índice de perspicuidad promedio de todos los párrafos por cada fórmula 
def calculate_average_formulas(formula):
    counter = 0
    total_sum = 0

    for table_object in formula:
        counter += 1
        total_sum += float(table_object[SORT_FIELD])
    
    if counter == 0:
        return 0
    average = total_sum/counter
    return round(average, 2)

#Crea todos los gráficos que se agregan al PDF de resultados
def plot_aggregate_results(paragraphsNumbers, plotData):
    bins = [0,10,20,30,40,50,60,70,80,90,100]
    plt.clf()
    plt.figure(figsize=[5.5,5], dpi=100)
    plt.hist(plotData[SIGRISZPAZOS], bins, color = "blue", ec = "black")
    plt.ylabel(LABEL_CANT_PARRAFOS)
    plt.xlabel(LABEL_VALOR_PERSPICUIDAD);
    plt.title('Resultados de '+SIGRISZPAZOS_TEXT+'_'+INFLESZ_TEXT);
    plt.savefig(DOCS_ROUTE+PLOT_SIGRISZPAZOS)
    plt.clf()
    plt.figure(figsize=[5.5,5], dpi=100)
    plt.hist(plotData[FERNANDEZHUERTA], bins, color = "red", ec = "black")
    plt.ylabel(LABEL_CANT_PARRAFOS)
    plt.xlabel(LABEL_VALOR_PERSPICUIDAD);
    plt.title('Resultados de '+FERNANDEZHUERTA_TEXT);
    plt.savefig(DOCS_ROUTE+PLOT_FERNANDEZHUERTA)
    plt.clf()
    plt.figure(figsize=[5.5,5], dpi=100)
    plt.hist(plotData[MULEGIBILITY], bins, color = "green", ec = "black")
    plt.ylabel(LABEL_CANT_PARRAFOS)
    plt.xlabel(LABEL_VALOR_PERSPICUIDAD);
    plt.title('Resultados de '+MULEGIBILITY_TEXT);
    plt.savefig(DOCS_ROUTE+PLOT_MULEGIBILITY)
    plt.clf()
    plt.figure(figsize=[10,6], dpi=250)
    plt.xlabel(LABEL_NUM_PARRAFO)
    plt.ylabel(LABEL_VALOR_PERSPICUIDAD)
    plt.title('');
    plt.grid(True)
    plt.plot(paragraphsNumbers, plotData[SIGRISZPAZOS], color='blue', marker='.', label=(SIGRISZPAZOS_TEXT+'/'+INFLESZ_TEXT))
    plt.plot(paragraphsNumbers, plotData[FERNANDEZHUERTA], color='red', marker='.', label=FERNANDEZHUERTA_TEXT)
    plt.plot(paragraphsNumbers, plotData[MULEGIBILITY], color='green', marker='.', label=MULEGIBILITY_TEXT)
    plt.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",mode="expand", borderaxespad=0, ncol=3)
    plt.ylim(ymin=0)
    plt.savefig(DOCS_ROUTE+PLOT_PARAGRAPHS)
    plt.clf()

def generatePDF(values_to_print, file_route, file_name, sorted_formulas, pdf_complete_report, number_of_pharagraphs):
    global current_date
    pdf = PDF()
    pdf.add_page()
    pdf.titles("ANÁLISIS DE LEGIBILIDAD")
    pdf.print_resumen(values_to_print, file_name)
    pdf.print_complete_report(pdf_complete_report, sorted_formulas, number_of_pharagraphs)
    pdf.add_page()
    pdf.seccion("Anexos")
    pdf.anexos()
    pdf.output(file_route+'/Resultados de análisis.pdf','F')


def PreGeneratePDF(general_values,szigriszt_values, fernandez_huerta_values, mu_legibility_values, szigriszt_average, fernandez_huerta_average, mu_average, Route, Param, sorted_formulas, pharagraphs):
    #PDF
    pdf_complete_report = []
    sorted_formulas = sort_formulas_results(general_values)
    szigriszt_average = calculate_average_formulas(szigriszt_values)
    fernandez_huerta_average = calculate_average_formulas(fernandez_huerta_values)
    mu_average = calculate_average_formulas(mu_legibility_values)
    values_to_print = {}
    values_to_print = {SIGRISZPAZOS: {"value": szigriszt_average, "name": SIGRISZPAZOS_TEXT}, FERNANDEZHUERTA: {"value": fernandez_huerta_average, "name": FERNANDEZHUERTA_TEXT}, "LegibilidadMu": {"value": mu_average,"name": MULEGIBILITY_VAR_TEXT}, "Inflesz": {"value": szigriszt_average, "name": INFLESZ_TEXT}}
    generatePDF(values_to_print, Route, Param, sorted_formulas, pdf_complete_report, len(pharagraphs))