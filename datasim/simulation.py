
import simpy
import random
import  itertools


sim_params = {
    'settings': {
            'sim_time' : 100,
    },
    'components' : [
        {
            'type': 'server',
            'name' : 'server_1',
            'conc_users':  4,
            'process_speed': 20,
        },
        {
            'type': 'user',
            'name': 'user_1',
            'processes': {
                'type': 'request to server',
                'name': 'process_1',
                'process_time': 10,
                'gen_inter': (1,10),
                'payload_size': (1,1000),
                'target': 'server_1',
            }
        }
    ]
}


class Simulation:
    def __init__(self, sim_params):
        self.sim_params = sim_params
        self.env = simpy.Environment()
        self.components = {}
        self.logs = []

    def _parse_components(self):
        components_params = self.sim_params['components']
        for params in components_params:    
            if params['type'] == 'server':
                component = {}
                component['resource'] = simpy.Resource(self.env, params['conc_users'])

                self.components[params['name']] = component

        return components
    
    def _create_processes(self):
        processes_params = self.sim_params['processes']
        for params in processes_params:
            if params['type'] == 'request to server':
                process = self.env.process(self.create_request_to_server(
                    params['name'], 
                    self.env, 
                    self.components[0]))    

    
    def create_user_request_to_server(self, name, env, server):        
        def a(i, env, server):
            print('%d of %d slots are allocated.' % (server.count, server.capacity))
            print(' Users:', server.users)
            print(' Queued events:', server.queue)
            with server.request() as req:
                yield req
                job_time = random.randint(
                    *sim_params['settings']['PAYLOAD_SIZE']) / sim_params['settings']['PROCESS_SPEED'] 
                yield env.timeout(job_time)
        
    
        for i in itertools.count(): 
            yield env.timeout(random.randint(*[0, 10]))
            server = self.components[target]['resource']
            env.process(a(i, env, server))
        
        
    
    def run(self):
        self.components = self._create_components()
        self.processes = self._create_processes()
        self.env.run(until=self.sim_params['settings']['sim_time'])
        return self.logs


Simulation(sim_params).run()