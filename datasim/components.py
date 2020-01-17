
from simpy import Resource, Process, FilterStore, Store
from utils import print_resource_info, print_stats, monitor_res, monitor_res2, patch_resource
from workloads import Job
from math import ceil
from functools import partial


class Component:
    def __init__(self, env, cp_params):
        self.env = env
        self.in_pipe = Store(self.env) # TODO: define capacity in cp_params
        self.pending_jobs = {}
        self.queue_lengths = []
        self.response_times = []
        self.waiting_times = []
        self.num_cores = cp_params['num_cores']
        self.used_cores = 0
        self.core_speed = cp_params['core_speed']
        self.cores = Resource(self.num_cores)
        self.name = cp_params['name']
        self.jobs_completed = 0
        self.sim_components = None
    
    def run(self):
        while True:
            # print(f'[{self.name}] Cores allocated : {self.used_cores} of {self.num_cores} at {self.env.now}')
            # print(f'[{self.name}] Queue size : {len(self.in_pipe.items)} at {self.env.now}')
            if len(self.in_pipe.items) < 1 or self.used_cores >= self.num_cores:
                yield self.env.timeout(1)
                continue
            self.used_cores += 1
            job = yield self.in_pipe.get()
            self.env.process(self.process_job(job))

    def receive_request(self, job):
        yield self.env.process(self.enqueue_job(job))

    def make_request(self, job, component):
        job.response_method = self.receive_response
        self.env.process(component.receive_request(job))
        yield self.env.timeout(1)
        self.pending_jobs[job.id] = job

    def receive_response(self, response_job):
        if response_job.name in list(self.pending_jobs.keys()):
            self.enqueue_job(self.pending_jobs[response_job.name])
            del self.pending_jobs[response_job.name]
        yield self.env.timeout(0)

    def process_job(self,job):
        processing_time = ceil(job.size / self.core_speed) #TODO: make it stochastic
        # print(f'[{self.name}] Processing job {job.id} at {self.env.now} estimated at {processing_time}')
        yield self.env.timeout(processing_time)
        print(f'[{self.name}] Finished processing job {job.id} at {self.env.now}')
        self.used_cores -= 1
        self.jobs_completed += 1
        print(f'[{self.name}] Finished {self.jobs_completed} jobs at {self.env.now}')
        
    def enqueue_job(self, job):
        job_stats = {}
        try:
            job_stats['arrival_time'] = self.env.now
            job_stats['processing_time'] = job.size / self.core_speed
            self.in_pipe.put(job)
            job.stats[self.name] = job_stats
            print(f'[{self.name}] Job {job.id} received at {self.env.now}')
        except Exception as e:
            print(f'[{self.name}] Error creating Job {job.id} at {self.env.now}: {str(e)}')
        yield self.env.timeout(0)
        

class Auth_Server(Component):
    def __init__(self, env, cp_params):
        Component.__init__(self, env, cp_params)
        self.db_server_name = cp_params['db_server_name']

    def authenticate_user(self, job):
        if job.action == 'AUTH':
            job.action = 'REQUEST_DATA'
            yield self.env.process(self.enqueue_job(job))
        else:
            yield self.env.timeout(0)
            print("not a valid authentication job")

    def process_job(self,job):       
        if job.action == 'REQUEST_DATA':
            db_server = self.sim_components[self.db_server_name]
            job.respond_method = self.receive_request
            self.env.process(self.make_request(job, db_server))
            yield self.env.timeout(1) #TODO: another parameter?
            print(f'[{self.name}] Requested user data for job {job.id} at {self.env.now}')
        
        if job.action == 'VALIDATE_DATA':
            processing_time = ceil(job.size / self.core_speed) #TODO: make it stochastic
            yield self.env.timeout(processing_time)
            print(f'[{self.name}] Finished processing job {job.id} at {self.env.now}')
            self.jobs_completed += 1
        self.used_cores -= 1
        

class DB_Server(Component):
    def __init__(self, env, cp_params):
        Component.__init__(self, env, cp_params)

    def process_job(self, job):
        processing_time = ceil(job.size / self.core_speed) #TODO: make it stochastic
        # print(f'[{self.name}] Processing job {job.id} at {self.env.now} estimated at {processing_time}')
        yield self.env.timeout(processing_time)
        print(f'[{self.name}] Finished processing job {job.id} at {self.env.now}')
        job.action='VALIDATE_DATA'
        yield self.env.process(job.respond_method(job))
        self.used_cores -= 1
        self.jobs_completed += 1



def get_component(env, params):
    component = dict(
        auth_server=Auth_Server,
        db_server=DB_Server
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