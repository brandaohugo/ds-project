
from simpy import Resource, Process, FilterStore, Store
from utils import print_resource_info, print_stats, monitor_res, monitor_res2, patch_resource
from workloads import Job
from math import ceil
from statistics import mean
from functools import partial
import pdb


class Component:
    def __init__(self, env, cp_params):
        self.env = env
        self.in_pipe = Store(self.env, capacity=100) # TODO: define capacity in cp_params
        self.pending_jobs = {}
        self.queue_lengths = []
        self.response_times = []
        self.waiting_times = []
        self.num_cores = cp_params['num_cores']
        self.used_cores = 0
        self.core_speed = cp_params['core_speed']
        self.cores = Resource(self.env, capacity=self.num_cores)
        self.name = cp_params['name']
        self.jobs_completed = 0
        self.sim_components = None

        # monitor resources
        self.data_res = []
        self.monitor_res2 = partial(monitor_res2, self.data_res)
        patch_resource(self.cores, post=self.monitor_res2)

        # # monitor stores
        # self.data_store = []
        # self.monitor_store = partial(monitor_res2, self.data_store)
        # patch_resource(self.in_pipe, post=self.monitor_store)
    
    def run(self):
        # while True:
        #     # print(f'[{self.name}] Cores allocated : {self.used_cores} of {self.num_cores} at {self.env.now}')
        #     # print(f'[{self.name}] Queue size : {len(self.in_pipe.items)} at {self.env.now}')
        #     if len(self.in_pipe.items) < 1 or self.used_cores >= self.num_cores:
        #         yield self.env.timeout(1)
        #         continue
        #     self.used_cores += 1
        #     job = yield self.in_pipe.get()
        #     self.env.process(self.process_job(job))

        with self.cores.request() as req:
            # print(f'[{self.name}] Cores allocated : {self.used_cores} of {self.num_cores} at {self.env.now}')
            # print(f'[{self.name}] Queue size : {len(self.in_pipe.items)} at {self.env.now}')
            if len(self.in_pipe.items) < 1 or self.used_cores >= self.num_cores:
                yield req
                yield self.env.timeout(1)
                self.used_cores += 1
                job = yield self.in_pipe.get()
                self.env.process(self.process_job(job))

    def get_stats(self):
        stats = dict(
            avg_response_time= 9999 if len(self.response_times) == 0 else mean(self.response_times),
            queue_size=len(self.in_pipe.items)
        )
        
        return stats

    def receive_request(self, job):
        yield self.env.process(self.enqueue_job(job))

    def make_request(self, job, component):
        job.response_method = self.receive_response
        self.env.process(component.receive_request(job))
        yield self.env.timeout(1)
        self.pending_jobs[job.id] = job

    def receive_response(self, response_job):
        self.logger("received_response_for", response_job.id)
        if response_job.id in list(self.pending_jobs.keys()):
            self.env.process(self.enqueue_job(self.pending_jobs[response_job.id]))
            del self.pending_jobs[response_job.id]
            yield self.env.timeout(0)
            return "OK"
        return "INVALID JOB"

    def process_job(self,job):
        self.logger('processing', job.id)
        processing_time = ceil(job.size / self.core_speed) #TODO: make it stochastic
        yield self.env.timeout(processing_time)
        self.used_cores -= 1
        self.complete_job(job)
        
    def complete_job(self,job):
        self.logger("finished_processing", job.id)
        self.jobs_completed += 1
        response_time = self.env.now - job.stats[self.name]['arrival_time']
        self.response_times.append(response_time)

    def enqueue_job(self, job):
        job_stats = {}
        try:
            job_stats['arrival_time'] = self.env.now
            job_stats['processing_time'] = job.size / self.core_speed
            self.in_pipe.put(job)
            job.stats[self.name] = job_stats
            self.logger("received", job.id)
        except Exception as e:
            self.logger("error_at_enqueue", job.id)
        yield self.env.timeout(0)
        

class AuthServer(Component):
    def __init__(self, env, cp_params):
        Component.__init__(self, env, cp_params)
        self.db_server_name = cp_params['db_server_name']

    def receive_request(self, job):
        if job.action == 'AUTH':
            job.action = 'REQUEST_DATA'
            yield self.env.process(self.enqueue_job(job))
            
        else:
            yield self.env.timeout(0)
            self.logger("not_an_auth_job", job.id)

    def process_job(self,job):       
        if job.action == 'REQUEST_DATA':
            db_server = self.sim_components[self.db_server_name]
            job.respond_method = self.receive_response
            self.env.process(self.make_request(job, db_server))
            yield self.env.timeout(0) #TODO: another parameter?
            self.logger("resqueted_user_data_for", job.id)
        
        if job.action == 'VALIDATE_DATA':
            self.logger('processing', job.id)
            processing_time = ceil(job.size / self.core_speed) #TODO: make it stochastic
            yield self.env.timeout(processing_time)
            self.complete_job(job)
        self.used_cores -= 1
        

class DBServer(Component):
    def __init__(self, env, cp_params):
        Component.__init__(self, env, cp_params)

    def process_job(self, job):
        self.logger('querying_user_data_for', job.id)
        processing_time = ceil(job.size / self.core_speed) #TODO: make it stochastic
        yield self.env.timeout(processing_time)
        self.logger("finished_querying_user_data", job.id)
        job.action='VALIDATE_DATA'
        self.env.process(job.respond_method(job))
        self.logger("provided_user_data_for", job.id)
        self.used_cores -= 1
        self.jobs_completed += 1


class LoadBalancer(Component):
    def __init__(self, env, cp_params):
        Component.__init__(self, env, cp_params)
        self.servers_names = cp_params['servers']
        self.servers_stats = {}

    def process_job(self, job):
        self.logger("choosing_server_for", job.id)
        self.update_servers_stats()
        fastest_server = self.get_fastest_server(self.servers_stats)
        if job.action == 'AUTH':
            self.env.process(fastest_server.receive_request(job))
        self.used_cores -= 1
        self.complete_job(job)
        yield self.env.timeout(0)


    def get_fastest_server(self, stats):
        shortest_response_time = 9999999999
        fastest_server = None
        for server_name in self.servers_stats.keys():
            servers_stats = self.servers_stats[server_name]
            estimated_time = servers_stats['avg_response_time'] * servers_stats['queue_size']
            if estimated_time < shortest_response_time:
                shortest_response_time = estimated_time
                fastest_server = self.sim_components[server_name]
        return fastest_server


    def update_servers_stats(self):
        for server_name in self.servers_names:
            server_component = self.sim_components[server_name]
            self.servers_stats[server_name] = server_component.get_stats()
        self.env.timeout(0)
        return self.servers_stats 


def get_component(env, params):
    component = dict(
        auth_server=AuthServer,
        db_server=DBServer,
        load_balancer=LoadBalancer
    )
    return component[params['type']](env, params)
    
def parse_components(env, components_list):
    components = {}
    for comp_params in components_list:
        components[comp_params['name']] = get_component(env, comp_params)
        env.process(components[comp_params['name']].run())
    for name in components.keys():
        components[name].sim_components = components
    return components