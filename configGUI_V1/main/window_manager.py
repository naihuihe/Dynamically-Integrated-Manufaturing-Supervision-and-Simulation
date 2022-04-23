
from configGUI_V1.main import InitTTKStyles

class WindowManager:

    def __init__(self):
        style = InitTTKStyles()

        self.nav_tree = None           # ttk.Treeview
        self.surface_frame = None      # ttk.Notebook
        self.config_frame = None       # ttk.Frame
        self.runtime_msg_frame = None  # ttk.Frame

        self.config_frame_toggle = False
        self.runtime_msg_frame_toggle = False

    def add_surface_canvas(self, surface):
        '''
        NB: the widget added to surface frame is surface.master <a tk.Frame> rather than surface
        :param surface:
        :return:
        '''
        self.surface_frame.add_surface(surface, tab_id = surface.agent.get_id(), text = surface.agent.name)

        self.add_nav(parent = surface.agent.parent.get_id() if surface.agent.parent else None,
                     text = surface.agent.name,
                     tag = surface.agent.get_id())

    def add_nav(self, parent, text, tag):
        '''
        :param parent:  tag_id of parent element, default is parent agent.id
        :param name:
        :param iid: agent.id
        :return:
        '''
        if not parent:
            parent = ''
        self.nav_tree.insert(parent, 'end', text = text, iid = tag, tags= tag)
        self.nav_tree.tag_bind(tag, '<Double-Button-1>', self.__pop_surface)

    def __pop_surface(self, event):
        self.surface_frame.select_surface_by_tabid(event.widget.focus())
        #self.surface_frame.event_generate('<<SurfaceReload>>')


    def show_config_frame(self):
        paned_window = self.config_frame.master
        paned_window.add(self.config_frame, weight=1)
        self.config_frame_toggle = True

    def hide_config_frame(self):
        paned_window = self.config_frame.master
        paned_window.forget(self.config_frame)
        self.config_frame_toggle = False



