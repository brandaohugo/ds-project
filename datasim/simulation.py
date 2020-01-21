
import simpy
from functools import partial
import io
from datetime import datetime
# from cases import sim_params_1 as sim_params
from components import parse_components
from workloads import parse_workloads, Workload
from utils import monitor_event, trace_event, log_event, log_res, combine_log, monitor_simulation_components
from errors import generate_error
import argparse
import json

def run_simulation(sim_params):
    # define environment
    env = simpy.Environment()
    # log_filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".txt"

    # parse paramaters
    components = parse_components(env, sim_params['components'])

    # workloads = parse_workloads(env, sim_params['workloads'],components)
    workload = Workload(env, components, sim_params['workloads'][0])

    # component monitoring
    env.process(monitor_simulation_components(env, components))

    # introduce errors
    env.process(generate_error(env, sim_params, components))

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