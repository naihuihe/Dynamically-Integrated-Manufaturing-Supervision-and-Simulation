import tkinter.ttk as ttk
from tkinter import dnd

from configGUI_V1.static.css import MainGuiStyle


class DndButton(ttk.Button):

    def __init__(self, master = None, **kwargs):
        """
        to create agents or plot graphs in drag-and-drop manner
        :param: rel_agent: the agent to be create
        :param master:
        :param kwargs: STANDARD ttk.Label options
        """

        super().__init__(master, **kwargs)

        self.bind("<ButtonPress-1>", self.on_start)
        self.bind("<Double-Button-1>", self.activate_interative_plotting)

    def activate_interative_plotting(self, event):
        label = event.widget["text"]
        if label == "Path":
            self.main_gui.surface_frame.current_canvas.activate_interative_line_plotting()
        elif label == "Material Flow":
            self.main_gui.surface_frame.current_canvas.launch_material_flow_plotting()


    def on_start(self, event):
        dnd.dnd_start(self, event)

    def where(self, canvas, event):
        # where the corner of the canvas is relative to the screen:
        x_org = canvas.winfo_rootx()
        y_org = canvas.winfo_rooty()
        # where the pointer is relative to the canvas widget:
        x = event.x_root - x_org
        y = event.y_root - y_org
        # compensate for initial pointer offset
        return x, y

    def dnd_end(self, target, event):
        pass
