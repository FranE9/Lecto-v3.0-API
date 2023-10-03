from fpdf import FPDF
from src.constants import *
from datetime import date

pdf_w=210
pdf_h=297

class PDF(FPDF):

    pdf_y=0

    #Aumenta el valor de la variable "y" global que se usa para colocar elementos en el PDF
    def aumentarValorY(self, aumento):
        self.pdf_y += aumento
        return self.pdf_y

    #Escribe títulos 
    def titles(self, text):
        self.set_xy(0.0,self.pdf_y)
        self.set_font('Arial', 'B', 16)
        self.cell(w=210.0, h=30.0, align='C', txt=text, border=0)

    #Escribe el header del documento
    def encabezado(self, archivo):
        self.set_font('Times', 'B', 12)
        self.set_xy(10.0,self.aumentarValorY(30.0))
        self.cell(0, 0, 'Texto analizado: %s' % (archivo), 0, 1, 'L', 0)

        self.set_font('Times', '', 12)

        self.cell(0, 0, 'Fecha: %s' % (date.today().strftime("%d/%m/%Y")), 0, 1, 'R', 0)

    #Escribe los separadores de cada sección
    def seccion(self, title):
        self.set_font('Times', 'B', 12)
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, '%s' % (title), 0, 1, 'L', 1)
        self.set_font('Times', '', 12)

    #Índice de perspicuidad de Szigrizs Pazos
    def get_ValorTablaSzigrizs(self,result):
        if 0 <= result < 15:
            self.set_fill_color(248,105,107)
            return "Lectura Muy Difícil"
        elif 15 <= result < 35:
            self.set_fill_color(250,148,115)
            return "Lectura Difícil"
        elif 35 <= result < 50:
            self.set_fill_color(252,191,123)
            return "Lectura Bastante Difícil"
        elif 50 <= result < 65:
            self.set_fill_color(255,235,132)
            return "Lectura Normal"
        elif 65 <= result < 75:
            self.set_fill_color(204,221,130)
            return "Lectura Bastante Fácil"
        elif 75 <= result < 85:
            self.set_fill_color(152,206,127)
            return "Lectura Fácil"
        elif 85 <= result <= 100:
            self.set_fill_color(99,190,123)
            return "Lectura Muy Fácil"
    
    #Índice de perspicuidad de Fernandez Huerta
    def get_ValorTablaFernandez(self,result):
        if 0 <= result < 30:
            self.set_fill_color(248,105,107)
            return "Lectura Muy Difícil"
        elif 30 <= result < 50:
            self.set_fill_color(250,148,115)
            return "Lectura Difícil"
        elif 50 <= result < 60:
            self.set_fill_color(252,191,123)
            return "Lectura Algo Difícil"
        elif 60 <= result < 70:
            self.set_fill_color(255,235,132)
            return "Lectura Normal"
        elif 70 <= result < 80:
            self.set_fill_color(204,221,130)
            return "Lectura Algo Fácil"
        elif 80 <= result < 90:
            self.set_fill_color(152,206,127)
            return "Lectura Fácil"
        elif 90 <= result <= 100:
            self.set_fill_color(99,190,123)
            return "Lectura Muy Fácil"

    #Índice de perspicuidad Mu
    def get_ValorTablaMu(self,result):
        if 0 <= result < 30:
            self.set_fill_color(248,105,107)
            return "Lectura Muy Difícil"
        elif 30 <= result < 50:
            self.set_fill_color(250,148,115)
            return "Lectura Difícil"
        elif 50 <= result < 60:
            self.set_fill_color(252,191,123)
            return "Lectura Un Poco Difícil"
        elif 60 <= result < 70:
            self.set_fill_color(255,235,132)
            return "Lectura Adecuada"
        elif 70 <= result < 80:
            self.set_fill_color(204,221,130)
            return "Lectura Un Poco Fácil"
        elif 80 <= result < 90:
            self.set_fill_color(152,206,127)
            return "Lectura Fácil"
        elif 90 <= result <= 100:
            self.set_fill_color(99,190,123)
            return "Lectura Muy Fácil"
    
    #Índice de perspicuidad de Inflesz
    def get_ValorTablaInflesz(self,result):
        if 0 <= result < 40:
            self.set_fill_color(248,105,107)
            return "Lectura Muy Difícil"
        elif 40 <= result < 55:
            self.set_fill_color(252,191,123)
            return "Lectura Algo Difícil"
        elif 55 <= result < 65:
            self.set_fill_color(255,235,132)
            return "Lectura Normal"
        elif 65 <= result < 80:
            self.set_fill_color(204,221,130)
            return "Lectura Bastante Fácil"
        elif 80 <= result <= 100:
            self.set_fill_color(99,190,123)
            return "Lectura Muy Fácil"
    
    #Obtiene el valor del índice de perspicuidad 
    def get_ValorTabla(self,formula,result,lenguage):
        if(lenguage=='Spanish'):
            if formula == SIGRISZPAZOS:
                return self.get_ValorTablaSzigrizs(result)
            elif formula == FERNANDEZHUERTA:
                return self.get_ValorTablaFernandez(result)
            elif formula == MULEGIBILITY:
                return self.get_ValorTablaMu(result)
            elif formula == INFLESZ:
                return self.get_ValorTablaInflesz(result)
        elif(lenguage=='English'):
            if formula == FLESH:
                return self.get_ValorTablaSzigrizs(result)

    #Conclusiones
    def get_ValorTablaGeneral(self,result):
        if 0 <= result < 15:
            return {"textos":"textos de contenido científico o filosófico, que tienen una naturaleza muy profunda", "publico_recomendado": "son las personas con grado universitario o a punto de culminar su educación superior."}
        elif 15 <= result < 35:
            return {"textos":"textos de contenido pedagógico o especializado, que tienen una naturaleza aburrida o complicada", "publico_recomendado": "son las personas cursando un grado universitario."}
        elif 35 <= result < 50:
            return {"textos":"textos literarios (como narrativa, poesía, teatro o ensayos) o de divulgación (textos informativos más especializados como artículos de descubrimientos o de nuevas tecnologías), que tienen una naturaleza sugestiva o contenido importante", "publico_recomendado": "son las personas cursando o que hayan culminado su educación media (bachillerato)."}
        elif 50 <= result < 65:
            return {"textos":"textos de tipo informativo (como diccionarios, enciclopedias, periódicos, reportajes, revistas, entre otros), que tratan temas de la actualidad y son de contenido claro", "publico_recomendado": "es el público en general."}
        elif 65 <= result < 75:
            return {"textos":"textos como novelas populares, revistas femeninas y textos educativos; que suelen ser interesantes o dirigidos al entretenimiento", "publico_recomendado": "son las personas mayores de 12 años."}
        elif 75 <= result < 85:
            return {"textos":"textos que pueden encontrarse en quioscos como revistas e historietas, cuyo contenido es considerablemente simple", "publico_recomendado": "son las personas mayores de 10 años."}
        elif 85 <= result <= 100:
            return {"textos":"textos como cuentos, relatos o tebeos (historietas cortas dirigidas a niños, también llamados viñetas), cuya naturaleza es superficial o coloquial", "publico_recomendado": "son los niños entre 6 y 10 años."}

    #Obtiene la conclusión en base al promedio de todos los valores de perspicuidad 
    def get_conclusion_general(self, result):
        avg_result = (result[SIGRISZPAZOS]['value']+result[FERNANDEZHUERTA]['value']+result[MULEGIBILITY]['value'])/3
        resultados = self.get_ValorTablaGeneral(avg_result)
        conclusion = CONCLUSION_GRAL_INICIO+resultados['textos']+CONCLUSION_GRAL_PUBLICO_RECOMENDADO+resultados['publico_recomendado']
        self.set_y(self.aumentarValorY(155.0))
        self.set_font('Times', 'B', 12)
        self.cell(0, 6, "Conclusión: ")
        self.set_font('Times', '', 12)
        self.set_y(self.aumentarValorY(6.5))
        self.multi_cell(0, self.font_size * 1.25, conclusion)

    #Escribe los resultados de las fórmulas en el PDF
    def print_formulas(self, result):
        
        self.set_y(self.aumentarValorY(12.0))

        self.set_xy(20.0,self.pdf_y)
        self.set_font('Times', 'B', 12)
        self.cell(0, 6, "Fórmulas")
        self.set_x(65.0)
        self.cell(0, 6, "Resultados")
        self.set_x(100.0)
        self.cell(0, 6, "Interpretaciones")
        self.set_font('Times', '', 12)
        self.set_y(self.aumentarValorY(8.0))

        for formula in result:
            self.set_xy(20.0,self.pdf_y)
            self.cell(0, 6, '> %s: ' % (result[formula]["name"]))
            self.set_x(65.0)
            self.cell(0, 6, str(result[formula]["value"]))
            self.set_x(100.0)
            self.set_font('Times', 'B', 12)
            self.cell(0, 6, self.get_ValorTabla(formula,result[formula]["value"]), 0, 1, 'L', 1)
            self.set_font('Times', '', 12)
            self.set_y(self.aumentarValorY(8.0))
        
        self.set_xy(10.0,self.aumentarValorY(4.0))

    def resultados(self, result):
        self.set_font('Times', '', 12)
        self.print_formulas(result)

    #Agrega las imágenes de los gráficos al PDF
    def graficos(self):
        self.set_y(self.aumentarValorY(8.0))
        self.image(DOCS_ROUTE + PLOT_SIGRISZPAZOS,10, self.pdf_y, 90)
        self.image(DOCS_ROUTE + PLOT_FERNANDEZHUERTA,110, self.pdf_y, 90)
        self.set_y(self.aumentarValorY(90.0))
        self.image(DOCS_ROUTE + PLOT_MULEGIBILITY,55, self.pdf_y, 100)
        self.set_y(self.aumentarValorY(90.0))
        self.add_page("L")
        self.pdf_y = 0
        self.set_xy(10,self.aumentarValorY(10.0))
        self.image(DOCS_ROUTE + PLOT_PARAGRAPHS,23.5, self.pdf_y, 250)

    #Índices de perspicuidad en los anexos del PDF
    def anexos(self):
        self.pdf_y = 0
        sigrisz = (
            ("Nivel", "Dificultad", "Contenido"),
            ("0 - 14", "Muy Difícil", "Científico / Filosófico"),
            ("15 - 34", "Difícil", "Pedagógico / Especializado"),
            ("35 - 49", "Bastante Difícil", "Literatura / Divulgación"),
            ("50 - 64", "Normal", "Informativo"),
            ("65 - 74", "Bastante Fácil", "Novela / Revista"),
            ("75 - 84", "Fácil", "Quioscos"),
            ("85 - 100", "Muy Fácil", "Cuentos / Relatos")
        )

        huerta = (
            ("Nivel", "Dificultad", "Grado de Lectura"),
            ("0 - 29", "Muy Difícil", "Graduado de Universidad"),
            ("30 - 49", "Difícil", "Universitario"),
            ("50 - 59", "Algo Difícil", "Bachillerato"),
            ("60 - 69", "Normal", "Grados 8 a 9"),
            ("70 - 79", "Algo Fácil", "Grado 7"),
            ("80 - 89", "Fácil", "Grado 6"),
            ("90 - 100", "Muy Fácil", "Grado 5")
        )

        mu = (
            ("Nivel", "Dificultad"),
            ("0 - 29", "Muy Difícil"),
            ("30 - 49", "Difícil"),
            ("50 - 59", "Algo Difícil"),
            ("60 - 69", "Normal"),
            ("70 - 79", "Algo Fácil"),
            ("80 - 89", "Fácil"),
            ("90 - 100", "Muy Fácil")
        )

        inflez = (
            ("Nivel", "Dificultad"),
            ("0 - 39", "Muy Difícil"),
            ("40 - 54", "Algo Difícil"),
            ("55 - 64", "Normal"),
            ("65 - 79", "Bastante Fácil"),
            ("80 - 100", "Muy Fácil")
        )

        aux = True

        self.set_y(self.aumentarValorY(25.0))
        line_height = self.font_size * 1.3
        col_width = self.epw / 3  # distribute content evenly
        self.set_fill_color(255, 255, 255)
        self.set_font('Times', 'B', 13)
        self.cell(0, 0, '%s' % ('Escala '+SIGRISZPAZOS_TEXT), 0, 1, 'L', 1)
        self.set_font('Times', '', 12)
        self.set_y(self.aumentarValorY(5.0))
        for row in sigrisz:
            if aux:
                self.set_font('Times', 'B', 12)
                aux = False
            else:
                self.set_font('Times', '', 12)
            for datum in row:
                self.multi_cell(col_width, line_height, datum, border=1,
                        new_x="RIGHT", new_y="TOP", max_line_height=self.font_size)
            self.ln(line_height)

        aux = True
        self.set_y(self.aumentarValorY(55.0))
        self.set_font('Times', 'B', 13)
        self.cell(0, 0, '%s' % ('Escala '+FERNANDEZHUERTA_TEXT), 0, 1, 'L', 1)
        self.set_font('Times', '', 12)
        self.set_y(self.aumentarValorY(5.0))
        for row in huerta:
            if aux:
                self.set_font('Times', 'B', 12)
                aux = False
            else:
                self.set_font('Times', '', 12)
            for datum in row:
                self.multi_cell(col_width, line_height, datum, border=1,
                        new_x="RIGHT", new_y="TOP", max_line_height=self.font_size)
            self.ln(line_height)

        aux = True
        self.set_y(self.aumentarValorY(55.0))
        self.set_font('Times', 'B', 13)
        self.cell(0, 0, '%s' % ('Escala '+MULEGIBILITY_VAR_TEXT), 0, 1, 'L', 1)
        self.set_font('Times', '', 12)
        self.set_y(self.aumentarValorY(5.0))
        col_width = self.epw / 2  # distribute content evenly
        for row in mu:
            if aux:
                self.set_font('Times', 'B', 12)
                aux = False
            else:
                self.set_font('Times', '', 12)
            for datum in row:
                self.multi_cell(col_width, line_height, datum, border=1,
                        new_x="RIGHT", new_y="TOP", max_line_height=self.font_size)
            self.ln(line_height)

        aux = True
        self.set_y(self.aumentarValorY(55.0))
        self.set_font('Times', 'B', 13)
        self.cell(0, 0, '%s' % ('Escala '+INFLESZ_TEXT), 0, 1, 'L', 1)
        self.set_font('Times', '', 12)
        self.set_y(self.aumentarValorY(5.0))
        for row in inflez:
            if aux:
                self.set_font('Times', 'B', 12)
                aux = False
            else:
                self.set_font('Times', '', 12)
            for datum in row:
                self.multi_cell(col_width, line_height, datum, border=1,
                        new_x="RIGHT", new_y="TOP", max_line_height=self.font_size)
            self.ln(line_height)        

    #Ejecuta los procesos del cuerpo del PDF resúmen
    def resultados_generales(self,result):
        self.set_xy(10.0,self.aumentarValorY(8.0))
        self.seccion("1. Resultados")
        self.resultados(result)
        self.seccion("2. Estadísticas")
        self.graficos()
        self.get_conclusion_general(result)

    #Crea el header y el cuerpo del PDF
    def print_resumen(self,result,titulo):
        self.encabezado(titulo)
        self.resultados_generales(result)

    #Crea el PDF completo con el detalle por párrafo
    def print_complete_report(self, pharagraph_values, sorted_formulas, number_of_pharagraphs):
        pdf = self
        pdf.add_page()
        

        top5 = validate_top_pharagraphs(number_of_pharagraphs, sorted_formulas)
        bottom5 = validate_lowest_pharagraphs(number_of_pharagraphs, sorted_formulas)
    
        pdf.set_font('Times','',10.0) 

        epw = pdf.w - 2*pdf.l_margin
       

        col_width = epw/3
        col_width_table2 = epw/4
        th = pdf.font_size

        #Seteamos primero el tamaño del encabezado
        pdf.set_font('Arial','B', 16.0) 
        pdf.cell(epw, 0.0, txt="ANÁLISIS POR PÁRRAFO", align = 'C')

        #Seteamos luego el tamaño de cada parrafo
        pdf.set_font('Times','', 10.0) 

        #Seteamos un salto de linea luego del encabezado 
        pdf.ln(6)
        
        for index, value in enumerate(pharagraph_values):
            
            index = index
            data = [['Cantidad de Frases','Cantidad de Palabras','Cantidad de Sílabas'], [str(value["frasesParrafo"]), str(value["palabrasParrafo"]), str(value["silabasParrafo"])]]

            data2 = [[SIGRISZPAZOS_TEXT,FERNANDEZHUERTA_TEXT,MULEGIBILITY_VAR_TEXT, INFLESZ_TEXT],
            [str(value["perspicuidad"]['SzigrisztPazos']), str(value["perspicuidad"]['FernandezHuerta']), str(value["perspicuidad"]['LegibilidadMu']),str(value["perspicuidad"]['SzigrisztPazos'])],
            [self.get_ValorTablaSzigrizs(value["perspicuidad"]['SzigrisztPazos']), self.get_ValorTablaFernandez(value["perspicuidad"]['FernandezHuerta']), self.get_ValorTablaMu(value["perspicuidad"]['LegibilidadMu']),self.get_ValorTablaInflesz(value["perspicuidad"]['SzigrisztPazos'])]]
            
            additional_title = set_aditional_title(index, number_of_pharagraphs, top5, bottom5)

            pdf.seccion("Párrafo #"+str(index+1)+''+additional_title)
            #salto de linea luego del numero de parrafo
            pdf.ln(5)
            #Celda que contiene todo el parrafo
            pdf.multi_cell(epw, th*2,txt=value["parrafo"])
            pdf.ln(6)
            #----------------------------Printeando tabla------------------------------------ 
            #Encabezado de la tabla
            pdf.set_font('Times','B', 10.0) 
            pdf.cell(epw, 2*th, "Características del párrafo", border=1, align = 'C')
            pdf.set_font('Times','', 10.0)
            pdf.ln(2*th)
            #Tabla 1
            for row in data:
                pdf.set_font('Times','', 10.0)
                for datum in row:
                    if (str(datum) == 'Cantidad de Frases'):
                        pdf.set_font('Times','B', 10.0)
                    pdf.cell(col_width, 2*th, str(datum), border=1, align = 'C')
                #Seteamos un salto de linea al terminar la fila 
                pdf.ln(2*th)

            pdf.ln(2*th)

            #Tabla 2
            pdf.set_font('Times','B', 10.0) 
            pdf.cell(epw, 2*th, "Indices de perspicuidad", border=1, align = 'C')
            pdf.set_font('Times','', 10.0)
            pdf.ln(2*th)
            for row in data2:

                pdf.set_font('Times','', 10.0) 
                for datum in row:

                    if(str(datum) == SIGRISZPAZOS_TEXT):
                        pdf.set_font('Times','B', 10.0) 
                    pdf.cell(col_width_table2, 2*th, str(datum), border=1, align = 'C')
                #Seteamos un salto de linea al terminar la fila 
                pdf.ln(2*th)
            #----------------------------Fin de tabla------------------------------------ 
            pdf.ln(4*th)
        #pdf.output("testing.pdf")

#Ajusta los 5 mejores párrafos para cuando el total de párrafos es menor a 10
def validate_top_pharagraphs(number_of_pharagraphs, top_pharagrahps):
    highest_pharagrahps = None
    if number_of_pharagraphs > 9:
        highest_pharagrahps = top_pharagrahps[:5]
    if number_of_pharagraphs == 9 or number_of_pharagraphs == 8:
        highest_pharagrahps = top_pharagrahps[:4]
    if number_of_pharagraphs == 7 or number_of_pharagraphs == 6:
        highest_pharagrahps = top_pharagrahps[:3]
    if number_of_pharagraphs == 5 or number_of_pharagraphs == 4:
        highest_pharagrahps = top_pharagrahps[:2]
    if number_of_pharagraphs == 3 or number_of_pharagraphs == 2:
        highest_pharagrahps = top_pharagrahps[:1]
    if number_of_pharagraphs == 1 or number_of_pharagraphs == 0:
        highest_pharagrahps = []
    return highest_pharagrahps

#Ajusta los 5 peores párrafos para cuando el total de párrafos es menor a 10
def validate_lowest_pharagraphs(number_of_pharagraphs, top_pharagrahps):
    lowest_pharagraps = None
    if number_of_pharagraphs > 9:
        lowest_pharagraps = top_pharagrahps[-5:]
    if number_of_pharagraphs == 9 or number_of_pharagraphs == 8:
        lowest_pharagraps = top_pharagrahps[-4:]
    if number_of_pharagraphs == 7 or number_of_pharagraphs == 6:
        lowest_pharagraps =  top_pharagrahps[-3:]
    if number_of_pharagraphs == 5 or number_of_pharagraphs == 4:
        lowest_pharagraps =  top_pharagrahps[-2:]
    if number_of_pharagraphs == 3 or number_of_pharagraphs == 2:
        lowest_pharagraps =  top_pharagrahps[-1:]
    if number_of_pharagraphs == 1 or number_of_pharagraphs == 0:
        lowest_pharagraps = []
    return lowest_pharagraps

#Agrega al título del párrafo un texto si se encuentra en los 5 mejores o peores párrafos
def set_aditional_title(index, number_of_pharagraphs, top_pharagrahps, lowest_pharagraps):
    additional_title = ''
    if any(x['parrafo'] == str(index) for x in top_pharagrahps):
        
        if number_of_pharagraphs == 2 or number_of_pharagraphs == 3:
            additional_title = ' (El mejor párrafo)'
        elif number_of_pharagraphs <= 1:
            additional_title = ''
        else:
            additional_title = ' (Entre los '+str(len(top_pharagrahps))+' mejores párrafos)'

    elif any(x['parrafo'] == str(index) for x in lowest_pharagraps):

        if number_of_pharagraphs == 2 or number_of_pharagraphs == 3:
            additional_title = ' (El peor párrafo)'
        elif number_of_pharagraphs <= 1:
            additional_title = ''
        else:
            additional_title = ' (Entre los '+str(len(lowest_pharagraps))+' peores párrafos)'
            
    return additional_title

def validate_highest_aditional_title(number_of_pharagraphs):
    title = ''
    if number_of_pharagraphs > 9:
         title = '(Entre los  mejores párrafos)'
    if number_of_pharagraphs == 9 or number_of_pharagraphs == 8:
         title = ''
    if number_of_pharagraphs == 7 or number_of_pharagraphs == 6:
         title = ''
    if number_of_pharagraphs == 5 or number_of_pharagraphs == 4:
         title = ''
    if number_of_pharagraphs == 3 or number_of_pharagraphs == 2:
         title = ''
    if number_of_pharagraphs == 1 or number_of_pharagraphs == 0:
        title = ''
    return title

