import os
from flask import ( Flask, render_template, request, Response, redirect, url_for, flash )
from . import db, auth, processor
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

    def bytes_todf(file):
        bytes_data = file.read()
        s=str(bytes_data,'utf-8')
        data = StringIO(s) 
        df=pd.read_csv(data)
        return df
        
    def random_hex():
        random_number = random.randint(0,16777215)
        hex_number = str(hex(random_number))
        hex_number ='#'+ hex_number[2:]
        return str(hex_number)

    def create_dict_list(df, y_attribute):
        lst = []
        for name in df.name.unique():
            dictionary = dict(
                data=list(df[df['name']==name][y_attribute].values), 
                label=name,
                borderColor=random_hex(),
                fill='false'
            )
            lst.append(dictionary)
        return lst
    
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
                data_uc = create_dict_list(df, 'used_cores')                
                data_qc = create_dict_list(df, 'queue_size')
                data_jc = create_dict_list(df, 'jobs_completed')
                data_it = create_dict_list(df, 'idle_time')
                data_at = create_dict_list(df, 'avg_response_time')
                data_qt = create_dict_list(df, 'avg_queue_time')
                data_ai = create_dict_list(df, 'avg_interarrival_time')
                sim_time = [i for i in range(len(data_uc[0]['data']))]
                
                return render_template("index.html", section='visualiser', data_qc=data_qc, data_uc=data_uc, data_jc=data_jc, data_it=data_it, data_at=data_at, data_qt=data_qt, data_ai=data_ai, sim_time=sim_time)
            
        return render_template("index.html", section='visualiser', data_qc=[], data_uc=[], data_jc=[], data_it=[], data_at=[], data_qt=[], data_ai=[], sim_time=[]) 

    @app.route("/parameters")
    @auth.login_required
    def parameters():
        return render_template("index.html", section = 'parameters')

    @app.route("/simulate")
    @auth.login_required
    def documentation():
        return render_template("index.html", section = 'simulate')

    @app.route('/api/v1/simulations/', methods=['GET','POST'])
    def simulations():
        return "Simulations"        

    return app