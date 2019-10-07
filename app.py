# lubrary
import streamlit as st
import numpy as np 
import pandas as pd
import simpy

# page title
st.title('ING Discrete Event Simulator')

# creating a table
st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

# title
st.write('### Example plot')

# line plot data
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

# adding line plot
st.line_chart(chart_data)