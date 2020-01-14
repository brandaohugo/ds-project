from datetime import datetime
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Events data preparation & visualisation

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

def create_event_count_figure(data):
        sns.set(style="whitegrid")
        ax = sns.barplot(x="type", y="count", data=data)
        bytes_image = io.BytesIO()
        plt.savefig(bytes_image, format='png')
        bytes_image.seek(0)
        return bytes_image


'''TODO: visualise resource usage (queues)
sim_time = pd.DataFrame(np.arange(sim_params['settings']['sim_time'])).rename(columns={0:'timestep'}) # change this time to simulation time

sim_merge = sim_time.merge(sim_data, how='left', left_on='timestep', right_on='time').fillna(0)

# make event counts dataframe

event_counts.index.name = 'timestep'

event_counts.reset_index(inplace=True)

# make queue dataframe

event_queue = sim_merge[['timestep','queue']]

def create_queue_figure():
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1) 
        xs = event_queue['timestep']
        ys = event_queue['queue']
        axis.plot(xs, ys)
        return fig

# make figure

def create_event_figure():
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1) 
        xs = event_counts['timestep']
        ys = event_counts['count']
        axis.plot(xs, ys)
        return fig
'''