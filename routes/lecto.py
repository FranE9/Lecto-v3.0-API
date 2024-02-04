from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from src.constants import *
from src.Logic import *
from models.ticket import Ticket, SpaResults, EngResults, ParagraphResults
from middlewares.auth import JWTBearer
import services.ticket as ticket_service
import services.user as user_service
from datetime import datetime
import asyncio
from smtplib import SMTP

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
        my_ticket = None
        shielded_task = None
        user_found = await user_service.get_user_by_id(user_id)
        
        if user_found["error"]:
            raise HTTPException(status_code=404, detail=user_found["message"])
        
        #Tiempo estimado
        _, time = CalculateEstimatedTime(inicio,final, Source)
        
        process_task  = asyncio.create_task(process_file([Source, inicio, final]))
        
        try:
            await asyncio.wait_for(process_task, 1)
        except (asyncio.TimeoutError, asyncio.CancelledError):
            print("Asyncio error")

            my_ticket = Ticket(duration=time, 
                            date=datetime.now(), 
                            file=f"{archivo_pdf.filename}", 
                            user_id=user_id,
                            pending=True,
                            language="-"
                            ) 
            new_ticket = await ticket_service.create(my_ticket)
            
            email_task = asyncio.create_task(send_email(user_found["email"], f"[LECTO] Creacion de ticket {new_ticket.id} en proceso", "Una vez el ticket termine de procesar, se enviara un correo con la confirmacion."))

            await asyncio.gather(email_task)
            
            shielded_task = asyncio.shield(process_task)

            return {
                    "status_code": 200,
                    "status": True,
                    "message": "Ticket in progress",
                    "data": new_ticket
                }
        
        print("La tarea continua")
        process_task  = asyncio.create_task(process_file([Source, inicio, final]))
        results = await shielded_task
        
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
            
        if my_ticket is None:
            my_ticket = Ticket(language=language, 
                            spaResults=spa_results, 
                            engResults=eng_results, 
                            paragraphs=paragraphs,
                            words=words,
                            phrases=phrases,
                            syllables=syllables,
                            paragraphInfo=results["paragraphInfo"],    
                            duration=time, 
                            date=datetime.now(), 
                            file=f"{archivo_pdf.filename}", 
                            user_id=user_id,
                            pending=False
                        )
            new_ticket = await ticket_service.create(my_ticket)
        else:
            update_ticket = await ticket_service.update(my_ticket.id, language, paragraphs, words, phrases, syllables, spa_results, eng_results, results["paragraphInfo"])
            new_ticket = update_ticket["ticket"]
        
        email_task = asyncio.create_task(send_email(user_found["email"], f"[LECTO] Creacion de ticket {new_ticket.id} finalizada", f"Ticket {new_ticket.id} ya esta listo para ser consultado."))

        await asyncio.gather(email_task)

        return {
            "status_code": 200,
            "status": True,
            "message": "Ticket created successfully",
            "data": new_ticket
        }
    except Exception as e:
        print("Exception error")
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected server error")

@router.post("/text", dependencies=[Depends(token_middleware)])
async def received_Text(Texto: str = Form()):
    Result = process_text(Texto)
    Result["id"] = str(datetime.now().timestamp() * 1000).replace('.','')
    return Result

async def send_email(receiver_email: str, subject: str, body: str):
    try:
        email = "lectov3.2024@gmail.com"
        text = f"Subject: {subject}\n\n{body}"
        server = SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, "ytfmskwmperussmm")
        server.sendmail(email, receiver_email, text)
        print("Correo enviado con exito")
        return True
    except Exception as e:
        print(f"Send email error: {e}")
        return False