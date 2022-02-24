from os import listdir
from os.path import exists
from time import sleep

ALLOWED_EXTENSIONS = {'txt', 'csv'}
ROOT_PATH = 'src/ui/Flask'

def get_extension(filename):
    """Returns the extension of the file (e.g. txt or csv)."""
    if '.' not in filename: return ''
    return filename.rsplit('.', 1)[1].lower()

def allowed_file(filename):
    return get_extension(filename) in ALLOWED_EXTENSIONS

def data_path():
    """Returns the folder at which the user's database should be saved."""
    return ROOT_PATH + '/temp_files'

def data_file_path():
    """Returns the path to the user's file or an empty string if it has not been uploaded."""
    root_path = data_path()
    files = listdir(root_path)
    config_files = [def_config_name(),
                    custom_config_name()]
    for f in files:
        if (allowed_file(f) and 
            not f in config_files):
            return data_path() + '/' + f
    return ''

def def_config_name():
    """Returns the name of the default config file."""
    return 'def_config.txt'

def custom_config_name():
    """Returns the name of the user's custom config file."""
    return 'custom_config.txt'

def config_file_path():
    """Returns the path to the user's file. 
    
    If the user has not selected any files, it will return the default configs.

    Args:
        None

    Returns:
        pth (str) : the path to the config files
    """
    root_path = data_path()
    custom = root_path + '/' + custom_config_name()
    if exists(custom):
        return custom
    return root_path + '/' + def_config_name()

def wait_for_data():
    """Waits for data to be placed in the data folder by Flask."""
    print('Starting to wait')
    while not data_file_path():
        sleep(1) # tell the OS to context switch away so we're not wasting time
    print('Found file')
