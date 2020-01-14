
import simpy
from functools import partial
import io

from cases import sim_params_1 as sim_params
from components import parse_components
from workloads import parse_workloads
from utils import monitor_event, trace_event, create_df

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
workloads = parse_workloads(env, sim_params['workloads'],components)

# run simulation
env.run(until=sim_params['settings']['sim_time'])

# store results
df_event = create_df(data_event, df_type='event')