"""
@file Button.py
@date 8/24/2010
@version 0.1
@author Aaron Taggart

@brief Button source code.
A button is a clickable object on screen, I'm sure you know.
"""

from object import Object
import Tkinter

class Button(Object):
    """
    @brief Clickable object with a label inside it.
    """
    
    def __init__(self, text=""):
        """
        @brief constructs a button with a given text.
        
        @var text: The label of the Button
        """
        self._text = text
        Object.__init__(self)
        self._forecolor = ""
        
    def set_message(self, text):
        """
        @brief Sets the message displayed within a Button
        
        @var text: The label of the Button
        """
        if self._component != None:
            self._component["text"] = text
        self._text = text
        
    def get_message(self):
        """
        @brief Gets the displayed message from the Button
        
        @return What is currently in the Button
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
            self._component = Tkinter.Button(parent, text=self._text)
            
            if self._forecolor != "":
                self._component["fg"] = self._forecolor

            self._parent()
            