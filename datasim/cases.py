sim_params_1 = {
    'settings': {
            'sim_time' : 10,
    },
    'components' : [
        {
            'type': 'auth_server',
            'db_server_name': 'auth_db_server',
            'name' : 'auth_server',
            'num_cores': 4,
            'core_speed': 1
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
            'end_time': 6,
            'type': 'db_request',
            'name': 'user_authentication',
            'request_size': 1,
            'target': {
                'name': 'auth_server',
            },
            'job_size' : {
                'distribution': 'uniform',
                'low': 1,
                'high': 1
            },
            'interarrival': {
                'distribution': 'uniform',
                'low': 1,
                'high': 1,
            },
            'volume': {
                'distribution': 'uniform',
                'low': 1,
                'high': 1
            }
        }
    ],
}

