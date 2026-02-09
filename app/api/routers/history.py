from typing import Optional
from fastapi import APIRouter, HTTPException

from app.api.deps import Auth
from schema.history import CreateHistory, UpdateHistory
from schema.time_spent import TimeSpentPayload

router = APIRouter(prefix="/history")


@router.get("/list")
def get_histories_from_bot(
    user_id: str, limit: int, auth: Auth, cursor: Optional[int] = None
):
    token, user_supabase = auth
    if not cursor:
        result = (
            user_supabase.table("history")
            .select("*")
            .match({"user_id": user_id})
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
    else:
        result = (
            user_supabase.table("history")
            .select("*")
            .match({"user_id": user_id})
            .order("created_at", desc=True)
            .lt("id", cursor)
            .limit(limit)
            .execute()
        )
    if not result.data:
        raise HTTPException(status_code=400, detail=result)
    if type(result.data[-1]) is not dict:
        raise HTTPException(status_code=400, detail=result)
    response = {
        "data": result.data,
        "pagination": {"cursor": result.data[-1]["id"], "count": len(result.data)},
    }
    print(response)
    return response


@router.get("/{history_id}")
def get_history(user_id: str, history_id: int, auth: Auth):
    token, user_supabase = auth
    result = (
        user_supabase.table("history")
        .select("*")
        .match({"user_id": user_id, "id": history_id})
        .execute()
    )
    print(result)
    return result


@router.post("")
def create_history(data: CreateHistory, auth: Auth):
    token, user_supabase = auth
    response = (
        user_supabase.table("history").insert(data.model_dump(mode="json")).execute()
    )
    print(response)
    return response


@router.put("/{history_id}")
def update_history(user_id: str, history_id: int, data: UpdateHistory, auth: Auth):
    token, user_supabase = auth
    response = (
        user_supabase.table("history")
        .update(data.model_dump(mode="json", exclude_none=True))
        .match({"user_id": user_id, "id": history_id})
        .execute()
    )
    print(response)
    return response


@router.post("/{history_id}/time-spent")
def update_history_time_spent(
    user_id: str, history_id: int, payload: TimeSpentPayload, auth: Auth
):
    token, user_supabase = auth
    response = (
        user_supabase.table("history")
        .select("*")
        .match({"user_id": user_id, "id": history_id})
        .execute()
    )
    if not response.data:
        raise HTTPException(status_code=400, detail="No history entry")
    sim = response.data[0]
    if type(sim) is not dict:
        return response
    data = UpdateHistory(
        seconds_spent=sim["seconds_spent"] + payload.elapsed_secs,
        updated_at=payload.updated_at,
    )
    response = (
        user_supabase.table("history")
        .update(data.model_dump(mode="json", exclude_none=True))
        .match({"user_id": user_id, "id": history_id})
        .execute()
    )
    # print(response)
    return response
