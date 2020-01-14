import os
from flask import ( Flask, render_template )
from . import db, auth, processor, cases
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pandas as pd

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'datasim.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    app.register_blueprint(auth.bp)

    '''TODO: plot resource usage 
    @app.route('/eventplot.png')
    def make_event_plot():
        fig = processor.create_event_figure()
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')

    @app.route('/queueplot.png')
    def make_queue_plot():
        fig = processor.create_queue_figure()
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')
    '''


    @app.route('/eventcount.png')
    def get_event_count_fig():
        #TODO: enable user to select different sim runs for plotting
        log_filename = 'datasim/log/event_20200114184808.txt'
        event_data = processor.extract_events_count(pd.read_csv(log_filename))
        bytes_obj = processor.create_event_count_figure(event_data)
        return Response(bytes_obj.getvalue(), mimetype='image/png')

    @app.route('/')
    @auth.login_required
    def index():
	    return render_template(
            "index.html", 
            time=cases.sim_params_1['settings']['sim_time'],
            components=len(cases.sim_params_1['components']), 
            workloads=len(cases.sim_params_1['workloads'])
        )


    @app.route('/api/v1/simulations/', methods=['GET','POST'])
    def simulations():
        return "Simulations"        

    return app