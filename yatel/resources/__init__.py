
import os

PATH = os.path.dirname(os.path.abspath(__file__))

def get(filename):
    filepath = os.path.join(PATH, filename)
    if not os.path.exists(filepath):
        raise IOError(2, 'No such file or directory', filename)
    return filepath
