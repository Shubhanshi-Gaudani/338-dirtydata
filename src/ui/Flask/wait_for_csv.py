from os import listdir
from time import sleep

def data_path():
    """Returns the folder at which the user's database should be saved."""
    return 'src/ui/Flask/data'

def file_path():
    """Returns the path to the user's file or an empty string if it has not been uploaded."""
    files = listdir(data_path())
    if len(files):
        return data_path() + '/' + files[0]
    return ''

def wait_for_data():
    """Waits for data to be placed in the data folder by Flask."""
    print('Starting to wait')
    while not file_path():
        sleep(1) # tell the OS to context switch away so we're not wasting time
    print('Found file')
