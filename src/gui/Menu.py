"""
@file Menu.py
@date 8/23/2010
@version 0.1
@author Aaron Taggart

@brief Contians code needed to build a full menubar

A Menubar is that convenient bar at the top of a window
which has all sorts of usefull menu options. 
"""

import Tkinter

class MenuItem:
    """
    @brief A single option within a menu.
    """
    
    def __init__(self, name="", info="", bind=None):
        """
        @brief Creates an option within a menu
        
        @var name: The value the user sees in the menu.
        @var info: What the menu options suppose to do.
        @var bind: The method/function bound to a click-event on that option.
        """
        self.__name = name
        self.__info = info
        self.__bind = bind
        self.__parentSet = False
        
    def parent(self, parent):
        if not self.__parentSet:
            self.__parentSet = True
            parent.add_command(label=self.__name, command=self.__bind)

class Menu:
    """
    @brief A single drop-down menu
    """
    
    def __init__(self, name):
        """
        @breif Creates and sets the displayed name of the Menu
        
        @var name: Name that the user will click to see the Menu
        """
        self.__name = name
        self.__menuitems = []
        self.__menu = None
        
    def add(self, menuItem):
        """
        @brief Adds a MenuItem to the drop-down list.
        
        @menuItem: A single MenuItem within the drop-down list to be added.
        """
        self.__menuitems.append(menuItem)
        
    def parent(self, parent):
        """
        @brief Sets the Parent the Menu will be in.
        @note This method can only be called once.
        
        @var parent: What Widget the Menu will be placed in.
        """
        if self.__menu == None:
            self.__menu = Tkinter.Menu(parent, tearoff=0)
            for item in self.__menuitems:
                item.parent(self.__menu)
            parent.add_cascade(label=self.__name, menu=self.__menu)        

class MenuBar:
    """
    @brief Menu Bar at the top of a Window
    """
    
    def __init__(self):
        """
        @brief Sets up a menuBar in memory (only displayed when it knows its parent)
        """
        self._component = None
        self.__menus = []
        
    def add(self, menu):
        """
        @brief Adds a menu to the MenuBar
        
        @var menu: Menu to be added to the bar.
        """
        self.__menus.append(menu)
        
    def parent(self, parent):
        """
        @brief Sets the parent of the MenuBar, and shows it onscreen.
        @note This can only be done once.
        @note Like a top level window, there is no need to package this item, so I will not call self._parent()
        
        @var parent: The Window the MenuBar will be on. 
        """
        if self._component == None:
            self._component = Tkinter.Menu(parent)
        
            for menu in self.__menus:
                menu.parent(self._component)
                
            parent.config(menu=self._component)
        