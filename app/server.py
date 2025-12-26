from schema.simulation import (
    CreateSimulation, UpdateSimulation, SimulationType
)
from schema.settings import CreateSettings, UpdateSettings
from schema.history import CreateHistory, UpdateHistory
from client.index import supabase

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv


load_dotenv()
project_url = os.environ.get("PROJECT_URL")
print(project_url)
if not project_url:
    print("[Exit] PROJECT_URL doesn't exist")
    exit(0)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        project_url,
        f"{project_url}/dashboard",
        f"{project_url}/simulations",
        f"{project_url}/simulations/stack",
        f"{project_url}/simulations/queue",
        f"{project_url}/simulations/binary-tree",
        f"{project_url}/simulations/binary-search-tree",
        f"{project_url}/simulations/recursion",
        # "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----- simulation endpoints -----

@app.get("/api/get-simulation")
def get_simulation(user_id: str, simulation_type: SimulationType, req: Request):
    response = supabase.table("simulation").select("*").match(
        {"user_id": user_id, "type": simulation_type.value}
    ).execute()
    print(response)
    print(req)
    return response


@app.post("/api/create-simulation")
def create_simulation(data:  CreateSimulation, req: Request):
    response = supabase.table("simulation").insert(
        data.model_dump(mode="json")).execute()
    print(response)
    print(req)
    return response


@app.put("/api/update-simulation")
def update_simulation(
        user_id: str, simulation_type: SimulationType, data:  UpdateSimulation, req: Request
):
    response = supabase.table("simulation").update(
        data.model_dump(mode="json", exclude_none=True)
    ).match({"user_id": user_id, "type": simulation_type.value}).execute()
    print(response)
    return response


# ----- history endpoints -----

@app.get("/api/get-histories")
def get_histories(user_id: str, count: int, req: Request):
    response = supabase.table("history").select("*").match(
        {"user_id": user_id}
    ).order("created_at", desc=True).limit(count).execute()
    print(response)
    return response


@app.post("/api/create-history")
def create_history(data:  CreateHistory, req: Request):
    response = supabase.table("history").insert(
        data.model_dump(mode="json")).execute()
    print(response)
    return response


@app.put("/api/update-history")
def update_history(
        user_id: str, history_id: int, data:  UpdateHistory, req: Request
):
    response = supabase.table("history").update(
        data.model_dump(mode="json", exclude_none=True)
    ).match({"user_id": user_id, "id": history_id}).execute()
    print(response)
    return response


# ----- settings endpoints -----

@app.get("/api/get-settings")
def get_settingss(user_id: str, req: Request):
    response = supabase.table("settings").select("*").match(
        {"user_id": user_id}).execute()
    print(response)
    return response


@app.post("/api/create-settings")
def create_settings(data:  CreateSettings, req: Request):
    response = supabase.table("settings").insert(
        data.model_dump(mode="json")).execute()
    print(response)
    return response


@app.put("/api/update-settings")
def update_settings(
        user_id: str, data:  UpdateSettings, req: Request
):
    response = supabase.table("settings").update(
        data.model_dump(mode="json", exclude_none=True)
    ).match({"user_id": user_id}).execute()
    print(response)
    return response
