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
        @brief Constructor for an abstract GUIobject
        """
        self._component = None
        self._borderWidth = 0
        self._bordertype="flat"
        self._align = "grid"
        self._bColor = ""
        self._bg = ""
        self._position = [0,0]
        self._colGrowthRate = []
        self._rowGrowthRate = []
        self._growth = [False, False]
        self._width = 0
        self._blend = []
        self._binds = []
        self._padding = [0,0]
        
        self._blended = True
        
        self._focus = False
        
    def bind(self, event, procedure):
        """
        @brief When the event occurs, the procedure will be called.
        
        @var event: Any event that can occur such as a key press.
        @var procedure: A funciton or method that is to be called following the event.
        """
        if self._component != None:
            self._component.bind(event, procedure)
        else:
            self._binds.append((event, procedure))
        
    def getComponent(self):
        """
        @brief returns the component of a GUIobject that can actually be drawn.
        """
        return self._component
    
    def _parent(self):
        """
        @brief Abstract parent method. 
        @note This method should never be called outside a parent setting method. (See parent methods of children classes)
        """
            
        for b in self._binds:
            self._component.bind(b[0], b[1])
            
        for i in self._colGrowthRate:
            self.columnGrowthRate(i[0], i[1])
            
        for i in self._rowGrowthRate:
            self.rowGrowthRate(i[0], i[1])

        self.setGrowth()
        self.setPadding()
        
        self._component["bd"] = self._borderWidth
        
        if self._bColor == "":
            self._bColor = self._component["bg"]
            
        self.setBackgroundColor(self._bColor)
        
        if self._width > 0:
            self._component["width"] = self._width
            
        self.setBorderType(self._bordertype)
        
        if self._align == "grid":
            self._component.grid(row=self._position[0], column=self._position[1])
        elif self._align == "pack":
            self._component.pack()
            
    def columnGrowthRate(self, column, growthRate):
        """
        @brief The rate at which the column on this object grows with respect to itself.
        
        @var column: The column number.
        @var growthRate: weight value that determines the growth rate of a column.
        """
        if self._component != None:
            self._component.grid_columnconfigure(column, weight=growthRate)
        else:
            self._colGrowthRate.append((column, growthRate))
            
    def rowGrowthRate(self, row, growthRate):
        """
        @brief The rate at which the row grows with respect to its parent.
        
        @var growthRate: weight value that determines the growth rate of a row.
        """
        if self._component != None:
            self._component.grid_rowconfigure(row, weight=growthRate)
        else:
            self._rowGrowthRate.append((row, growthRate))
        
            
    def setGrowth(self, width = -1, height = -1):
        """
        @brief Sets how the objects size changes as its parent changes.
        @note Its parent is likely a cell, be sure to use columnGrowthRate and/or rowGrowthRate.
        
        @var width: True/False values indicating the object's width will grow or not (-1 means unchanged).
        @var height: True/False values indicating the object's height will grow or not (-1 means unchanged).
        
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
                
            self._component.grid_configure(sticky=sticky)
            
    def setPadding(self, x=-1, y=-1):
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
            self._component.grid_configure(padx=self._padding[0], pady=self._padding[1])
            
    def setAlign(self, align):
        """
        @brief Set the type of screen alignment control to be used.
        
        @var align: The alignment type of the object. grid = (row, column), pack = center it!
        """
        if self._component != None:
            if self._align == "grid":
                self._component.grid(row=self._position[0], column=self._position[1])
            elif self._align == "pack":
                self._component.pack()
        
        self._align = align
        
    def setBorderWidth(self, width):
        """
        @brief Sets the width of the border in pixels.
        
        @var width: The new width of the border.
        """
        if self._component != None:
            self._component["bd"] = width
            
        self._borderWidth = width
        
    def getBorderWidth(self):
        """
        @brief Gets the border width.
        
        @return The current border width.
        """
        if self._component != None:
            return self._component["bd"]
        return self._borderWidth
    
    def setBorderType(self, type):
        """
        @brief Sets the type of border that is drawn.
        
        @var type: Type of border (raised, sunken, groove, ridge, and flat).
        """
        self._bordertype = type
        if self._component != None:
            self._component["relief"] = type
                
    def setBackgroundColor(self, color):
        """
        @brief Sets the color of the backgorund of the Object.
        For a list of the accepted colors, see the Tkinter documentation.
        
        @var color: Color you wish to change it too. (lowercase spelling, Tkinter provides other valid methods for specifying color)
        """
        
        self._bColor = color
            
        if self._component != None:
            self.blend()
            
        
    def blending(self, blended):
        """
        @brief Determines whether the background uses and passes the blended background colors or not.
        
        @var blended: True/False Whether or not to use blending
        """
        self._blended = blended
        
    def blend(self, add = "", remove = ""):
        """
        @brief Blends a color into the background (i.e. White + Red = Pink)
        @note (Pink - White = Red) only if you had pink via blending white and red.
        
        @var add: The color to be blended into the background.
        @var remove: The color to be taken out of the blend (has to be in there already).
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
            if self._bColor != "clear":
                bg = self._component.winfo_rgb(self._bColor)
                count += 1
                r+= bg[0]
                g+= bg[1]
                b+= bg[2]
            
            # If there is no blended colors and a clear base background, leave it alone
            if count != 0:
                self._bg = "#%04x%04x%04x" %(r/count,g/count,b/count)
                
                if self._blended == True:
                    self._component["bg"] = self._bg
                else:
                    self._component["bg"] = self._bColor
        
            
    def getBackgroundColor(self, blended=True):
        """
        @brief Gets the color of the background of the Object.
        
        @var blended: True means it will return the blended value of the background.
        @return The current color of the background of the Object.
        """
        if self._component != None and blended:
            return self._component["bg"]
        return self._bColor
    
    def setPosition(self, pos):
        """
        @brief Sets the (x,y) coordinates of the top left corner of the object.
        
        @var position: A tuple of size 2 indicating the (x,y) coordinates of the object (top left corner)
        """
        self._position=pos
        
        if self._component != None:
            if self._align == "grid":
                self._component.grid(row=pos[0], column=pos[1])
            else:
                self._component.pack()
        
    def getPosition(self):
        """
        @brief Gets the current relative position of the object
        
        @return The (x,y) coordinates of the object
        """
        return self._position
    
    def setWidth(self, width):
        """
        @brief Sets the width of the object (units depends on what's in the object).
        
        @var width New width of the object.
        """
        if self._component != None:
            self._component["width"] = width

        self._width = width

