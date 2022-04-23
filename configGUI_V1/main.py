from tkinter.filedialog import *
from std_agents.SystemAgent import *


from .widgets.dnd_button import DndLabel
from .widgets.popup_window import PopupWindow
from .widgets.surface_frame import SurfaceFrame
from .widgets.config_frame import ConfigFrame
from .static.css import *


class Main:

    def __init__(self):

        self.root = None
        self.system_frame = None
        self.surface_frame = None
        self.config_frame = None

        self.element_library_frame = None
        self.surface_list = {}
        self.active_surface = None

        self.num_of_element = 0

        self.setup_main_window()
        self.config_resource_lib()
        self.setup_menu()


    def setup_main_window(self):

        self.setup_tk_root()

        # The BODY_WINDOW is a paned window containing three parts, left, middle and right
        # Left pane has two parts:
        #                        Top: The LABEL_FRAME showing all system elements created and their structures
        #                        Bottom: The AGENT_FRAME includes all types of Agent Elements uses can drag and drop
        # Middle pane: shows the system graphically
        # right pane: a frame enabling users to configure selected elements

        # create a paneWindow first
        main_window = PanedWindow(self.root, bg="WHITE", sashrelief=SUNKEN, relief=SUNKEN)
        main_window.pack(fill=BOTH, expand=1)

        # split the panedWindow to three parts: left_pane, middle_pane, and right_pane
        left_pane = PanedWindow(main_window, orient=VERTICAL, bg="WHITE", sashrelief=SUNKEN, relief=SUNKEN)
        middle_pane = Frame(main_window)
        right_pane = Frame(main_window)

        # configure the SYSTEM_FRAME and RESOURCE_LIBRARY to the left_pane created
        # 1st: configure the SYSTEM_FRAME
        left_top = Frame()
        Label(left_top, text="System", height=1, anchor=W, padx=10).pack(fill="x")  # a label on the top of LABEL_FRAME
        Frame(left_top, height=2, bd=1, relief=SUNKEN).pack(fill="x")  # this is a line seperator
        self.system_frame = Frame(left_top, height=400, width=300, relief=SUNKEN, background="WHITE")
        self.system_frame.pack(fill=BOTH, expand=1)
        left_pane.add(left_top)

        left_bottom = Frame()
        Label(left_bottom, text="Resources", height=1, anchor="w", padx=10).pack(fill="x")
        Frame(left_bottom, height=2, bd=1, relief=SUNKEN).pack(fill="x")  # this is a line seperator
        self.element_library_frame = Frame(left_bottom, height=500, width=300, relief=SUNKEN, background="WHITE")
        self.element_library_frame.pack(fill=BOTH, expand=1)
        left_pane.add(left_bottom)

        # configure the middle_pane
        self.surface_frame = SurfaceFrame(middle_pane)
        """
        Frame(middle_pane, width = 500, height=2, bd=1, relief=SUNKEN).pack(fill="x")  # this is a line seperator
        surface_frame_label = Label(middle_pane, height=1, anchor=W, padx=10) # label in the surface_frame. The text on the label will be the name of the created system.
        surface_frame_label.pack(fill="x")
        Frame(middle_pane, height=2, bd=1, relief=SUNKEN).pack(fill="x")  # this is a line seperator
        self.surface_frame = Frame(middle_pane, bg="WHITE")
        self.surface_frame.pack(fill=BOTH, expand=1)
        """

        # configure the right pane
        Frame(right_pane, height=2, bd=1, relief=SUNKEN).pack(fill="x")  # this is a line seperator
        surface_frame_label = Label(right_pane, text="Properties", height=1, anchor=W,padx=10)  # label in the surface_frame. The text on the label will be the name of the created system.
        surface_frame_label.pack(fill="x")
        Frame(right_pane, height=2, bd=1, relief=SUNKEN).pack(fill="x")  # this is a line seperator
        self.config_frame = ConfigFrame(right_pane, bg = "WHITE")
        self.config_frame.pack(fill=BOTH, expand=1)

        # add the configured panes to the main_window
        main_window.add(left_pane)
        main_window.add(middle_pane)
        main_window.add(right_pane)

    def setup_tk_root(self):
        """
        This function setup the tkinter root window with a specific size and title
        :return:
        """
        self.root = Tk()
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.geometry("{}x{}".format(width, height))
        self.root.iconbitmap(bitmap="../configGUI/figs/Corot.ico")
        self.root.title("Corot D2S Configuration Platform")

    def config_resource_lib(self):
        self.add_resource_to_lib("Machine")
        self.add_resource_to_lib("Robot")
        self.add_resource_to_lib("Path")

    def add_resource_to_lib(self, resource):
        """
        :param resource: type of the resource, e.g. "Machine", "Robot", "Buffer", "Route"
        :return: None
        """
        resource_label = DndLabel(self, self.element_library_frame, text=resource, width=15, anchor=W, padx=10, borderwidth=1,
                                  highlightbackground="Black", fg="red")
        #resource_label.set_target_canvas(self.active_surface)
        resource_label.grid(row=self.num_of_element, padx=2, pady=2, sticky=W)
        self.num_of_element += 1

    # create top navigation menu
    def setup_menu(self):
        # create a root menu bar on startup_window
        root_menubar = Menu(self.root, font=("Verdana", 14))

        # create a new menu called as file_menu to be added to the root_menu
        file_menu = Menu(root_menubar, tearoff=False)
        file_menu.add_command(label="New System", command=self.popup_newsystem_creation)
        file_menu.add_command(label="Open")
        file_menu.add_separator()
        root_menubar.add_cascade(label="Start", menu=file_menu)  # configure the file_menu to root_menubar

        # configure the root_menubar to the startup_window
        self.root.config(menu=root_menubar)


    # The callback function of the start menu to create a new system
    # this function is used as a callback function in popup_newsystem_creation() function
    def create_new_system(self, name):
        self.main_system = System_Agent(name, self.system_frame, self.surface_frame, self.config_frame)
        self.surface_list[name] = self.main_system.surface
        self.active_surface = self.main_system.surface

    def popup_newsystem_creation(self):
        #: create variables for getting parameters of new system
        sys_name = StringVar()  # C- the name of system, which must be given by users
        path = StringVar()  # C- the path for saving documents, which must be given by users

        def get_path():
            path.set(askdirectory())

        # create a new popup window
        popup_window = PopupWindow("Create new system")

        # setup the popup window
        frame1 = LabelFrame(popup_window, text="System information", padx=10, pady=10, labelanchor=N)
        frame1.pack()
        Label(frame1, text="Name", width=10).grid(row=0, sticky=W)
        Label(frame1, text="Path", width=10).grid(row=1, sticky=W)
        Entry(frame1, textvariable=sys_name, width=30).grid(row=0, column=1, sticky=W)
        Entry(frame1, textvariable=path, width=30).grid(row=1, column=1, sticky=W)

        folder_photo = PhotoImage(file="D2SSystem/configGUI/figs/folder_image.png")
        path_button = Button(frame1, image=folder_photo, command=get_path)
        path_button.image = folder_photo
        path_button.grid(row=1, column=2, sticky=W)

        # define a callback funcion for the "Confirm" button to create a new system
        def callback(event):
            self.create_new_system(sys_name.get())
            popup_window.destroy()

        # setup popup_window's "Confirm" button
        popup_window.confirm_button.bind("<Button-1>", callback)

        popup_window.grab_set()
