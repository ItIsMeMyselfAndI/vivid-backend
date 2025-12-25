from schema.simulation import (
    CreateSimulation, UpdateSimulation, SimulationType
)
from schema.history import CreateHistory, UpdateHistory
from client.index import supabase

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv


load_dotenv()
project_url = os.environ.get("PROJECT_URL")
if not project_url:
    print("[Exit] PROJECT_URL doesn't exist")
    exit(0)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # allow_origins=[project_url],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----- simulation endpoints -----

@app.get("/api/get-simulation")
def get_simulation(user_id: str, simulation_type: SimulationType):
    response = supabase.table("simulation").select("*").match(
        {"user_id": user_id, "type": simulation_type.value}
    ).execute()
    print(response)
    return response


@app.post("/api/create-simulation")
def create_simulation(data:  CreateSimulation):
    response = supabase.table("simulation").insert(
        data.model_dump(mode="json")).execute()
    print(response)
    return response


@app.put("/api/update-simulation")
def update_simulation(
        user_id: str, simulation_type: SimulationType, data:  UpdateSimulation
):
    response = supabase.table("simulation").update(
        data.model_dump(mode="json", exclude_none=True)
    ).match({"user_id": user_id, "type": simulation_type.value}).execute()
    print(response)
    return response


# ----- history endpoints -----

@app.get("/api/get-histories")
def get_historys(user_id: str, count: int):
    response = supabase.table("history").select("*").match(
        {"user_id": user_id}
    ).order("created_at", desc=True).limit(count).execute()
    print(response)
    return response


@app.post("/api/create-history")
def create_history(data:  CreateHistory):
    response = supabase.table("history").insert(
        data.model_dump(mode="json")).execute()
    print(response)
    return response


@app.put("/api/update-history")
def update_history(
        user_id: str, history_id: int, data:  UpdateHistory
):
    response = supabase.table("history").update(
        data.model_dump(mode="json", exclude_none=True)
    ).match({"user_id": user_id, "id": history_id}).execute()
    print(response)
    return response
