import simpy

def main():
    env = simpy.Environment()
    env.process(login_server(env))
    env.run(until=300)
    print("Simulation complete")

login_times=[]
transaction_times=[]

def login_server(env):
    while True:
        login_times.append('Login at %d' % (env.now))
        yield env.timeout(30)

        transaction_times.append('Transaction at %d' % (env.now))
        yield env.timeout(20)

        print(login_times)
        print(transaction_times)

if __name__ == '__main__':
    main()