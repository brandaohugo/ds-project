from pymongo import MongoClient

def get_simulation_db()
    client = MongoClient()
    datasim = client.datasim
    return datasim.simulation

def store_sim_params(sim_params):
    simulation = get_simulation_db()
    result = simulation.insert_one(sim_params)