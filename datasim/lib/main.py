
"""
Simulation: Read/Write operations with multiple servers.

When instantiated server executes the idle() process, which waits for new transaction requests to be received. This waiting time is modelled by a idle time parameter. 

After this idle time period the server receives a request to process a transaction. It also receives a number of transactions to be processed at that time period.

The server then executes a read/write operation defined by the read_write() function. Once this read/write operation is finished the server is idle again and waits for the next transaction request.

Setup:
Using context manager to pipe all standard output to a file.

Usage of helpers.py for functions used within simulation.
"""

import io
import simpy
from contextlib import redirect_stdout
from helpers import *
# from simulation.working.helpers import *

# use context manager to capture print outputs
with open('log/sim_stdout.txt', 'w') as f:
	with redirect_stdout(f):

		# Server object
		class Server(object):
			def __init__(self, env, name, resource):
				
				self.env = env
				
				# start the idle process everytime server object is instantiated
				
				self.action = env.process(self.idle())

				self.name = name

				self.resource = resource

			def idle(self):
				while True:
					
					# Server is idle for a while
					
					print('Server_%s is idle at %d' % (self.name, self.env.now))

					yield self.env.timeout(IDLE_TIME)

					# Server starts processing transactions, waits for read_write() to be done

					print('Server_%s received transaction request at %d' % (self.name, self.env.now))

					try:
						yield self.env.process(self.read_write(PROCESSING_TIME))
					except simpy.Interrupt:
						print('Server_%s was interrupted at %d, aborting read_write operation.' % (self.name, self.env.now))

			def read_write(self, processing_time):
				
				# print resource statistics
				print_stats(self.resource)

				# make request to resource
				with self.resource.request() as req:
					yield req

					# processing a transaction takes time
					yield self.env.timeout(processing_time)
					
					print('Server_%s finished read_write operation at %d.' % (self.name, self.env.now))

		# Introduce new servers into the simulation (creates new global objects)
		def generate_server(number):
			for i in range(number):
				server_name = str(i)
				globals()['server_object{}'.format(i)] = Server(env, server_name, processing_res)

		# define environment
		env = simpy.Environment()

		# generate resources
		processing_res = simpy.Resource(env, capacity=PROCESSING_CAPACITY)

		# data list to monitor resources
		data =[]

		monitor = partial(monitor, data)
		patch_resource(processing_res, post=monitor)


		# generate servers
		generate_server(SERVER_NUM)

		# introduce an error process
		env.process(generate_error(env, server_object0))

		# run simulation
		env.run(until=SIM_TIME)

		# monitor results: creates txt-file
		df = create_df(data)