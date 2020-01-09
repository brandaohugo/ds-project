
import simpy
import random
import  itertools
from datetime import datetime

sim_params = {
    'settings': {
            'sim_time' : 100,
    },
    'components' : [
        {
            'type': 'server',
            'name' : 'server_1',
            'idle_time' : {
                'distribution' : 'uniform',
                'low': 0,
                'high': 1000,
                },
            'recovery_time' : 0,
            'process_speed': 20,
            'resource': 
                {
                    'name' : 'database',
                    'capacity' : 4
                },
        },
        # {
        #     'type': 'user',
        #     'name': 'user_1',
        #     'processes': {
        #         [
        #             {
        #                 'type': 'request to server',
        #                 'name': 'process_1',
        #                 'process_time': 10,
        #                 'gen_inter': (1,10),
        #                 'payload_size': (1,1000),
        #                 'target': 'server_1',
        #             },
        #         ]
        #     }
        # }
    ]
}



"""
Simulation: Read/Write operations with multiple servers.

When instantiated server executes the idle() process, which waits for new transaction requests to be received. This waiting time is modelled by a idle time parameter. 

After this idle time period the server receives a request to process a transaction. It also receives a number of transactions to be processed at that time period.

The server then executes a read/write operation defined by the read_write() function. Once this read/write operation is finished the server is idle again and waits for the next transaction request.

Setup:
Using context manager to pipe all standard output to a file.

Usage of helpers.py for functions used within simulation.
"""

import io
import simpy
from contextlib import redirect_stdout

def generate_error(env, affected_server):
    ''' Introduce Internal Server Error (500)'''
    yield env.timeout(25)
    affected_server.action.interrupt()



def log_event(log_file_name, message):
    with open(log_file_name, 'a') as f:
        with redirect_stdout(f):
            print(message)

# use context manager to capture print outputs

# Define Simulation Parameters
SERVER_NUM = 10
SIM_TIME = 100
PROCESSING_TIME = 10
PROCESSING_CAPACITY = 20

# Server object
class Server(object):
    def __init__(self, env, log_filename, params):
        self.env = env
        self.resource = simpy.Resource(self.env, capacity=params['resource']['capacity'])
        # start the idle process everytime server object is instantiated
        # self.action = env.process(self.idle())
        # self.name = params['name']
        # self.log_filename = log_filename
        self.params = params



def some_process(resource, log_filename):
    
    def print_stats(resource,log_filenmae):
        log_event(log_filename, f'{resource.count} of {resource.capacity} are allocated')
        log_event(log_filename, f'Users: {resource.users}')
        log_event(log_filename, f'Queued events: {resource.queue}')

    def read_write(processing_time):
        
        # print resource statistics
        print_stats()

        # make request to resource
        with self.resource.request() as req:
            yield req

            # processing a transaction takes time
            yield self.env.timeout(processing_time)
            
            log_event(self.log_filename, 'Server_%s finished read_write operation at %d.' % (self.name, self.env.now))

    while True:
        
        # Server is idle for a while
        
        log_event(self.log_filename, 'Server_%s is idle at %d' % (self.name, self.env.now))

        idle_time = 5 #self.params['idle_time']
        yield self.env.timeout(idle_time)

        # Server starts processing transactions, waits for read_write() to be done

        log_event(self.log_filename, 'Server_%s received transaction request at %d' % (self.name, self.env.now))

        try:
            yield self.env.process(self.read_write(PROCESSING_TIME))
        except simpy.Interrupt:
            log_event(self.log_filename, 'Server_%s was interrupted at %d, aborting read_write operation.' % (self.name, self.env.now))

    
    
# Introduce new servers into the simulation (creates new global objects)
def get_server(env,log_file_name, params):
    server  = Server(env, log_file_name, params)
    return server

def get_router(asdasdsad):
    pass    

def add_component(env, log_file_name, params):
    component = dict(server=get_server, router=get_router)
    globals()[params['name']] = component[params['type']](env, log_file_name, params)

# define environment
env = simpy.Environment()
log_filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".txt"

for comp_params in sim_params['components']:
    add_component(env, log_filename, comp_params)

# introduce an error process
# env.process(generate_error(env, server_object2))

# run simulation
env.run(until=sim_params['settings']['sim_time'])