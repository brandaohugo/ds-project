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
        {
            'type': 'server',
            'name' : 'load_balancer',
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
        {
            'type': 'server',
            'name' : 'load_balancer2',
            'recovery_time' : 0,
            'actions' : {
                    'read_write' : {
                        'proc_speed': 1
                    },
            },
            'resource': {
                    'name' : 'database',
                    'capacity' : 2
                },
        }
    ],
    'workloads' : [
        {
            'type': 'db_request',
            'origin': 'user_1',
            'target': {
                'name': 'db_server',
            },
            'request_size': 10,
            'distribution': 'uniform',
            'low': 1,
            'high': 5
        },
        {
            'type': 'db_request',
            'origin': 'user_2',
            'target': {
                'name': 'load_balancer',
            },
            'request_size': 12,
            'distribution': 'uniform',
            'low': 6,
            'high': 7
        },
        {
            'type': 'db_request',
            'origin': 'user_3',
            'target': {
                'name': 'load_balancer2',
            },
            'request_size': 12,
            'distribution': 'uniform',
            'low': 6,
            'high': 7
        }
    ],
}

