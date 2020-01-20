import numpy as np

def generate_error(env, params, components):
    ''' Introduce Internal Server Error '''

    # get simulation time
    for items in params:
        sim_time = params['settings']['sim_time']
    
    # get list of components with errors
    error_lst=[]
    for items in params['components']:
            if items['error'] == True:
                error_lst.append(items['name'])

    # random time error will be introduced
    error_wait = np.random.uniform(0, sim_time)

    # generate interrupts into affect components
    while True:
        yield env.timeout(error_wait)

        # increases used core count
        for key in error_lst:
            if key in components:
                affected_server_object = components[key]
                print('Introducing error into object --> ' + str(type(affected_server_object)))
                affected_server_object.used_cores = int(np.random.uniform(1, 4))
                print(affected_server_object.used_cores)
