# process stdout from main.py and return DES dataframeimport json
from datetime import datetime
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import json

sim_time = pd.DataFrame(np.arange(10000)).rename(columns={0:'timestep'}) # change this time to simulation time

log_filename = 'log/20200110105717.txt' # file to plot

log_columns = ['time','count','queue']

sim_data = pd.read_csv(log_filename)[log_columns]

sim_merge = sim_time.merge(sim_data, how='left', left_on='timestep', right_on='time').fillna(0)

# make event counts dataframe

event_counts = sim_merge.groupby(['timestep']).sum()[['count']]

event_counts.index.name = 'timestep'
event_counts.reset_index(inplace=True)

# make figure

def create_figure():
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1) 
        xs = event_counts['timestep']
        ys = event_counts['count']
        axis.plot(xs, ys)
        return fig





