
import tkinter as tk


class DynamicOptionMenu(tk.OptionMenu):

    def __init__(self, master, variable, options = [],**kwargs):
        """
        :param master: master frame of the OptionMenu
        :param textvariable: textvariable for receive value of users' input
        :param options: values of options for selection, NB, the values in the list of options must be tk.StringVar()
        :param has_add_new_menu: False -  which means the Optionmenu is just a normal OptionMenu where all menus are for selection
                                 True - which means the Optionmenu has a menu (e.g., add new) whose command is not tk._setit (for receiving users' selection) but
                                        a user-defined command for creating new options

                                 To define an "add new" menu, Optionmenu["menu"].insert_command MUST be called when setting up
                                 where "index" MUST be set to 0 and the "has_add_new_menu" MUST be changed to True.
                                 For example:
                                 optionMenu = DynamicOptionMenu(master, variable, *options...)
                                 optionMenu["menu"].insert_command(index = 0, label = label, command = ...)
        :param kwargs: [static_values: [], has_add_new_menu: boolean, add_new_menu_label: String, add_new_command: func, command: func]
        static_values will be added to the option list, whose values, however, will not change
        """
        self.options = options
        self.variable = variable
        self.__command = kwargs.get("command")

        # load parameters from **kwargs
        kw = self.load_setup_parameters(**kwargs)

        ops = []
        if options:
            ops = [opt.get() for opt in options]

        if self.static_values:
            ops = self.static_values + ops

        # if finally there is still no values existing in ops
        if not ops:
            ops = [None]

        super().__init__(master, variable, *ops, **kw)

        self.bind("<Button-1>", self.reload_menus)

    def insert_add_new_menu(self, menu_label, callback):
        self.has_add_new_menu = True
        self["menu"].insert_command(index=0, label=menu_label, command=callback,
                                    background="yellow", foreground="red")
        if not self.options:
            self["menu"].delete(1)


    def load_setup_parameters(self, **kw):

        if 'static_values' in kw:
            setattr(self, 'static_values', kw.get('static_values'))
            del kw['static_values']
        else:
            setattr(self, 'static_values', [])

        if 'has_add_new_menu' in kw:
            setattr(self, "has_add_new_menu", kw.get('has_add_new_menu'))
            del kw['has_add_new_menu']
        else:
            setattr(self, "has_add_new_menu", False)

        if 'add_new_menu_label' in kw:
            setattr(self, "add_new_menu_label", kw.get('add_new_menu_label'))
            del kw['add_new_menu_label']
        else:
            setattr(self, "add_new_menu_label", "New")

        if 'add_new_menu_callback' in kw:
            setattr(self, 'add_new_menu_callback', kw.get('add_new_menu_callback'))
            del kw['add_new_menu_callback']
        else:
            setattr(self, 'add_new_menu_callback', lambda: False)

        return kw


    def add_option_to_menu(self, option):
        """
        the new option is always inserted to the end
        :param option: a dynamic option defined in tk.StringVar()
        :return:
        """
        label = option.get()
        self["menu"].add_command(label = label, command=tk._setit(self.variable, label, self.__command))

    def reload_menus(self, event = None):

        if self.options:

            # get the number of existing options added to the menu
            num_of_existing_options = self["menu"].index("end")
            pointer = 0

            # if there is no available menu defined
            if num_of_existing_options == None:
                num_of_existing_options = -1

            num_of_existing_options += 1

            # if has_add_new = True, the first menu is the "add new " menu rather than an option
            # So the available options is from 1 to "END"
            if self.has_add_new_menu:
                num_of_existing_options -= 1
                pointer +=1

            # if not self.default_value:
            #     num_of_existing_options -=1
            #     pointer +=1

            if self.static_values:
                v = len(self.static_values)
                num_of_existing_options -=v
                pointer += v

            # reload the self.options list to the menubar

            for index in range(len(self.options)):
                label = self.options[index].get()
                if index < num_of_existing_options:
                    # if has_add_new = True, menu of index = 0 is alwasys the "add new" menu
                    # the reload position should start from 1
                    self["menu"].entryconfigure(index + pointer, label = label, command = tk._setit(self.variable, label, self.__command))
                    # self["menu"].entryconfigure(index + 1 if self.has_add_new_menu else index,
                    #                             label = label, command = tk._setit(self.variable, label, self.__command))
                else:
                    self.add_option_to_menu(self.options[index])

            # if the number of existing options is larger than the updated self.options
            # remove the excesive options
            if num_of_existing_options > len(self.options):
                #self["menu"].delete(len(self.options)+2 if self.has_add_new_menu else len(self.options)+1, "end")
                self["menu"].delete(len(self.options) + 1 + pointer, "end")