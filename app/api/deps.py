from typing import Annotated, Optional, Tuple
from supabase import create_client, Client
from fastapi import Depends,  HTTPException, Header, Request
from dotenv import load_dotenv
import os


load_dotenv()


SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")


async def validate_token(
    request: Request,
    authorization: Annotated[Optional[str], Header()] = None,
):
    token = authorization
    if not token:
        # beacon fallback
        try:
            body = await request.json()
        except Exception:
            body = {}
        token = body.get("authorization")

    if not token or not token.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Missing or invalid Authorization token")
    access_token = token.split(" ", 1)[1]
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("[Exit] No user_supabase url or key")
    user_supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    user_supabase.auth.set_session(access_token=access_token, refresh_token="")
    return token, user_supabase

Auth = Annotated[Tuple[str, Client], Depends(validate_token)]
