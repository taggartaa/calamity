"""
@file TextBox.py
@date 8/23/2010
@version 0.1
@author Aaron Taggart

@brief TextBox source code.

The TextBox is a read only (can be changed via setMessage, 
but can't be changed via the User clicking and typing) message
that is displayed on the screen. Can be used for something like 
a label.
"""

from object import Object
import Tkinter

class TextBox(Object):
    """
    @brief A way of displaying information onto Widgets
    """
    
    def __init__(self, text="", pos = (0,0), align="grid", 
                 width = 0, justify="center"):
        """
        @brief Constructs a TextBox (not displayed until added to something)
        
        @var text: The text within the TextBox.
        @var pos: Tuple of size 2 indicating position. i.e. (50,50)
        @var align: The alignment type of the object. grid = (row, column), 
        pack = center it!
        @var width: How large the textbox should be 
        (0 will expand to fit the text)
        @var justify: The alignment of the text within the textbox 
        (left, right, center)
        """
        Object.__init__(self)
        
        self._text = text
        self._forecolor = ""
        self._justified = justify
        
        self.set_position(pos)
        self.set_align(align)
        if width > 0:
            self.set_width(width)
            
    def justify(self, justify=""):
        """
        @brief Sets or returns how the text is aligned within the textbox.
        
        @var justify: The alignment of the text within the textbox 
        (left, right, center)
        @return What the current alignment of the text is.
        """
        self._justified = justify
        if self._component != None:
            if self._justified == "left":
                self._component["anchor"]="w"
            elif self._justified == "right":
                self._component["anchor"]="e"
            elif self._justified == "center":
                self._component["anchor"]="center"
                
        return self._justified
    
    def set_message(self, text):
        """
        @brief Sets the message displayed within a TextBox
        
        @var message: New message to be displayed.
        """
        if self._component != None:
            self._component["text"] = text

        self._text = text
        
    def get_message(self):
        """
        @brief Gets the displayed message from the TextBox
        
        @return What is currently in the TextBox
        """
        if self._component != None:
            return self._component["text"]
        return self._text
    
    def set_foreground_color(self, color):
        """
        @brief Sets the color of the text itself.
        For a list of the accepted colors, see the Tkinter documentation.
        
        @var color: Color you wish to change it too. (lowercase spelling, 
        Tkinter provides other valid methods for specifying color)
        """
        if self._component != None:
            self._component["fg"] = color
            
        self._forecolor = color 
            
    def get_foreground_color(self, color):
        """
        @brief Gets the color of the text.
        
        @return The current color of the text.
        """
        if self._component != None:
            return self._component["fg"]
        return self._forecolor
            
    
    def parent(self, parent):
        """
        @brief Sets the parent of the TextBox
        @note Can only be called once
        
        @var parent The Widget that the TextBox is to be placed on.
        """
        if self._component == None:
            self._component = Tkinter.Label(parent, text=self._text)
            self.justify(self._justified)
            
            if self._forecolor != "":
                self._component["fg"] = self._forecolor

            self._parent()
            