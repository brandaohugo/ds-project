from contextlib import redirect_stdout
import numpy as np

# Simulation logging

def log_event(log_file_name, message):
    with open(log_file_name, 'a') as f:
        with redirect_stdout(f):
            print(message)

def print_stats(resource,log_filenmae):
    log_event(log_filename, f'{resource.count} of {resource.capacity} are allocated')
    log_event(log_filename, f'Users: {resource.users}')
    log_event(log_filename, f'Queued events: {resource.queue}')

def print_resource_info(resource):
    print(f'Count: {resource.count}, Capacity: {resource.capacity} ,Users: {len(resource.users)}, Queue: {len(resource.queue)}')

# Random number generators

def random_uniform(wl_params):
    number = np.random.uniform(wl_params['low'], wl_params['high'])
    return number

def random_number(wl_params):
    distributions = dict(uniform=random_uniform)
    return distributions[wl_params['distribution']](wl_params)