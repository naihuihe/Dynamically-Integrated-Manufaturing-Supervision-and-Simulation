from tkinter import *
from .line_seperator import LineSeperator

class SurfaceFrame (Frame):

    def __init__(self, master = None):

        super().__init__(master)

        # add a top seperator
        LineSeperator(master=self, width = 800).pack(fill = "x")

        self.label_frame = Frame(master=self, height = 20)
        self.label_frame.pack(fill = "x")

        # add a bottom seperator
        LineSeperator(master=self, width = 800).pack(fill = "x")

        self.canvas_frame = Frame(master=self, bg="WHITE")
        self.canvas_frame.pack(fill=BOTH, expand=1)

        # there may be multiple canvas in the window
        # But only one canvas is active, which will be shown in the canvas_frame
        # current_canvas is the one currently active and shown in the frame
        self.current_canvas = None

        #
        self.canvas_list = []


    def set_current_canvas(self, surface):
        if self.current_canvas:
            self.current_canvas.hide_canvas()

        self.current_canvas = surface
        self.current_canvas.reload_canvas()

    def move_to_next_canvas(self, removed_surface):
        """
        this function should be called after a surface is closed.
        :param removed_surface: the index of the removed_surface from the canvas_list
        :return:
        """
        if self.canvas_list:
            if not removed_surface:
                # if the removed_surface was the first one in the list, then showing the one on its right side (whose current index becomes 0)
                canvas = self.canvas_list[removed_surface]
            else:
                # otherwise, showing the one on the left side of the removed one (whose index = removed_surface - 1)
                canvas = self.canvas_list[removed_surface - 1]

            self.set_current_canvas(canvas)

    def remove_surface_from_list(self, surface):
        """
        remove a surface from the list and return its original index in the list
        :param surface: to be removed
        :return: position index in the list
        """
        index = self.canvas_list.index(surface)
        self.canvas_list.remove(surface)

        return index

