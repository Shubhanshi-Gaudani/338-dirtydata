from flask import Flask, render_template
from .path_utils import data_path, file_path, allowed_file, ROOT_PATH
from src import csvToMatrix
import os
from flask import flash, request, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename
import numpy as np
from .integration import CLEAN_PATH, CLEAN_NAME, get_dirty, save_clean

UPLOAD_FOLDER = data_path()

app = Flask('main ui',
            template_folder = ROOT_PATH + '/templates',
            static_folder = ROOT_PATH + '/static')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        # show the form, it wasn't submitted
        print(request.form.getlist('source'))
        return render_template('config.html')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
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
            start_processing()
            return redirect(url_for('download_file', name=CLEAN_NAME))  #"<h1>Upload Succesful</h1>" #
    return render_template('home.html')

# idk how to get this user download part to work yet
@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name, as_attachment=True)

@app.route("/about")
def about():
    return "<h1>About Page</h1>"

def start_processing():
    """Starts the backend code to process the data after it is saved by Flask."""
    pth = file_path()
    if pth == '':
        flash('No selected file')
        return redirect(request.url)
    mat = csvToMatrix(pth)
    os.remove(pth)
    inds, reasons, cols = get_dirty(mat)
    save_clean(mat, inds, reasons, cols)
    print('Processing complete.')

def launch_server():
    """Launches the server UI."""
    if os.path.exists(CLEAN_PATH): os.remove(CLEAN_PATH)
    app.run(debug=True, use_reloader=False)
