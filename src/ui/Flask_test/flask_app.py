from flask import Flask,render_template
from .wait_for_csv import wait_for_data, data_path
from src import all_dirty_cells, csvToMatrix
import multiprocessing as mp
import os

app = Flask('main ui')

@app.route("/")
@app.route("/home")
def homepage():
    return render_template('home.html')

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
