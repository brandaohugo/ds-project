from pprint import pprint
import random
import itertools
import simpy

# Class defining users that make requests.

class User:
	
	def __init__(self, env, name, server):
		self.env = env
		self.name = name
		self.server = server

	def make_request(self):
		
		pprint('User %s requesting server at time %d' % (self.name, self.env.now))
		
		print_stats(self.server)  # Print server object statistics
		
		with self.server.request() as req:
			yield req
			
			"""Job time computed as a function of payload size and 
			processing speed of the server."""
			
			job_time = random.randint(*PAYLOAD_SIZE) / PROCESS_SPEED
			
			yield self.env.timeout(job_time)  # Processing of the resources takes time.
			
			pprint('Server finished processing User %s request at %d with job_time = %d seconds.' % (self.name, self.env.now, job_time))
			
			print_stats(self.server)

# Class defining servers that handle requests (extends simpy.Resource)

class Server(simpy.Resource):
	
	def __init__(self, env, capacity, name):
		self.env = env
		self.name = name
		
	def print_stats(self):
		print('%d of %d slots are allocated.' % (self.count, self.capacity))
		print(' Users:', self.users)
		print(' Queued events:', self.queue)

# Class defining a user_generator

class UserGenerator:
	
	def __init__(self, env, user, user_number, server):
		self.env = env
		self.user = user
		self.user_number = user_number
		self.server = server
		
	"""Iteratively generate new users, within a random time-interval
	specified within GEN_INTER."""
	
	def make_users(self, GEN_INTER):
		
		for i in range(self.user_number):
			
			yield self.env.timeout(random.randint(*GEN_INTER))
			
			env.process(self.user(i, self.env, self.server))
