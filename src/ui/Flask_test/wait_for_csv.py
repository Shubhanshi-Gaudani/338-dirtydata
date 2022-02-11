from os.path import exists
from time import sleep

def wait_for_data():
    """Waits for data to be placed in data/data.csv by javascript."""
    while not exists('data/data.csv'):
        sleep(1)

    return 1