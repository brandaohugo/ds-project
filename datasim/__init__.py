import os
from flask import ( Flask, render_template, request, Response, redirect, url_for, flash )
from . import db, auth, processor, cases
import io
import random
import pandas as pd
from werkzeug.utils import secure_filename
from io import StringIO

ALLOWED_EXTENSIONS = {'txt', 'csv'}

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
        log_filename = 'datasim/log/event_20200115185434.txt'
        event_data = processor.extract_events_count(pd.read_csv(log_filename))
        event_count = event_data['count']
        
        bytes_obj = processor.create_event_count_figure(event_data)
        print(event_data)
        return Response(bytes_obj.getvalue(), mimetype='image/png')

    def allowed_file(filename):
        if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            return True
        else:
            return False

    def bytes_todf(file):
        bytes_data = file.read()
        s=str(bytes_data,'utf-8')
        data = StringIO(s) 
        df=pd.read_csv(data)
        
    # web application routes
    @app.route("/")
    @auth.login_required
    def index():
        return render_template("index.html", section = 'about')

    @app.route("/about")
    @auth.login_required
    def about():
        return render_template("index.html", section = 'about')
    
    @app.route("/visualiser", methods=['POST','GET'])
    @auth.login_required
    def visualiser():
        if request.method == 'POST':
            
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            
            if file and allowed_file(file.filename):
                # Process upload 
                df = bytes_todf(file)
                event_data = processor.extract_events_count(df)
                res_legend = 'Resource Queue'
                res_values = event_data['count']
                res_labels = event_data['type']
                return render_template("index.html", section='visualiser', res_values=res_values, res_labels=res_labels)

            # other functions used previously to parse data:    
            # res_labels, res_values = processor.prepare_plot('datasim/log/res_20200115185434.
            # event_data = processor.extract_events_count(pd.read_csv(log_filename))
            
        return render_template("index.html", section='visualiser')

    @app.route("/parameters")
    @auth.login_required
    def parameters():
        return render_template("index.html", section = 'parameters')

    @app.route("/documentation")
    @auth.login_required
    def documentation():
        return render_template("index.html", section = 'documentation')

    @app.route('/api/v1/simulations/', methods=['GET','POST'])
    def simulations():
        return "Simulations"    

    @app.route('/testing')
    def testing():
        #TODO: Add real data from simulation and pass it to charts
        legend = 'Monthly Data'
        labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
        values = [10, 9, 8, 7, 6, 4, 7, 8]
        return render_template("testing.html", time=cases.sim_params_1['settings']['sim_time'], components=len(cases.sim_params_1['components']), workloads=len(cases.sim_params_1['workloads']),values=values, labels=labels, legend=legend)
    

    return app