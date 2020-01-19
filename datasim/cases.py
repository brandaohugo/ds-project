sim_params_1 = {
    'settings': {
            'sim_time' : 50,
    },
    'components' : [
        {
            'type': 'load_balancer',
            'name': 'auth_load_balancer',
            'servers': ['auth_server_01','auth_server_02'],
            'num_cores': 4,
            'core_speed': 1
        },
        {
            'type': 'auth_server',
            'db_server_name': 'auth_db_server',
            'load_balancer': 'auth_load_balancer',
            'name' : 'auth_server_01',
            'num_cores': 4,
            'core_speed': 1
        },
         {
            'type': 'auth_server',
            'db_server_name': 'auth_db_server',
            'load_balancer': 'auth_load_balancer',
            'name' : 'auth_server_02',
            'num_cores': 4,
            'core_speed': 1,
        },
        {
            'type': 'db_server',
            'name': 'auth_db_server',
            'num_cores': 4,
            'core_speed': 1
        }
    ],
    'workloads' : [
        {
            'start_time': 0,
            'end_time': 9,
            'type': 'db_request',
            'name': 'user_authentication',
            'request_size': 1,
            'job_action': 'auth',
            'target': {
                'name': 'auth_load_balancer',
            },
            'job_size' : {
                'distribution': 'uniform',
                'low': 1,
                'high': 1
            },
            'interarrival': {
                'distribution': 'uniform',
                'low': 2,
                'high': 2,
            },
            'volume': {
                'distribution': 'uniform',
                'low': 15,
                'high': 15
            }
        }
    ],
}

