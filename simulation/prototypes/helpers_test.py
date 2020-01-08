import simpy
import random

def generate_error(env, affected_server):
    ''' Introduce Internal Server Error (500)'''
    yield env.timeout(25)
    affected_server.action.interrupt()

def generate_time_out(env, affected_server):
    '''Introduce Temporary Server Error (501)'''
    time = random.randint(0, 25)
    yield env.timeout(time)
    affected_server.action.interrupt()

def random_interrupt(env, affected_server):
    try:
        yield env.timeout(random.randint(20, 40))
        affected_server.action.interrupt()
        print(f'Interruption of test done at {env.now}')
    except simpy.Interrupt as i:
        print(f'Environment interrupted at {env.now}! msg: {i.cause}')

def resource_user(env, resource):

    while True:
        request = resource.request()
        yield request
        print(f'requested at {env.now}')
        yield env.timeout(2)
        print(f'released at {env.now}')
        resource.release(request)

# def server(env, channel):
#     yield env.timeout(66)
#     if channel.items:
#         msg = yield channel.get()