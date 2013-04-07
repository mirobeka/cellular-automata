import sys
import os

ca_directory = os.getcwd()
if ca_directory not in sys.path:
    sys.path.insert(0, ca_directory)


class Evolution(object):
    def __init__(self):
        pass