from simpy import Resource
from functools import partial
from utils import print_resource_info, print_stats, monitor_res, monitor_res2, patch_resource


# Server object
class Server(object):
    def __init__(self, env, params):
        self.env = env
        self.resource = Resource(self.env, capacity=params['resource']['capacity'])
        self.name = params['name']
        self.params = params
        self.data_res = []

        # monitor resources
        self.monitor_res2 = partial(monitor_res2, self.data_res)
        patch_resource(self.resource, post=self.monitor_res2)

    def read_write(self, origin, request_size):
        with self.resource.request() as req:
            yield req
            print('%s started read_write operation from %s at %d.' % (self.name, origin, self.env.now))
            processing_time = request_size / self.params['actions']['read_write']['proc_speed']
            yield self.env.timeout(processing_time)
            print('%s finished read_write operation from %s at %d.' % (self.name, origin, self.env.now))
            print_resource_info(self.resource)
            # simple resource monitoring
            # monitor_res(self.name, self.resource, self.data_res)

def get_component(env, params):
    component = dict(
        server=Server
        )
    return component[params['type']](env, params)
    
def parse_components(env, components_list):
    components = {}
    for comp_params in components_list:
        components[comp_params['name']] = get_component(env, comp_params)
    return components