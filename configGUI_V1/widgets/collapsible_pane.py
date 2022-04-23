import tkinter as tk
from static.css import CollapsiblePaneStyle
from tkinter import ttk


class CollapsiblePane(tk.Frame):
    """
     -----USAGE-----
    collapsiblePane = CollapsiblePane(parent,
                          expanded_text =[string],
                          collapsed_text =[string])

    collapsiblePane.pack()
    button = Button(collapsiblePane.frame).pack()
    """

    def __init__(self, master, text = None, **kwargs):

        tk.Frame.__init__(self, master, **kwargs)

        # These are the class variable
        # see a underscore in expanded_text and _collapsed_text
        # this means these are private to class
        self.master = master
        self._variable = True
        #self.config(bg = "white")


        # Create two labels to be added to the first row
        self.exp_label_frame = tk.Frame(self, width = 2)
        self.exp_label_frame.grid(row = 0, column  =0, padx = 0, sticky = tk.NS)
        self.exp_label_frame.grid_propagate(0)
        self.expanded_label = tk.Label(self.exp_label_frame, text = "-", heigh = 1, width = 2)
        self.expanded_label.pack(fill = "both", expand = 1)

        self.name_label_frame = tk.Frame(self)
        self.name_label_frame.grid(row = 0, column=1, sticky = tk.NSEW)
        self.name_label = tk.Label(self.name_label_frame, textvariable = text, height = 1, anchor = tk.W)
        self.name_label.pack(fill = "both", expand = 1)


        # self.expanded_label = tk.Label(self, text = " - ", height = 1, width = 2, bg = "white")
        # self.expanded_label.grid(row = 0, column  =0, padx = 0, sticky = tk.NS)
        # #self.expanded_label.pack(fill = tk.BOTH, side = tk.LEFT)
        # self.name_label = tk.Label(self, textvariable = text, height = 1, anchor = tk.W, bg = "white")
        # #self.info_label.pack(fill = tk.BOTH, expand = 1, side = tk.LEFT)
        # self.name_label.grid(row = 0, column=1, sticky = tk.NSEW)
        self.expanded_label.bind("<Button-1>", lambda x: self._activate(x))
        #self.name_label.bind("<Double-Button-1>", lambda x: self._activate(x))


        # Here weight implies that it can grow it's
        # size if extra space is available
        # default weight is 0
        self.columnconfigure(1, weight=1)

        # define a frame to contain the Collapsible items
        self.frame = tk.Frame(self)
        self.frame.grid(row=1, columnspan=2, sticky = tk.W)

        # the index of the next empty row on self.frame
        self.next_row = 0


    def _activate(self, event = None):
        self._variable = not self._variable
        if self._variable:
            self.expanded_label.configure(text=" + ")
            self.frame.grid_remove()
        else:
            self.expanded_label.configure(text=" - ")
            self.frame.grid_configure()

    def _fill_gap(self):
        tk.Label(self.frame, width=2).grid(row=self.next_row, column=0)

    def add_item_to_configframe(self, item_name, item = None):

        if item:
            self._fill_gap()
            item.master = self.frame
            item.grid(row = self.next_row, column = 1, cnf=CollapsiblePaneStyle.grid_item_c1)
            self.next_row +=1
        else:
            item_label = tk.Label(self.frame, anchor="w")
            if isinstance(item_name, tk.StringVar):
                item_label.config(textvariable=item_name)
            else:
                item_label.config(text=item_name)

            #self._fill_gap()
            item_label.grid(row=self.next_row, column = 1, cnf=CollapsiblePaneStyle.grid_item_c1)

            #
            # item = tk.Label(self.frame, text=" ", width=2, cnf=CollapsiblePaneStyle.item_in_frame)
            #
            # item.grid(row=self.next_row, column=1, cnf=CollapsiblePaneStyle.grid_item_c2)
            self.next_row +=1
            return item_label

    def remove_item_from_configframe(self, item):

        item.grid_forget()
        del item



