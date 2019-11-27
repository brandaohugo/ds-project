import simpy
import itertools
import random
from pprint import pprint 

# SIMULATION VARIABLES

PROCESS_TIME = 10 # Time it takes to process a transaction.
SIM_TIME = 100 # Time for which simulation will run.
GEN_INTER = [0, 10] # New user generation time interval.
PAYLOAD_SIZE = [1, 1000] # User request processing load size in mb.
PROCESS_SPEED = 20 # Server payload processing speed in mb/second.
CONC_USERS = 4 # Number of concurrent users that can access servers.

def user(name, env, server):

	pprint('User %s requesting server at time %d' % (name, env.now))
	
	print_stats(server) # Print server object statistics
	
	with server.request() as req:
		
		yield req
		
		"""Job time computed as a function of payload size and 
		processing speed of the server."""

		job_time = random.randint(*PAYLOAD_SIZE) / PROCESS_SPEED 

		yield env.timeout(job_time) # Processing of the resources takes time.

		pprint('Server finished processing User %s request at %d with job_time = %d seconds.' % (name, env.now, job_time))
		
		print_stats(server)
    	
def user_generator(env, server):
    """Iteratively generate new users, within a random time-interval
    specified within GEN_INTER."""
    
    for i in itertools.count(): 

        yield env.timeout(random.randint(*GEN_INTER))

        env.process(user(i, env, server))


def print_stats(server):
	"""Prints the current state of the server resource object."""
	print('%d of %d slots are allocated.' % (server.count, server.capacity))
	print(' Users:', server.users)
	print(' Queued events:', server.queue)

# SIMULATION ENVIRONMENT

env = simpy.Environment() # Define simpy simulation environment

server = simpy.Resource(env, CONC_USERS) # Define server resource object

env.process(user_generator(env, server)) # Define user generator process

env.run(until=SIM_TIME) # run simulation until the specified simulation time

"""
# SIMULATION NOTES

- Changing number of CONC_USERS can result in queues forming.

- Varying the PROCESS_TIME will directly impact when users are served.

- Varying PROCESS_SPEED of server also directly impacts performance.

- Varying PAYLOAD_SIZE also has an effect as it will change the 
  overall job_time of the transaction job, again this is dependent on
  processing speed.
-

# THINGS TO DO NEXT

- Model other behaviour such as read/write operations in a database.

- Explore adding additional servers/modules to the simulation.

- Find ways to pipe simulation output into a JSON or CSV/Pandas Df.
"""