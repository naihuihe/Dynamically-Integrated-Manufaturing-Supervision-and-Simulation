import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from PIL import Image, ImageTk

from data_models.resource import VariableContent
from static.css import FormStyle
from widgets.dynamic_optionmenu import DynamicOptionMenu
from widgets.form import Form
from widgets.popup_window import PopupWindow
from widgets.tooltip import CreateToolTip


class DisplayForm(tk.Frame):

    def __init__(self, master = None, method = 'GET', **kwargs):
        """
        :param master:
        :param method: "GET" ==> collect and display input information, "POST" ==> display information
        :param kwargs: STANDARD tk.Frame OPTIONS
                     + widget SPECIFIC OPTIONS [agent: agent_model, columns:(), has_seq_column: boolean]
        """
        self.method = method
        # agent which the form belongs to
        self.agent = None

        # [Column,] ==> list of Column instances
        self.columns = ()

        # dict: key: row_index, value: DynamicVariable()
        self.data = {}

        # if true, a sequence column is added to the form by default as the first column
        # in addition to the columns given above
        self.has_seq_column = 0

        if "agent" in kwargs:
            self.agent = kwargs.get("agent")
            del kwargs["agent"]
        if "columns" in kwargs:
            self.columns = kwargs.get('columns')
            del kwargs['columns']
        if 'has_seq_column' in kwargs:
            self.has_seq_column = 1 if kwargs.get('has_seq_column') else 0
            del kwargs['has_seq_column']

        super().__init__(master, **kwargs)

        self.next_row = 0 if not self.columns else 1
        self.num_columns = 1 if not self.columns else len(self.columns)

        self.highlighted_row = None

        if self.method == "GET":
            self.entry_widgets = {}
            self.edit_widgets = {}


    def add_column_titles(self):

        if self.has_seq_column:
            tk.Label(self, text="No.", cnf=FormStyle.sequence_label).grid(row=0, column=0)

        if self.columns:
            for column in range(self.num_columns):
                column_title = self.columns[column].title
                label = tk.Label(self, text=column_title if self.columns[column].nullable else column_title + "*",
                                 cnf=FormStyle.label)
                label.grid(row=0, column=column + self.has_seq_column, sticky="nsew")

        # this is an additional column reserved for placing functional widgets, e.g, "Add", "edit" or "remove" button
        tk.Label(self, text="", width=18, cnf=FormStyle.label, relief="flat").grid(row=0,
                                                                                   column=self.num_columns + self.has_seq_column)

    def add_entry(self, column, input:tk.StringVar = None):
        """
        add a "tk.Entry" widget to the last row of the form to receive user input
        :param input: tk.StringVar
        :param column: the index of the column
        :return:
        """
        input = tk.StringVar() if not input else input
        entry = tk.Entry(self, textvariable=input, cnf=FormStyle.entry)
        entry.grid(row=self.next_row, column=column)
        self.entry_widgets[entry] = input

    def add_option_menu(self, column, options, variable:tk.StringVar = None, **kwargs):
        """
        To add a standard tk.OptionMenu to the last row of the given column
        for collecting user input
        :param variable: tk.StringVar
        :return:
        """
        variable = variable if variable else tk.StringVar()
        option_menu = tk.OptionMenu(self, variable, *options, **kwargs)
        self._setup_option_menu(option_menu, column)
        self.entry_widgets[option_menu] = variable

        return option_menu

    def add_dynamic_option_menu(self, column, options, variable:tk.StringVar = None, **kwargs):
        """
        :param column:
        :param options: [tk.StringVar()...]
        :param variable:
        :param kwargs: see details in the class file
        :return:
        """
        if not getattr(self, "_dynamic_menu_column_indice", None):
            self._dynamic_menu_column_indice = []
        self._dynamic_menu_column_indice.append(column)

        variable = variable if variable else tk.StringVar()
        option_menu = DynamicOptionMenu(self, variable, options, **kwargs)
        self._setup_option_menu(option_menu, column)
        self.entry_widgets[option_menu] = variable

        return option_menu


    def _setup_option_menu(self, option_menu, column):
        option_menu.configure(cnf=FormStyle.option_menu)
        option_menu.grid(row=self.next_row, column=column)
        option_menu["menu"].configure(cnf=FormStyle.menu)

    def process_input_data(self, is_new_input = True, event = None):
        """
        :param is_new_input:
        :return: [tk.StringVar()...]
        """

        widgets = self.entry_widgets if is_new_input else self.edit_widgets

        # get the inputs from the widgets and put to a list
        input_data = []
        values = [value.get() for value in widgets.values()]

        if not is_new_input:
            for value in widgets.values():
                value.set("")

        if not self.is_input_valid(values):
            messagebox.showerror(message="Please make sure all elements market in * must not be empty")
            return False

        for column in range(self.num_columns):
            if self._is_dynamic_option_column(column):
                optionmenu = list(widgets.keys())[column]
                retrieved_text_index = optionmenu["menu"].index(values[column])

                # if the option_menu has a "add new part" menu,
                # the selectable options will start from 1 rather than 0,
                # therefore, the index must be minus 1
                if optionmenu.has_add_new_menu:
                    retrieved_text_index -= 1
                var = optionmenu.options[retrieved_text_index]
            else:
                var = tk.StringVar()
                var.set(values[column])
            input_data.append(var)

        return input_data


    def save_and_display_data(self, values, event = None):
        """
        :param values: [tk.StringVar()...]
        :return:
        """

        # create a Variable Instance to store the values of inputs
        column_titles = [column.title for column in self.columns] if self.columns else ["undefined"]
        variable = DynamicVariable(column_titles)

        for column in range(self.num_columns):
            label = tk.Label(self, textvariable=values[column], cnf=FormStyle.label)
            label.grid(row=self.next_row, column=column + self.has_seq_column, sticky="nsew")
            label.bind("<Button-1>", lambda event: self.highlight_row(label.grid_info()["row"], event))

            #save data
            variable.set_attr(column_titles[column], values[column])

        # if self.has_seq_column:
        #     tk.Label(self, text = len(self.data), cnf=FormStyle).grid(row = self.next_row, column = 0, sticky = "nsew")
        self.data[self.next_row] = variable
        self.next_row += 1

    def remove_data(self, row, event=None):
        """
        the callback function for the "Edit" button
        :param row: the index of the row to be edited
        :param event:
        :return:
        """
        # if there is sequencing column, get the next sequence number ready
        # recalculate sequential numbers for rows below
        if self.has_seq_column:
            start_seq_number = int(self.grid_slaves(row, 0)[0]["text"])

        # remove the given row
        for widget in self.grid_slaves(row):
            widget.grid_forget()
        del self.data[row]

        if self.rm_frame:
            self.rm_frame.grid_remove()

        if self.has_seq_column:
            self.reset_variables_sequence(row, start_seq_number)
        self.highlighted_row = None


    def reset_variables_sequence(self, start_row, start_seq_number):
        if self.has_seq_column:
            for row in range(start_row, self.next_row):
                if row in self.data.keys():
                    sequence_label = self.grid_slaves(row, 0)[0]
                    sequence_label.configure(text=start_seq_number)
                    start_seq_number += 1

            # do not forget the entry_row
            self.grid_slaves(self.next_row, 0)[0].configure(text = start_seq_number)



    def change_data(self, values, row, event = None):

        # retrieve the display labels
        dis_labels = [self.grid_slaves(row, column + self.has_seq_column)[0] for column in range(self.num_columns)]

        for column in range(self.num_columns):
            dis_labels[column].configure(textvariable = values[column])
            self.data[row].set_attr(self.columns[column].title, values[column])


    def _is_dynamic_option_column(self, column):
        if getattr(self, "_dynamic_menu_column_indice", None):
            if column in self._dynamic_menu_column_indice:
                return True
        return False

    def is_input_valid(self, values):
        """
        Check whether the input data is valid
        :param input_values:
        :return:
        """
        if len(self.columns):
            for index in range(self.num_columns):
                if not values[index] and not self.columns[index].nullable:
                    return False

        return True

    def setup_add_button(self, **kwargs):
        """
        :param kwargs: STANDARD tk.Button options
        :return:
        """
        def callback():
            self.save_and_display_data(self.process_input_data())
            self.reset_entry_row()

        # initialise a frame to place functional buttons related to new variable creation
        self.add_bt_frame = tk.Frame(self)
        self.add_bt_frame.grid(row = self.next_row, column = self.num_columns + self.has_seq_column)

        if 'text' not in kwargs:
            kwargs['text'] = "Add"

        if 'command' not in kwargs:
            kwargs['command'] = callback

        self.add_button = tk.Button(master = self.add_bt_frame, **kwargs)
        self.add_button.pack(side = "left")

    def setup_edit_button(self, **kwargs):

        def callback():
            #self.change_data(self.process_input_data(is_new_input=False), self.highlighted_row)
            self._edit()

        if not hasattr(self, "rm_frame"):
            self.rm_frame = tk.Frame(self)

        # set a defaut icon to the button
        if "text" not in kwargs and "textvariable" not in kwargs and "image" not in kwargs:
            image = self._get_default_bt_icon('edit')

        if 'command' not in kwargs:
            kwargs['command'] = callback

        self.edit_button = tk.Button(self.rm_frame, image = image, **kwargs)
        self.edit_button.pack(side = 'left')
        CreateToolTip(self.edit_button, text='Edit')

    def setup_remove_button(self, **kwargs):

        def callback():
            self.remove_data(self.highlighted_row)

        if not hasattr(self, "rm_frame"):
            self.rm_frame = tk.Frame(self)

        # set a defaut icon to the button
        if "text" not in kwargs and "textvariable" not in kwargs and "image" not in kwargs:
            image = self._get_default_bt_icon('delete')

        if 'command' not in kwargs:
            kwargs['command'] = callback

        self.remove_button = tk.Button(self.rm_frame, image = image, **kwargs)
        self.remove_button.pack(side = "left")
        CreateToolTip(self.edit_button, text='Delete')



    def _get_default_bt_icon(self, bt_name:['edit','remove','up','down']):
        img_home_dir = os.path.split(os.getcwd())[0] + os.sep + 'images'
        for img in os.listdir(img_home_dir):
            if bt_name in img:
                img_dir = img_home_dir + os.sep + img
        image = self.load_bt_icon(img_dir)
        setattr(self, bt_name + '_icon', image)

        return image

    def load_bt_icon(self, path, size:() = (15, 15)):
        with Image.open(path) as img:
            icon = img.resize(size, Image.ANTIALIAS)

        return ImageTk.PhotoImage(icon)

    def _edit(self):
        """
        Callback function for the <Edit> Button if there is
        :return:
        """

        if not hasattr(self, '_edit_window'):
            self.__init_edit_window()
        else:
            try:
                self.__edit_window.deiconify()
            except:
                print("edit_window was destroyed")
        self._load_data_to_edit_window()
        self.__edit_window.grab_set()

    def _load_data_to_edit_window(self):
        """
        This method will load the existing variable information to the edit window
        :return:
        """
        var_labels = [self.grid_slaves(self.highlighted_row, column + self.has_seq_column)[0] for column in range(self.num_columns)]
        edit_widget_values = list(self.edit_widgets.values())
        for index in range(self.num_columns):
            edit_widget_values[index].set(var_labels[index]["text"])


    def __init_edit_window(self):

        def cancel_callback():
            self.__edit_window.withdraw()
            self.__edit_window.grab_release()

        def confirm_callback():
            data = self.process_input_data(is_new_input=False)
            if data is not False:
                self.change_data(data, self.highlighted_row)
                cancel_callback()

        self.__edit_window = EditWindow("Edit")
        self.__edit_window.focus_set()
        self.__edit_frame = self.__edit_window.input_frame
        self.__edit_window.cancel_button.configure(command=cancel_callback)
        self.__edit_window.confirm_button.configure(command=confirm_callback)

        self.setup_edit_widgets(self.__edit_frame)

        edit_widget_list = list(self.edit_widgets.keys())
        for index in range(self.num_columns):
            text = self.columns[index].title if self.columns[index].nullable else self.columns[index].title + "*"
            tk.Label(self.__edit_frame, text=text + ":",
                     font=("Arial", 11, "bold")).grid(row=index, column=0, sticky="w")
            edit_widget_list[index].grid(row=index, column=1, sticky="w")


    def setup_edit_widgets(self, frame):

        for widget in self.entry_widgets.keys():
            variable = tk.StringVar()
            if isinstance(widget, tk.Entry):
                entry = tk.Entry(frame, textvariable=variable, cnf=Form.entryStyle)
                self.edit_widgets[entry] = variable

            elif isinstance(widget, DynamicOptionMenu):
                opMenu = DynamicOptionMenu(frame, variable, widget.options, static_values = widget.static_values, has_add_new_menu=widget.has_add_new_menu,
                                           add_new_menu_label=widget.add_new_menu_label,
                                           add_new_menu_callback=widget.add_new_menu_callback)
                opMenu.configure(cnf=FormStyle.option_menu)
                opMenu["menu"].configure(cnf=FormStyle.menu)
                self.edit_widgets[opMenu] = variable
            else:
                retrieved_menus = widget["menu"]
                num_of_menu = retrieved_menus.index("end") + 1
                options = [retrieved_menus.entrycget(index, "label") for index in range(num_of_menu)]
                opMenu = tk.OptionMenu(frame, variable, *options)
                opMenu.configure(cnf=FormStyle.option_menu)
                opMenu["menu"].configure(cnf=FormStyle.menu)
                self.edit_widgets[opMenu] = variable

    def reset_entry_row(self):
        """
        the entry row is the last row in the form.

        It gives users a blank row with Entry or Menu widget to input data
        :return:
        """
        if(self.has_seq_column):
            tk.Label(self, text=len(self.data) + 1, cnf = FormStyle.sequence_label).grid(row = self.next_row, column = 0)

        for widget in self.entry_widgets.keys():
            widget.grid_configure(row = self.next_row)
        for value in self.entry_widgets.values():
            value.set("")
        self.add_bt_frame.grid_configure(row = self.next_row)

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



class EditWindow(PopupWindow):

    def destroy(self):
        self.withdraw()
        self.grab_release()

class Column:

    def __init__(self, title, nullable = True):
        """
        :param title:
        :param value_type: str, bool, float, int
        :param nullable:
        """
        self.title = title
        self.nullable = nullable


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



if __name__=="__main__":
    root = tk.Tk()
    columns = (Column("Item1"), Column("Item2"), Column("Item3"))
    frame = DisplayForm(root, columns = columns, has_seq_column=True)
    frame.add_column_titles()
    frame.add_option_menu(1, [1,2,3])
    frame.add_entry(2)
    frame.add_entry(3)

    frame.pack()
    frame.setup_add_button()
    frame.setup_edit_button()
    frame.setup_remove_button()
    frame.reset_entry_row()


    root.mainloop()

    # from tkinter import *
    # import tkinter
    # import tkinter.messagebox
    # from PIL import Image
    # from PIL import ImageTk
    #
    # master = Tk()
    #
    #
    # def callback():
    #     print("click!")
    #
    #
    # width = 50
    # height = 50
    # img = Image.open("edit_icon.jpg")
    # img = img.resize((width, height), Image.ANTIALIAS)
    # photoImg = ImageTk.PhotoImage(img)
    # b = Button(master, image=photoImg, command=callback, width=50)
    # b.pack()
    # mainloop()



