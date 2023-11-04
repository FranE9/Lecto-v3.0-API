from beanie import Document
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.user import User

class EngResults(BaseModel):
    flesch_reading_easy: float
    fog_reading: float
    smog_reading: float

class SpaResults(BaseModel):
    szigriszt_pazos: float
    fernandez_huerta: float
    readability: float

class Ticket(Document):
    duration: int
    date: datetime
    file: str
    language: str
    paragraphs: int
    words: int
    phrases: int
    syllables: int
    spaResults: Optional[SpaResults] = None
    engResults: Optional[EngResults] = None
    user_id: str
    