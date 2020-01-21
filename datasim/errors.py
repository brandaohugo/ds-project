import numpy as np

def generate_error(env, params, components):
    ''' Introduce Internal Server Error '''

    # simulation time
    sim_time = params['settings']['sim_time']

    # list of targeted servers
    error_lst = [server['name'] for server in params['components'] if server['error'] is True]

    # random timeout
    error_wait = np.random.uniform(0, sim_time)

    # generate interrupts into affect components
    while True:
        yield env.timeout(error_wait)

        # increases used core count
        for key in error_lst:
            if key in components:
                affected_server_object = components[key]
                print('Introducing error into object --> ' + str(type(affected_server_object)))
                affected_server_object.used_cores += 1
                print(affected_server_object.used_cores)


