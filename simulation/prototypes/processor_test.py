# process stdout from main.py and return DES dataframe
import pandas as pd
import re

# regex library

with open('sim_stdout_test.txt', 'r') as f:
    data = [line.lower() for line in f]



# file = open('sim_stdout_test.txt', 'r')


# print(data[1][2])