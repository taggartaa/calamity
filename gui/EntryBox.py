"""
@file EntryBox.py
@date 8/23/2010
@version 0.1
@author Aaron Taggart

@brief EntryBox source code.

An EntryBox is a single line user-writable box.
"""

from Object import Object
import Tkinter

class EntryBox(Object):
    """
    @brief A textbox that is writable, and is used for user input.
    """
    
    def __init__(self):
        """
        @brief Creates an EntryBox
        """
        Object.__init__(self)
        self.__text = ""
        
    def setMessage(self, message):
        """
        @brief Sets the visable text to message
        
        @var message: The new text that is visable within the EntryBox
        """
        self.__text = message
        
        if self._component != None:
            self.clear()
            self._component.insert(0, message)
        
    def getMessage(self):
        """
        @brief Gets the message from the EntryBox.
        
        @return The message in the EntryBox
        """
        if self._component != None:
            return self._component.get()
        return self.__text
    
    def clear(self):
        """
        @brief Clears out the EntryBox text.
        """
        self.__text = ""
        if self._component != None:
            self._component.delete(0,Tkinter.END)

    
    def parent(self, parent):
        """
        @brief Sets the parent of the EntryBox
        @note Can only be called once
        
        @var parent The Widget that the EntryBox is to be placed on.
        """
        self._component = Tkinter.Entry(parent)
        self._parent()
