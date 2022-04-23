from tkinter import *
from tkinter import colorchooser

from static.css import ConfigPanelStyle
from tk_view_models.product import Product
from tk_view_models.resource import Resource
from .bom_form import BomForm
from .collapsible_pane import CollapsiblePane
from .dynamic_optionmenu import DynamicOptionMenu
from .form import Form, Column
from .line_seperator import LineSeperator
from .text_box import TextBox


class ConfigPanel(Frame):

    def __init__(self, master_frame = None, name = None, object = None, type = None, **kwargs):

        super().__init__(master_frame, **kwargs)
        self.config(bg = "white")

        self.master_frame = master_frame
        self.object = object
        self.name = name
        self.type = type



    class TagLabel(Label):

        def __init__(self, frame, **kwargs):
            super().__init__(frame, **kwargs)
            self.configure(font = ("Arial", 11, "bold"), foreground = "Blue", bg = "lightblue", anchor = W)

    class VarTitlelabel(Label):

        def __init__(self, frame, **kwargs):
            super().__init__(frame, **kwargs)
            self.configure(font = ("Arial", 11), anchor = W)

    class VarEntry(Entry):

        def __init__(self, frame, **kwargs):
            super().__init__(frame, **kwargs)
            self.config(bg = "white", highlightbackground = "black")


    class ConfigButton(Button):

        def __init__(self, frame = None, **kwargs):
            super().__init__(frame, **kwargs)
            self.config(background = "lightgrey", borderwidth = 1, height = 1, width = 2)

    def config_profile_frame(self):

        self.tag_label = self.TagLabel(self, textvariable = self.object.t_name)
        self.tag_label.pack(side = TOP, fill= "x")
        self.profile_frame = Frame(self, bg = "white")
        self.profile_frame.pack(fill="x")

        self.VarTitlelabel(self.profile_frame, text = "name: ", anchor = E).grid(row = 0, column = 0, sticky = W, padx = 20, pady = 5)
        self.name_entry = self.VarEntry(self.profile_frame)
        self.name_entry.config(textvariable = self.object.t_name)
        self.name_entry.grid(row = 0, column=1, sticky = E,padx = 20, pady = 5)


    def config_variable_frame(self):
        # set up title for the frame
        if isinstance(self.object, Resource):
            self.variable_frame = self.create_new_config_frame("Variable")

            # set up variable form
            self.variable_form = self.init_add_variable_form_for_machine(self.variable_frame.frame)
            #self.variable_form.grid(row = self.variable_frame.next_row, columnspan = 2)
        # if the object is a product agent
        elif isinstance(self.object, Product):
            self.variable_frame = self.create_new_config_frame("Bills of Materials (BOM)")

            # set up variable form
            self.variable_form = self.init_bom_form_for_product(self.variable_frame.frame)
        self.variable_form.grid(row=self.variable_frame.next_row, columnspan=2)

        self.object.variables = self.variable_form.variables

    def init_add_variable_form_for_machine(self, container_frame):
        # initialise columns
        columns = (
            Column(title="Name", nullable=False),
            Column(title="Type", nullable=False),
            Column(title="Initial Value"),
            Column(title="Unit")
        )

        variable_form = Form(agent=self.object, master=container_frame, columns=columns, has_seq_column=True)
        variable_form.add_input_by_entry(variable_form.get_column_index_by_title("Name"))
        variable_form.add_input_by_option(variable_form.get_column_index_by_title("Type"),
                                               ["String", "Integer", "Double", "Boolean"])
        variable_form.add_input_by_entry(variable_form.get_column_index_by_title("Initial Value"))
        variable_form.add_input_by_entry(variable_form.get_column_index_by_title("Unit"))
        variable_form.setup_fun_buttons()

        return variable_form


    def config_appearance_frame(self):

        self.appearance_frame = CollapsiblePane(self, text = StringVar(value = "Appearance"))
        self.appearance_frame.pack(fill = "x")
        self.appearance_frame.name_label.config(font = ("Arial", 11, "bold"), foreground = "Blue", bg = "lightblue")
        self.appearance_frame.expanded_label.configure(foreground="Blue", bg="lightblue")

        self.VarTitlelabel(self.appearance_frame.frame, text="Color: ", anchor=E).grid(row=0, column=0, sticky=W, padx=20, pady=5)
        self.VarEntry(self.appearance_frame.frame, textvariable = self.object.t_color).grid(row = 0, column = 1, sticky = W, padx = 10, pady = 5)
        self.color_choose_button = Button(self.appearance_frame.frame, width = 2, height = 1, bg = self.object.t_color.get(), command = self.change_surface_color)
        self.color_choose_button.grid(row=0, column=2, sticky=W, pady=5)

    def kwargs_filter(self, args):
        """
        this function will be used by all grid funcs() below.
        It will make a pre-processing of the **kwargs from user by
        deleting all args related to grid() and returning a new kw for grid()
        :return: args1: without grid() options, args2: only containing grid()options
        """
        kw = {}
        grid_options = ["row", "column", "rowspan", "columnspan", "ipadx", "ipady", "padx", "pady", "sticky"]
        for option in grid_options:
            if option in args:
                kw[option] = args.get(option)
                del args[option]
        return args, kw



    def grid_var_title(self, title, des_widget, cnf = {}, **kwargs):
        args = self.kwargs_filter(kwargs)
        kw = args[0]
        grid_kw = args[1]
        self.VarTitlelabel(des_widget, text = title, anchor = "e", **kw).grid(cnf = ConfigPanelStyle.var_grid_style, **grid_kw)

    def grid_an_entry(self, des_frame, textvariable = None, value = None, command = None, cnf = {}, **kwargs):
        args = self.kwargs_filter(kwargs)
        kw = args[0]
        grid_kw = args[1]

        if textvariable is None:
            entry_value = StringVar()
            if value:
                entry_value.set(value)
        else:
            entry_value = textvariable
        entry = self.VarEntry(des_frame, textvariable = entry_value, **kw)
        entry.grid(cnf = ConfigPanelStyle.var_grid_style, **grid_kw)
        if command is not None:
            entry.bind("<FocusOut>", lambda event: command(entry_value, event))
            entry.bind("<Return>",lambda event: command(entry_value, event))
        return entry

    def grid_an_textbox(self, des_frame, cnf = {}, **kwargs):
        args = self.kwargs_filter(kwargs)
        kw = args[0]
        grid_kw = args[1]

        textbox = TextBox(des_frame, cnf = cnf, **kw)
        textbox.grid(cnf = ConfigPanelStyle.var_grid_style, **grid_kw)

        return textbox

    def grid_an_optionmenu(self, des_frame, textvariable, options = [], isMenuDynamic = False, **kwargs):
        """
        :param des_frame:
        :param textvariable:
        :param static_values: list - only passed if isMenuDynamic = True. Values in the list will not be changed dynamically
        :param options: list - values in the list are tk variables if isMenuDynamic = True, which will be dynamically changed.
        :param isMenuDynamic:
        :param cnf:
        :param kwargs:
        :return:
        """
        args = self.kwargs_filter(kwargs)
        op_kw = args[0]
        grid_kw = args[1]

        if isMenuDynamic:
            option_menu = DynamicOptionMenu(des_frame, textvariable, options, **op_kw)
        else:
            option_menu = OptionMenu(des_frame, textvariable, *options, **op_kw)

        option_menu.configure(cnf = ConfigPanelStyle.optionmenu_style)
        option_menu["menu"].configure(cnf = ConfigPanelStyle.menu_style)

        option_menu.grid(cnf = ConfigPanelStyle.var_grid_style, **grid_kw)

        return option_menu

    def grid_line_seperator(self, des_frame, cnf = {}, **kwargs):

        args = self.kwargs_filter(kwargs)
        kw = args[0]
        grid_kw = args[1]

        seperator = LineSeperator(des_frame, **kw)
        seperator.grid(cnf = ConfigPanelStyle.var_grid_style, **grid_kw)
        seperator.configure(bg = "lightblue", width = 100)

    def grid_a_button(self, des_frame, cnf = {}, **kwargs):

        args = self.kwargs_filter(kwargs)
        kw = args[0]
        grid_kw = args[1]

        button = Button(des_frame, cnf = cnf, **kw)
        button.grid(cnf = ConfigPanelStyle.var_grid_style, **grid_kw)

        return button

    def create_new_config_frame(self, frame_title):
        frame = CollapsiblePane(self, text=StringVar(value=frame_title))
        frame.pack(fill="x")
        frame.name_label.configure(font=("Arial", 11, "bold"), foreground="Blue", bg="lightblue")
        frame.expanded_label.configure(foreground="Blue", bg="lightblue")

        return frame

    # a callback function by the color_choose_button
    def change_surface_color(self):

        color = colorchooser.askcolor()
        self.object.color = str(color[1])
        self.object.surface_frame.itemconfigure(self.object.surface_tag, fill = color[1])
        self.color_choose_button.config(bg = color[1])



    def hide_panel(self):
        self.pack_forget()

    def reload_panel(self):
        self.pack(side = LEFT, fill = BOTH, expand = 1)