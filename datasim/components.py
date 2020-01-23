
from simpy import Resource, Process, FilterStore, Store
from .utils import random_number
from .workloads import Job
from math import ceil
from statistics import mean



class Component:
    def __init__(self, env, cp_params):
        self.env = env
        self.in_pipe = Store(self.env) # TODO: define capacity in cp_params
        self.pending_jobs = {}
        self.response_times = []
        self.interarrivals = []
        self.queue_times = []
        self.num_cores = cp_params['num_cores']
        self.used_cores = 0
        self.core_speed = random_number(cp_params['core_speed'])
        self.cores = Resource(self.num_cores)
        self.name = cp_params['name']
        self.jobs_completed = 0
        self.sim_components = None
        self.data_res = []
        self.idle_time = 0
        self.time_last_arrival = None

    def __str__(self):
        return f'[{self.name}]'

    def logger(self, message, job_id):
        #print(f'{self} {message} {job_id} time_{self.env.now}')
        pass

    def run(self):

        while True:
            if len(self.in_pipe.items) < 1 or self.used_cores >= self.num_cores:
                yield self.env.timeout(1)
                self.idle_time += 1
                continue
            self.used_cores += 1
            job = yield self.in_pipe.get()
            job.stats[self.name]
            enqueue_time = job.stats[self.name]['enqueue_time']
            queue_time = self.env.now - enqueue_time
            self.queue_times.append(queue_time)
            self.env.process(self.process_job(job))

    def get_stats(self):
        stats = dict(
            avg_response_time =  9999 if len(self.response_times) == 0 else mean(self.response_times),
            avg_queue_time = 9999 if len(self.queue_times) == 0 else mean(self.queue_times),
            avg_interarrival_time = 9999 if len(self.interarrivals) == 0 else mean(self.interarrivals),
            queue_size=len(self.in_pipe.items),
            idle_time = self.idle_time,
            used_cores = self.used_cores,
            jobs_completed = self.jobs_completed,
            name = self.name,
            sim_time = self.env.now
        )
        
        return stats

    def init_job_stats(self, job):
        job.stats[self.name] = {}
        job.stats[self.name]['arrival_time'] = self.env.now
        if self.time_last_arrival is None:
            self.time_last_arrival = self.env.now
        else:
            interarrival = self.env.now - self.time_last_arrival 
            self.interarrivals.append(interarrival)

    def receive_request(self, job):
        self.init_job_stats(job)
        self.logger("received", job.id)
        yield self.env.process(self.enqueue_job(job))
        
    def make_request(self, job, component):
        job.response_method = self.receive_response
        self.env.process(component.receive_request(job))
        yield self.env.timeout(0) # NOTE: make request delay
        self.pending_jobs[job.id] = job

    def receive_response(self, response_job, type_of_response='response'):
        self.logger(f'received_{type_of_response}_for', response_job.id)
        if response_job.id in list(self.pending_jobs.keys()):
            self.env.process(self.enqueue_job(self.pending_jobs[response_job.id]))
            del self.pending_jobs[response_job.id]
            yield self.env.timeout(0)
            return "OK"
        return "INVALID JOB"

    def process_job(self,job):
        self.logger('processing', job.id)
        processing_time = ceil(job.size / self.core_speed)
        yield self.env.timeout(processing_time)
        self.used_cores -= 1
        self.complete_job(job)
        
    def complete_job(self,job):
        job.stats[self.name]['finish_time'] = self.env.now
        self.jobs_completed += 1
        response_time = self.env.now - job.stats[self.name]['arrival_time']
        self.response_times.append(response_time)

    def enqueue_job(self, job):
        job_stats = {}
        try:
            job_stats['arrival_time'] = self.env.now
            job_stats['estimated_processing_time'] = job.size / self.core_speed
            job_stats['enqueue_time'] = self.env.now
            yield self.in_pipe.put(job)
            job.stats[self.name] = job_stats
        except Exception as e:
            self.logger("error_at_enqueue", job.id)
        # yield self.env.timeout(0)
        

class AuthServer(Component):
    def __init__(self, env, cp_params):
        Component.__init__(self, env, cp_params)
        self.db_server_name = cp_params['db_server_name']
        self.load_balancer_name = cp_params['load_balancer']

    def receive_request(self, job):
        self.init_job_stats(job)
        if job.action == 'auth':
            job.action = 'request_data'
            yield self.env.process(self.enqueue_job(job))
        else:
            yield self.env.timeout(0)
            self.logger("not_an_auth_job", job.id)
        self.logger("received", job.id)

    def process_job(self,job):    
        if job.action == 'request_data':
            self.logger("resqueting_data_for", job.id)
            yield self.env.timeout(1) # making request processing delay
            db_server = self.sim_components[self.db_server_name]
            job.response_method = self.receive_response
            self.env.process(self.make_request(job, db_server))
            self.logger("finished_resqueting_data_for", job.id)
            
            
        
        if job.action == 'auth_data':
            self.logger('authenticating', job.id)
            processing_time = ceil(job.size / self.core_speed)
            yield self.env.timeout(processing_time)
            self.logger('finished_authenticating', job.id)
            job.action='auth_response'
            self.env.process(self.sim_components[self.load_balancer_name].receive_response(job,type_of_response='auth_response'))
            self.complete_job(job)
            self.logger("replied_auth_reponse_for", job.id)
            

        self.used_cores -= 1
        

class DBServer(Component):
    def __init__(self, env, cp_params):
        Component.__init__(self, env, cp_params)

    def process_job(self, job):
        self.logger('querying_user_data_for', job.id)
        processing_time = ceil(job.size / self.core_speed)
        yield self.env.timeout(processing_time)
        self.logger("finished_querying_user_data_for", job.id)
        job.action='auth_data'
        self.env.process(job.response_method(job,type_of_response='user_data'))
        self.complete_job(job)
        self.logger("replied_user_data_for", job.id)
        self.used_cores -= 1


class LoadBalancer(Component):
    def __init__(self, env, cp_params):
        Component.__init__(self, env, cp_params)
        self.servers_names = cp_params['servers']
        self.servers_stats = {}

    def process_job(self, job):
        self.update_servers_stats()
        fastest_server = self.get_fastest_server(self.servers_stats)
        job.response_method = self.receive_response
        if job.action == 'auth':
            self.env.process(self.make_request(job, fastest_server))
            self.logger(f'forwarded_to_{fastest_server.name}', job.id)
            yield self.env.timeout(0)
        
        if job.action == 'auth_response':
            self.logger('completed', job.id)
            yield self.env.timeout(0)
            self.complete_job(job)

        self.used_cores -= 1
        

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