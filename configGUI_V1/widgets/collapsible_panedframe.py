import tkinter as tk
import tkinter.ttk as ttk

from static.css import ConfigPanel_css

class CollapsiblePanedFrame(ttk.Frame):
    '''
    A frame used to manage sub-windows, showing of which can be opene and closed like Treeview

    '''

    def __init__(self, master = None, **kwargs):

        super().__init__(master, **kwargs)

        self.__children = {} # key = pane_id, value = pane


    def add_pane(self, text, open = True, iid = None, **kw):
        '''
        :param text: heading of the pane to be added
        :param open: if True, window of the pane will be shown
        :param kw: STANDARD ttk.Frame initialisation options
        :return: pane ID
        '''

        kw['text'] = text
        kw['open'] = open

        id = str(iid) if iid else 'I%03d' % (len(self.__children) + 1)

        if self.__children.get(id):
            raise Exception('There is already a pane with id %s' % id)
        else:
            pane = CollapsiblePane(self, **kw)
            pane.pack(side='top', anchor = 'nw', fill = 'both')

            self.__children[id] = pane

            return pane


    def get_pane(self, iid):

        try:
            pane = self.__children[iid]
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
            pane.container_style = '%s.ContainerPane.TFrame' % iid
            if pane.container['style'] != pane.container_style:
                pane.container.configure(style=pane.container_style)
            pane.container_configure(**kw)


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

        self.heading_style, self.container_style = 'IndicatorLabel', 'ContainerPane.TFrame'

        # 1 ==> next row, 0 ==> current row
        self.next_row = lambda x: self.container.grid_size()[1] if x else self.container.grid_size()[1] - 1


    def __init_pane(self):

        self.heading = ttk.Label(self, text = self.heading_text, style = 'IndicatorLabel')
        self.heading.pack(side = 'top', anchor = 'nw', fill = 'x', pady = 2)
        self.heading.bind("<Button-1>", self.__on_press_indicator, True)

        self.container = ttk.Frame(self, style = 'ContainerPane.TFrame')

        # padx = indicator image_size + indicator_image padding + indicator_border + label_border
        # by default, they are 10, 5, 1, 1
        self.container.pack(side = 'top', anchor = 'nw', fill = 'both', padx = 17)


    def __on_press_indicator(self, event):

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
            self.__switch_container_display()


    def __switch_container_display(self):
        self.open = False if self.open else True
        if self.open:
            self.container.pack(side = 'top', anchor = 'nw', fill = 'both', padx = 17)
        else:
            self.container.pack_forget()

    def heading_configure(self, **kw):
        """
        configure the ttk style of the heading label

        kw: STANDARD ttk.Label options
        """
        self.style.configure(self.heading_style, **kw)

    def container_configure(self, **kw):
        """
        configure the ttk style of the container frame

        kw: STANDARD ttk.Frame options
        """
        self.style.configure(self.container_style, **kw)


    def grid_item(self, *args, **kw):
        """
        Use the grid layout to place one or more widgets to the container frame

        The widget(s) is packed to a frame which is then gridded to a cell in the container frame

        If too many widgets are included, it may affect the general grid structure of the container frame,
        therefore, it might be better to just enclose maximum two widgets at the same time but call this function
        multiple times

        :param args: widgets
        :param kw: label <str>: if Label is given, a tk.Label is created and placed at the front of the widget(s).
                   STANDARD tk.grid options
        :return:
        """
        # if grid options are not given, the item is placed to the first column of next row

        from widgets.config import Label

        frame = ttk.Frame(self.container)

        if 'label' in kw:
            label = kw.get('label')
            Label(frame, text = label).pack(ConfigPanel_css.pack_item)
            del kw['label']

        for widget in args:
            widget.master = frame
            widget.pack(ConfigPanel_css.pack_item, in_ = frame)

        if kw:
            kw.update(ConfigPanel_css.grid_item)
            frame.grid(kw, in_ = self.container)
        else:
            frame.grid( ConfigPanel_css.grid_item, in_ = self.container, row = self.next_row(1), column = 0)


    def __init_style(self):

        self._load_images()

        self.style.element_create("toggle", "image", 'default',
                             ('pressed','open'),
                             ("!pressed", "close"), padding = 10, sticky='')

        self.style.layout('IndicatorLabel',[('IndicatorLabel.border', {'sticky': 'nswe',
                                                                  'border': '1',
                                                                  'children': [('IndicatorLabel.padding', {'sticky': 'nswe',
                                                                                                           'border': '1',
                                                                                                           'children': [
                                                                                                               ('IndicatorLabel.toggle', {'side': 'left', 'sticky':''}),
                                                                                                               ('IndicatorLabel.label', {'side': 'left','sticky': 'nswe'})]})]})])
        self.style.configure('IndicatorLabel', background = '#def2fc')

        self.style.configure('ContainerPane.TFrame', background = 'white')


    def _load_images(self):
        from PIL import Image, ImageTk
        from configGUI_V1 import PROJECT_BASE_DIR
        import os

        image_size = (10, 10)
        with Image.open(PROJECT_BASE_DIR + os.sep + '/images/icons/indicator_open.png') as img:
            img = img.resize(image_size, Image.ANTIALIAS)
            self.img_open = ImageTk.PhotoImage(img, name='open')

            if not self.open:
                self.img_default = ImageTk.PhotoImage(img, name='default')

        with Image.open(PROJECT_BASE_DIR + os.sep + '/images/icons/indicator_close.png') as img:
            img = img.resize(image_size, Image.ANTIALIAS)
            self.img_close = ImageTk.PhotoImage(img, name='close')

            if self.open:
                self.img_default = ImageTk.PhotoImage(img, name='default')





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
    frame.pane_configure('001')
    pane = frame.get_pane('001')
    pane.grid_item(ttk.Entry(), label = 'test',row = 0, column = 0)
    print([each.__class__.__name__ for each in root.pack_slaves()])
    root.mainloop()

