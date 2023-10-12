from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings
from models.user import User

mongodb_uri: str = 'mongodb+srv://fran:root@prueba1.8gevvtj.mongodb.net/lectoDB?retryWrites=true&w=majority'
# class Settings(BaseSettings):
#     mongodb_uri: str = 'mongodb+srv://fran:root@prueba1.8gevvtj.mongodb.net/?retryWrites=true&w=majority'
#     class Config:
#         orm_mode = True
        
async def init_db():
    client = AsyncIOMotorClient(mongodb_uri)
    await init_beanie(database=client.get_default_database(), document_models=[User])
