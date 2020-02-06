
import simpy
from functools import partial

import numpy as np
from components import parse_components
from workloads import parse_workloads, Workload
from utils import monitor_event, trace_event, log_event, monitor_simulation_components
import argparse
import json

def generate_error(env, components, err_params):
    err_time = err_params['time']
    print("error time", err_time)
    yield env.timeout(err_time)
    env.process(get_error_function(err_params['type'])(env, components, err_params))




def very_slow(env, components, err_params):
    target_component = components[err_params['target']]
    original_core_speed = target_component.core_speed
    print(f'Setting ${target_component.name} core_speed to ${err_params["core_speed"]}')
    target_component.core_speed = err_params['core_speed']
    if 'duration' in err_params:
        yield env.timeout(env.now + err_params['duration'])
        print(f'Setting ${target_component.name} core_speed back to to ${original_core_speed}')
        target_component.core_speed = original_core_speed

def get_error_function(error_type):
    errors = dict(
        very_slow=very_slow
    )
    print('got error function')
    return errors[error_type]

def run_simulation(sim_params):
    # define environment
    env = simpy.Environment()
    # log_filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".txt"

    # parse paramaters
    components = parse_components(env, sim_params['components'])

    # workloads = parse_workloads(env, sim_params['workloads'],components)
    for wl_params in sim_params['workloads']:
        Workload(env, components, wl_params)

    for err_params in sim_params['errors']:
        print("generatinggggg error", generate_error)
        env.process(generate_error(env, components, err_params))
        print("errors generated")
    # component monitoring
    env.process(monitor_simulation_components(env, components))

    # introduce errors
    # env.process(generate_error(env, sim_params, components))
    # def generate_error(env,er_params,components):
    #     yield env.timeout(er_params['time'])
    #     components[er_params['target']].core_speed = er_params['core_speed']

    # for er_params in sim_params['errors']:
    #     env.process(generate_error(env,er_params,components))


    # run simulation
    # print(sim_params['settings']['sim_time'])
    env.run(until=sim_params['settings']['sim_time'])

    # store results
    # df_event = log_event(data_event)
    # print(df_event['type'].values[0])
    # df_res = log_res(components)
    # df = combine_log(df_event, df_res)
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--scenario', metavar='scenario', type=str, nargs='+',
                    help='json file')

    args = parser.parse_args()
    scenario_file = args.scenario[0]
    sim_params = json.loads(open(scenario_file).read())
    run_simulation(sim_params)
