from models.ticket import Ticket, SpaResults, EngResults, ParagraphResults
from typing import Optional, List

async def create(ticket: Ticket):
    new_ticket = await ticket.create()
    return new_ticket

async def update(id: str, language: str, paragraphs: int,  words: int, phrases: int, syllables: int, spaResults: Optional[SpaResults], engResults: Optional[EngResults], paragraphInfo: Optional[List[ParagraphResults]]):
    ticket_found = await Ticket.get(id)

    if not ticket_found:
        return {"error": True, "message": f"Could not find ticket with id: {id}", "ticket": None}
    
    ticket_found.language = language
    ticket_found.paragraphs = paragraphs
    ticket_found.words = words
    ticket_found.phrases = phrases
    ticket_found.syllables = syllables
    ticket_found.spaResults = spaResults
    ticket_found.engResults = engResults
    ticket_found.paragraphInfo = paragraphInfo
    ticket_found.pending = False

    await ticket_found.save()
    return {"error": False, "message": "Ticket updated successfully", "ticket": ticket_found}

   