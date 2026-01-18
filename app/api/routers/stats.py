from fastapi import APIRouter, HTTPException

from app.api.deps import Auth
from schema.stats import CreateStats, UpdateStats
from schema.time_spent import TimeSpentPayload

router = APIRouter(prefix="")


@router.get("/get-stats")
async def get_stats(user_id: str, auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("stats").select("*").match(
        {"user_id": user_id}).execute()
    print(response)
    return response


@router.post("/create-stats")
async def create_stats(data:  CreateStats, auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("stats").insert(
        data.model_dump(mode="json")).execute()
    print(response)
    return response


@router.put("/update-stats")
async def update_stats(user_id: str, data:  UpdateStats, auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("stats").update(
        data.model_dump(mode="json", exclude_none=True)
    ).match({"user_id": user_id}).execute()
    print(response)
    return response


@router.post("/update-stats-time-spent")
async def update_stats_time_spent(
        user_id: str, payload: TimeSpentPayload, auth: Auth
):
    token, user_supabase = auth
    response = user_supabase.table("stats").select("*").match(
        {"user_id": user_id}
    ).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="No stats entry")
    sim = response.data[0]
    if type(sim) is not dict:
        return response
    data = UpdateStats(
        seconds_spent=sim["seconds_spent"]+payload.elapsed_secs,
        updated_at=payload.updated_at
    )
    print(data)
    response = user_supabase.table("stats").update(
        data.model_dump(mode="json", exclude_none=True)
    ).match({"user_id": user_id}).execute()
    print(response)
    return response
