from fastapi import APIRouter, HTTPException

from app.api.deps import Auth
from schema.profile import CreateProfile, UpdateProfile

router = APIRouter(prefix="/profile")


@router.get("")
async def get_profile(user_id: str, auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("profile").select("*").match(
        {"id": user_id}).execute()
    print(response)
    return response


@router.post("")
async def create_profile(data:  CreateProfile, auth: Auth):
    token, user_supabase = auth
    session = user_supabase.auth.get_user()
    if not session:
        raise HTTPException(status_code=400, detail="User not found")
    if not session.user.user_metadata["username"]:
        raise HTTPException(status_code=400, detail="User not found")
    username = session.user.user_metadata.get("username")
    if not username:
        raise HTTPException(status_code=400, detail="Username not found")
    print(username)
    data.username = username
    response = user_supabase.table("profile").insert(
        data.model_dump(mode="json", exclude_none=True)).execute()
    print(response)
    return response


@router.put("")
async def update_profile(user_id: str, data:  UpdateProfile, auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("profile").update(
        data.model_dump(mode="json", exclude_none=True)
    ).match({"id": user_id}).execute()
    print(response)
    return response
