import tkinter as tk
from tkinter import ttk
from configGUI_V1 import PROJECT_BASE_DIR
import os

from configGUI_V1.static.css import MainWindow_css


class PopupWindow(tk.Toplevel):

    def __init__(self, text = None, **kwargs):
        if 'width' not in kwargs:
            self.width = kwargs['width'] = 350

        if 'height' not in kwargs:
            self.height = kwargs['height'] = 200

        super().__init__(**kwargs)

        self.cc_frame_height = 50

        # set the tytle for the popup window
        if text:
            self.title (text)

        # place the window to the centre of screen
        self.geometry("+%d+%d" % (self.winfo_screenwidth()/2-self.width/2, self.winfo_screenheight()/2 - self.height/2))
        self.minsize(width = self.width, height = self.height)

        self.set_bitmap()

        # input_frame for collecting user's input informaiton
        self.input_frame = ttk.Frame(self, width = self.width, height = self.height - self.cc_frame_height)
        self.input_frame.pack()
        self.input_frame.pack_propagate(0)

        # by default, the window has two buttons, "Confirm" and "Cancel"
        # create "Confirm" and "Cancel" buttons
        self.cc_frame = ttk.Frame(self, width = self.width, height = self.cc_frame_height)  # a frame to include the two buttons

        self.confirm_button = ttk.Button(self.cc_frame, text="Confirm")
        self.confirm_button.pack(side = 'right', anchor="center", padx = 20, pady = 10)

        # self.cancel_button = ttk.Button (self.cc_frame, text = "Cancel", command=self.destroy)
        # self.cancel_button.pack(side = 'right', anchor = "center", padx = 10, pady = 10)
        self.cc_frame.pack()
        self.cc_frame.pack_propagate(0)

    def set_bitmap(self):

        self.iconbitmap(bitmap=PROJECT_BASE_DIR + os.sep + 'images/Corot.ico')

    def set_confirm_command(self, func):
        """
        :param func: callback function
        :return:
        """
        self.confirm_button.config(command = func)


if __name__=="__main__":

    window = PopupWindow( "Test")


    tk.mainloop()
