from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from src.constants import *
from src.Logic import *
from models.ticket import Ticket, SpaResults, EngResults, ParagraphResults
from middlewares.auth import JWTBearer
import services.ticket as ticket_service
from datetime import datetime

router = APIRouter()

token_middleware = JWTBearer()

@router.post("/pdf", dependencies=[Depends(token_middleware)])
async def upload_file(archivo_pdf: UploadFile = File(...), inicio: int= Form(...), final: int= Form(...), user_id:str=Form(...)):
    Validation_Result()

    if not archivo_pdf.filename:
        raise HTTPException(status_code=400, detail="Se requiere un archivo PDF")

    if pageValidation(inicio,final):
        raise HTTPException(status_code=400, detail="La primer página debe de ser menor que la última")
    
    #Create intern PDF
    Source = f"src/Files/PDF/{archivo_pdf.filename}"
    with open(Source, "wb") as buffer:
        buffer.write(await archivo_pdf.read())

    if ValidacionPaginas(inicio, final, Source):
        raise HTTPException(status_code=400, detail="No puede poner paginas que sean mayores a las del PDF")

    try:
        #Tiempo estimado
        _, time = CalculateEstimatedTime(inicio,final, Source)
        results = process_file([Source, inicio, final])
        DeletePDF(Source)
        
        paragraphs = int(results["Parrafo"])
        words = int(results["words"])
        phrases = int(results["phrases"])
        syllables = int(results["syllables"])

        spa_results = None
        eng_results = None

        language = results["language"]
        
        if language == "es":
            szigrisztPazos_INFLESZ = float(results["szigrisztPazos_INFLESZ"])
            fernandezHuerta = float(results["fernandezHuerta"])
            legibilidadMu = float(results["legibilidadMu"])
            spa_results = SpaResults(
                                szigriszt_pazos=szigrisztPazos_INFLESZ, 
                                fernandez_huerta=fernandezHuerta, 
                                readability=legibilidadMu)
        else:
            fleshReadingEasy = float(results["fleshReadingEasy"])
            fogReading = float(results["fogReading"])
            smogReading = float(results["smogReading"])
            eng_results = EngResults(
                                flesch_reading_easy=fleshReadingEasy,
                                fog_reading=fogReading,
                                smog_reading=smogReading)
            
        my_ticket = Ticket(duration=time, 
                        date=datetime.now(), 
                        file=f"{archivo_pdf.filename}", 
                        language=language, 
                        spaResults=spa_results, 
                        engResults=eng_results, 
                        user_id=user_id,
                        paragraphs=paragraphs,
                        words=words,
                        phrases=phrases,
                        syllables=syllables,
                        paragraphInfo=results["paragraphInfo"],    
                        )
        
        new_ticket = await ticket_service.create(my_ticket)
        return {
            "status_code": 200,
            "status": True,
            "message": "Ticket created successfully",
            "data": new_ticket
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected server error")

@router.post("/text", dependencies=[Depends(token_middleware)])
async def received_Text(Texto: str = Form()):
    Result = process_text(Texto)
    Result["id"] = str(datetime.now().timestamp() * 1000).replace('.','')
    return Result