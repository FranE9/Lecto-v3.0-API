from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from config.database import init_db
from routes.auth import router as auth_router
from routes.ticket import router as ticket_router
from routes.lecto import router as lecto_router

#Aplicacion Apifast
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_directory = "static"

app.mount("/static", StaticFiles(directory=static_directory), name="static")

@app.on_event("startup")
async def startup_db():
    await init_db()
    
@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def read_root():
    return RedirectResponse(url="/docs")
    
app.include_router(auth_router, tags=["auth"], prefix="/auth")
app.include_router(ticket_router, tags=["ticket"], prefix="/tickets")
app.include_router(lecto_router, tags=["lecto"], prefix="/lecto")