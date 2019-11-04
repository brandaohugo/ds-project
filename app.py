# library
import numpy as np 
import pandas as pd
import simpy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Simulation(db.Model):
    name = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

@app.route('/')
def page_title():
    return '<h1>ING Discrete Event Simulation</h1>'



if __name__ == '__main__':
    app.run()