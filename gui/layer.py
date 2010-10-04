"""
@file Layer.py
@date 8/23/2010
@version 0.1
@author Aaron Taggart

@brief Layer source code.

A layer is an object that contains other graphical objects (even other Layers)
in specific locations on it.
"""

import Tkinter
from object import Object

class Layer(Object):
    """
    @brief A subdivision of the parent Widget for organization sake.
    
    This allows you to group on screen objects and allows for 
    relative placement.It will also dynamically grow to fit whatever 
    is inside it.
    """
    def __init__(self, pos = (0,0), align="grid"):
        """
        @brief Constructs a Layer at specified position.
        
        @var position: A tuple of size 2 indicating the (x,y) 
        coordinates of the layer (top left corner)
        @var align: The alignment type of the object. 
        grid = (row, column), pack = center it!
        """
        Object.__init__(self)
        self._items = []
        
        self.set_align(align)
        self.set_position(pos)
        
        self._blended_background = False
        
    def get_blend(self):
        return str(self._blend)
    
    def blending(self, blended):
        """
        @brief Determines whether the background uses and passes the 
        blended background colors or not.
        
        @var blended: True/False Whether or not to use blending
        """
        if blended == False and self._blended_background == True:
            for item in self._items:
                item.blend(remove=self._bColor)
            self._blended_background = False
            
        Object.blending(self, blended)
    
    def add(self, item):
        """
        @brief Adds an item to a layer.
        
        @var item: The drawable item that is to be added to the layer.
        """
        self._items.append(item)
        
        if (self.get_background_color(False) != "" and 
            self.get_background_color(False) != "clear" and 
            self._blended):
            item.blend(self.get_background_color(blended=False))
            self._blendedBackground = True
  
        for color in self._blend:
            item.blend(color)
                
        if self._component != None:                
            item.parent(self._component)
            
    def parent(self, parent):
        """
        @brief Sets the parent of the Layer object.
        @note Can only be called once.
        
        @var parent: The object the Layer will be on.
        """
        if self._component == None:
            self._component = Tkinter.Frame(parent)

            for item in self._items:
                item.parent(self._component)
                
            self._parent() 
                
            
    def set_background_color(self, color):
        """
        @brief Overloaded background color set to include blending.
        
        @var color: Color of the base background (before blending).
        """
        if self._blended:
            for item in self._items:
                item.blend(add=color, 
                           remove=self.get_background_color(blended=False))
                self._blendedBackground = True
            
        # The old method can carry on from here
        Object.set_background_color(self, color)
        
    def blend(self, add="", remove=""):
        """
        @brief Overloaded blend to propagate blend to all children 
        of all sub-layers.
        
        @var add: The color to be blended into the background.
        @var remove: The color to be taken out of the blend 
        (has to be in there already).
        """
        for item in self._items:
            item.blend(add=add, remove=remove)
            
        # The old method can carry on from here
        Object.blend(self, add=add, remove=remove)
     