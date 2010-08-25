"""
@file Button.py
@date 8/24/2010
@version 0.1
@author Aaron Taggart

@brief Button source code.
A button is a clickable object on screen, I'm sure you know.
"""

from Object import Object
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
        self.__text = text
        Object.__init__(self)
        self.__fColor = ""
        
    def setMessage(self, text):
        """
        @brief Sets the message displayed within a Button
        
        @var text: The label of the Button
        """
        if self._component != None:
            self._component["text"] = text
        self.__text = text
        
    def getMessage(self):
        """
        @brief Gets the displayed message from the Button
        
        @return What is currently in the Button
        """
        if self._component != None:
            return self._component["text"]
        return self.__text
    
    def setForegroundColor(self, color):
        """
        @brief Sets the color of the text itself.
        For a list of the accepted colors, see the Tkinter documentation.
        
        @var color: Color you wish to change it too. (lowercase spelling, Tkinter provides other valid methods for specifying color)
        """
        if self._component != None:
            self._component["fg"] = color
            
        self.__fColor = color 
            
    def getForegroundColor(self, color):
        """
        @brief Gets the color of the text.
        
        @return The current color of the text.
        """
        if self._component != None:
            return self._component["fg"]
        return self.__fColor
            
    
    def parent(self, parent):
        """
        @brief Sets the parent of the TextBox
        @note Can only be called once
        
        @var parent The Widget that the TextBox is to be placed on.
        """
        if self._component == None:
            self._component = Tkinter.Button(parent, text=self.__text)
            
            if self.__fColor != "":
                self._component["fg"] = self.__fColor

            self._parent()
            