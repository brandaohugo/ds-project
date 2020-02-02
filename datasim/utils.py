import pandas as pd
import numpy as np
from contextlib import redirect_stdout
from functools import wraps
from datetime import datetime



# random distributions
def random_logistic(dist_params, start=None, end=None):
    return np.random.logistic(dist_params['location'], dist_params['scale'])

def random_lognormal(dist_params,  start=None, end=None):
    return np.random.lognormal(dist_params['mean'], dist_params['sd'])

def random_normal(dist_params, start=None, end=None):
    return np.random.normal(dist_params['mean'], dist_params['sd'])

def random_uniform(dist_params, start=None, end=None):
    return np.random.uniform(dist_params['low'], dist_params['high'])

def random_poisson(dist_params, start=None, end=None):
    return np.random.poisson(dist_params['lambda'])

def random_number(dist_params, start=None, end=None):
    distributions = dict(
        uniform=random_uniform,
        normal=random_normal,
        lognormal=random_lognormal,
        logistic=random_logistic,
        poisson=random_poisson)
    return distributions[dist_params['distribution']](dist_params, start, end)



# monitoring
def trace_event(env, callback):
    ''' Replace the step() method of *env* with a tracing function that calls
    *callbacks* with an event time, priority ID and its instance just before
    being processed.'''
    def get_wrapper(env_step, callback):
        '''generate wrapper for env.step()'''
        @wraps(env_step)
        def tracing_step():
            '''Call *callback* for the next event if on exist before
            calling env.step()'''
            if len(env._queue):
                t, prio, eid, event = env._queue[0]
                callback(t, prio, eid, event)
            return env_step()
        return tracing_step
    env.step = get_wrapper(env.step, callback)

def monitor_event(data, t, prio, eid, event):
    data.append((t, eid, type(event)))

def log_event(data):
    names = ['time', 'eid', 'type']
    log_filename = 'event_' + datetime.now().strftime("%Y%m%d%H%M%S") + ".csv"
    df = pd.DataFrame(data, columns=names)
    # save results in log directory
    df.to_csv('log/' + log_filename, header=True)
    return df

def monitor_simulation_components(env, components):
    stats_filename = 'stat_' + datetime.now().strftime("%Y%m%d%H%M%S") + ".csv"
    df = pd.DataFrame()
    while True:
        for name in components.keys():
            cp_stats = components[name].get_stats()
            df = (df.append(cp_stats, ignore_index=True))
            df.to_csv('datasim/log/' + stats_filename)

            # python simulation.py | grep -F "[monitor]" for stdout stats
            # print(f'[monitor] {env.now} {name} {cp_stats}')
        yield env.timeout(1)