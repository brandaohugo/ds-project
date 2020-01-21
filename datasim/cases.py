sim_params = {
    'settings': {
            'sim_time' : 50,
    },
    'components' : [
        {
            'type': 'load_balancer',
            'name': 'auth_load_balancer',
            'servers': ['auth_server_01','auth_server_02','auth_server_03'],
            'num_cores': 4,
            'core_speed': 1,
            'error': False
        },
        {
            'type': 'auth_server',
            'db_server_name': 'auth_db_server',
            'load_balancer': 'auth_load_balancer',
            'name' : 'auth_server_01',
            'num_cores': 4,
            'core_speed': 1,
            'error': False
        },
         {
            'type': 'auth_server',
            'db_server_name': 'auth_db_server',
            'load_balancer': 'auth_load_balancer',
            'name' : 'auth_server_02',
            'num_cores': 4,
            'core_speed': 1,
            'error': True
        },
        {
            'type': 'auth_server',
            'db_server_name': 'auth_db_server',
            'load_balancer': 'auth_load_balancer',
            'name' : 'auth_server_03',
            'num_cores': 4,
            'core_speed': 1,
            'error': False
        },
        {
            'type': 'db_server',
            'name': 'auth_db_server',
            'num_cores': 4,
            'core_speed': 1,
            'error': False
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
                'high': 6
            },
            'interarrival': {
                'distribution': 'uniform',
                'low': 2,
                'high': 7,
            },
            'volume': {
                'distribution': 'uniform',
                'low': 4,
                'high': 15
            }
        }
    ],
    'errors':[
        {
            'type': 'very_slow',
            'core_speed': 1,
            'target': 'auth_server_01',
            'time': 10
        }
    ]
}

