from fastapi import APIRouter, Depends, HTTPException, Body
from models.ticket import Ticket
from middlewares.auth import JWTBearer
import services.ticket as ticket_service

router = APIRouter()

token_middleware = JWTBearer()

@router.get('/user/{user_id}', dependencies=[Depends(token_middleware)])
async def get_tickets_by_user(user_id: str):
    try:
        results = await Ticket.find({"user_id": user_id}).to_list()
        return {
            "status_code": 200,
            "status": True,
            "message": "Tickets obtained successfully",
            "data": results
        }
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected server error")
    
@router.get('/{id}', dependencies=[Depends(token_middleware)])
async def get_ticket_by_id(id: str):
    try:
        ticket = await Ticket.get(id)
        if not ticket: 
            raise HTTPException(status_code=404, detail="Ticket not found with id: {}".format(id))
        else:
            return {
                "status_code": 200,
                "status": True,
                "message": "Ticket obtained successfully",
                "data": ticket
            }
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected server error")

@router.post('/new', dependencies=[Depends(token_middleware)])
async def create_ticket(ticket: Ticket = Body(...)):
    try:
        new_ticket = await ticket_service.create(ticket)
        return {
            "status_code": 200,
            "status": True,
            "message": "Ticket created successfully",
            "data": new_ticket
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected server error")