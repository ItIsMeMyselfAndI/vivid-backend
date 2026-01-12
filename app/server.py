import json
from typing import Annotated, Optional
from openai import OpenAI
from schema.profile import CreateProfile, UpdateProfile
from schema.simulation import (
    CreateSimulation, UpdateSimulation, SimulationType
)
from schema.settings import CreateSettings, UpdateSettings
from schema.history import CreateHistory, UpdateHistory
from client.index import supabase

from fastapi import Depends, FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from schema.stats import CreateStats, UpdateStats


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
OPEN_ROUTER_URL = "https://openrouter.ai/api/v1"
OPEN_ROUTER_API_KEY = os.environ.get("OPEN_ROUTER_API_KEY")


async def validate_token(
    request: Request,
    authorization: Annotated[Optional[str], Header()] = None,
) -> str:
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
    supabase.auth.set_session(access_token=access_token, refresh_token="")
    return token

Auth = Annotated[str, Depends(validate_token)]


# ----- simulation endpoints -----

@app.get("/api/get-simulation")
async def get_simulation(user_id: str, simulation_type: SimulationType,
                         auth: Auth):
    response = supabase.table("simulation").select("*").match(
        {"user_id": user_id, "type": simulation_type.value}
    ).execute()
    print(response)
    return response


@app.get("/api/get-all-simulations")
async def get_all_simulations(user_id: str, auth: Auth):
    response = supabase.table("simulation").select("*").match(
        {"user_id": user_id}
    ).execute()
    print(response)
    return response


@app.post("/api/create-simulation")
async def create_simulation(data:  CreateSimulation, auth: Auth):
    response = supabase.table("simulation").insert(
        data.model_dump(mode="json")).execute()
    print(response)
    return response


@app.put("/api/update-simulation")
async def update_simulation(
        user_id: str, simulation_type: SimulationType,
        data:  UpdateSimulation, auth: Auth
):
    response = supabase.table("simulation").update(
        data.model_dump(mode="json", exclude_none=True)
    ).match({"user_id": user_id, "type": simulation_type.value}).execute()
    print(response)
    return response


@app.post("/api/update-simulation-time-spent")
async def update_simulation_time_spent(
        user_id: str, simulation_type: SimulationType,
        req: Request
):
    req_body = await req.body()
    blob = json.loads(req_body.decode())
    print(blob)
    response = supabase.table("simulation").select("*").match(
        {"user_id": user_id, "type": simulation_type.value}
    ).execute()
    if not response.data:
        return HTTPException(status_code=400, detail="No stats entry")
    sim = response.data[0]
    if type(sim) is not dict:
        return response
    elapsed_secs = blob["elapsed_secs"]
    data = UpdateSimulation(
        seconds_spent=sim["seconds_spent"]+elapsed_secs,
        updated_at=blob["updated_at"]
    )
    print(data)
    response = supabase.table("simulation").update(
        data.model_dump(mode="json", exclude_none=True)
    ).match({"user_id": user_id, "type": simulation_type.value}).execute()
    print(response)
    return response


# ----- history endpoints -----

@app.get("/api/get-history")
async def get_history(user_id: str, history_id: int, auth: Auth):
    response = supabase.table("history").select("*").match(
        {"user_id": user_id, "id": history_id}
    ).execute()
    print(response)
    return response


@app.get("/api/get-histories-from-bot")
async def get_histories_from_bot(user_id: str, limit: int,
                                 auth: Auth, cursor: Optional[int] = None,
                                 ):
    if not cursor:
        result = supabase.table("history").select("*").match(
            {"user_id": user_id}
        ).order("created_at", desc=True).limit(limit).execute()
    else:
        result = supabase.table("history").select("*").match(
            {"user_id": user_id}
        ).order(
            "created_at", desc=True
        ).lt("id", cursor).limit(limit).execute()
    if not result.data:
        return HTTPException(status_code=400, detail=result)
    if type(result.data[-1]) is not dict:
        return HTTPException(status_code=400, detail=result)
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
    response = supabase.table("history").insert(
        data.model_dump(mode="json")).execute()
    print(response)
    return response


@app.put("/api/update-history")
async def update_history(user_id: str, history_id: int,
                         data:  UpdateHistory, auth: Auth):
    response = supabase.table("history").update(
        data.model_dump(mode="json", exclude_none=True)
    ).match({"user_id": user_id, "id": history_id}).execute()
    print(response)
    return response


@app.post("/api/update-history-time-spent")
async def update_history_time_spent(user_id: str,
                                    history_id: int, req: Request):
    req_body = await req.body()
    blob = json.loads(req_body.decode())
    # print(blob)
    response = supabase.table("history").select("*").match(
        {"user_id": user_id,  "id": history_id}
    ).execute()
    if not response.data:
        return HTTPException(status_code=400, detail="No history entry")
    sim = response.data[0]
    if type(sim) is not dict:
        return response
    elapsed_secs = blob["elapsed_secs"]
    data = UpdateHistory(
        seconds_spent=sim["seconds_spent"]+elapsed_secs,
        updated_at=blob["updated_at"]
    )
    print(type(sim))
    print(sim["seconds_spent"]+elapsed_secs)
    response = supabase.table("history").update(
        data.model_dump(mode="json", exclude_none=True)
    ).match({"user_id": user_id, "id": history_id}).execute()
    # print(response)
    return response


# ----- settings endpoints -----

@app.get("/api/get-settings")
async def get_settings(user_id: str, auth: Auth):
    response = supabase.table("settings").select("*").match(
        {"user_id": user_id}).execute()
    print(response)
    return response


@app.post("/api/create-settings")
async def create_settings(data:  CreateSettings,
                          auth: Auth):
    response = supabase.table("settings").insert(
        data.model_dump(mode="json")).execute()
    print(response)
    return response


@app.put("/api/update-settings")
async def update_settings(
    user_id: str, data:  UpdateSettings,
        auth: Auth):
    response = supabase.table("settings").update(
        data.model_dump(mode="json", exclude_none=True)
    ).match({"user_id": user_id}).execute()
    print(response)
    return response


# ----- stats endpoints -----

@app.get("/api/get-stats")
async def get_stats(user_id: str,
                    auth: Auth):
    response = supabase.table("stats").select("*").match(
        {"user_id": user_id}).execute()
    print(response)
    return response


@app.post("/api/create-stats")
async def create_stats(data:  CreateStats,
                       auth: Auth):
    response = supabase.table("stats").insert(
        data.model_dump(mode="json")).execute()
    print(response)
    return response


@app.put("/api/update-stats")
async def update_stats(
    user_id: str, data:  UpdateStats,
        auth: Auth):
    response = supabase.table("stats").update(
        data.model_dump(mode="json", exclude_none=True)
    ).match({"user_id": user_id}).execute()
    print(response)
    return response


@app.post("/api/update-stats-time-spent")
async def update_stats_time_spent(
        user_id: str, req: Request
):
    req_body = await req.body()
    blob = json.loads(req_body.decode())
    print(blob)
    response = supabase.table("stats").select("*").match(
        {"user_id": user_id}
    ).execute()
    if not response.data:
        return HTTPException(status_code=400, detail="No stats entry")
    sim = response.data[0]
    if type(sim) is not dict:
        return response
    elapsed_secs = blob["elapsed_secs"]
    data = UpdateSimulation(
        seconds_spent=sim["seconds_spent"]+elapsed_secs,
        updated_at=blob["updated_at"]
    )
    print(data)
    response = supabase.table("stats").update(
        data.model_dump(mode="json", exclude_none=True)
    ).match({"user_id": user_id}).execute()
    print(response)
    return response


# ----- profile endpoints -----

@app.get("/api/get-profile")
async def get_profile(user_id: str,
                      auth: Auth):
    response = supabase.table("profile").select("*").match(
        {"id": user_id}).execute()
    print(response)
    return response


@app.post("/api/create-profile")
async def create_profile(data:  CreateProfile,
                         auth: Auth):
    session = supabase.auth.get_user()
    if not session:
        return HTTPException(status_code=400, detail="User not found")
    if not session.user.user_metadata["username"]:
        return HTTPException(status_code=400, detail="User not found")
    username = session.user.user_metadata.get("username")
    if not username:
        return HTTPException(status_code=400, detail="Username not found")
    print(username)
    data.username = username
    response = supabase.table("profile").insert(
        data.model_dump(mode="json", exclude_none=True)).execute()
    print(response)
    return response


@app.put("/api/update-profile")
async def update_profile(
    user_id: str, data:  UpdateProfile,
        auth: Auth):
    response = supabase.table("profile").update(
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
