import simpy

class Server(object):
	def __init__(self, env):
		
		self.env = env
		
		# start the idle process everytime server object is instantiated
		
		self.action = env.process(self.idle())
		
	def idle(self):
		while True:
			
			# Server is idle for a while
			
			print('Server is idle at %d' % self.env.now)
			
			idle_time = 5

			yield self.env.timeout(idle_time)

			# Server starts processing transactions, waits for read_write() to be done

			print('Server received transaction request at %d' % self.env.now)

			transaction_num = 10

			yield self.env.process(self.read_write(transaction_num))
			
	def read_write(self, number_transactions):
		yield self.env.timeout(number_transactions)

env = simpy.Environment()

server_one = Server(env)

server_two = Server(env)

env.run(until=50)

"""
Simulation: Read/Write operations with multiple servers.

When instantiated server executes the idle() process, which waits for new transaction requests to be received. This waiting time is modelled by a idle time parameter. 

After this idle time period the server receives a request to process a transaction. It also receives a number of transactions to be processed at that time period.

The server then executes a read/write operation defined by the read_write() function. Once this read/write operation is finished the server is idle again and waits for the next transaction request.
"""