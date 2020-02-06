import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('test.csv')
df = df.drop(columns=[df.columns[0]])
kwargs = {'range': [0,1000]}
df.plot.hist(bins=100,**kwargs)
plt.savefig('test.png')