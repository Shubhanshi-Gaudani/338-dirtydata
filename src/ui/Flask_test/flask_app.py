from flask import Flask,render_template
from .wait_for_csv import wait_for_data, data_path
from src import all_dirty_cells, csvToMatrix
import multiprocessing as mp
import os
from flask import Flask, flash, request, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = data_path()
ALLOWED_EXTENSIONS = {'txt', 'csv'}

app = Flask('main ui')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
            return "<h1>Upload Succesful</h1>"#redirect(url_for('download_file', name=filename)) 
    return render_template('home.html')

# idk how to get this user download part to work yet
@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route("/about")
def about():
    return "<h1>About Page</h1>"

def start_waiter():
    """Starts the backend code to process the data after it is saved by .js code."""
    wait_for_data()
    inds, reasons, cols = all_dirty_cells(csvToMatrix(data_path()),
                                          parallel = True,
                                          return_cols = True)
    os.remove(data_path())

def launch_server():
    """Launches the server UI."""
    waiter = mp.Process(target = start_waiter, args = tuple())
    waiter.start()
    app.run(debug=True, use_reloader=False)
    waiter.join()
