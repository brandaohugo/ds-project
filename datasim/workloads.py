import itertools
from utils import random_number

def db_request_generator(env, wl_params, components):
    for i in itertools.count():
        # generate interval according to stochastic distribution
        interval = random_number(wl_params)
        # print('%s wating to request read_write operation at %d.' % (wl_params['origin'],env.now))
        yield env.timeout(interval)
        # print('%s starting request read_write operation at %d.' % (wl_params['origin'],env.now))
        env.process(components[wl_params['target']['name']].read_write(wl_params['origin'], wl_params['request_size']))
        # print('%s finished request read_write operation at %d.' % (wl_params['origin'],env.now))

def get_workload(env, wl_params, components):
    workload = dict(
        db_request=db_request_generator
        )
    return env.process(workload[wl_params['type']](env, wl_params, components))
    
def parse_workloads(env, workloads_list, components):
    workloads = {}
    for wl_params in workloads_list:
        workloads[wl_params['origin']] = get_workload(env, wl_params, components)
    return workloads
