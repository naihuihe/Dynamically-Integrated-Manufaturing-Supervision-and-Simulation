import os
PROJECT_BASE_DIR = os.path.dirname(os.path.realpath(__file__))

from configGUI_V1.main.main_window import MainWindow

def create_main():
    main = MainWindow()
    return main
