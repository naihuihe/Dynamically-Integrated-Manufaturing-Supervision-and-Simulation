import tkinter as tk

class TextBox(tk.Text):

    def __init__(self, master=None, max_length = None, cnf={}, **kw):

        super().__init__(master, cnf, **kw)
        self.max_length = max_length
        self.max_length_reached = False


    def disable_edit(self):
        self.configure(state = "disabled")

    def enable_edit(self):
        self.configure(state = "normal")




