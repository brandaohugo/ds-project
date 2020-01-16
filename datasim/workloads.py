import itertools
from utils import random_number
from simpy import Process
from helpers import random_uniform

class Job:
    def __init__(self, job_id, job_size):
        self.id = job_id
        self.status = STATUS_NEW
        self.size = job_size
        self.stats = {}
        self.action = 'AUTH'
        self.respond_method = None

class Workload(Process):
    def __init__(self, env, components, wl_params):
        self.env = env
        self.components = components
        self.wl_params = wl_params
        self.jobs = []
        self.last_job_id = None
        self.name = self.wl_params['name']
        self.start_time = self.wl_params['start_time']
        self.end_time = self.wl_params['end_time']
        self.target_name = self.wl_params['target']['name']
        self.js_params = wl_params['job_size']
        self.ia_params = wl_params['interarrival']
        self.vl_params = wl_params['volume']
        Process(self.env,self.generate())
    def generate(self):
        while self.env.now >= self.start_time and self.env.now <= self.end_time:    
            # interarrival time
            interarrival = int(random_uniform(self.ia_params)) #TODO: get specified interarrival distribution
            yield self.env.timeout(interarrival)
            for i in range(int(random_uniform(self.vl_params))):
                try:
                    # create new job in the workload
                    last_job_id = self.last_job_id + 1 if self.last_job_id is not None else 0
                    job_name = self.name + "_" + str(last_job_id)
                    job_size = int(random_uniform(self.js_params))
                    job = Job(job_name,job_size)

                    # send job to target component
                    target = self.components[self.target_name]
                    self.env.process(target.authenticate_user(job))
                    self.last_job_id = last_job_id
                    print(f'[workload] Job {job.id} sent to {target.name} at {self.env.now}')
                except Exception as e:
                    print(f'[workload] Error generating job {last_job_id} from workload {self.name} at {self.env.now}: {str(e)}')


    
def parse_workloads(env, components, workloads_list):
    workloads = {}
    for wl_params in workloads_list:
        workloads[wl_params['name']] = Workload(env, components, wl_params)
    return workloads
