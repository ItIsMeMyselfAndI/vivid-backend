from datetime import datetime
from typing import Annotated, Optional, Tuple
from fastapi.responses import JSONResponse
from openai import OpenAI
from supabase import create_client, Client
from fastapi import Depends, FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field
from dotenv import load_dotenv
import os

from schema.simulation import (
    CreateSimulation, UpdateSimulation, SimulationType
)
from schema.profile import CreateProfile, UpdateProfile
from schema.settings import CreateSettings, UpdateSettings
from schema.history import CreateHistory, UpdateHistory
from schema.stats import CreateStats, UpdateStats

load_dotenv()


class TimeSpentPayload(BaseModel):
    model_config = ConfigDict(extra="ignore")
    elapsed_secs: float = Field(ge=0)
    updated_at: datetime


SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")

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
OPEN_ROUTER_URL = "https://openrouter.ai/api/v1"
OPEN_ROUTER_API_KEY = os.environ.get("OPEN_ROUTER_API_KEY")


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


# ----- guest -----
@app.post("/api/auth/guest")
def set_guest_cookie():
    res = JSONResponse({"ok": True})
    res.set_cookie(
        key="guest",
        value="true",
        path="/",
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24,
    )
    return res


@app.post("/api/auth/guest/clear")
def clear_guest_cookie():
    res = JSONResponse({"ok": True})
    res.set_cookie(
        key="guest",
        value="",
        path="/",
        max_age=0,      # clears the cookie
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return res

# ----- simulation endpoints -----


@app.get("/api/get-simulation")
async def get_simulation(user_id: str,
                         simulation_type: SimulationType, auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("simulation").select("*").match(
        {"user_id": user_id, "type": simulation_type.value}
    ).execute()
    print(response)
    return response


@app.get("/api/get-all-simulations")
async def get_all_simulations(user_id: str, auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("simulation").select("*").match(
        {"user_id": user_id}
    ).execute()
    print(response)
    return response


@app.post("/api/create-simulation")
async def create_simulation(data:  CreateSimulation, auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("simulation").insert(
        data.model_dump(mode="json")).execute()
    print(response)
    return response


@app.put("/api/update-simulation")
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


@app.post("/api/update-simulation-time-spent")
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


# ----- history endpoints -----

@app.get("/api/get-history")
async def get_history(user_id: str, history_id: int, auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("history").select("*").match(
        {"user_id": user_id, "id": history_id}
    ).execute()
    print(response)
    return response


@app.get("/api/get-histories-from-bot")
async def get_histories_from_bot(user_id: str, limit: int,
                                 auth: Auth, cursor: Optional[int] = None,
                                 ):
    token, user_supabase = auth
    if not cursor:
        result = user_supabase.table("history").select("*").match(
            {"user_id": user_id}
        ).order("created_at", desc=True).limit(limit).execute()
    else:
        result = user_supabase.table("history").select("*").match(
            {"user_id": user_id}
        ).order(
            "created_at", desc=True
        ).lt("id", cursor).limit(limit).execute()
    if not result.data:
        raise HTTPException(status_code=400, detail=result)
    if type(result.data[-1]) is not dict:
        raise HTTPException(status_code=400, detail=result)
    response = {
        "data": result.data,
        "pagination": {
            "cursor": result.data[-1]["id"],
            "count": len(result.data)
        }
    }
    print(response)
    return response


@app.post("/api/create-history")
async def create_history(data:  CreateHistory, auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("history").insert(
        data.model_dump(mode="json")).execute()
    print(response)
    return response


@app.put("/api/update-history")
async def update_history(user_id: str, history_id: int,
                         data:  UpdateHistory, auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("history").update(
        data.model_dump(mode="json", exclude_none=True)
    ).match({"user_id": user_id, "id": history_id}).execute()
    print(response)
    return response


@app.post("/api/update-history-time-spent")
async def update_history_time_spent(user_id: str, history_id: int,
                                    payload: TimeSpentPayload, auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("history").select("*").match(
        {"user_id": user_id,  "id": history_id}
    ).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="No history entry")
    sim = response.data[0]
    if type(sim) is not dict:
        return response
    data = UpdateHistory(
        seconds_spent=sim["seconds_spent"]+payload.elapsed_secs,
        updated_at=payload.updated_at
    )
    response = user_supabase.table("history").update(
        data.model_dump(mode="json", exclude_none=True)
    ).match({"user_id": user_id, "id": history_id}).execute()
    # print(response)
    return response


# ----- settings endpoints -----

@app.get("/api/get-settings")
async def get_settings(user_id: str, auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("settings").select("*").match(
        {"user_id": user_id}).execute()
    print(response)
    return response


@app.post("/api/create-settings")
async def create_settings(data:  CreateSettings,
                          auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("settings").insert(
        data.model_dump(mode="json")).execute()
    print(response)
    return response


@app.put("/api/update-settings")
async def update_settings(user_id: str,
                          data:  UpdateSettings, auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("settings").update(
        data.model_dump(mode="json", exclude_none=True)
    ).match({"user_id": user_id}).execute()
    print(response)
    return response


# ----- stats endpoints -----

@app.get("/api/get-stats")
async def get_stats(user_id: str, auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("stats").select("*").match(
        {"user_id": user_id}).execute()
    print(response)
    return response


@app.post("/api/create-stats")
async def create_stats(data:  CreateStats, auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("stats").insert(
        data.model_dump(mode="json")).execute()
    print(response)
    return response


@app.put("/api/update-stats")
async def update_stats(user_id: str, data:  UpdateStats, auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("stats").update(
        data.model_dump(mode="json", exclude_none=True)
    ).match({"user_id": user_id}).execute()
    print(response)
    return response


@app.post("/api/update-stats-time-spent")
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


# ----- profile endpoints -----

@app.get("/api/get-profile")
async def get_profile(user_id: str, auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("profile").select("*").match(
        {"id": user_id}).execute()
    print(response)
    return response


@app.post("/api/create-profile")
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


@app.put("/api/update-profile")
async def update_profile(user_id: str, data:  UpdateProfile, auth: Auth):
    token, user_supabase = auth
    response = user_supabase.table("profile").update(
        data.model_dump(mode="json", exclude_none=True)
    ).match({"id": user_id}).execute()
    print(response)
    return response


@app.post("/api/generate-profile-monthly-messages")
async def generate_profile_monthly_messages(auth: Auth):
    prompt = """Generate a short message of the day.
        This will be used in an app called
        VIVID - visually intuitive & versatile interactive data strcuture.
        this is an app made to simplify learning dsa and make it fun thru
        the use of automated simulations based on user input. I want you
        to generate motivating & encauraging words to support the user.
        make it short sentence of 5-10 words.
        generate 50 diff messages, separated by | no spaces before and after."
        """
    client = OpenAI(
        base_url=OPEN_ROUTER_URL,
        api_key=OPEN_ROUTER_API_KEY,
    )
    referer_url = ""
    if PROJECT_URL:
        referer_url = PROJECT_URL
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": referer_url,
            "X-Title": "Vivid"
        },
        extra_body={},
        model="deepseek/deepseek-v3.1-terminus",
        messages=[
            {
              "role": "user",
              "content": prompt
            }
        ]
    )
    content = completion.choices[0].message.content
    if (not content):
        return
    messages = content.split("|")
    print(messages)
    return messages
