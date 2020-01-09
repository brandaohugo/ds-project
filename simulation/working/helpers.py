import simpy
import random
import numpy as np

def generate_error(env, affected_server):
    ''' Introduce Internal Server Error (500)'''
    yield env.timeout(IDLE_TIME)
    affected_server.action.interrupt()

# functions to return distributions

def random_uniform(dist_params):
    for i in range(10):
        number = np.random.logistic(dist_params['low'], dist_params['high'])
        if number > 0:
            return number

def random_normal(dist_params):
    for i in range(10):
        number = np.random.logistic(dist_params['size'], dist_params['scale'])
        if number > 0:
            return number

def random_logistic(dist_params):
    for i in range(10):
        number = np.random.logistic(dist_params['location'], dist_params['scale'])
        if number > 0:
            return number

def random_poisson(dist_params):
    for i in range(10):
        number = np.random.logistic(dist_params['lambda'])
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

dist_params = {'distribution': 'normal', 
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


# Define Simulation Parameters
IDLE_TIME = random_number(dist_params)
SERVER_NUM = random_number(dist_params)
PROCESSING_TIME = random_number(dist_params)
PROCESSING_CAPACITY = random_number(dist_params)
SIM_TIME = settings['sim_time']

print(IDLE_TIME)
print(PROCESSING_CAPACITY)