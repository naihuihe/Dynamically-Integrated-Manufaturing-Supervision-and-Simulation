import tkinter as tk
from tkinter import messagebox

from data_models.resource import VariableContent
from widgets.dynamic_optionmenu import DynamicOptionMenu
from widgets.popup_window import PopupWindow

class EditWindow(PopupWindow):

    def destroy(self):
        self.withdraw()
        self.grab_release()

class Column:

    def __init__(self, title, nullable = True):
        self.title = title
        self.nullable = nullable

    def set_value(self, value):
        self.value = value

    def get_value(self):
        try:
            return self.value.get()
        except ValueError:
            print("Value is not given")

    def is_value_valid(self):
        try:
            return self.nullable if not self.value.get() else True
        except ValueError:
            print("Value is not given")



class Form(tk.Frame):

    labelStyle = {"width": "10",
                  "anchor": "center",
                  "font": ("Arial, 10"),
                  "relief": "sunken",
                  "borderwidth": "1",
                  "highlightbackground": "black",
                  "highlightthickness": "1"
                  }

    sequenceStype = {"width": "4",
                     "anchor": "center",
                     "font": ("Arial, 10"),
                     "relief": "sunken",
                     "borderwidth": "1",
                     "background": "white"
                    }

    entryStyle = {"width": "12",
                  "font": ("Arial, 11"),
                  "bg": "white",
                  "relief": "groove",
                  "borderwidth": "1"
                  }

    option_menuStyle = {
                  "font": ("Arial, 11"),
                  "bg": "white",
                  "borderwidth": "1",
                  "relief": "raised",
                  "borderwidth": "1"
                  }


    def __init__(self, agent = None, master = None,  columns = (), has_seq_column = False, **kwargs):

        super().__init__(master, **kwargs)

        # the agent which the form belongs to
        self.agent = agent

        self.has_seq_column = 1 if has_seq_column else 0

        # columns in the form
        # list [class _ Column_]
        self.columns = columns

        # Dict: key = column title, value = column index of this column (i.e., 0, 1, 2...)
        self.column_indice = {}
        if columns:
            self.set_form_columns(columns)
        else:
            self.num_columns = 1

        # next row to for new varaible inputs
        self.next_row = 1

        # The entry widget is placed at the bottom of the form, which is used to get new inputs from users
        # A dict: key = entry widget, value = textvariable
        self.entry_widgets = {}

        # the index of the row which is selected
        self.highlighted_row = None


        # a Toplevel popup window to edit an existing variable
        self.__edit_window = None
        # a frame to be place to the edit_window to contain edit entry widgets
        self.__edit_frame = None
        # the edit widget is place in a popup window to receive the revised input from users for a variable
        # A dict: key = edit widget, value = textvariable
        self.edit_widget = {}


        # a dict to store the input data to the form
        # key = row_index value = variable
        self.variables = {}
        #self.bind("<Leave>", self.reload_entry_widgets)


    def reload_entry_widgets(self, event = None):
        print("checked!")
        x = event.x_root
        y = event.y_root

        area1 = self.grid_bbox(row=self.next_row)
        area0 = self.grid_bbox(row=self.next_row - 1)
        print(self.next_row)
        print(x, y)

        print(area1)
        print(area0)

    def set_form_columns(self, columns):
        """
        this function will be called at the beginning of setting up the form.

        :param columns: a list -  representing the columns to be set in the form, e.g., ["name", "data-type", ...]
        :return: None
        """
        self.columns = columns
        self.num_columns = len(columns)

        if self.has_seq_column:
            tk.Label(self, text = "No.", cnf = Form.labelStyle, width = 6).grid(row = 0, column = 0)

        for column in range(self.num_columns):

            column_title = columns[column].title
            label = tk.Label(self, text=column_title if columns[column].nullable else column_title + "*", cnf=Form.labelStyle)
            label.grid(row=0, column=column + self.has_seq_column, sticky="nsew")

            self.column_indice[columns[column].title] = column + self.has_seq_column

        # this is an additional column reserved for placing functional widgets, e.g, "Add", "edit" or "remove" button
        tk.Label(self, text="", width = 18, cnf=Form.labelStyle, relief = "flat").grid(row=0, column=self.num_columns + self.has_seq_column)


    def get_column_index_by_title(self, column_title):
        return self.column_indice[column_title]


    def add_input_by_entry(self, column):
        """
        this function is called when the value for a cell in a column is received via "tk.Entry" widget
        :param column: the index of the column
        :return:
        """
        value = tk.StringVar()
        entry = tk.Entry(self, textvariable = value, cnf=Form.entryStyle)
        entry.grid(row = self.next_row, column = column)
        self.entry_widgets[entry] = value

    def add_input_by_label(self, column, **kwargs):
        """
        :param column:
        :return:
        """
        if "textvariable" in kwargs:
            textvariable = kwargs.get("textvariable")
            del kwargs["textvariable"]
        else:
            textvariable = tk.StringVar()

        label = tk.Label(self, textvariable = textvariable, cnf = Form.labelStyle, **kwargs)
        label.grid(row = self.next_row, column = column)
        self.entry_widgets[label] = textvariable

    def add_input_by_option(self, column, options, variable = None):
        """
        called when the values in a column is received via "tk.OptionMenu" widget
        :param column: the index of the column
        :param options: a list - for optionnal values given to the "OptionMenu" widget
        :return:
        """
        var_selected = variable if variable else tk.StringVar()
        option_menu = tk.OptionMenu(self, var_selected, *options)
        option_menu.configure(background = "white",relief = "groove", borderwidth = 1, height = 1, width = 10, highlightcolor = "white", highlightthickness = 1)
        option_menu.grid(row = self.next_row, column = column)
        option_menu["menu"].configure(cnf = Form.option_menuStyle)
        self.entry_widgets[option_menu] = var_selected

        return option_menu


    def setup_fun_buttons(self):
        """
        configure the "Add New", "Edit" and "Remove" button to the last column
        :return:
        """
        self.config_add_new_button()
        if self.columns:
            self.config_edit_button()
        self.config_remove_button()


    def remove_variable(self, row, event = None):
        """
        the callback function for the "Edit" button
        :param row: the index of the row to be edited
        :param event:
        :return:
        """
        # if there is sequencing column, get the next sequence number ready
        if self.has_seq_column:
            start_seq_number = int(self.grid_slaves(row, 0)[0]["text"])

        # remove the given row
        for widget in self.grid_slaves(row):
            widget.grid_forget()
        del self.variables[row]
        self.rm_frame.grid_remove()
        self.highlighted_row = None

        # recalculate sequential numbers for rows below
        self.reset_variables_sequence(row, start_seq_number)


    def reset_variables_sequence(self, start_row, start_seq_number):
        if self.has_seq_column:
            for row in range(start_row, self.next_row):
                if row in self.variables.keys():
                    sequence_label = self.grid_slaves(row, 0)[0]
                    sequence_label.configure(text = start_seq_number)
                    start_seq_number += 1


    def add_new_variable(self, event = None):
        """
        A callback function for the <Add New> button
        :param event:
        :return:
        """

        inputs = [value.get() for value in self.entry_widgets.values()]
        if not self.is_input_valid(inputs):
            messagebox.showerror(message="Please make sure all elements market in * must not be empty")
            return

        for index in range(self.num_columns):
            var_label = tk.Label(self, text = inputs[index], background = "white", cnf = Form.labelStyle)
            var_label.grid(row = self.next_row, column = index + self.has_seq_column, sticky = "nsew")
            var_label.bind("<Button-1>", lambda event: self.highlight_row(var_label.grid_info()["row"], event))

        column_titles = [column.title for column in self.columns] if self.columns else ["undefined"]
        variable = VariableContent(column_titles)
        for index in range(self.num_columns):
            variable.set_attr(column_titles[index], inputs[index])

        self.variables[self.next_row] = variable
        if self.has_seq_column:
            tk.Label(self, text = len(self.variables), cnf=Form.sequenceStype).grid(row = self.next_row, column = 0, sticky = "nsew")

        self.next_row += 1
        self.reset_entry_row()


    def change_variable(self, row):
        """
        A callback function for the <confirm> button in the popuped <Edit> Window
        :param row: the index of the row to be edited
        :return:
        """
        inputs = [value.get() for value in self.edit_widget.values()]
        if not self.is_input_valid(inputs):
            messagebox.showerror(message="Please make sure all elements market in * must not be empty")
            return False

        # reset the textvariable for edit_widgets
        for value in self.edit_widget.values():
            value.set("")

        # set new inputs to variable
        var_labels = [self.grid_slaves(row, column+self.has_seq_column)[0] for column in range(self.num_columns)]
        for index in range(self.num_columns):
            var_labels[index].configure(text=inputs[index])
            self.variables[row].set_attr(self.columns[index].title, inputs[index])

        return True


    def is_input_valid(self, input_values):
        """
        Check whether the input data is valid
        :param input_values:
        :return:
        """

        for index in range(self.num_columns):
            if not input_values[index] and not self.columns[index].nullable:
                return False
        return True


    def edit_variable(self):
        """
        this function will show the edit variable window

        It is a callback function for the <Edit> Button
        :return:
        """

        if not self.__edit_window:
            self.__init_edit_window()
            self.show_varinfo_to_edit_window()
        else:
            try:
                self.__edit_window.deiconify()
                self.show_varinfo_to_edit_window()
            except:
                print("edit_window is destroyed")
        self.__edit_window.grab_set()

    def show_varinfo_to_edit_window(self):
        """
        This method will load the existing variable information to the edit window
        :return:
        """
        var_labels = [self.grid_slaves(self.highlighted_row, column + self.has_seq_column)[0] for column in range(self.num_columns)]
        edit_widget_values = list(self.edit_widget.values())
        for index in range(self.num_columns):
            edit_widget_values[index].set(var_labels[index]["text"])

    def config_add_new_button(self, bt_title = None, command = None):

        # initialise a frame to place functional buttons related to new variable creation
        self.add_new_frame = tk.Frame(self)
        self.add_new_frame.grid(row = self.next_row, column = self.num_columns + self.has_seq_column)

        # place an "Add" button to the frame
        self.add_button = tk.Button(self.add_new_frame, text = "Add" if not bt_title else bt_title, width = 20, command = self.add_new_variable if not command else command)
        self.add_button.pack(side = "left")
        self.add_button.configure(background = "white")

    def config_edit_button(self):

        if not hasattr(self, "rm_frame"):
            self.rm_frame = tk.Frame(self)

        self.edit_button = tk.Button(self.rm_frame, text="Edit", width = 9, command=self.edit_variable)
        self.edit_button.pack(side = "left")
        self.edit_button.configure(background="white")

    def config_remove_button(self):

        def callback():
            self.remove_variable(self.highlighted_row)

        if not hasattr(self, "rm_frame"):
            self.rm_frame = tk.Frame(self)
        self.remove_button = tk.Button(self.rm_frame, text="Remove", width = 9)
        self.remove_button.pack(side = "left")
        self.remove_button.configure(background="white", command = callback)


    def __init_edit_window(self):

        def cancel_callback():
            self.__edit_window.withdraw()
            self.__edit_window.grab_release()

        def confirm_callback():
            if self.change_variable(self.highlighted_row):
                cancel_callback()

        self.__edit_window = EditWindow("Edit")
        self.__edit_window.focus_set()
        self.__edit_frame = self.__edit_window.input_frame
        self.__edit_window.cancel_button.configure(command=cancel_callback)
        self.__edit_window.confirm_button.configure(command=confirm_callback)

        self.config_edit_widgets(self.__edit_frame)

        edit_widget_list = list(self.edit_widget.keys())
        for index in range(self.num_columns):
            text = self.columns[index].title if self.columns[index].nullable else self.columns[index].title + "*"
            tk.Label(self.__edit_frame, text=text + ":",
                     font=("Arial", 11, "bold")).grid(row=index, column=0, sticky="w")
            edit_widget_list[index].grid(row=index, column=1, sticky="w")



    def config_edit_widgets(self, frame = None):
        for widget in self.entry_widgets.keys():
            if isinstance(widget, tk.Entry):
                variable = tk.StringVar()
                entry = tk.Entry(frame, textvariable=variable, cnf=Form.entryStyle)
                self.edit_widget[entry] = variable

            else:
                variable = tk.StringVar()
                retrieved_menus = widget["menu"]
                num_of_menu = retrieved_menus.index("end") + 1
                options = [retrieved_menus.entrycget(index, "label") for index in range(num_of_menu)]
                opMenu = tk.OptionMenu(frame, variable, *options)
                opMenu.configure(background = "white",relief = "groove", borderwidth = 1, height = 1, width = 10, highlightcolor = "white", highlightthickness = 1)
                opMenu["menu"].configure(cnf = Form.option_menuStyle)
                self.edit_widget[opMenu] = variable

    def reset_entry_row(self):
        """
        the entry row is the last row in the form.

        It gives users a blank row with Entry or Menu widget to input data
        :return:
        """
        if(self.has_seq_column):
            tk.Label(self, text="", cnf = Form.labelStyle, width = 6).grid(row = self.next_row, column = 0)

        for widget in self.entry_widgets.keys():
            widget.grid_configure(row = self.next_row)
        for value in self.entry_widgets.values():
            value.set("")
        self.add_new_frame.grid_configure(row = self.next_row)

    def highlight_row(self, row, event):

        """
        a callback function when curse clicks a row
        :param row: the index of the row
        :param event: <Button-1>
        :return:
        """

        if self.highlighted_row is None:
            # apply highlight to the row given
            self.appy_highlight_to_row(row)
        else:
            self.de_highlight_row(self.highlighted_row)
            if self.highlighted_row != row:
                # apply highlight to the new row
                self.appy_highlight_to_row(row)
            else:
                self.highlighted_row = None

    def de_highlight_row(self, row):
        """
        a callback function when curse clicks the highlighted row

        it will cancel the effect of highlight and meanwhile hide the <Edit> and <Remove> button on the row
        :param row: the index of the row
        :return:
        """
        for widget in self.grid_slaves(row=row):
            widget.configure(background="white")
        self.rm_frame.grid_remove()
        self.rm_frame.tk_focusNext()

    def appy_highlight_to_row(self, row):
        for widget in self.grid_slaves(row=row):
            widget.configure(background="lightblue")
        self.rm_frame.grid(row=row, column=self.num_columns + 1)
        self.rm_frame.focus_set()
        # update the highlighted row record
        self.highlighted_row = row



    def get_input_value(self, entry_object):
        """
        :param entry_object: Entry/OptionMenu
        :return:
        """
        return self.entry_widgets[entry_object].get()

    def get_varaibles(self):

        pass


if __name__ == "__main__":
    root = tk.Tk()
    # initialise columns
    columns = (
        Column(title="Part", nullable=False),
        Column(title="Unit", nullable=False),
        Column(title="Quantity", nullable=False)
    )

    form = Form(master=root, width =200, columns = columns, has_seq_column=True)
    form.add_input_by_entry(1)
    form.add_input_by_entry(2)
    form.add_input_by_entry(3)
    form.setup_fun_buttons()

    form.pack()

    tk.mainloop()

    # variable = ContentInRow(["name", "value", "type"])
    # variable.set_attr("name", "nihao")
    # print(variable.name)


