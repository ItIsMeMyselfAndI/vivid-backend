from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os


from app.api.routers import auth, simulation, stats, profile, history, settings

load_dotenv()

PROJECT_URL = os.environ.get("PROJECT_URL")
PROJECT_ORIGINS = os.environ.get("PROJECT_ORIGINS", PROJECT_URL or "")
ALLOWED_ORIGINS = [o.strip() for o in PROJECT_ORIGINS.split(",") if o.strip()]
if not ALLOWED_ORIGINS:
    raise RuntimeError("[Exit] No allowed origins configured")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(simulation.router, prefix="/api")
app.include_router(stats.router, prefix="/api")
app.include_router(profile.router, prefix="/api")
app.include_router(history.router, prefix="/api")
app.include_router(settings.router, prefix="/api")
