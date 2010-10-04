"""
@file MessageBox.py
@date 8/23/2010
@version 0.1
@author Aaron Taggart

@brief MessageBox source code.

A MessageBox is multi-line TextBox which supports features such as 
tagged text formatting (different formating for text between tags). 
"""

from object import Object
import Tkinter

class MessageBox(Object):
    """
    @brief A multi-line Textbox with some extra features.
    """
    
    def __init__(self):
        """
        @brief Creates a multi-line text box.
        """
        Object.__init__(self)
        self._text = ""
        
    def append(self, message = "", to="bottom"):
        """
        @brief Appends a message onto the existing message.
        
        @var message: Message to be appended.
        @var to: Where to append it. (top, bottom)
        """
        if to == "bottom":
            self._text += message
                
        if to == "top":
            self._text = message + self._text
            
        if self._component != None:
            self._component["state"]=Tkinter.NORMAL
            if to == "bottom":
                self._component.insert(Tkinter.END, message)
            elif to == "top":
                self._component.insert("1.0", message)
                
            self._component["state"]=Tkinter.DISABLED
                
    def parent(self, parent):
        """
        @brief Sets the parent of the MessageBox
        @note Can only be called once
        
        @var parent The Widget that the MessageBox is to be placed on.
        """
        self._component = Tkinter.Text(parent)
        self._component["state"] = Tkinter.DISABLED
        self.append(self._text)
        self._parent()