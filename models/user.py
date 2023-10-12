from pydantic import BaseModel
from beanie import Document
from typing import Optional

class User(Document):
    username: str
    password: str
    
class Login(BaseModel):
	username: str
	password: str
 
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: Optional[str] = None