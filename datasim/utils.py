import pandas as pd
import numpy as np
from contextlib import redirect_stdout
from functools import wraps
from datetime import datetime

# Simulation logging
def log_event(log_file_name, message):
    with open(log_file_name, 'a') as f:
        with redirect_stdout(f):
            print(message)

def print_stats(resource,log_filename):
    log_event(log_filename, f'{resource.count} of {resource.capacity} are allocated')
    log_event(log_filename, f'Users: {resource.users}')
    log_event(log_filename, f'Queued events: {resource.queue}')

def print_resource_info(resource):
    print(f'Count: {resource.count}, Capacity: {resource.capacity} ,Users: {len(resource.users)}, Queue: {len(resource.queue)}')

#TODO: implement resource monitoring in components.py
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

# event monitoring
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

def create_df(data, df_type):
    # dictionary with column names
    df_type_dict = {
        'event': ['time', 'eid', 'type'],
        'res': ['time', 'count', 'queue'],
    }
    # create dataframe
    names = df_type_dict[df_type]
    log_filename = df_type + '_' + datetime.now().strftime("%Y%m%d%H%M%S") + ".txt"
    df = pd.DataFrame(data, columns=names)
    # save results in log directory
    df.to_csv('log/' + log_filename, header=True)
    return df

# Random number generators
def random_uniform(wl_params):
    number = np.random.uniform(wl_params['low'], wl_params['high'])
    return number

def random_number(wl_params):
    distributions = dict(uniform=random_uniform)
    return distributions[wl_params['distribution']](wl_params)