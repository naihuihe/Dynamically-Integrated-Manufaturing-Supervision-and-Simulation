from tkinter import ttk

class ScrolledFrame(ttk.Frame):

    def __init__(self, master = None, **kwargs):

        '''
        A Frame with built-in scroll bars fitted
        To use this frame, the scroll_window packed must support xview and yview.
        '''

        super().__init__(master, **kwargs)

        self.__h_scroll = ttk.Scrollbar(self, orient = 'horizontal')
        self.__v_scroll = ttk.Scrollbar(self, orient = 'vertical')


    def set_scroll_to_window(self, scroll_window, orient = 'both'):
            '''
            used to configure the scroll bar to the scroll_window (that to be scrolled)

            NB: if scroll_window is Canvas, please set up the scrollregion in canvas separately

            '''
            self.scroll_window = scroll_window

            # scroll window by pressing mouse right-button
            self.scroll_window.bind("<Button-3>", self.__start_scroll)
            self.scroll_window.bind("<B3-Motion>", self.__update_scroll)
            self.scroll_window.bind("<ButtonRelease-3>", self.__stop_scroll)

            if scroll_window.master == self:
                if orient == 'horizontal':
                    self.__config_h_scroll(scroll_window)
                elif orient == 'vertical':
                    self.__config_v_scroll(scroll_window)
                elif orient == 'both':
                    self.__config_h_scroll(scroll_window)
                    self.__config_v_scroll(scroll_window)
                else:
                    raise Exception ('orient %s error, must be - horizontal, vertical, or both' % orient)
            else:
                raise Exception ('%s is not scroll_window of this frame' % scroll_window)


    def __config_h_scroll(self, scroll_window):
        try:
            self.__h_scroll.configure(command=scroll_window.xview)
            scroll_window.configure(xscrollcommand=self.__h_scroll.set)
        except:
            self.__h_scroll.configure(command=self.xview)
            self.configure(xscrollcommand=self.__h_scroll.set)

        self.__h_scroll.pack(side='bottom', fill='x')

    def __config_v_scroll(self, scroll_window):
        try:
            self.__v_scroll.configure(command=scroll_window.yview)
            scroll_window.configure(yscrollcommand=self.__v_scroll.set)

        except:
            self.__v_scroll.configure(command=self.yview)
            self.configure(yscrollcommand=self.__v_scroll.set)
        self.__v_scroll.pack(side = 'right', fill = 'y')

    def __start_scroll(self, event):

        # set the scrolling increment.
        # value of 0 is unlimited and very fast
        # set it to 1,2,3 or whatever to make it slower
        self.scroll_window.config(yscrollincrement=3)
        self.scroll_window.config(xscrollincrement=3)

        self._starting_drag_position = (event.x, event.y)

        self.scroll_window.config(cursor="fleur")

    def __update_scroll(self, event):

        deltaX = event.x - self._starting_drag_position[0]
        deltaY = event.y - self._starting_drag_position[1]

        self.scroll_window.xview('scroll', deltaX, 'units')
        self.scroll_window.yview('scroll', deltaY, 'units')

        self._starting_drag_position = (event.x, event.y)

    def __stop_scroll(self, event):

        # set scrolling speed back to 0, so that mouse scrolling
        # works as expected.
        self.scroll_window.config(xscrollincrement=0)
        self.scroll_window.config(yscrollincrement=0)

        self.scroll_window.config(cursor="")
