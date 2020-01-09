# process stdout from main.py and return DES dataframe
import pandas as pd
import re

# regex library
re_dict = {
    'server': 'server',
    'test': 'hello'
}

test_string = 'server how are you doing?'

with open('sim_stdout_test.txt', 'r') as f:
    data = [line.lower() for line in f]

for i in re_dict:
    print(re_dict[i])

print(re_dict['server'])

result = re.match(re_dict['server'], test_string)

if result:
    print('Succesful')
else:
    print('Unsuccesful')
# file = open('sim_stdout_test.txt', 'r')


# print(data[1][2])