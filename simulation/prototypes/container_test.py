import itertools
import random
import simpy

# SIMULATION VARIABLES
SIM_TIME = 1000 
CONC_USERS = 3 # Number of concurrent users per server.
HPC_CAP = 1000 # Total processing capacity of HPC Cluster.
BUF_CAP = 0.2 # Buffering capacity of remote server has to be between 0 and 1.
TRANSACTION_REQ = [1, 1000] # Range of transactions to process.
PROC_SPEED = 15 # Transaction processing speed per second.
GEN_INTER = [5, 45] # Interval in seconds between which new users can be generated.


class Cluster:
    def __init__(self, env):
        self.server = simpy.Resource(env, CONC_USERS)
        self.cluster_capacity = simpy.Container(env, init= HPC_CAP, capacity=HPC_CAP)
        self.system_monitor = env.process(self.monitor(env))

    def monitor(self, env):
        while True:
            if self.cluster_capacity.level < 100:
                print("Reached minimum capacity at %s, deploying a remote server for back-up." % env.now)
                env.process(deploy_remote(env, self))

def deploy_remote(env, hpc_cluster):
    yield env.timeout(10)
    
    print('remote server deployed at %s' % env.now)

    cluster_remaining_capacity = Cluster.cluster_capacity.capacity - Cluster.cluster_capacity.level

    remote_buffer_capacity = BUF_CAP * cluster_capacity

    yield Cluster.cluster_capacity.put(remote_buffer_capacity)

def user(name, env, hpc_cluster):
    transactions_requested = random.randint(*TRANSACTION_REQ)

    print('User %s requested %d transactions at time: %d' % (name, transactions_requested, env.now))

    with Cluster.server.request() as req:
        yield req

        yield Cluster.cluster_capacity.get(transactions_requested)

        yield env.timeout(transactions_requested / PROC_SPEED) 
        print('User %s has finished processing transactions at %s' % (name, env.now))


def user_generator(env, hpc_cluster):
    """Generate new users """
    for i in itertools.count():
        yield env.timeout(random.randint(*GEN_INTER))
        env.process(user('User %d' % i, env, hpc_cluster))


env = simpy.Environment()
hpc_cluster = Cluster(env)
user_gen = env.process(user_generator(env, hpc_cluster))
env.run(until=SIM_TIME)


def user(name, env, cluster, server): #
    """A user arrives at the hpc cluster for processing his transaction.

    It requests one of the hpc cluster's servers and tries to process the 
    desired amount of transactions on it. If the hpc cluster's capacity is
    depleted, the user has to wait for a remote server to be deployed.
    """
    transactions_requested = random.randint(*TRANSACTION_REQ)
    print('%s making request at %.1f of %d transactions' % (name, transactions_requested, env.now))
    
    with server.request() as req:
        start = env.now

        # Print the remaining server processing capacity
        print('the remaining server capacity is %d' % cluster.level)

        # Request transactions to be processed at an available server.
        yield req

        # Process required amount of transactions at the available server.
        yield cluster.get(transactions_requested)
        print('%s finished processing transactions in %.1f seconds.' % (name, env.now - start))

        # The transaction processing depends on server processing speed
        yield env.timeout(transactions_requested / PROC_SPEED)

        

def user_generator(env, cluster, server):
    """Generate new cars that arrive at the gas station."""
    for i in itertools.count():
        yield env.timeout(random.randint(*GEN_INTER))
        env.process(user('User %d' % i, env, cluster, server))

env = simpy.Environment()
server = simpy.Resource(env, 2)
env.process(user_generator(env, server))
env.run(until=SIM_TIME)