"""
@file Window.py
@date 8/9/2010
@version 0.1
@author Aaron Taggart

@brief Contains classes that create new Windows (like popups)

A Window is an object that does not need a parent, as it is not placed onto anything.
"""

import Tkinter
from Object import Object

"""
@note Tk is a class in Tkinter in charge of the whole application. This makes App an alias to it.
@note The run method is the only method that will be used by App, and is therefore important that it exists. (i.e. if you port it)
"""
App = Tkinter.Tk    

        
class PopUp(Tkinter.Toplevel):
    """
    @brief A popup message to be displayed
    """
    
    def __init__(self, parent = None, title = "Pop Up", message = "This is a Pop Up!"):
        """
        @brief A class for giving a message to the user.
        
        @var parent: The Pop Up will be displayed in the center of the parent.
        @var title: What will be in the title bar of the Pop Up.
        @var message: The message that the user will be displayed.
        """
        Tkinter.Toplevel.__init__(self, parent.getComponent())
        self.transient(parent.getComponent())
        
        self.title(title)
        Tkinter.Label(self, text=message).pack()
        Tkinter.Button(self, text = "OK", command=self.destroy).pack(pady = 5)

class Window(Object):
    """
    @brief This will be a top level Window. (It has no parent)
    
    @cvar windows: The number of windows that have been created so far. (Used since the first one is created with Tk()
    """
    __windows = 0
    
    def __init__(self, title = "Title", app = None):
        """
        @brief Constructs a top level Window with obvious binds already done. (such as close, minimise, and maximise)
        
        @var title: The title of the window.
        @var app: The application it belongs to. (Only needed for the first Window created)
        """
        Object.__init__(self)
        
        if Window.__windows != 0:
            self._component = Tkinter.Toplevel()
        else:
            self._component = app
            
        self._align = "none"
        self._bColor = "clear"
        self._component.title(title)
            
        Window.__windows+=1
        
    def add(self, item):
        """
        @brief Adds Window specific items to the Window. (i.e. MenuBar, Layer)
        
        @var item: Item to be added to the screen
        """
        item.parent(self._component)
        
        if self.getBackgroundColor(False) != "" and self.getBackgroundColor(False) != "clear":
            try:
                item.blend(self.getBackgroundColor(blended=False))
            except:
                pass
            