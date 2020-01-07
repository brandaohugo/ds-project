import simpy

# Introduce Internal Server Error (500)
def generate_error(env, affected_server):
    yield env.timeout(25)
    affected_server.action.interrupt()