from models.ticket import Ticket

async def create(ticket: Ticket):
    new_ticket = await ticket.create()
    return new_ticket
   