import tkinter.ttk as ttk


class ConfigFrame (ttk.Frame):

    '''
    A frame managest a set of children widgets (usually Frame)
    But each time, only one child is displayed
    '''

    __child_pack_style = {'side': 'top', 'fill': 'both', 'expand': 1}

    def __init__(self, master = None, **kwargs):

        super().__init__(master, **kwargs)

        self.__children = {}
        self.__current = None

    @property
    def current(self):
        return self.__current

    @current.setter
    def current(self, child):
        if self.__current:
            self.__current.pack_forget()
        self.__current = child
        child.pack(self.__child_pack_style)



    def add(self, child, **kw):

        '''
        :param child: child window
        :param kw: [text, iid]
        :return: iid
        '''

        iid = kw.get('iid') if 'iid' in kw else 'I%03d' % (len(self.__children) + 1)

        self.__children[iid] = child
        self.current = child


    def select(self, iid):
        '''
        called to show a child referenced by its idd
        '''
        try:
            child = self.__children[iid]
            self.current = child
        except Exception as e:
            raise e

    def delete(self, iid):

        '''
        Delete a child window by its iid.
        Once deleted, the child window will no longer be managed by the frame
        '''

        try:
            target = self.__children[iid]
            if target == self.current:
                target.pack_forget()
                self.__current = None
            del self.__children[iid]

        except Exception as e:
            raise e

    #
    # def set_current_panel(self, panel):
    #     if self.current_panel:
    #         self.current_panel.hide_panel()
    #
    #     self.current_panel = panel
    #     self.current_panel.reload_panel()
    #
    # def add_scroll(self):
    #     hb = Scrollbar(self, width=10, orient="horizontal", relief="groove")
    #     hb.pack(side="bottom", fill="x")
    #     vb = Scrollbar(self, width=10, orient="vertical", relief="groove")
    #     vb.pack(side="right", fill="y")
    #     # self.config(xscrollcommand = hb.set, yscrollcommand = vb.set)