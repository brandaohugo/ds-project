import simpy

# Define Simulation Parameters
TRANSACTION_NUM = 10
IDLE_TIME = 5
SERVER_NUM = 3

# Server object
class Server(object):
	def __init__(self, env):
		
		self.env = env
		
		# start the idle process everytime server object is instantiated
		
		self.action = env.process(self.idle())
		
	def idle(self):
		while True:
			
			# Server is idle for a while
			
			print('Server is idle at %d' % self.env.now)

			yield self.env.timeout(IDLE_TIME)

			# Server starts processing transactions, waits for read_write() to be done

			print('Server received transaction request at %d' % self.env.now)

			yield self.env.process(self.read_write(TRANSACTION_NUM))
			
	def read_write(self, number_transactions):
		yield self.env.timeout(number_transactions)

# Introduce new servers into the simulation
def generate_server(number):
	for i in range(number):
		Server(env)

# define environment
env = simpy.Environment()

# generate servers
generate_server(SERVER_NUM)

env.run(until=100)

"""
Simulation: Read/Write operations with multiple servers.

When instantiated server executes the idle() process, which waits for new transaction requests to be received. This waiting time is modelled by a idle time parameter. 

After this idle time period the server receives a request to process a transaction. It also receives a number of transactions to be processed at that time period.

The server then executes a read/write operation defined by the read_write() function. Once this read/write operation is finished the server is idle again and waits for the next transaction request.
"""