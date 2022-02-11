from flask import Flask,render_template
from .wait_for_csv import wait_for_data, data_path
from src import all_dirty_cells, csvToMatrix

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def homepage():
    return render_template('home.html')

@app.route("/about")
def about():
    return "<h1>About Page</h1>"

def launch_server():
    app.run(debug=True)
    wait_for_data()
    inds, reasons, cols = all_dirty_cells(csvToMatrix(data_path()),
                                          parallel = True,
                                          return_cols = True)
