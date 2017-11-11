import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Output_Files')
DATA_FILES = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Input_Data_Files')


def init():
    global OUTPUT_DIR
    global DATA_FILES
