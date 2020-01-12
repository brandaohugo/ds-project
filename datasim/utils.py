from contextlib import redirect_stdout

def log_event(log_file_name, message):
    with open(log_file_name, 'a') as f:
        with redirect_stdout(f):
            print(message)

def print_stats(resource,log_filenmae):
    log_event(log_filename, f'{resource.count} of {resource.capacity} are allocated')
    log_event(log_filename, f'Users: {resource.users}')
    log_event(log_filename, f'Queued events: {resource.queue}')

def print_resource_info(resource):
    print(f'Count: {resource.count}, Capacity: {resource.capacity} ,Users: {len(resource.users)}, Queue: {len(resource.queue)}')