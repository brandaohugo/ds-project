from datetime import datetime
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
import io
import os
import random

def extract_events_count(events_df):
        re_1 = "(^<[a-z]* \'[a-z]*\.[a-z]*\.)"
        re_2 = "(\'>)"
        re_3 = "([a-z]*\.)"
        df_1 = events_df.replace(to_replace =re_1, value = '', regex = True)
        df_2 = df_1.replace(to_replace =re_2, value = '', regex = True) 
        events_df = df_2.replace(to_replace =re_3, value = '', regex = True)
        event_count = pd.DataFrame(events_df['type'].value_counts()).rename(columns={'type':'count'})
        event_count['type'] = event_count.index
        return event_count

def prepare_plot(filename, target1, target2):
        df = pd.read_csv(filename)
        obj_type = random.choice(df['name'].unique())
        df_obj_type = df.loc[df['name'] == obj_type]
        list1 = df_obj_type[target1].to_list()
        list2 = df_obj_type[target2].to_list()
        return list1, list2