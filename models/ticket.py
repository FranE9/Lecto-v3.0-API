from beanie import Document, Link
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.user import User

class EngResults(BaseModel):
    paragraph: int
    flesch_reading_easy: float
    fog_reading: float
    smog_reading: float

class SpaResults(BaseModel):
    paragraph: int
    szigriszt_pazos: float
    fernandez_huerta: float
    readability: float

class Ticket(Document):
    duration: int
    date: datetime
    file: str
    language: str
    spaResults: Optional[SpaResults] = None
    engResults: Optional[EngResults] = None
    user_id: str
    