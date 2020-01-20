
def generate_error(env, affected_server):
    ''' Introduce Internal Server Error (500)'''

    ''''below are parsed from cases dictionary'''
    # simulation time
    # number of errors
    # error_interval = sim_time/nr_errors
    # yield timeout(error_interval)


    yield env.timeout(5) #TODO:

    affected_server.action.interrupt('\n\nSmall interrupter\n\n')


