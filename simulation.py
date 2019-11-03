import simpy
import pandas as pd
import numpy as np

# SIMULATION CODE # 
def main():
    env = simpy.Environment()
    env.process(login_server(env))
    env.run(until=300)
    print("Simulation complete")

login_times=[]
transaction_times=[]

def login_server(env):
    while True:
        login_times.append('Login at simulation time %d' % (env.now))
        yield env.timeout(30)

        transaction_times.append('Transaction at simulation time %d' % (env.now))
        yield env.timeout(20)

        print(login_times)
        print(transaction_times)

if __name__ == '__main__':
    main()