from tkinter import messagebox

from data_models.resource import VariableContent
from static.css import PopupWindowStyle
from widgets.dynamic_optionmenu import DynamicOptionMenu
from widgets.form import Form, Column
import tkinter as tk

from widgets.popup_window import PopupWindow

class DynamicVariable(VariableContent):

    """
    In this class, a value gives to an attribute is a tk.Variable (e.g, tk.StringVar, tk.IntegerVar...)
    This is to make sure values of attributes can be dynamically updated if they are changed by users through other agents.
    For example, if a product name is changed by users, it will be automatically changed
    """

    def get_variable(self):
        """
        :return: an instance of VariableContent.
        """
        variable = VariableContent(self.attributes)
        for each in self.attributes:
            variableValue = self.get_attr(each)
            self.set_attr(each, variableValue.get())

        return variable


class BomForm(Form):

    def __init__(self, agent = None, master=None, columns=(), has_seq_column = False, **kwargs):
        super().__init__(agent, master, columns, has_seq_column,**kwargs)

        # a dict to store the dynamic options for particular columns
        # key: the index of a column, value: a list of dynamic options of tk.StringVar()
        self.dynamic_options_map = {}


    def add_input_by_dynamic_option(self, column, options=[], has_add_new_menu = True, variable = None):
        """
        :param column: to which column the option menue will be created
        :param options: list of textvariable options
        :return:
        """
        # save the dynamic options to the dict map
        self.dynamic_options_map[column] = options

        # ops = [option.get() for option in options]

        if not variable:
            var_selected = tk.StringVar()
            var_selected.set("")
        else:
            var_selected = variable
            var_selected.set("")

        option_menu = DynamicOptionMenu(self, variable = var_selected, options=options)
        option_menu.configure(background="white", relief="groove", borderwidth=1, height=1, width=10,
                              highlightcolor="white", highlightthickness=1)

        option_menu.grid(row=self.next_row, column=column)
        option_menu["menu"].configure(cnf=Form.option_menuStyle)
        self.entry_widgets[option_menu] = var_selected

        return option_menu

    def update_dynamic_optionmenu(self, column, option):
        """
        :param column: the index of the column where the option_menu is
        :param option: the new option to be added to the option_menu
        :return:
        """
        widget = self.grid_slaves(row=self.next_row, column = column)[0]
        #widget.add_option_to_menu(option)
        self.reload_dynamic_optionmenu(column)


    def reload_dynamic_optionmenu(self, column):
        """
        this function will reload the menus in the option_menu.
        It should be called once a change is made to the options, e.g., a new option is added or the text for a option is changed
        :param column: the index of the column where the option_menu is
        :return:
        """
        widget = self.grid_slaves(row=self.next_row, column = column)[0]
        widget.reload_menus()


    def add_new_variable(self, event = None):
        """
        re-write the function
        :param event:
        :return:
        """
        # get the inputs from the entry widgets and put to a list
        inputs = [value.get() for value in self.entry_widgets.values()]

        # create a Variable Instance to store the values of inputs
        column_titles = [column.title for column in self.columns] if self.columns else ["undefined"]
        variable = DynamicVariable(column_titles)

        if not self.is_input_valid(inputs):
            messagebox.showerror(message="Please make sure all elements market in * must not be empty")
            return

        for index in range(self.num_columns):
            var_label = tk.Label(self, background="white", cnf=Form.labelStyle)
            if index + self.has_seq_column not in list(self.dynamic_options_map.keys()):
                var_label.configure(text = inputs[index])
                variable.set_attr(column_titles[index], (tk.StringVar()).set(inputs[index]))

            else:
                optionmenu_widget = list(self.entry_widgets.keys())[index]
                retrieved_text_index = optionmenu_widget["menu"].index(inputs[index])

                # if the option_menu has a "add new part" menu,
                # the selectable options will start from 1 rather than 0,
                # therefore, the index must be minus 1
                if optionmenu_widget.has_add_new_menu:
                    retrieved_text_index -=1
                text_var = optionmenu_widget.options [retrieved_text_index]
                var_label.configure(textvariable = text_var)
                variable.set_attr(column_titles[index], text_var)
            var_label.grid(row=self.next_row, column=index + self.has_seq_column, sticky="nsew")
            var_label.bind("<Button-1>", lambda event: self.highlight_row(var_label.grid_info()["row"], event))

        self.variables[self.next_row] = variable
        if self.has_seq_column:
            tk.Label(self, text = len(self.variables), cnf=Form.sequenceStype).grid(row = self.next_row, column = 0, sticky = "nsew")
        self.next_row += 1
        self.reset_entry_row()

    def change_variable(self, row):

        inputs = [value.get() for value in self.edit_widget.values()]
        if not self.is_input_valid(inputs):
            messagebox.showerror(message="Please make sure all elements market in * must not be empty")
            return False

        # reset the textvariable for edit_widgets
        for value in self.edit_widget.values():
            value.set("")

        # set new inputs to variable
        var_labels = [self.grid_slaves(row, column + self.has_seq_column)[0] for column in range(self.num_columns)]
        for index in range(self.num_columns):

            if index + self.has_seq_column not in list(self.dynamic_options_map.keys()):
                var_labels[index].configure(text=inputs[index])
                self.variables[row].set_attr(self.columns[index].title, inputs[index])
            else:
                optionmenu_widget = list(self.edit_widget.keys())[index]
                retrieved_text_index = optionmenu_widget["menu"].index(inputs[index])

                # if the option_menu has a "add new part" menu,
                # the selectable options will start from 1 rather than 0,
                # therefore, the index must be minus 1
                if optionmenu_widget.has_add_new_menu:
                    retrieved_text_index -= 1
                text_var = optionmenu_widget.options[retrieved_text_index]
                var_labels[index].configure(textvariable=text_var)
                self.variables[row].set_attr(self.columns[index].title, text_var)

        return True

    def config_edit_widgets(self, frame = None):
        for widget in self.entry_widgets.keys():
            if isinstance(widget, tk.Entry):
                variable = tk.StringVar()
                entry = tk.Entry(frame, textvariable=variable, cnf=Form.entryStyle)
                self.edit_widget[entry] = variable

            elif isinstance(widget, DynamicOptionMenu):
                variable = tk.StringVar()
                opMenu = DynamicOptionMenu(frame, variable, widget.options, has_add_new_menu = widget.has_add_new_menu,
                                           add_new_menu_label = widget.add_new_menu_label, add_new_menu_callback = widget.add_new_menu_callback)
                # if opMenu.has_add_new_menu:
                #     opMenu["menu"].insert_command(index = 0, label = "New Part", command = self.add_new_part, background = "yellow", foreground = "red")
                opMenu.configure(background="white", relief="groove", borderwidth=1, height=1, width=10,
                                 highlightcolor="white", highlightthickness=1)
                opMenu["menu"].configure(cnf=Form.option_menuStyle)
                self.edit_widget[opMenu] = variable
            else:
                variable = tk.StringVar()
                retrieved_menus = widget["menu"]
                num_of_menu = retrieved_menus.index("end") + 1
                options = [retrieved_menus.entrycget(index, "label") for index in range(num_of_menu)]
                opMenu = tk.OptionMenu(frame, variable, *options)
                opMenu.configure(background="white", relief="groove", borderwidth=1, height=1, width=10,
                                 highlightcolor="white", highlightthickness=1)
                opMenu["menu"].configure(cnf=Form.option_menuStyle)
                self.edit_widget[opMenu] = variable

    def get_textvariable_from_text(self, text, options):
        """
        this function is called to get the textvariable from a options of a dynamic_option_menu using a given text input
        :param text: an user input to dynamic_option_menu
        :param options: list of options in a dynamic_option_menu
        :return: textvariable
        """




if __name__ == "__main__":
    root = tk.Tk()
    product = None
    form = BomForm(product, root, columns=tuple([Column(x, nullable=False) for x in ("Part", "Unit", "Quantity")]),
                width=200)
    var1 = tk.StringVar()
    var1.set("New Agent")
    var2 = tk.StringVar()
    var2.set("Part A")
    form.add_input_by_dynamic_option(0, [var1, var2])
    form.add_input_by_option(1, ["pcs", "kg", "ml", "L"])
    form.add_input_by_entry(2)
    form.setup_fun_buttons()
    form.config_newpart_button()

    var3 = tk.StringVar()
    var3.set("Part B")
   # form.update_dynamic_optionmenu(0, var3)

    form.pack()

    tk.mainloop()
