
import simpy
from functools import partial
import io
from datetime import datetime
from cases import sim_params_1 as sim_params
from components import parse_components
from workloads import parse_workloads, Workload
from utils import monitor_event, trace_event, log_event, log_res, combine_log, monitor_simulation_components
from errors import generate_error

globals()['components'] = {}

# store results
data_event = []

# monitor events
monitor_event = partial(monitor_event, data_event)

# define environment
env = simpy.Environment()
# log_filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".txt"

# trace events in environment
trace_event(env, monitor_event)

# parse paramaters
components = parse_components(env, sim_params['components'])
print(components)
# workloads = parse_workloads(env, sim_params['workloads'],components)
workload = Workload(env, components, sim_params['workloads'][0])

# component monitoring
env.process(monitor_simulation_components(env, components))

# introduce errors
env.process(generate_error(env, sim_params, components))

# run simulation
print(sim_params['settings']['sim_time'])
env.run(until=sim_params['settings']['sim_time'])

# store results
df_event = log_event(data_event)
# print(df_event['type'].values[0])
# df_res = log_res(components)
# df = combine_log(df_event, df_res)
