import numpy as np

def generate_error(env, components, err_params):
    err_time = err_params['time']
    print("error time", err_time)
    yield env.timeout(err_time)
    get_error_function(err_params['type'])(env, components, err_params)


def get_error_function(error_type):
    errors = dict(
        very_slow=very_slow
    )
    return errors[error_type]

def veryslow(env, components, err_params):
    target_component = components[err_params['target']]
    original_core_speed = target_component.core_speed
    print(f'Setting ${target_component.name} core_speed to ${err_params["core_speed"]}')
    target_component.core_speed = err_params['core_speed']
    if 'duration' in err_params:
        yield env.timeout(env.now + err_params['duration'])
        print(f'Setting ${target_component.name} core_speed back to to ${original_core_speed}')
        target_component.core_speed = original_core_speed