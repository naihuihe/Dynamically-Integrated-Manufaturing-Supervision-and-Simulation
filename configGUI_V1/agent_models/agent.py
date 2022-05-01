import tkinter as tk
from tkinter import messagebox
import uuid
from abc import ABC, abstractmethod

from PIL import Image, ImageTk

from agent_models.agent_config import AgentConfig
from widgets.config import ConfigPanel, Entry
from widgets.collapsible_panedframe import CollapsiblePanedFrame


class Agent (ABC):
    """
    Basic model to be succeeded by all agents
    """

    seperate_canvas_required = False


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
        self.__init_std_attrs()
        self.__id = uuid.uuid4()
        self.__load_attrs(kwargs)
        self.__init_agent_displays()

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
    def height(self):
        return self.tk_height.get()

    @height.setter
    def height(self, val):
        self.tk_height.set(val)

    @property
    def color(self):
        return self.tk_color.get()

    @color.setter
    def color(self, val):
        self.tk_color.set(val)

    # ================================================ Agent initialisation functions ===================================================

    def __init_std_attrs(self):
        self.tk_name = tk.StringVar()
        self.tk_ref = tk.StringVar()
        self.tk_x = tk.IntVar()
        self.tk_y = tk.IntVar()
        self.tk_width = tk.IntVar()
        self.tk_height = tk.IntVar()
        self.tk_color = tk.StringVar()

    def __load_attrs(self, kw):
        for key in kw:
            try:
                getattr(self, key)
                setattr(self, key, kw[key])
            except AttributeError as e:
                raise e

    def __init_agent_displays(self):
        self.create_surface()
        self.create_config_panel()


    @abstractmethod
    def create_surface(self, *args, **kwargs):
        pass

    @abstractmethod
    def create_config_panel(self, *args, **kwargs):

        # create panel
        self.config_panel = ConfigPanel(self, self.wm.config_frame)
        self.wm.config_frame.add(self.config_panel)

        if not self.wm.config_frame_toggle:
            self.wm.show_config_frame()

        # set up the config_panel using the default panel structure
        default_panels = AgentConfig.CONFIG_PANEL_STRUCTURE

        self.load_config_panel(default_panels)

        # load name configuration for all agents by default
        panel = self.agent_model_panel().get_pane('agent_info')
        name_entry = Entry(textvariable=self.tk_name, command=self.__on_name_change)
        ref_entry = Entry(textvariable=self.tk_ref)
        panel.grid_item(name_entry, label='Name:')
        panel.grid_item(ref_entry, label='Ref Number:')


    def load_config_panel(self, structure:dict):

        """
        :param structure: check agent_config file for details of structure requirements
        """
        for id, item in structure.items():

            # create a new panel or get the panel with the given id
            if item.get('heading'):
                panel = self.config_panel.add_new_panel(text = item['heading'], panel_id = id)
            else:
                panel = self.config_panel.get_panel(id)

            # load panes to the panel
            children = item.get('children')
            if children:
                for iid, text in children.items():
                    panel.add_pane(text=text, iid=iid)


    # ================================================ GET functions ===================================================

    def agent_model_panel(self):
        """
        A shortcut function to get the agent_model panel
        """
        return self.config_panel.get_panel('agent_model')

    def simulation_panel(self):
        """
        A shortcut function to get the simulation panel
        """
        return self.config_panel.get_panel('simulation')

    def data_model_panel(self):
        """
        A shortcut function to get the db_model panel
        """
        return self.config_panel.get_panel('db_model')

    def get_id(self):

        return str(self.__id)

    # ==================================================== callback funcs ========================================================


    def __on_name_change(self, event):
        """
        callback by the config_panel name_entry
        this function can be called by either <Return> or <Focusout> event
        """
        if not event.widget.get():
            tk.messagebox.showwarning(title="Input Error", message="Agent name can not be empty!")
            self.name = event.widget.get_origin_value()
            event.widget.focus()

        else:
            self.apply_name_change()


    def apply_name_change(self):
        if self.seperate_canvas_required:
            self.wm.surface_frame.tab(self.surface.master, text = self.name)

        self.wm.nav_tree.item(self.get_id(), text = self.name)
        self.config_panel.update_heading()

    # =================================================== Universial operational functions ============================================


    def load_img(self, file, size = ()):

        """
        Called by agents to load images related to their surface (e.g., layout background of System Agent, or
        surface graphs of resource agent) or any other purposes if necessary

        :param file: image file path
        :param size: image size (width, height). If not give, image will be loaded with its original size
        :return: PhotoImage
        """
        with Image.open(file) as img:

            src = img.resize(size, Image.ANTIALIAS) if size else img
            image = ImageTk.PhotoImage(src)

        return image







if __name__ == '__main__':
    root = tk.Tk()
    agent = Base(wm = None, x = 123)
    print(agent.get_id())
    root.mainloop()