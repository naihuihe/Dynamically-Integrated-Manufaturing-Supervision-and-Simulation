from tkinter import Frame
from static.css import MainGuiStyle


class LineSeperator(Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.config(cnf = MainGuiStyle.line_seperator)