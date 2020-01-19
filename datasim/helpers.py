import simpy
import random
import numpy as np
import pandas as pd
from datetime import datetime
from functools import partial, wraps

def generate_error(env, affected_server):
    ''' Introduce Internal Server Error (500)'''
    yield env.timeout(IDLE_TIME)
    affected_server.action.interrupt()

# functions to return distributions

def random_uniform(dist_params):
    for i in range(10):
        number = np.random.uniform(dist_params['low'], dist_params['high'])
        if number > 0:
            return number

def random_normal(dist_params):
    for i in range(10):
        number = np.random.normal(dist_params['size'], dist_params['scale'])
        if number > 0:
            return number

def random_logistic(dist_params):
    for i in range(10):
        number = np.random.logistic(dist_params['location'], dist_params['scale'])
        if number > 0:
            return number

def random_poisson(dist_params):
    for i in range(10):
        number = np.random.poisson(dist_params['lambda'])
        if number > 0:
            return number

# generate updated distributions object

def random_number(dist_params):
    distributions = dict(uniform=random_uniform, normal=random_normal, logistic=random_logistic, poisson=random_poisson)
    return abs(int(distributions[dist_params['distribution']](dist_params)) + 1)

def print_stats(self):
    print(f'{self.count} of {self.capacity} are allocated')
    print(f'Users: {self.users}')
    print(f'Queued events: {self.queue}')

def patch_resource(resource, pre=None, post=None):
    '''
    :param resource:
    :param pre:
    :param post:
    :return:
    '''

    def get_wrapper(func):
        # generate a wrapper for put/get/request/release
        @wraps(func)
        def wrapper(*args, **kwargs):

            if pre:
                pre(resource)

            # perform actual operation
            ret = func(*args, **kwargs)

            # call "post" callback
            if post:
                post(resource)

            return ret
        return wrapper

    # replace the original operations with our wrapper
    for name in ['put', 'get', 'request', 'release']:
        if hasattr(resource, name):
            setattr(resource, name,  get_wrapper(getattr(resource, name)))

def monitor_res(data, resource):
    '''Monitoring callbacks'''
    item = (
        resource._env.now,
        resource.count,
        len(resource.queue),
    )
    data.append(item)

def create_df(data, df_type_dict, df_type):
    names = df_type_dict[df_type]
    log_filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".txt"
    df = pd.DataFrame(data, columns=names)
    # df.to_csv('log/' + log_filename, header=True)
    return df

def merge_df(df1, df2):
    # filename
    time = datetime.now().strftime("%Y%m%d%H%M%S") + ".txt"
    log_filename = 'log/' + 'merged_' + time
    # merge df
    df = df1.merge(df2, on='time')
    # save to log directory
    df.to_csv(log_filename, header=True)
    return df

def trace_event(env, callback):
    '''
    Replace the step() method of *env* with a tracing function that calls
    *callbacks* with an event time, priority ID and its instance just before
    being processed.
    :param env:
    :param callback:
    :return:
    '''

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


# initialize parameters
dist_params = {'distribution': 'poisson',
                'low' : 2, 
                'high' : 1000, 
                'scale': 2,
                'size' : 100,
                'location': 1,
                'mean': 1,
                'sigma': 2.5,
                'lambda': 85
                }

settings = {'sim_time' : 10000}

# dictionary for column names df params
df_names = {
    'event': ['time', 'eid', 'type'],
    'res': ['time', 'count', 'queue'],
}

# # Define Simulation Parameters
# IDLE_TIME = random_number(dist_params)
# SERVER_NUM = random_number(dist_params)
# PROCESSING_TIME = random_number(dist_params)
# PROCESSING_CAPACITY = random_number(dist_params)
# SIM_TIME = settings['sim_time']

# Define Simulation Parameters
# print(f'This run is initialized with hard coded params. Can be changed to stochastic in helpers.py.\n')
# IDLE_TIME = 5
# SERVER_NUM = 5
# PROCESSING_TIME = 10
# PROCESSING_CAPACITY = 4
# SIM_TIME =  40

# print(f'IDLE TIME: {IDLE_TIME}')
# print(f'PROCESSING_CAPACITY: {PROCESSING_CAPACITY}')