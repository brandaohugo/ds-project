import os
from flask import ( Flask, render_template )
from . import db, auth, processor, helpers
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


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
        
    @app.route('/')
    @auth.login_required
    def index():
	    return render_template("index.html", time=helpers.SIM_TIME,
        idle=helpers.IDLE_TIME, servers=helpers.SERVER_NUM,
        proc_time=helpers.PROCESSING_TIME, proc_cap=helpers.PROCESSING_CAPACITY)


    @app.route('/api/v1/simulations/', methods=['GET','POST'])
    def simulations():
        return "Simulations"        

    return app



