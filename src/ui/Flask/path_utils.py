from os import listdir
from time import sleep

ALLOWED_EXTENSIONS = {'txt', 'csv'}
ROOT_PATH = 'src/ui/Flask'

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def data_path():
    """Returns the folder at which the user's database should be saved."""
    return ROOT_PATH + '/data'

def file_path():
    """Returns the path to the user's file or an empty string if it has not been uploaded."""
    files = listdir(data_path())
    for f in files:
        if allowed_file(f):
            return data_path() + '/' + f
    return ''

def wait_for_data():
    """Waits for data to be placed in the data folder by Flask."""
    print('Starting to wait')
    while not file_path():
        sleep(1) # tell the OS to context switch away so we're not wasting time
    print('Found file')
