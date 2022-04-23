import tkinter as tk
import tkinter.ttk as ttk


class CollapsiblePanedFrame(ttk.Frame):
    '''
    A frame used to manage sub-windows, showing of which can be opene and closed like Treeview

    '''

    def __init__(self, master = None, **kwargs):

        super().__init__(master, **kwargs)

        self._children = {} # key = pane_id, value = pane


    def add_pane(self, text, open = True, iid = None, **kw):
        '''
        :param text: heading of the pane to be added
        :param open: if True, window of the pane will be shown
        :param kw: STANDARD ttk.Frame initialisation options
        :return: pane ID
        '''

        kw['text'] = text
        kw['open'] = open

        pane = CollapsiblePane(self, **kw)
        pane.pack(side='top', anchor = 'nw', fill = 'both')

        id = str(iid) if iid else 'I%03d' % (len(self._children) + 1)
        self._children[id] = pane

        return pane


    def get_pane(self, iid):

        try:
            pane = self._children[iid]
            return pane

        except KeyError as e:
            raise e

    def remove_pane(self, pane_id):
        """
        pane_id: can be either the pane's iid or pane instance itself
        """
        if pane_id.__class__.__name__ != 'str':
            pane = pane_id
        else:
            pane = self.get_pane(pane_id)

        pane.pack_forget()

    def heading_configure(self, iid, **kw):

        """
        :param iid: pane's id. Set iid = 'all' to apply the new configuration to all panes
        :param kw: STANDARD ttk.Label options
        """
        style = ttk.Style()
        if iid == 'all':
            style.configure('IndicatorLabel', **kw)
        else:
            pane = self.get_pane(iid)
            pane.heading_style = '%s.IndicatorLabel' % iid

            if pane.heading['style'] != pane.heading_style:
                pane.heading.configure(style = pane.heading_style)

            pane.heading_configure(**kw)

    def pane_configure(self, iid, **kw):
        '''
        :param iid: pane's id. Set iid = 'all' to apply the new configuration to all panes
        :param kw: STANDARD ttk.Frame options
        '''
        style = ttk.Style()
        if iid == 'all':
            style.configure('ContainerPane.TFrame', **kw)
        else:
            pane = self.get_pane(iid)
            pane.pane_style = '%s.ContainerPane.TFrame' % iid
            if pane.pane['style'] != pane.pane_style:
                pane.pane.configure(style=pane.pane_style)
            pane.pane_configure(**kw)


class CollapsiblePane(ttk.Frame):

    def __init__(self, master = None, **kwargs):

        '''
        A frame which has a built-in label with indicator attached.

        Contents in this frame is organised in GRID layout

        the indicator images size is (10, 10). Indicator images can be changed
        by changing the image file path in the __init_style function
        '''

        self.open = True  # if open = True, the pane is unfolded and the collapsible indicator (e.g., + or -) is <close>

        if 'text' in kwargs:
            self.heading_text = kwargs.get('text')
            del kwargs['text']

        if 'open' in kwargs:
            self.open = kwargs.get('open')
            del kwargs['open']

        super().__init__(master, **kwargs)

        self.style = ttk.Style()
        try:
            # check if the new style has been loaded to ttk.Style()
            self.style.layout('IndicatorLabel')
        except:
            self.__init_style()

        self.__init_pane()

        self.heading_style, self.pane_style = 'IndicatorLabel', 'ContainerPane.TFrame'

        self.next_row = 0
        self.max_col = 1
        self.next_row = lambda x: self.pane.grid_size()[1] if x else self.pane.grid_size()[1] - 1


    def __init_pane(self, **kw):

        self.heading = ttk.Label(self, text = self.heading_text, style = 'IndicatorLabel')
        self.heading.pack(side = 'top', anchor = 'nw', fill = 'x')
        self.heading.bind("<Button-1>", self.on_press_indicator, True)

        self.pane = ttk.Frame(self, style = 'ContainerPane.TFrame')
        self.pane.pack(side = 'top', anchor = 'nw', fill = 'both')


    def on_press_indicator(self, event):

        '''
        Called when the indicator button is pressed.

        Remember: because the new style <IndicatorLabel> is applied to the heading label,
                  so it is the label's state this function should change rather than the
                  whole frame
        '''

        widget = event.widget
        element = widget.identify(event.x, event.y)

        if "toggle" in element:

            if not widget.instate(['pressed']):
                state = "pressed"
            else:
                state = "!pressed"

            widget.state([state])

    def heading_configure(self, **kw):
        """
        kw: STANDARD ttk.Label options
        """
        self.style.configure(self.heading_style, **kw)

    def pane_configure(self, **kw):
        """
        kw: STANDARD ttk.Frame options
        """
        self.style.configure(self.pane_style, **kw)


    def grid_item(self, item:tk.Widget, label:str = None, **kw):
        """
        :param kw: STANDARD Grid options
        :return:
        """
        # if grid options are not given, the item is placed at front of the next row by default
        next_column = 0
        if not kw:

            if label:
                label = ttk.Label(self.pane, text = label)
                label.grid(row = self.next_row, column = next_column)
                next_column += 1

            if not item.master:
                item.master = self.pane
                item.grid(row = self.next_row, column = next_column)
                
        else:




    def __init_style(self):

        self._load_images()

        self.style.element_create("toggle", "image", 'img_close',
                             ('pressed','img_open'),
                             ("!pressed", "img_close"), padding = 10, sticky='')

        self.style.layout('IndicatorLabel',[('IndicatorLabel.border', {'sticky': 'nswe',
                                                                  'border': '1',
                                                                  'children': [('IndicatorLabel.padding', {'sticky': 'nswe',
                                                                                                           'border': '1',
                                                                                                           'children': [
                                                                                                               ('IndicatorLabel.toggle', {'side': 'left', 'sticky':''}),
                                                                                                               ('IndicatorLabel.label', {'side': 'left','sticky': 'nswe'})]})]})])
        self.style.configure('ContainerPane.TFrame', )


    def _load_images(self):
        from PIL import Image, ImageTk
        from configGUI_V1 import PROJECT_BASE_DIR
        import os

        image_size = (10, 10)
        with Image.open(PROJECT_BASE_DIR + os.sep + '/images/icons/indicator_open.png') as img:
            img = img.resize(image_size, Image.ANTIALIAS)
            self.img_open = ImageTk.PhotoImage(img, name='img_open')

            if not self.open:
                self.img_default = ImageTk.PhotoImage(img, name='img_default')

        with Image.open(PROJECT_BASE_DIR + os.sep + '/images/icons/indicator_close.png') as img:
            img = img.resize(image_size, Image.ANTIALIAS)
            self.img_close = ImageTk.PhotoImage(img, name='img_close')

            if self.open:
                self.img_default = ImageTk.PhotoImage(img, name='img_default')





if __name__ == '__main__':

    # with open(PROJECT_BASE_DIR + os.sep + '/images/icons/add.ico', 'rb') as file:
    #     str = base64.b64encode(file.read())
    #     print(str)

    # icon_sizes = [(16, 16)]
    # with Image.open(PROJECT_BASE_DIR + os.sep + '/images/icons/add.png') as img:
    #     img = img.resize((16, 16), Image.ANTIALIAS)
    #     img.save(PROJECT_BASE_DIR + os.sep + '/images/icons/add_icon.png')
    #
    root = tk.Tk()
    # frame = CollapsiblePane(root, text = 'yahoo', width = 200, height = 200, borderwidth = 2)
    # frame.pane_configure(background = 'red', width = 200, height = 200)
    # frame.heading_configure(borderwidth = 2)
    # frame.pack()
    # frame.pack_propagate(0)

    frame = CollapsiblePanedFrame(root, width = 500, height = 500)
    frame.pack()
    frame.pack_propagate(0)
    frame.add_pane('google', iid='001')
    frame.add_pane('yahoo', iid = '002')
    frame.pane_configure('001', background = 'red')
    root.mainloop()

