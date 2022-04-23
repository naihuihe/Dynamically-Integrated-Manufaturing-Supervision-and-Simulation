from tkinter import *
from PIL import Image, ImageTk


class SurfaceCanvas(Canvas):

    GRID = "GRID"
    HIGHLIGHT = "HIGHLIGHTED"

    def __init__(self, object, master_frame, title=None, setGrid=True, **kwargs):
        """
        :param master: the master object of the surface, e.g. system_agent, sub_system_agent...
        :param master_frame: the surface_frame of the Main_Gui
        :param kwargs: optional parameters including ["width", "height", "x"(x position), "y" (y position), tag, image_path, name_text]
        """
        super().__init__(master_frame)
        self.object = object  # the agent corresponding to the surface
        self.master_frame = master_frame
        self.title = title
        self.setGrid = setGrid

        # dict: key: ID   value: agent which the graph with the ID is related
        self.item_list = {}

        self.__setattr__("title_frame", kwargs.get("title_frame"))

        # to dynamically mornitor the position of mouse on the canvas
        self.dynamic_mouse_x = 0
        self.dynamic_mouse_y = 0

        # a switch value to check if there are any selected items on the canvas
        self.has_selected = False

        # a temparory rectangle areas for selecting items on the canvas.
        # The rectangle area will change dynamicaly with Button-1 until it is released
        self.temp_rect = None

        # bind events to items on canvas
        self.bind_event()

        # this function will add a title frame on top of the surface
        # the title frame will show which agent this surface is for. Also it will provide a button to close the surface

    def setup_canvas(self):
        # default parameters:
        self.origin_coord_x = 100
        self.origin_coord_y = 100

        self.scale = 10  # the default scale of surface is 100px = 10 meters

        # 1st: add grid lines
        if self.setGrid:
            self.addGridLines()

        # 2nd: set scrolls
        self.addScrolls()

        # 3rd create coordination system
        self.create_coordination_system()
        self.add_scale_meter()


    def add_nav_bar (self, nav_bar):
        self.nav_bar = nav_bar

    def bind_event(self):
        self.bind("<ButtonPress-1>", self.update_mouse_pos)  # update mouse position when Button-1 is clicked
        self.bind("<Control-B1-Motion>", self.select_items_by_mouse)  # select items by pressing and moving Ctrl-Button-1
        self.bind("<Control-ButtonRelease-1>",self.confirm_selected_items)  # confirm the selection by releasing Ctrl-Button-1
        self.bind("<ButtonRelease-1>", self.cancel_selection)  # after operation, cancel the selection by releasing Button-1
        self.tag_bind(SurfaceCanvas.HIGHLIGHT, "<B1-Motion>", lambda event: self.move_items_by_tag(SurfaceCanvas.HIGHLIGHT, event))  # moving selected items


    def create_coordination_system(self):

        self.create_line(self.origin_coord_x - 100, self.origin_coord_y, 1200, self.origin_coord_y, arrow = LAST)
        self.create_line(self.origin_coord_x, 1200, self.origin_coord_x, self.origin_coord_y - 100, arrow = LAST)

    def add_scale_meter(self):

        pass


    def update_config_frame(self, resource_name, event):
        # this is a callback function of add_left_click()
        # it will update the config_frame by resource name given

        self.object.resources[resource_name].update_config_frame()


    def add_left_click(self, tag):
        # this function adds left_click response to every graph created on the surface
        # once a graph is left_clicked, its information will be shown on the config_frame of the interface
        # the callback command of the left_click event to make the config_frame visible
        self.bind("<Button-1>", lambda event: self.update_config_frame(tag, event))


    # this function adds grid lines to the surface
    def addGridLines(self):
        screen_width = 2000
        scree_height = 1500

        interval = 10
        index = 10
        while index < screen_width:
            # add vertical grid lines
            self.create_line(index, 0, index, scree_height, tags=SurfaceCanvas.GRID, fill="LightGrey")
            # add horizontal grid lines
            self.create_line(0, index, screen_width, index, tags=SurfaceCanvas.GRID, fill="LightGrey")
            index += interval

        self.tag_lower(SurfaceCanvas.GRID)


    # this function adds both H and V scrolls to the surface
    def addScrolls(self):
        self.configure(scrollregion=(0, 0, 2000, 1500))
        # add horizontal bar
        self.hbar = Scrollbar(self.master_frame, orient=HORIZONTAL, command=self.xview)
        self.hbar.pack(side=BOTTOM, fill="x")
        self.config(xscrollcommand=self.hbar.set)

        # add vertical bar
        self.vbar = Scrollbar(self.master_frame, orient=VERTICAL, relief = RAISED, command=self.yview)
        self.config(yscrollcommand=self.vbar.set)
        self.vbar.pack(side=RIGHT, fill=Y)



    def load_image(self, image_path, **kwargs):
        """
        :param image: A PhotoImage instance
        :param kwargs: "size" = (width, height), "position" = (x, y)
        :return:
        """
        size = kwargs.get("size")
        position = kwargs.get("position")

        if size:
            image_width = size[0]
            image_height = size[1]
        else:
            image_width, image_height = self.width, self.height

        if position:
            image_x = position[0]
            image_y = position[1]
        else:
            image_x, image_y = 0, 0

        self.image = (Image.open(image_path)).resize((image_width, image_height), Image.ANTIALIAS)
        self.photoimage = ImageTk.PhotoImage(self.image)
        self.image_tag = self.create_image(image_x, image_y, image=self.photoimage, anchor=NW)


    def hide_canvas(self):
        self.pack_forget()
        self.hbar.pack_forget()
        self.vbar.pack_forget()
        self.nav_bar.un_highlight()


    def reload_canvas(self):
        self.hbar.pack(side=BOTTOM, fill="x")
        self.vbar.pack(side=RIGHT, fill=Y)
        self.pack(side=LEFT, fill=BOTH, expand=True)
        self.nav_bar.highlight()

    def load_as_current_canvas(self):
        self.master_frame.master.set_current_canvas(self)

    #======================================== functions for creating resources by drag-and-drop ==============================================
    def dnd_accept(self, source, event):
        return self
        #element = MachineAgent(parent = self.object, id = "o", name = "dnd", label_frame=self.object.label, surface_frame=self.object.surface, config_frame=self.object.config_frame, x = event.x, y = event.y)

    def where(self, event):
        # where the corner of the canvas is relative to the screen:
        x_org = self.winfo_rootx()
        y_org = self.winfo_rooty()
        # where the pointer is relative to the canvas widget:
        x = event.x_root - x_org
        y = event.y_root - y_org
        # compensate for initial pointer offset
        return x, y

    def dnd_enter(self, source, event):
        pass
        #self.focus_set()  # Show highlight border
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
        pass
        #self.top.focus_set()  # Hide highlight border
        # self.delete(self.dndid)
        # self.dndid = None

    def dnd_commit(self, source, event):
        self.dnd_leave(source, event)
        x, y = self.where(event)
        type = source["text"]
        self.object.create_agent(type, position_x = x, position_y = y)


    #=========================================== functions for interative line plotting ====================================
    def activate_interative_line_plotting(self):
        # this function is triggered by double-click the DNDLable in "element_library"
        # click Button-1, the interative plotting  function is launched
        self.focus_set()
        bind_id= self.bind("<Button-1>", lambda event: self.interative_line_plotting(bind_id, event))

    def interative_line_plotting(self, bind_id, event):

        # determine the starting point and initialise the a line
        self.update_mouse_pos(event)
        newline = self.create_line(self.dynamic_mouse_x, self.dynamic_mouse_y, self.dynamic_mouse_x, self.dynamic_mouse_y)
        line_bbox = [self.dynamic_mouse_x, self.dynamic_mouse_y]

        # remove the "Button-1" event binded to the interative_line_plotting function
        self.unbind("<Button-1>", bind_id)

        def track_line(event):
            self.coords(newline, *line_bbox, event.x, event.y)

        def update_line(event):
            line_bbox.extend([event.x, event.y])
            self.coords(newline, *line_bbox)

        # remove all events binded for plotting lines
        # reset all binded events in the canvas related to "Button-1" or "ButtonPress-1"
        def confirm_line_plotting(event):
            line_bbox.extend([event.x, event.y])
            self.coords(newline, *line_bbox)
            self.unbind("<Motion>", track_bind_id)
            self.unbind("<Button-1>", update_bind_id)
            self.unbind("<Double-Button-1>", confirm_bind_id)
            self.bind("<ButtonPress-1>", self.update_mouse_pos) # reset the all events related to Button-1

            path = self.object.create_element("Path")
            path.update_path_bbox(line_bbox)
            self.addtag_withtag(path.name, newline)


        track_bind_id = self.bind("<Motion>", track_line)
        update_bind_id = self.bind("<Button-1>", update_line)
        confirm_bind_id = self.bind("<Double-Button-1>", confirm_line_plotting)

    #################################################functions for create material flow ################################

    def launch_material_flow_plotting(self):
        # this function is triggered by double-click the DNDLable in "element_library"
        # click Button-1, the interative plotting  function is launched
        self.focus_set()
        bind_id = self.bind("<Button-1>", lambda event: self.plot_material_flow(bind_id, event))

    def plot_material_flow(self, bind_id, event = None):
        from tk_view_models.operation import Operation

        # locate the mouse position
        self.update_mouse_pos(event)
        # closest_item = self.find_closest(self.dynamic_mouse_x, self.dynamic_mouse_y)   # please note, the return closest_item is a turple

        # if item detected
        item = self.find_closest_item(event=event)
        if item and isinstance(item, Operation):

            flow_out_point_x = item.flow_out_point.t_position_x.get()
            flow_out_point_y = item.flow_out_point.t_position_y.get()

            flow_line = self.create_line(flow_out_point_x, flow_out_point_y, flow_out_point_x, flow_out_point_y, width = 2, arrow = "last")
            line_bbox = [flow_out_point_x, flow_out_point_y]

            # now need to bind a new "<Button-1>" event to find the flow-out point
            self.unbind("<Button-1>", bind_id)
            track_line_id = self.bind("<Motion>", lambda event: self.track_line(flow_line, line_bbox, event))
            complete_plotting_id = self.bind("<Button-1>",
                                             lambda event: self.complete_material_flow_plotting(flow_line, line_bbox,
                                                                                                track_line_id,
                                                                                                complete_plotting_id,
                                                                                                event))
        else:
            self.unbind("<Button-1>", bind_id)
            self.bind("<ButtonPress-1>", self.update_mouse_pos)  # reset the all events related to Button-1
            return


    def find_closest_item(self, event = None):
        #self.update_mouse_pos(event)
        #closest_item = self.find_closest(self.dynamic_mouse_x, self.dynamic_mouse_y)
        closest_item = self.find_closest(event.x, event.y)

        # if items nearby are detected
        if closest_item:

            # get the item_id and check whether it is registered to the item_list
            # only graphs of agents are registered to the list
            item_id = closest_item[0]
            if item_id in list(self.item_list.keys()):
                return self.item_list[item_id]
            # if not registered, it means the item detected is not an agent, then return False
            else:
                return False
        # no items detected
        else:
            return False

    def track_line(self, line, bbox, event = None):
        """
        to make a line goes along with the mouse
        :param line: tag/id of a line
        :param bbox: bbox of the line
        :param event: "<Motion>"
        :return:
        """
        self.coords(line, *bbox, event.x, event.y)


    def complete_material_flow_plotting(self, line, bbox, track_line_id, complete_plotting_id, event):
        from tk_view_models.operation import Operation

        # delete the material flow line temporarily.
        # otherwise, find_closest() function will alwasy return the flow line other than graphs of operations
        self.delete(line)

        # find the item closest to the mouse
        item = self.find_closest_item(event)
        if item and isinstance(item, Operation):
            # get the flow-in connection point positions
            flow_in_point_x = item.flow_in_point.t_position_x.get()
            flow_in_point_y = item.flow_in_point.t_position_y.get()
            # re-plot the flow line again
            self.create_line(*bbox, flow_in_point_x, flow_in_point_y, width=2, arrow="last")

        self.unbind("<Motion>", track_line_id)
        self.unbind("<Button-1>", complete_plotting_id)
        self.bind("<ButtonPress-1>", self.update_mouse_pos)  # reset the all events related to Button-1


    def update_mouse_pos(self, event):
        """
        :param event: ButtonPress-1
        :return:
        """
        x = event.x
        y = event.y

        if x >= 0:
            self.dynamic_mouse_x = x
        if y >=0:
            self.dynamic_mouse_y = y

    def cancel_selection(self, event):
        if self.has_selected:
            self.itemconfigure(SurfaceCanvas.HIGHLIGHT, dash = "")
            self.dtag(SurfaceCanvas.HIGHLIGHT, SurfaceCanvas.HIGHLIGHT)
            self.has_selected = False

    # this function is only applies to the surface for root system or sub_systems
    def select_items_by_mouse(self, event):
        """
        :param event: B1-Motion
        :return:
        """
        if not self.temp_rect:
            self.temp_rect = self.create_rectangle(self.dynamic_mouse_x, self.dynamic_mouse_y, event.x, event.y, dash = (2,2), fill ="")
        else:
            self.coords(self.temp_rect, self.dynamic_mouse_x, self.dynamic_mouse_y, event.x, event.y)

    # this function will highglight the selected item and add a "TEMP" tag to the items.
    def confirm_selected_items(self, event):
        self.delete(self.temp_rect)
        self.temp_rect = None
        # self.temp_selected_items=self.find_enclosed(self.dynamic_mouse_x, self.dynamic_mouse_y, event.x, event.y)
        # self.selected_items.extend(self.temp_selected_items)
        self.addtag_enclosed(SurfaceCanvas.HIGHLIGHT, self.dynamic_mouse_x, self.dynamic_mouse_y, event.x, event.y)
        #self.itemconfigure(SurfaceCanvas.HIGHLIGHT, stipple="gray50")
        self.itemconfigure(SurfaceCanvas.HIGHLIGHT, dash = (2,2))
        self.has_selected = True


    def move_items_by_tag (self, tag, event):
        from tk_view_models.operation import Operation
        """
        :param tag: tag of graphs
        :param event: B1 - Motion
        :return:
        """
        # calculate how much the mouse moved
        delta_x = 0
        delta_y = 0

        if event.x>0:
            delta_x = event.x - self.dynamic_mouse_x
        if event.y>0:
            delta_y = event.y - self.dynamic_mouse_y

        # move the referenced items
        self.move(tag, delta_x, delta_y)

        # update the mouse position
        self.dynamic_mouse_x = event.x
        self.dynamic_mouse_y = event.y

        # now need to update the positions of all items if registered
        # firstly, find all relevant items using the tag
        all_items_relevant = self.find_withtag(tag)    # a turple of item graphic ids
        for item in all_items_relevant:
            # if the graph is for an agent
            if item in list(self.item_list.keys()):

                # find the agent with using the ID (item), and update its positions
                agent = self.item_list[item]
                agent.update_position (movement= (delta_x, delta_y))

                # if the agent has connection points, update the position of their connection points as well
                if isinstance(agent, Operation):
                    agent.flow_in_point.update_position(movement=(delta_x, delta_y))
                    agent.flow_out_point.update_position(movement=(delta_x, delta_y))



