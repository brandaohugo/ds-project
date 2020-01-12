
import simpy
from datetime import datetime
import io

from cases import sim_params_1 as sim_params
from components import parse_components
from workloads import parse_workloads

globals()['components'] = {}

# define environment
env = simpy.Environment()
# log_filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".txt"

# parse paramaters
components = parse_components(env, sim_params['components'])
workloads = parse_workloads(env, sim_params['workloads'],components)

# run simulation
env.run(until=sim_params['settings']['sim_time'])