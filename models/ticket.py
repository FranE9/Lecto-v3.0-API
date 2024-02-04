from beanie import Document
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class EngResults(BaseModel):
    flesch_reading_easy: float
    fog_reading: float
    smog_reading: float

class SpaResults(BaseModel):
    szigriszt_pazos: float
    fernandez_huerta: float
    readability: float

class ParagraphResults(BaseModel):
    Parrafo: str
    words: int
    phrases: int
    syllables: int
    letters: int
    Three_sillabls_words: int
    fleshReadingEasy: Optional[str] = None
    fogReading: Optional[str] = None
    smogReading: Optional[str] = None
    szigrisztPazos_INFLESZ: Optional[str] = None
    fernandezHuerta: Optional[str] = None
    legibilidadMu: Optional[str] = None
    content: str

class Ticket(Document):
    duration: int = None
    date: datetime 
    file: str = None
    language: str = None
    paragraphs: int = None
    words: int = None
    phrases: int = None
    syllables: int = None
    spaResults: Optional[SpaResults] = None
    engResults: Optional[EngResults] = None
    paragraphInfo: Optional[List[ParagraphResults]] = []
    user_id: str = None
    pending: bool = True
    