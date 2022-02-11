from os.path import exists
from time import sleep

def data_path():
    return 'src/ui/Flask task/data/data.csv'

def wait_for_data():
    """Waits for data to be placed in data/data.csv by javascript."""
    pth = data_path()
    while not exists(pth):
        sleep(1) # tell the OS to context switch away so we're not wasting time
    return