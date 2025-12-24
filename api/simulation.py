from schema.main import CreateSimulation, UpdateSimulation, SimulationType
from client.main import supabase


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
