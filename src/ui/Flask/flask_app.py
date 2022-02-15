from flask import Flask,render_template
from .wait_for_csv import wait_for_data, data_path, file_path
from src import all_dirty_cells, csvToMatrix, clean_cell, has_header
import multiprocessing as mp
import os
from flask import Flask, flash, request, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename
import numpy as np

UPLOAD_FOLDER = data_path()
ALLOWED_EXTENSIONS = {'txt', 'csv'}
ROOT_PATH = 'src/ui/Flask'

app = Flask('main ui',
            template_folder = ROOT_PATH + '/templates',
            static_folder = ROOT_PATH + '/static')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            return redirect(url_for('download_file', name=filename))  #"<h1>Upload Succesful</h1>" #
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
    mat = csvToMatrix(pth)
    os.remove(pth)
    inds, reasons, cols = all_dirty_cells(mat,
                                          parallel = True,
                                          return_cols = True,
                                          header = has_header(mat))
    suggs = np.empty(inds.shape[0], dtype = 'U128')
    for i in range(suggs.shape[0]):
        suggs[i] = clean_cell(inds[i],
                              mat,
                              cols[inds[i, 1]],
                              reasons[i])
    for i in range(suggs.shape[0]):
        mat[tuple(inds[i])] = suggs[i]
    np.savetxt(pth, mat, fmt = '%s')
    print('Processing complete.', suggs)

def launch_server():
    """Launches the server UI."""
    app.run(debug=True, use_reloader=False)
