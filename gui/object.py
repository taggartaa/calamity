"""
@file Object.py
@date 8/23/2010
@version 0.1
@author Aaron Taggart

@brief Object source code.
The Object is an abstract class which all on screen objects will inherit from.
"""

class Object:
    """
    @brief All GUI classes share these specific methods and data.
    """
    def __init__(self):
        """
        @brief Constructor for an abstract GUIobject visable
        """
        self._component = None
        self._border_width = 0
        self._border_type="flat"
        self._align = "grid"
        self._border_color = ""
        self._background_color = ""
        self._position = [0,0]
        self._column_growth_rate = dict()
        self._row_growth_rate = dict()
        self._growth = [False, False]
        self._width = 0
        self._blend = []
        self._binds = []
        self._padding = [0,0]
        self._visible = True
        self._sticky = ""
        self._blended = True
        
        self._focus = False
        
    def bind(self, event, procedure):
        """
        @brief When the event occurs, the procedure will be called.
        
        @var event: Any event that can occur such as a key press.
        @var procedure: A funciton or method that is to be called 
        following the event.
        """
        if self._component != None:
            self._component.bind(event, procedure)
        else:
            self._binds.append((event, procedure))
        
    def get_component(self):
        """
        @brief returns the component of a GUIobject that can actually be drawn.
        """
        return self._component
    
    def _parent(self):
        """
        @brief Abstract parent method. 
        @note This method should never be called outside a parent setting 
        method. (See parent methods of children classes)
        """
        
        # for efficiency
        tmpVis = self.get_visibility()
        self.set_visibility(False)
        
        for b in self._binds:
            self._component.bind(b[0], b[1])
         
        self.column_growth_rate()   
        #for i in self._colGrowthRate:
        #    self.column_growth_rate(i[0], i[1])
            
        self.row_growth_rate()
        #for i in self._row_growth_rate:
        #    self.row_growth_rate(i[0], i[1])

        self.set_growth()
        self.set_padding()
        
        self._component["bd"] = self._border_width
        
        if self._border_color == "":
            self._border_color = self._component["bg"]
            
        self.set_background_color(self._border_color)
        
        if self._width > 0:
            self._component["width"] = self._width
            
        self.set_border_type(self._border_type)
        self.set_align(self._align)
        
        self.set_visibility(tmpVis)
            
    def set_visibility(self, visible):
        """
        @brief Sets whether or not an object is currently visible.
        
        @var visible: Whether or not the object should be on screen or not.
        """
        
        if self._visible != visible:
            self._visible = visible
        
            if self._component != None:
                if visible == False:
                    if self._align == "pack":
                        self._component.forget()
                    elif self._align == "grid":
                        self._component.grid_forget()
                else:
                    self._configure()
            
        
    def get_visibility(self):
        """
        @brief Determines if an object is currently visible.
        Visibility may be True even though it does not appear on screen if the 
        main loop has not been started, or if the parent object of this object 
        has a visibility set to False.
        
        @return True/False Whether or not the object is visible.
        """
        return self._visible
            
    def column_growth_rate(self, column=-1, growthRate=0):
        """
        @brief The rate at which the column on this object grows with 
        respect to itself.
        
        @var column: The column number.
        @var growthRate: weight value that determines the growth rate 
        of a column.
        """
        
        if column != -1:
            self._column_growth_rate[column] = growthRate
        
        if self._component != None:
            self._configure()
            
    def row_growth_rate(self, row=-1, growthRate=0):
        """
        @brief The rate at which the row grows with respect to its parent.
        
        @var growthRate: weight value that determines the growth rate of a row.
        """
        if row != -1:
            self._row_growth_rate[row] = growthRate
            
        if self._component != None:
            self._configure()
            
    def set_growth(self, width = -1, height = -1):
        """
        @brief Sets how the objects size changes as its parent changes.
        @note Its parent is likely a cell, be sure to use column_growth_rate 
        and/or row_growth_rate.
        
        @var width: True/False values indicating the object's width will grow 
        or not (-1 means unchanged).
        @var height: True/False values indicating the object's height will grow 
        or not (-1 means unchanged).
        
        @todo Packed objects can't grow, only Grid objects can.
        """
        if width != -1:
            self._growth[0] = width
        if height != -1:
            self._growth[1] = height
            
        if self._align == "grid" and self._component != None:
            
            sticky = ""
            if self._growth[0]:
                sticky += "we"
                    
            if self._growth[1]:
                sticky += "ns"
                
            self._sticky = sticky
                
            self._configure()
            
    def set_padding(self, x=-1, y=-1):
        """
        @brief Sets the padding of the cell containing this object.
        
        @var x: Padding on the left and right sides (-1 means don't change it)
        @var y: Padding on the top and bottom sides (-1 means don't change it)
        """
        if x != -1:
            self._padding[0] = x
        if y != -1:
            self._padding[1] = y
            
        if self._component != None:
            self._configure()
            
    def set_align(self, align):
        """
        @brief Set the type of screen alignment control to be used.
        
        @var align: The alignment type of the object. grid = (row, column), 
        pack = center it!
        """
        self._align = align
        
        if self._component != None:
            self._configure()
        
        
        
    def set_border_width(self, width):
        """
        @brief Sets the width of the border in pixels.
        
        @var width: The new width of the border.
        """
        if self._component != None:
            self._component["bd"] = width
            
        self._border_width = width
        
    def get_border_width(self):
        """
        @brief Gets the border width.
        
        @return The current border width.
        """
        if self._component != None:
            return self._component["bd"]
        return self._border_width
    
    def set_border_type(self, type):
        """
        @brief Sets the type of border that is drawn.
        
        @var type: Type of border (raised, sunken, groove, ridge, and flat).
        """
        self._border_type = type
        if self._component != None:
            self._component["relief"] = type
                
    def set_background_color(self, color):
        """
        @brief Sets the color of the backgorund of the Object.
        For a list of the accepted colors, see the Tkinter documentation.
        
        @var color: Color you wish to change it too. (lowercase spelling, 
        Tkinter provides other valid methods for specifying color)
        """
        
        self._border_color = color
            
        if self._component != None:
            self.blend()
            
        
    def blending(self, blended):
        """
        @brief Determines whether the background uses and passes the 
        blended background colors or not.
        
        @var blended: True/False Whether or not to use blending
        """
        self._blended = blended
        
    def blend(self, add = "", remove = ""):
        """
        @brief Blends a color into the background (i.e. White + Red = Pink)
        @note (Pink - White = Red) only if you had pink via 
        blending white and red.
        
        @var add: The color to be blended into the background.
        @var remove: The color to be taken out of the blend 
        (has to be in there already).
        """
            
        if remove != "":
            try:
                self._blend.remove(remove)
            except:
                pass
            
        if add != "" and add != "clear":
            self._blend.append(add)
        
        if self._component != None:
            r=g=b=0
            count = len(self._blend)
            
            # Add up all colors
            for c in self._blend:
                tmp = self._component.winfo_rgb(c)
                r+= tmp[0]
                g+= tmp[1]
                b+= tmp[2]
                
            # Add in current background color
            if self._border_color != "clear":
                bg = self._component.winfo_rgb(self._border_color)
                count += 1
                r+= bg[0]
                g+= bg[1]
                b+= bg[2]
            
            # If there is no blended colors and a clear base background, 
            # then leave it alone!
            if count != 0:
                self._bg = "#%04x%04x%04x" %(r/count,g/count,b/count)
                
                if self._blended == True:
                    self._component["bg"] = self._bg
                else:
                    self._component["bg"] = self._border_color
        
            
    def get_background_color(self, blended=True):
        """
        @brief Gets the color of the background of the Object.
        
        @var blended: True means it will return the blended value of the 
        background.
        @return The current color of the background of the Object.
        """
        if self._component != None and blended:
            return self._component["bg"]
        return self._border_color
    
    def set_position(self, pos):
        """
        @brief Sets the (x,y) coordinates of the top left corner of the object.
        
        @var position: A tuple of size 2 indicating the (x,y) 
        coordinates of the object (top left corner)
        """
        self._position=pos
        
        if self._component != None:
            self._configure()
        
    def get_position(self):
        """
        @brief Gets the current relative position of the object
        
        @return The (x,y) coordinates of the object
        """
        return self._position
    
    def set_width(self, width):
        """
        @brief Sets the width of the object 
        (units depends on what's in the object).
        
        @var width New width of the object.
        """
        if self._component != None:
            self._component["width"] = width

        self._width = width
        
    def _configure(self):
        """
        @brief Internal function that should not be called outside of here. 
        It is what actually draws the objects on screen.
        """
        if self._visible:
            if self._align == "pack":
                self._component.pack()
            elif self._align == "grid":
                self._component.grid_configure(padx=self._padding[0], 
                                               pady=self._padding[1], 
                                               sticky=self._sticky, 
                                               row=self._position[0], 
                                               column=self._position[1])
             
            # Even if this item is packed or exists without packaging, 
            # doesn't mean the children aren't packaged!   
            for row, rate in self._row_growth_rate.items():
                self._component.grid_rowconfigure(row, weight=rate)
                    
            for column, rate in self._column_growth_rate.items():
                self._component.grid_columnconfigure(column, weight=rate)
                    

    def __str__(self):
        """
        @brief string version of an object. 
        Tells a little about the object.
        """
        
        string = ""
        
        if self._align == "grid":
            string = "Grid info: " + str(self._component.grid_info()) + "\n"
        elif self._align == "pack":
            string = "Pack info:" + str(self._component.pack_info()) + "\n"
        
        string += "Row Growth Rate: " + str(self._row_growth_rate) + "\n"
        string += "Column Growth Rate: " + str(self._column_growth_rate) + "\n"
        
        return string

