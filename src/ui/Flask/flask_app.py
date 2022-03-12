from flask import Flask, render_template
from src import CLEAN_XL, CLEAN_XL_PATH, data_path, data_file_path, allowed_file, ROOT_PATH, custom_config_name, CLEAN_PATH, CLEAN_NAME
import os
from flask import flash, request, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename
import numpy as np
from .integration import get_preds
import webbrowser
from threading import Timer, Thread
from src import Driver
from time import sleep

UPLOAD_FOLDER = data_path()

app = Flask('main ui',
            template_folder = ROOT_PATH + '/templates',
            static_folder = ROOT_PATH + '/static')
driver = None

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['SECRET_KEY'] = '0000'

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods =['GET', 'POST'] )
def upload_file():
    if os.path.exists(CLEAN_PATH): os.remove(CLEAN_PATH)
    if os.path.exists(CLEAN_XL_PATH): os.remove(CLEAN_XL_PATH)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # t = Thread(target = start_processing)
            # t.start()
            # while driver is None or driver.progress < 150:
            #     sleep(1)
            #     # update progress
            # t.join()
            start_processing()
            return redirect(url_for('download_page')) 
    return render_template('home.html')

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        configs = request.form.getlist('source')
        with open(data_path() + '/' + custom_config_name(), 'w') as config:
            config.write('\n'.join(configs))
        return redirect(url_for('upload_file'))
    return render_template('config.html')

@app.route('/download', methods=['GET', 'POST'])
def download_page():
    if request.method == 'POST':
        if request.form['submit_button'] == "Download as CSV" :
            return redirect(url_for('download_file', name=CLEAN_NAME))
        else:
            return redirect(url_for('download_file', name=CLEAN_XL))
    else:
        return render_template('download.html')
    
@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name, as_attachment=True)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/summary")
def summary():
    return render_template('summary.html')

def start_processing():
    """Starts the backend code to process the data after it is saved by Flask."""
    global driver
    pth = data_file_path()
    if pth == '':
        flash('No selected file')
        return redirect(request.url)
    print(f'Reading {pth}')
    preds, dupes = get_preds()
    driver = Driver(pth, preds = preds, dupes = dupes)
    os.remove(pth)
    print(f'Finding dirty cells in sheet with shape {driver.clean_mat.shape}')
    driver.find_dirty_cells()
    print(f'Cleaning {driver.dirty_inds.shape[0]} cells')
    driver.clean_all_cells()
    driver.save_clean(CLEAN_PATH)
    driver.save_excel(CLEAN_XL_PATH)
    driver.highlight_excel(CLEAN_XL_PATH)
    print('Processing complete.')

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

def launch_server():
    """Launches the server UI."""
    Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=True, port = 5000, threaded=True)
