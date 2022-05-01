
import tkinter as tk

class ToolTip:

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text, event = None):
        "Display text in tooltip window"
        if isinstance(text, tk.StringVar):
            self.text = text
        else:
            self.text = tk.StringVar()
            self.text.set(text)

        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox(0)
        x = x + cx + self.widget.winfo_rootx()
        y = y + cy + self.widget.winfo_rooty() + 10

        if self.text.get():
            self.tipwindow = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(1)
            tw.wm_geometry("+%d+%d" % (x, y))

            label = tk.Label(tw, textvariable=self.text, justify=tk.LEFT,
                             background="white", relief=tk.SOLID, borderwidth=1,
                             font=("tahoma", "8", "normal"))
            label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text, event)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
