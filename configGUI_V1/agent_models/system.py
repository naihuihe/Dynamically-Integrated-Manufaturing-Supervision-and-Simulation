import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

from widgets.tooltip import CreateToolTip
from widgets.config import Entry
from widgets.scrolled_frame import ScrolledFrame
from .agent import Agent
from widgets.canvas import SurfaceCanvas_M
from .agent_config import SystemConfig


class System(Agent):

    seperate_canvas_required = True

    def __init__(self, wm, pm, **kwargs):

        """
        System agent which is the agent in the highest level to represent a whole system

        :param kwargs:
        """
        super().__init__(wm, pm, **kwargs)


    def create_surface(self):
        """
        :return:
        """
        self.surface_container = ScrolledFrame()
        self.surface = SurfaceCanvas_M(agent = self, master = self.surface_container)
        self.surface.pack()

        self.width = SystemConfig.LAYOUT_WIDTH
        self.height = SystemConfig.LAYOUT_HEIGHT
        self.layout()

        self.wm.add_surface_canvas(self.surface)

    def create_config_panel(self):

        Agent.create_config_panel(self)

        self.load_config_panel(SystemConfig.CONFIG_PANEL_STRUCTURE)
        self.setup_agent_model_panel()


    def layout(self):

        """
        Create or update the system layout on its surface <Canvas>
        :return:
        """
        bbox = self.layout_bbox()

        if not hasattr(self, 'layout_tag'):
            self.layout_tag = self.surface.create_rectangle(bbox, SystemConfig.LAYOUT_STYLE)
        else:
            self.surface.coords(self.layout_tag, *bbox)


    def layout_bbox(self):

        (x, y) = self.surface.origin_coordinate()

        bbox = (
            x,
            y,
            x + self.width,
            y + self.height
        )
        return bbox


    def setup_agent_model_panel(self):

        pane = self.agent_model_panel().get_pane('layout')

        self.width_entry= Entry(textvariable = self.tk_width, command = lambda e: self._on_change_layout('width', e))
        self.height_entry = Entry(textvariable = self.tk_height, command = lambda e: self._on_change_layout('height', e))

        pane.grid_item(self.width_entry, label = 'Width (px):')
        pane.grid_item(self.height_entry, label = 'Height (px):')

        bt1 = ttk.Button(text = 'Upload Image', command = self._on_choose_layout_img)
        pane.grid_item(bt1, label='Layout Background:')

        self.bg_img_path = tk.StringVar()
        layout_bg_textarea = ttk.Entry(textvariable = self.bg_img_path, state ='disabled')
        CreateToolTip(layout_bg_textarea, self.bg_img_path)
        pane.grid_item(layout_bg_textarea)

        self.layout_bg_lock = ttk.Checkbutton(text = 'Lock Background', variable = tk.IntVar(), command = self._on_lock_bg)
        pane.grid_item(self.layout_bg_lock, row = pane.next_row(0), column = 1)


    def _on_change_layout(self, source, event = None):

        if self.bg_img_path.get():

            if 'width' == source:
                self.height = int (self.layout_image_src.height()/self.layout_image_src.width() * self.width)
            else:
                self.width = int( self.layout_image_src.width()/self.layout_image_src.height() * self.height)

            self.layout_image_src = self.load_img(self.img_file, (self.width, self.height))
            self.surface.itemconfigure(self.layout_image, image = self.layout_image_src)

        self.layout()


    def _on_choose_layout_img(self):

        self.img_file = askopenfilename(title = 'Select Layout Image')

        self.layout_image_src = self.load_img(self.img_file)
        self.layout_image = self.surface.create_image(self.surface.origin_coordinate(), image = self.layout_image_src, anchor = 'nw')

        self.width = self.layout_image_src.width()
        self.height = self.layout_image_src.height()

        self.bg_img_path.set(self.img_file)


    def _on_lock_bg(self):

        if hasattr(self, 'layout_image'):

            var_name = self.layout_bg_lock.cget('variable')
            var_value = self.layout_bg_lock.getvar(var_name)

            if int(var_value):
                self.surface.itemconfigure(self.layout_image, state = 'disabled')
            else:
                self.surface.itemconfigure(self.layout_image, state = 'normal')




