import tkinter as tk



class Surface:

    def __init__(self, object):

        self.object = object
        self.canvas = object.surface_frame

        self.color = tk.StringVar()
        self.color.set("blue")


    def create_surface_graph(self):

        bbox = self.object.plot_surface_graph()
        tag = self.object.t_name.get()
        self.object.surface_frame.create_rectangle(bbox, fill = self.color.get(), tag = tag)


