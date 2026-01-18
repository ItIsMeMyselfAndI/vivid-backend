from fastapi import APIRouter

from app.api.deps import Auth
from schema.settings import CreateSettings, UpdateSettings

router = APIRouter(prefix="")


@router.get("/get-settings")
async def get_settings(user_id: str, auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("settings").select("*").match(
        {"user_id": user_id}).execute()
    print(response)
    return response


@router.post("/create-settings")
async def create_settings(data:  CreateSettings,
                          auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("settings").insert(
        data.model_dump(mode="json")).execute()
    print(response)
    return response


@router.put("/update-settings")
async def update_settings(user_id: str,
                          data:  UpdateSettings, auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("settings").update(
        data.model_dump(mode="json", exclude_none=True)
    ).match({"user_id": user_id}).execute()
    print(response)
    return response
