
import tkinter as tk

from configGUI_V1.static.css import Canvas_css
from widgets.scrolled_frame import ScrolledFrame


class SurfaceCanvas_M(tk.Canvas):

    Configs = Canvas_css.default_configs
    Grid = 'GRID'
    Scale_text = 'SCALE_TEXT'

    def __init__(self, agent, master:ScrolledFrame, cnf = {}, **kwargs):
        '''
        :param agent: corresponding agent
        :param master: a scrolled frame
        :param cnf:
        :param kwargs:
        '''

        self.agent = agent
        self.master = master

        if 'width' not in kwargs:
            kwargs['width'] = self.Configs['canvas_width']
        if 'height' not in kwargs:
            kwargs['height'] = self.Configs['canvas_height']

        if 'grid_lines' in kwargs:
            self.grid_lines = kwargs['grid_lines']
            del kwargs['grid_lines']
        else:
            self.grid_lines = False

        super().__init__(master, cnf, **kwargs)

        self._setup_canvas()


    #=============================================================== Canvas Initialisation Funcs =======================================================================
    def _setup_canvas(self):

        self.__init_coordinate_system()
        self.__init_shopfloor_layout()
        self.__add_grid_lines()
        self.__add_scale_meter()
        self.__add_scrolls()



    def __init_shopfloor_layout(self):
        self.shopfloor_bbox = (
            self.__coord_x,
            self.__coord_y,
            self.__coord_x + self.Configs['shopfloor_width'],
            self.__coord_y + self.Configs['shopfloor_height']
        )

        self.shopfloor_layout = self.create_rectangle(self.shopfloor_bbox, Canvas_css.shopfloor_layout, tag = 'shopfloor_layout')

    def __init_coordinate_system(self):

        self.__coord_x, self.__coord_y = 100, 100

        h_x1, h_x2 = self.__coord_x - 50, self.__coord_x + self.Configs['shopfloor_width'] + 50
        h_y1 = h_y2 = self.__coord_y

        v_x1 = v_x2 = self.__coord_x
        v_y1, v_y2 = self.Configs['shopfloor_height'] + self.__coord_y + 50, self.__coord_y - 50

        self.h_axis_bbox = (h_x1, h_y1, h_x2, h_y2)
        self.v_axis_bbox = (v_x1, v_y1, v_x2, v_y2)

        self.create_line(self.h_axis_bbox, width = 2, arrow=tk.LAST, tags = 'h_axis')
        self.create_line(self.v_axis_bbox, width = 2, arrow=tk.LAST, tags = 'v_axis')

    def __add_grid_lines(self):
        width = self.Configs['canvas_width']
        height = self.Configs['canvas_height']
        grid_interval = self.Configs['gridline_interval']

        def plot_lines(horizontal = True):
            nextline = grid_interval
            stopline = height if horizontal else width

            while nextline < stopline:
                bbox = (0, nextline, width, nextline) if horizontal else (nextline, 0, nextline, height)
                self.create_line(bbox, tags = self.Grid, fill="LightGrey")
                nextline += grid_interval

        plot_lines(True)
        plot_lines(False)
        self.tag_lower(self.Grid)

    def __add_scale_meter(self):
        self.scale = self.Configs['scale']
        x1, y1 = self.__coord_x + 30, self.__coord_y - 40
        x2, y2 = x1 + 10, y1 +10
        for i in range(5):
            self.create_rectangle(x1, y1, x2, y2, fill = 'white' if not i%2 else 'black')
            x1 += 10
            x2 += 10

        self.create_text(x2, y1, text = '50 px = {} meter'.format(int(50/self.scale)),
                         anchor = tk.NW, tags = self.Scale_text)

    def __add_scrolls(self):
        self.master.set_scroll_to_window (self)
        self.configure(scrollregion = (0, 0, self.Configs['canvas_width'], self.Configs['canvas_height']))

    # =============================================================== Drag and Drop Funcs =======================================================================

    def dnd_accept(self, source, event):
        return self

    def where(self, event):
        '''
        return the mouse position relative to the left corner of canvas
        '''
        x_canvas_root = self.winfo_rootx()
        y_canvas_root = self.winfo_rooty()

        x = event.x_root - x_canvas_root
        y = event.y_root - y_canvas_root

        return x, y

    def dnd_enter(self, source, event):
        self.focus_set()
        # self.focus_set()  # Show highlight border
        # x, y = self.where(event)
        # self.dndid = self.create_oval(x-5, y-5, x+5, y+5, fill = "Red")
        # self.dnd_motion(source, event)

    def dnd_motion(self, source, event):
        pass
        # x, y = self.where(event)
        # x1, y1, x2, y2 = self.coords(self.dndid)
        # x_move, y_move = x - x1, y - y1
        # self.move(self.dndid, x_move, y_move)

    def dnd_leave(self, source, event):
        event.widget.master.focus_set()
        # self.top.focus_set()  # Hide highlight border
        # self.delete(self.dndid)
        # self.dndid = None

    def dnd_commit(self, source, event):
        self.dnd_leave(source, event)
        x, y = self.where(event)
        type = source["text"]
        #self.object.create_agent(type, position_x=x, position_y=y)


if __name__ == '__main__':
    root = tk.Tk()
    frame = tk.Frame(root)
    canvas = SurfaceCanvas_M(None, frame)
    canvas.pack()
    root.mainloop()
