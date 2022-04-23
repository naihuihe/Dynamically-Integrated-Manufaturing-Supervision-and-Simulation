from tkinter import Frame, Label, Button


class H_surface_nav(Frame):
    """
    This class creates navigation widget for each surface loaded to the surface_frame

    The widget will be packed to the label_frame of the surface_frame
    """



    def __init__(self, surface_name, master = None, cnf = {}, **kw):
        super().__init__(master, cnf, **kw)
        self.surface_name = surface_name
        self.__create_nav()
        self.__config()


    def __create_nav(self):
        self.text_label = Label(self, textvariable=self.surface_name, bg = "lightgrey", height=1, bd=1, relief="raised", padx=10)
        self.text_label.pack(side="left")

        self.close_button = Button(self, text="X", bg = "lightgrey", height=1, padx=5)
        self.close_button.pack(side="left")

    def __config(self):
        self.config(bd = 1, bg = "lightgrey", highlightthickness=1, height = 20, width = 100)
        self.pack(side = "left")
        self.pack_propagate(flag=False)  # fix the height

    def highlight(self):
        self.config(bg = "lightyellow")
        self.text_label.config(bg = "lightyellow")
        self.close_button.config(bg = "lightyellow")

    def un_highlight (self):
        self.config(bg="lightgrey")
        self.text_label.config(bg="lightgrey")
        self.close_button.config(bg="lightgrey")
