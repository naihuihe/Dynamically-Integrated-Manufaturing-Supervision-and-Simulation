import tkinter.ttk as ttk

class ConfigPanel(ttk.Frame):

    """
    The config_panel is created for each agent when initialised,
    where users can define the detailed variables and parameters for the agent
    """

    def __init__(self, agent, master = None, **kwargs):
        """
        :param agent:
        :param master:
        :param kwargs: STANDARD ttk.Frame options
        """

        super().__init__(master, **kwargs)

        self.agent = agent
        self.panels = {}
        self.__init_panel()


    def __init_panel(self):
        self.heading = ttk.Label(self, text = '%s \'s Configuration' % self.agent.name, style = 'ConfigPanelHeading.TLabel')
        self.heading.pack(side = 'top', fill = 'x')
        self.book = ttk.Notebook(self, style = 'Config.TNotebook')
        self.book.pack(side = 'top', fill = 'both')

    def add_new_panel(self, text, panel_id: str = None):
        """
        add a new child window - CollapsiblePanedFrame to the panel
        :param text: book's heading
        :param panel_id:
        :return: panel_id
        """
        from widgets.collapsible_panedframe import CollapsiblePanedFrame

        panel = CollapsiblePanedFrame(self)
        id = panel_id

        if not id:
            id = 'B%02d' % (len(self.panels) + 1)

        self.panels[id] = panel
        self.book.add(panel, text = text)

        return panel


    def get_panel(self, panel_id):
        try:
            panel = self.panels[panel_id]
            return panel
        except KeyError as e:
            print('Can not find a panel with id %s' % panel_id)
            raise e

    def update_heading(self):
        self.heading.configure(text = '%s \'s Configuration' % self.agent.name)


#=================================== ttk widgets with customised style ===============================================
#
# for details of styles, please refer to main.__init__

class Entry(ttk.Entry):

    def __init__(self, *args, **kwargs):

        if 'command' in kwargs:
            self.command = kwargs.get('command')
            del kwargs['command']
        else:
            self.command = self.__command

        kwargs['style'] = 'ConfigPanelEntry.TEntry'

        super().__init__(*args, **kwargs)

        self.__origin_value = self.get()

        self.bind('<Return>', self.__on_press_return)
        self.bind('<FocusOut>', self.__on_focusout)


    def __on_press_return(self, event):
        self.master.focus()

    def __on_focusout(self, event):
        self.command(event)
        self.__origin_value = self.get()

    def __command(self, event):
        pass

    def get_origin_value(self):
        return self.__origin_value


class Label(ttk.Label):

    def __init__(self, *args, **kwargs):

        kwargs['style'] = 'ConfigPanelItemLabel.TLabel'

        super().__init__(*args, **kwargs)


