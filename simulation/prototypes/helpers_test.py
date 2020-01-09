import simpy
import random
import pandas as pd

from datetime import datetime
from functools import partial, wraps


def generate_error(env, affected_server):
    ''' Introduce Internal Server Error (500)'''
    yield env.timeout(25)
    affected_server.action.interrupt()

def generate_time_out(env, affected_server):
    '''Introduce Temporary Server Error (501)'''
    time = random.randint(0, 25)
    yield env.timeout(time)
    affected_server.action.interrupt()

def random_interrupt(env, affected_server):
    try:
        yield env.timeout(random.randint(20, 40))
        affected_server.action.interrupt()
        print(f'Interruption of test done at {env.now}')
    except simpy.Interrupt as i:
        print(f'Environment interrupted at {env.now}! msg: {i.cause}')

def resource_user(env, resource):

    while True:
        request = resource.request()
        yield request
        print(f'requested at {env.now}')
        yield env.timeout(2)
        print(f'released at {env.now}')
        resource.release(request)

# def server(env, channel):
#     yield env.timeout(66)
#     if channel.items:
#         msg = yield channel.get()

simpy.Container

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

def monitor(data, resource):
    '''Monitoring callbacks'''
    item = (
        resource._env.now,
        resource.count,
        len(resource.queue),
    )
    data.append(item)

def create_df(data):
    names = ['time', 'count', 'queue']
    log_filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".txt"

    df = pd.DataFrame(data, columns=names)
    df.to_csv(log_filename, header=True)
    return df





