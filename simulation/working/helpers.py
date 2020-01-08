import simpy

def generate_error(env, affected_server):
    ''' Introduce Internal Server Error (500)'''
    yield env.timeout(25)
    affected_server.action.interrupt()