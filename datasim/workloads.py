from simpy import Process
from utils import random_number
import pandas as pd
from datetime import datetime

class Job:
    def __init__(self, job_id, job_size,job_action):
        self.id = job_id
        self.status = 'new'
        self.size = job_size
        self.stats = {}
        self.action = job_action
        self.respond_method = None

class Workload(Process):
    def __init__(self, env, components, wl_params):
        self.env = env
        self.components = components
        self.wl_params = wl_params
        self.jobs = []
        self.job_action = wl_params['job_action']
        self.last_job_id = None
        self.name = self.wl_params['name']
        self.start_time = self.wl_params['start_time']
        self.end_time = self.wl_params['end_time']
        self.target_name = self.wl_params['target']['name']
        self.js_params = wl_params['job_size']
        self.ia_params = wl_params['interarrival']
        self.vl_params = wl_params['volume']
        self.jobs = pd.DataFrame(columns=['id','time'])
        self.generate()
        # Process(self.env,self.generate())
    
    def generate_job(self):
        job_id = self.last_job_id + 1 if self.last_job_id is not None else 0
        job_name = self.name + "_" + str(job_id)
        job_size = 1
        job_action = self.job_action
        job = Job(job_name,job_size,job_action)
        self.last_job_id = job_id
        return job
        

    def send_job(self,job,time):
        yield self.env.timeout(time)
        try:
            # create new job in the workload
            
            # send job to target component
            target = self.components[self.target_name]
            self.env.process(target.receive_request(job))
            
            print(f'[workload] Job {job.id} sent to {target.name} at {self.env.now}')
        except Exception as e:
            print(f'[workload] Error generating job {job_id} from workload {self.name} at {self.env.now}: {str(e)}')

    def generate(self):
        number_of_request = int(random_number(self.vl_params))
        for i in range(number_of_request):
            time = random_number(self.ia_params)
            job = self.generate_job()
            self.jobs = self.jobs.append({'id': job.id, 'time': time}, ignore_index=True)
            self.env.process(self.send_job(job,time))
        self.jobs.to_csv('log/workload_' + datetime.now().strftime("%Y%m%d%H%M%S") + '.csv')
        

    
def parse_workloads(env, components, workloads_list):
    workloads = {}
    for wl_params in workloads_list:
        workloads[wl_params['name']] = Workload(env, components, wl_params)
    return workloads
