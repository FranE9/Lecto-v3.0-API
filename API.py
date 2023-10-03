from src.constants import *
from src.Logic import *
from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta

from fastapi.staticfiles import StaticFiles


#Aplicacion Apifast
app = FastAPI()

static_directory = "static"

app.mount("/static", StaticFiles(directory=static_directory), name="static")




@app.post("/lecto/pdf")
async def upload_file(archivo_pdf: UploadFile = File(...), inicio: int= Form(...), final: int= Form(...), idioma:str=Form(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    Validation_Result()

    if not archivo_pdf.filename:
        raise HTTPException(status_code=400, detail="Se requiere un archivo PDF")

    if languageValidation(idioma):
        raise HTTPException(status_code=400, detail="Solo se acepta el idioma español (spa) o inglés (eng)")
        return {"idioma": f"{idioma}"}

    if pageValidation(inicio,final):
        raise HTTPException(status_code=400, detail="La primer página debe de ser menor que la última")
        return {"start": f"{inicio}"}
    
    #Create intern PDF
    Source = f"src/Files/PDF/{archivo_pdf.filename}"
    with open(Source, "wb") as buffer:
        buffer.write(await archivo_pdf.read())

    if ValidacionPaginas(inicio, final, Source):
        raise HTTPException(status_code=400, detail="No puede poner paginas que sean mayores a las del PDF")
        return {"finish": f"{final}"}


    #Create ticket result
    ticket = str(datetime.now().timestamp() * 1000).replace('.','')

    #Tiempo estimado
    time = CalculateEstimatedTime(inicio,final, Source)
    
    List = [Source, inicio, final, ticket, archivo_pdf, idioma, archivo_pdf.filename]
    background_tasks.add_task(Create_Result, List)

    data = {
        "ticket": f"{ticket}",
        "tiempo_estimado": f"{time}",
        "idioma": f"{idioma}",
        "Fecha": str(datetime.now() - timedelta(hours=6)),
        "Nombre": f"{archivo_pdf.filename}",
    }
    return JSONResponse(content=data)
    



@app.post("/lecto/text")
async def received_Text(Texto: str = Form(), Idioma:str = Form()):
    Result = process_text(Texto, Idioma)
    return Result


@app.post("/lecto/ticket")
async def received_Ticket(Ticket: str = Form(...)):
    return FindTicket(Ticket)