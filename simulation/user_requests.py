"""
User requests simulation

PROCESS_TIME: Time it takes to process a transaction.
SIM_TIME: Time for which simulation will run.
GEN_INTER: New user generation time interval.
PAYLOAD_SIZE: User request processing load size in mb.
PROCESS_SPEED: Server payload processing speed in mb/second.
Number of concurrent users that can access servers.
"""

from pprint import pprint
import random
import itertools
import simpy

# PARAMETERS
SIM_TIME = 100
GEN_INTER = [0, 10]
PAYLOAD_SIZE = [1, 1000]
PROCESS_SPEED = 20
CONC_USERS = 4


def user(name, env, server):

	pprint('User %s requesting server at time %d' % (name, env.now))

	print_stats(server)  # Print server object statistics

	with server.request() as req:

		yield req

    """Job time computed as a function of payload size and 
    processing speed of the server."""

    job_time = random.randint(*PAYLOAD_SIZE) / PROCESS_SPEED

    yield env.timeout(job_time)  # Processing of the resources takes time.

    pprint('Server finished processing User %s request at %d with job_time = %d seconds.' % (
        name, env.now, job_time))

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

env = simpy.Environment()  # Define simpy simulation environment

server = simpy.Resource(env, CONC_USERS)  # Define server resource object

env.process(user_generator(env, server))  # Define user generator process

env.run(until=SIM_TIME)  # run simulation until the specified simulation time