from components import Component
from workloads import Workload
from simpy import Environment

wl_params = {
    'start_time': 0,
    'end_time': 50,
    'type': 'db_request',
    'name': 'user_authentication',
    'request_size': 10,
    'target': {
        'name': 'db_server',
    },
    'interarrival': {
        'distribution': 'uniform',
        'low': 1,
        'high': 1,
    },
    'volume': {
        'distribution': 'uniform',
        'low': 0,
        'high': 10
    },
}

cp_params = {
    'type': 'server',
    'name' : 'db_server',
    'recovery_time' : 0, 
    'actions' : {
            'read_write' : {
                'proc_speed': 1
            },
    },
    'resource': {
            'name' : 'database',
            'capacity' : 2
        } 
}


env = Environment()
components = dict(
    db_server=Component(env,cp_params)
)

workload = Workload(env, components, wl_params)

env.run(until=10)
