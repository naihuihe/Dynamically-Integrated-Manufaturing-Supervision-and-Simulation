import tkinter as tk
import uuid
from abc import ABC, abstractmethod

from widgets.config import ConfigPanel


class Agent (ABC):
    """
    Basic model to be succeeded by all agents
    """

    seperate_canvas_required = True


    def __init__(self, wm, pm, parent = None, **kwargs):
        '''
        :param wm: WindowManager
        :param pm: ProjectManager
        :param parent: Agent
        :param kwargs:
        '''
        self.wm = wm
        self.pm = pm
        self.parent = parent
        self._init_std_attrs()
        self.load_attrs(kwargs)
        self.__id = uuid.uuid4()

    def _init_std_attrs(self):
        self.tk_name = tk.StringVar()
        self.tk_ref = tk.StringVar()
        self.tk_x = tk.IntVar()
        self.tk_y = tk.IntVar()
        self.tk_width = tk.IntVar()
        self.tk_length = tk.IntVar()
        self.tk_color = tk.StringVar()

    def load_attrs(self, kw):
        for key in kw:
            try:
                getattr(self, key)
                setattr(self, key, kw[key])
            except AttributeError as e:
                raise e

    def get_id(self):
        return str(self.__id)

    @abstractmethod
    def init_agent_displays(self):
        pass

    @abstractmethod
    def create_surface(self):
        pass


    def create_config_panel(self):
        self.config_panel = ConfigPanel(self, self.wm.config_frame)
        self.wm.config_frame.add(self.config_panel)

        if not self.wm.config_frame_toggle:
            self.wm.show_config_frame()

    def setup_info_panel(self):
        panel = self.config_panel.panels['agent_modelling_panel']
        pane = panel.add_pane(text = 'Agent Information', iid = 'agent_info')


    @property
    def name(self):
        return self.tk_name.get()

    @name.setter
    def name(self, val):
        self.tk_name.set(val)

    @property
    def ref(self):
        return self.tk_ref.get()

    @ref.setter
    def ref(self, val):
        self.tk_ref.set(val)

    @property
    def x(self):
        return self.tk_x.get()

    @x.setter
    def x(self, val):
        self.tk_x.set(val)

    @property
    def y(self):
        return self.tk_y.get()

    @y.setter
    def y(self, val):
        self.tk_y.set(val)

    @property
    def width(self):
        return self.tk_width.get()

    @width.setter
    def width(self, val):
        self.tk_width.set(val)

    @property
    def length(self):
        return self.tk_length.get()

    @length.setter
    def length(self, val):
        self.tk_length.set(val)

    @property
    def color(self):
        return self.tk_color.get()

    @color.setter
    def color(self, val):
        self.tk_color.set(val)


if __name__ == '__main__':
    root = tk.Tk()
    agent = Base(wm = None, x = 123)
    print(agent.get_id())
    root.mainloop()