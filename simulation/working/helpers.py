import simpy
import random

def generate_error(env, affected_server):
    ''' Introduce Internal Server Error (500)'''
    yield env.timeout(25)
    affected_server.action.interrupt()

def print_stats(self):
    print(f'{self.count} of {self.capacity} are allocated')
    print(f'Users: {self.users}')
    print(f'Queued events: {self.queue}')