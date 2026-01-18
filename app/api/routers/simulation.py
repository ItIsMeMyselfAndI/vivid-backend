from fastapi import APIRouter, HTTPException

from app.api.deps import Auth
from schema.simulation import CreateSimulation, SimulationType, UpdateSimulation
from schema.time_spent import TimeSpentPayload

router = APIRouter(prefix="/simulation")


@router.get("")
async def get_simulation(user_id: str,
                         simulation_type: SimulationType, auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("simulation").select("*").match(
        {"user_id": user_id, "type": simulation_type.value}
    ).execute()
    print(response)
    return response


@router.get("/list")
async def get_all_simulations(user_id: str, auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("simulation").select("*").match(
        {"user_id": user_id}
    ).execute()
    print(response)
    return response


@router.post("")
async def create_simulation(data:  CreateSimulation, auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("simulation").insert(
        data.model_dump(mode="json")).execute()
    print(response)
    return response


@router.put("")
async def update_simulation(
        user_id: str, simulation_type: SimulationType,
        data:  UpdateSimulation, auth: Auth
):
    token, user_supabase = auth
    response = user_supabase.table("simulation").update(
        data.model_dump(mode="json", exclude_none=True)
    ).match({"user_id": user_id, "type": simulation_type.value}).execute()
    print(response)
    return response


@router.post("/time-spent")
async def update_simulation_time_spent(
        user_id: str, simulation_type: SimulationType,
        payload: TimeSpentPayload, auth: Auth
):
    token, user_supabase = auth
    response = user_supabase.table("simulation").select("*").match(
        {"user_id": user_id, "type": simulation_type.value}
    ).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="No stats entry")
    sim = response.data[0]
    if type(sim) is not dict:
        return response
    data = UpdateSimulation(
        seconds_spent=sim["seconds_spent"]+payload.elapsed_secs,
        updated_at=payload.updated_at
    )
    print(data)
    response = user_supabase.table("simulation").update(
        data.model_dump(mode="json", exclude_none=True)
    ).match({"user_id": user_id, "type": simulation_type.value}).execute()
    print(response)
    return response
