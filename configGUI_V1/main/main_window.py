import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

import configGUI_V1.main.config as config
from agent_models.system import System
from configGUI_V1.widgets.dnd_button import DndButton
from configGUI_V1.static.css import MainWindow_css

from configGUI_V1.widgets.popup_window import PopupWindow
from configGUI_V1.main.window_manager import WindowManager
from configGUI_V1.widgets.notebook import SurfaceNotebook
from configGUI_V1 import PROJECT_BASE_DIR
from main.project_manager import ProjectManager
from widgets.config_frame import ConfigFrame


class MainWindow(tk.Tk):

    def __init__(self):

        super().__init__()

        self.wm = WindowManager()

        self._init_window()
        self._init_menus()

        self.projects = {}
        self.current_project = None

    def _init_window(self):
        """
        The main window is packed with a two-pane ttk.Panedwindow
        :return:
        """
        self._setup_window()
        self.tool_bar = ttk.Frame(self, height = 25, borderwidth = 2)
        self.tool_bar.pack(side = 'top', fill = 'x')
        self.container = ttk.Panedwindow(self, style = 'Container.TPanedwindow', orient = tk.HORIZONTAL)
        self.container.pack(side = 'top', fill = tk.BOTH, expand = 1)

        # NB: right_pane must be setup first to get the surface_frame ready
        self._setup_right_pane()
        self._setup_left_pane()

    def _setup_window(self):
        '''
        setup the size and basic information of the main window
        :return:
        '''
        self.geometry("{}x{}".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.iconbitmap(bitmap=PROJECT_BASE_DIR + os.sep + 'images/Corot.ico')
        self.title("Corot D2S Configuration Platform")
        self.config(background='white')

    def _setup_left_pane(self):
        """
        The left pane is seperated into two parts:
        1. top part: nav_frame, the container of project navigatiion tree
        2. bottm part: dnd_frame, the container of all dnd labels to create agents
        :return:
        """
        self.left_pane= ttk.Panedwindow(style = 'Container.TPanedwindow', orient = tk.VERTICAL)
        nav_frame, dnd_frame = ttk.Frame(), ttk.Frame()
        self.left_pane.add(nav_frame)
        self.left_pane.add(dnd_frame)

        self._setup_nav_tree(nav_frame)
        self._setup_dnd_frame(dnd_frame)

        self.container.insert(0, self.left_pane, weight = 1)

    def _setup_nav_tree(self, container):
        self.nav_tree = ttk.Treeview(container, style = 'Nav.Treeview')
        self.nav_tree.pack(fill=tk.BOTH, expand=1)
        self.nav_tree.heading('#0', text = 'Project', anchor = 'w')

        self.wm.nav_tree = self.nav_tree

    def _setup_dnd_frame(self, container):
        for agent in config.AGENT_MAPPER:
            DndButton(container, text=agent, style='Dnd.TButton').pack(MainWindow_css.DndLabel_Pack)


    def _setup_right_pane(self):
        """
        The right pane has two parts:
        1: Top part: {top - left: surface_frame, top - right: config_frame}
        2: Bottom part: msg_info_area: where runing message and information are shown
        :return:
        """
        self.right_pane = ttk.Panedwindow(style = 'Container.TPanedwindow', orient = tk.VERTICAL)
        self.container.add(self.right_pane, weight = 50)

        right_pane_top = ttk.Panedwindow(style = 'Container.TPanedwindow', orient = tk.HORIZONTAL)
        self.right_pane.add(right_pane_top)

        # by default, only the surface_frame will be shown in the main_window
        self.surface_frame = self.wm.surface_frame = SurfaceNotebook(right_pane_top)
        self.config_frame = self.wm.config_frame = ConfigFrame(right_pane_top)
        right_pane_top.add(self.surface_frame, weight = 20)

        # by default, the runtime msg area is not shown at the beginning
        self.runtime_msg_frame = self.wm.runtime_msg_frame = ttk.Frame(self.right_pane)


    def _init_menus(self):
        self.menu_bar = tk.Menu(self)
        self.config(menu = self.menu_bar)
        self._add_menu(label = 'File', menu = self._init_file_menu())

    def _add_menu(self, label:str, menu:tk.Menu):
        self.menu_bar.add_cascade(label = label, menu = menu)

    def _init_file_menu(self):
        f_menu = tk.Menu(cnf = MainWindow_css.Menu, tearoff = False)
        f_menu.add_command(label = "New Project", command = self._on_click_new_project)
        f_menu.add_command(label = 'Open')
        f_menu.add_command(label='Save')
        f_menu.add_command(label = 'Export Project')

        return f_menu

    def _on_click_new_project(self):

        pp_window = PopupWindow('Create New Project', **MainWindow_css.PopupWindow)
        pp_window.focus_set()

        name = tk.StringVar()
        name_label = ttk.Label(pp_window.input_frame, text = 'Project Name:')
        name_entry = ttk.Entry(pp_window.input_frame, textvariable = name, width = 30)
        name_label.grid(row = 0, column = 0, padx = 30, pady = 20)
        name_entry.grid(row = 0, column = 1, sticky = 'ew', pady = 20)
        pp_window.input_frame.grid_propagate(0)

        def confirm():
            if self.create_project(name.get()):
                pp_window.destroy()

        pp_window.set_confirm_command(confirm)
        pp_window.grab_set()

    def create_project(self, name):
        if not name:
            messagebox.showerror(message="Project name must not be empty")
        else:
            project = ProjectManager(name, self.wm)
            self.projects[project.system_agent.get_id()] = project
            return True

    def switch_config_frame(self, event=None):
        if not self.config_frame_toggle:
            self.config_frame.master.add(self.config_frame)
        else:
            self.config_frame.master.remove(self.config_frame)
        self.config_frame_toggle = not self.config_frame_toggle

    def switch_runtime_msg_frame(self, event=None):
        if not self.runtime_msg_frame_toggle:
            self.runtime_msg_frame.master.add(self.runtime_msg_frame)
        else:
            self.config_frame.master.remove(self.runtime_msg_frame)
        self.runtime_msg_frame_toggle = not self.runtime_msg_frame_toggle

    def export_project(self):
        if self.current_project:
            self.current_project.save_project()




if __name__ == "__main__":

    main = MainWindow()
    main.mainloop()
