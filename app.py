# library
import numpy as np 
import pandas as pd
import simpy
from flask import Flask

app = Flask(__name__)

@app.route('/')
def page_title():
    return '<h1>ING Discrete Event Simulation</h1>'

if __name__ == '__main__':
    app.run()