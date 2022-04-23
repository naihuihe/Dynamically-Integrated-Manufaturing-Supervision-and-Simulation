from tkinter import ttk

class ScrolledFrame(ttk.Frame):

    def __init__(self, master = None, **kwargs):

        '''
        A Frame with scroll bars fitted by default.
        To use this frame, the child window appended must support xview and yview.
        '''

        super().__init__(master, **kwargs)

        self.__h_scroll = ttk.Scrollbar(self, orient = 'horizontal')
        self.__v_scroll = ttk.Scrollbar(self, orient = 'vertical')



    def set_scroll_to_window(self, child, orient = 'both'):
        '''
        used to configure the scroll bar to the child window (that to be scrolled)

        NB: if child is Canvas, please set up the scrollregion in canvas separately

        '''
        if child.master == self:
            if orient == 'horizontal':
                self.__config_h_scroll(child)
            elif orient == 'vertical':
                self.__config_v_scroll(child)
            elif orient == 'both':
                self.__config_h_scroll(child)
                self.__config_v_scroll(child)
            else:
                raise Exception ('orient %s error, must be - horizontal, vertical, or both' % orient)
        else:
            raise Exception ('%s is not child of this frame' % child)


    def __config_h_scroll(self, child):
        try:
            self.__h_scroll.configure(command=child.xview)
            child.configure(xscrollcommand=self.__h_scroll.set)
        except:
            self.__h_scroll.configure(command=self.xview)
            self.configure(xscrollcommand=self.__h_scroll.set)

        self.__h_scroll.pack(side='bottom', fill='x')

    def __config_v_scroll(self, child):
        try:
            self.__v_scroll.configure(command=child.yview)
            child.configure(yscrollcommand=self.__v_scroll.set)
        except:
            self.__v_scroll.configure(command=self.yview)
            self.configure(yscrollcommand=self.__v_scroll.set)
        self.__v_scroll.pack(side = 'right', fill = 'y')