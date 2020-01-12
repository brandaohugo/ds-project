sim_params_1 = {
    'settings': {
            'sim_time' : 50,
    },
    'components' : [
        {
            'type': 'server',
            'name' : 'db_server',
            'recovery_time' : 0, 
            'actions' : {
                    'read_write' : {
                        'proc_speed': 1
                    },
            },
            'resource': {
                    'name' : 'database',
                    'capacity' : 2
                } 
        }, 
    ],
    'workloads' : [
        {
            'type': 'db_request',
            'origin': 'user_1',
            'target': {
                'name': 'db_server',
            },
            'request_size': 10,
            'interval': 5
        },
        {
            'type': 'db_request',
            'origin': 'user_2',
            'target': {
                'name': 'db_server',
            },
            'request_size': 12,
            'interval': 3
        },
    ],
}