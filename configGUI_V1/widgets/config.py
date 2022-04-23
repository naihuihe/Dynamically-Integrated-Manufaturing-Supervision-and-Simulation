import tkinter as tk
import tkinter.ttk as ttk

from widgets.collapsible_panedframe import CollapsiblePanedFrame


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
        self.heading = ttk.Label(self, text = '%s \'s Properties' % self.agent.name, style = 'Heading.TLabel')
        self.heading.pack(side = 'top', fill = 'x')
        self.book = ttk.Notebook(self, style = 'Config.TNotebook')
        self.book.pack(side = 'top', fill = 'both')

        self._init_default_panels()

    def _init_default_panels(self):
        self.add_new_panel(text = 'Agent modelling', panel_id = 'agent_modelling_panel')

    def add_new_panel(self, text, panel_id: str = None):
        """
        add a new book window to the config_panel(Notebook)
        :param text: book's heading
        :param panel_id:
        :return: panel_id
        """
        panel = CollapsiblePanedFrame(self)
        id = panel_id

        if not id:
            id = 'B%02d' % (len(self.panels) + 1)

        self.panels[id] = panel
        self.book.add(panel, text = text)

        return id
