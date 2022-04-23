

class MainWindow_css:

    # widget design
    window = {}

    Menu = {"bg": 'white', "relief": "sunken"}

    PopupWindow = {'background': '#ebedee', 'relief':'sunken'}


    # geometry design: pack, grid, or place

    Frame_Pack = {'padx': 10, 'pady': 10}

    Entry_Pack = {'padx': 10}

    DndLabel_Pack = {'anchor':'w', 'ipadx': 5, 'padx': 10, 'pady': 2}

    RuntimeMsgArea_Pack = {'side':'bottom', 'fill':'both', 'expand':'True'}


class Canvas_css:

    default_configs = {
        'canvas_width': 2000,
        'canvas_height': 2000,
        'scale': 5, # how many px represent 1 meter
        'scale_interval': 5,
        'gridline_interval': 5,
        'min_scale': 1,
        'shopfloor_width': 1000,
        'shopfloor_height': 800
    }

    shopfloor_layout = {
        'fill': "lightgrey", 'outline': "orange", 'stipple': "gray25"
    }




class MainGuiStyle:
    # css styles for window of main_GUI
    panedwindow = {"bg": "WHITE", "sashrelief": "sunken", "relief": "sunken"}
    frame = {"bg": "WHITE", "relief": "sunken"}
    frame_label = {"height": "1", "anchor": "w", "padx": "10"}
    menu_font = ("Verdana", 14)
    line_seperator = {"height": "2", "bd": "1", "relief": "sunken"}

    dnd_label = {"width": "15", "anchor": "w", "padx": "10", "highlightbackground": "Black", "fg":"red"}


class ConfigPanelStyle:

    config_panel_pack = {"side": "left", "fill": "both", "expand": "1"}
    var_grid_style = {"sticky": "w", "padx": "20"}
    textbox_style = {"width": "50", "height": "6"}
    optionmenu_style = {"width": "14", "height": "1", "bg": "white", "relief": "sunken"}
    menu_style = {"bg": "white", "relief": "sunken"}

class CollapsiblePaneStyle:

    grid_item_c1 = {"padx": "20",
                    "sticky": "w"}
    grid_item_c2 = {"padx": "10",
                    "sticky": "w"}


class ResourceSurfaceStyle:

    machine_default_color = "blue"

class PopupWindowStyle:

    option_menu = {"bg":"white",
                   "relief": "groove",
                   "borderwidth": "1",
                   "height": "1",
                   "width": "10",
                   "highlightcolor": "white",
                   "highlightthickness": "1"}

    menu = {"font": ("Arial, 11"),
              "bg": "white",
              "borderwidth": "1",
              "relief": "raised",
              "borderwidth": "1"
              }

class FormStyle:

    label = {"width": "10",
              "anchor": "center",
              "font": ("Arial, 10"),
              "relief": "sunken",
              "borderwidth": "1",
              "highlightbackground": "black",
              "highlightthickness": "1"
              }

    sequence_label = {"width": "6",
                     "anchor": "center",
                     "font": ("Arial, 10"),
                     "relief": "sunken",
                     "borderwidth": "1",
                      "highlightbackground": "black",
                      "highlightthickness": "1"
                     }

    entry = {"width": "12",
          "font": ("Arial, 11"),
          "bg": "white",
          "relief": "groove",
          "borderwidth": "1"
    }

    option_menu = {"background": "white",
                   "relief": "groove",
                   "borderwidth": "1",
                   "height" : "1",
                   "width": "10",
                   "highlightcolor": "white",
                   "highlightthickness": "1"
    }

    menu = {
            "font": ("Arial, 10"),
            "bg": "white",
            "relief": "raised",
            "borderwidth": "1"
            }


