import pandas as pd
import numpy as np
from contextlib import redirect_stdout
from functools import wraps
from datetime import datetime

# Simulation logging
def log_event_from_print(log_file_name, message):
    with open(log_file_name, 'a') as f:
        with redirect_stdout(f):
            print(message)

def print_stats(resource,log_filename):
    log_event_from_print(log_filename, f'{resource.count} of {resource.capacity} are allocated')
    log_event_from_print(log_filename, f'Users: {resource.users}')
    log_event_from_print(log_filename, f'Queued events: {resource.queue}')

def print_resource_info(resource):
    print(f'Count: {resource.count}, Capacity: {resource.capacity} ,Users: {len(resource.users)}, Queue: {len(resource.queue)}')

# simple resource monitoring (outside class)
def monitor_res(name, resource, data):
    item = (
        name,
        resource._env.now,
        resource.count,
        len(resource.queue),
    )
    data.append(item)

# resource monitoring within class
def patch_resource(resource, pre=None, post=None):
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

def monitor_res2(data, resource):
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

def log_event(data):
    names = ['time', 'eid', 'type']
    log_filename = 'event_' + datetime.now().strftime("%Y%m%d%H%M%S") + ".txt"
    df = pd.DataFrame(data, columns=names)
    # save results in log directory
    df.to_csv('log/' + log_filename, header=True)
    return df

def log_res(components):
    df = pd.DataFrame()
    log_filename = 'res_' + datetime.now().strftime("%Y%m%d%H%M%S") + ".txt"
    # log components resources
    for key, server_object in components.items():
        name = [f'{server_object.name}'] * len(server_object.data_res)
        df_temp = pd.DataFrame(server_object.data_res)
        df_temp['name'] = name
        df = df.append(df_temp)
        # format and save dataframe
    df.columns = ['time', 'count', 'queue', 'name']
    df = df.sort_values('time', ascending=True)
    df.to_csv('log/' + log_filename, header=True)
    return df

def combine_log(df1, df2):
    # filename
    time = datetime.now().strftime("%Y%m%d%H%M%S") + ".txt"
    log_filename = 'log/' + time
    # merge df
    df = df1.merge(df2, on='time')
    # save to log directory
    df.to_csv(log_filename, header=True)
    return df

# functions to return distributions

def random_uniform(wl_params):
    number = np.random.uniform(wl_params['low'], wl_params['high'])
    return number

def random_normal(wl_params):
    for i in range(10):
        number = np.random.normal(wl_params['size'], wl_params['scale'])
        if number > 0:
            return number

def random_logistic(wl_params):
    for i in range(10):
        number = np.random.logistic(wl_params['location'], wl_params['scale'])
        if number > 0:
            return number

def random_poisson(wl_params):
    for i in range(10):
        number = np.random.poisson(wl_params['lambda'])
        if number > 0:
            return number

# generate updated distributions object

def random_number(wl_params):
    distributions = dict(uniform=random_uniform, normal=random_normal, logistic=random_logistic, poisson=random_poisson)
    return abs(int(distributions[wl_params['distribution']](wl_params)) + 1)