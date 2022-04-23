import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
from _tkinter import TclError

from widgets.config import ConfigPanel
from widgets.scrolled_frame import ScrolledFrame
from .agent import Agent
from widgets.canvas import SurfaceCanvas_M


class System(Agent):


    def __init__(self, wm, pm, **kwargs):

        """
        System agent which is the agent in the highest level to represent a whole system

        :param kwargs:
        """
        super().__init__(wm, pm, **kwargs)

        self.init_agent_displays()



    def init_agent_displays(self):
        self.create_surface()
        self.create_config_panel()

    def create_surface(self):
        self.surface_container = ScrolledFrame()
        self.surface = SurfaceCanvas_M(agent = self, master = self.surface_container)
        self.surface.pack()
        self.wm.add_surface_canvas(self.surface)

    def create_config_panel(self):
        self.config_panel = ConfigPanel(self, self.wm.config_frame)
        self.wm.config_frame.add(self.config_panel)

        if not self.wm.config_frame_toggle:
            self.wm.show_config_frame()
