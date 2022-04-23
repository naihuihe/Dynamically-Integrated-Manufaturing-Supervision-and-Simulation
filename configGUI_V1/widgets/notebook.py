import tkinter as tk
import tkinter.ttk as ttk

class SurfaceNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab

       called to display surface canvas for agents
    """

    __initialized = False

    def __init__(self, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            SurfaceNotebook.__inititialized = True

        kwargs["style"] = "SurfaceNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None
        self.item_stack = {}

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index
            return "break"

    def on_close_release(self, event):
        """Called when the button is released"""
        if not self.instate(['pressed']):
            return

        element = self.identify(event.x, event.y)
        if "close" not in element:
            # user moved the mouse off of the close button
            return

        index = self.index("@%d,%d" % (event.x, event.y))

        if self._active == index:
            self.forget(index)
            #self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None





    #============================== Customised functions particularly to add surfaces as child items to this Notebook ===============================

    def add_surface(self, surface, tab_id = None, **kw):

        if tab_id:
            self.__map_tab_surface(tab_id, surface)

        # surface is canvas, which is packed in a tk.Frame
        # So it is surface.master <the packed tk.Frame> added to the Notebook
        super().add(surface.master, **kw)
        self.select(surface.master)

    def insert_surface(self, pos, surface, tab_id = None, **kw):

        if tab_id:
            self.__map_tab_surface(tab_id, surface)

        super().insert(pos, surface.master, **kw)
        self.select(surface.master)

    def __map_tab_surface(self, tab_id, surface):
        if not self.item_stack.get(tab_id):
            self.item_stack[tab_id] = surface


    def select_surface_by_tabid(self, tab_id):
        surface = self.item_stack[tab_id]
        try:
            self.select(surface.master)
        except:
            self.add(surface, text = surface.agent.name)


    # =========================================== Style initialisation =============================
    # This can be moved to the global ttk style initialisation function/module,
    # but kept here to facilitate the class to be used separately in somewhere else.

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            tk.PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            tk.PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            tk.PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )

        style.element_create("close", "image", "img_close",
                            ("active", "pressed", "!disabled", "img_closepressed"),
                            ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("SurfaceNotebook", [("SurfaceNotebook.client", {"sticky": "nswe"})])

        # the Notebook.focus subelement is not included in the style layout below
        # in order to remove the'dotted' line around the tab label in classic Notebook
        style.layout('SurfaceNotebook.Tab', [("SurfaceNotebook.tab", {"sticky": "nswe",
                                                                    "children": [('SurfaceNotebook.padding', {'side': 'top',
                                                                                                             'sticky': 'nswe',
                                                                                                             'children': [('SurfaceNotebook.label', {"side": "left", "sticky": ''}),
                                                                                                                          ("SurfaceNotebook.close", {"side": "left", "sticky": ''})
                                                                                                                          ]
                                                                                                             }
                                                                                  )]
                                                                    }
                                             )]
                     )



class ConfigNotebook(ttk.Notebook):


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.__load_default_panels()


    def __load_default_panels(self):
        self.add(ttk.Frame(), text = 'Basic Info')
        self.add(ttk.Frame(), text = 'Layout and Appereance')
        self.add(ttk.Frame(), text = 'Simulation')
        self.add(ttk.Frame(), text = 'D2S Settings')




if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.layout('ConfigNotebook', [("ConfigNotebook.client", {"sticky": "nswe"})])

    style.layout('ConfigNotebook.Tab', [("ConfigNotebook.tab", {"sticky": "nswe",
                                                                  "children": [
                                                                      ('ConfigNotebook.padding', {'side': 'top',
                                                                                                   'sticky': 'nswe',
                                                                                                   'children': [(
                                                                                                                'ConfigNotebook.label', {
                                                                                                                    "side": "left",
                                                                                                                    "sticky": '',
                                                                                                                })
                                                                                                   ]
                                                                                                   }
                                                                       )]
                                                                  }
                                          )]
                 )

    style.configure('Tab', background = 'red', padding = (0, 0, 0, 0), relief = 'groove' )

    book = ConfigNotebook(root, style = 'ConfigNotebook')
    book.pack(fill = 'both', expand = 1)
    book.add(tk.Frame(bg = 'red', width = 200), text = 't1')
    book.add(tk.Frame(bg = 'yellow', width = 200), text = 't2')
    root.mainloop()
