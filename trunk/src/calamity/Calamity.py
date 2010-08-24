
"""
@file Calamity.py
@date 7/31/2010
@version 0.1
@author Aaron Taggart

@brief Contains source code for the Calamity app that should be implementation independent for easy porting.
"""

import gui

import Globals
from Member import Member
from Group import Group
from Conversation import Conversation

class CalamityApp:
    """
    The entire application in one class object. One instance of this class will
    be one instance of calamity running on your computer.
    """
    
    def __init__(self):
        """
        @brief Constructs the Calamity application
        """
        
        self.__app = gui.App()
        
        self.__window = gui.Window("Calamity", self.__app)
        
        self.__layer = gui.Layer(align="pack")
        self.__layer.setBackgroundColor("clear")
        
        menu = gui.Menu("File")
        menu.add(gui.MenuItem("About", "Shows info about the program.", self.about))
        menu.add(gui.MenuItem("Exit", "Closes the window.", self.close))
        
        menubar = gui.MenuBar()
        menubar.add(menu)
        
        self.__groups = []
        
        self.add(Group("Default"))
                
        self.__window.add(menubar)
        self.__window.add(self.__layer)
        
        # Bindings
        self.__app.bind(gui.Globals.UP, self.tab)
        self.__app.bind(gui.Globals.DOWN, self.tab)
        self.__app.bind(gui.Globals.TAB, self.tab)
        
        self.__app.bind(gui.Globals.ENTER, self.enter)
        
        
    def add(self, item):
        """
        @brief Adds an item (i.e Group) to the window.
        
        @param item: A valid object to be added to the Calamity Window. (Group)
        """
        
        # If its a member, add it to the default group
        try:
            item.getNickname()
            self.__groups[0].add(item)
            return
        except:
            pass
            
        item.setPosition((len(self.__groups),0))

	# recolor every other group
        if len(self.__groups)%2 == 1:
            item.setBackgroundColor(Globals.GROUP_ODD_COLOR)
            item.setHighlightColor(Globals.HIGHLIGHT_BORDER_COLOR_ODD)
        else:
            item.setBackgroundColor(Globals.GROUP_EVEN_COLOR)
            item.setHighlightColor(Globals.HIGHLIGHT_BORDER_COLOR_EVEN)

        self.__groups.append(item)
        self.__layer.add(item.getLayer())
        
        
    def tab(self, event):
        """
        @brief Highlights the next/previous thing in the tab order.
        
        @var event: The event that triggered the tab.
        """
        
        if Member.focus == []:
            self.__groups[0].tab(gui.Globals.DOWN)
            return
        
        curGroup = Member.focus[0].getGroup()
        
        if event.keysym == "Up":
            if not curGroup.tab(gui.Globals.UP):
                if curGroup == self.__groups[0]:
                    self.__groups[-1].tab(gui.Globals.UP)
                else:
                    self.__groups[self.__groups.index(curGroup)-1].tab(gui.Globals.UP)
                    
        elif event.keysym == "Down" or event.keysym == "Tab":
            if not curGroup.tab(gui.Globals.DOWN):
                if curGroup == self.__groups[-1]:
                    self.__groups[0].tab(gui.Globals.DOWN)
                else:
                    self.__groups[self.__groups.index(curGroup)+1].tab(gui.Globals.DOWN)
                    
    def enter(self, event):
        """
        @brief Start a conversation with all selected members. (when the enter button is pressed)
        """
        if len(Member.focus) > 1:
            Conversation(members=Member.focus, bg=Globals.CONVERSATION_GROUP_COLOR)
        elif len(Member.focus) == 1:
            Member.focus[0].startConversation(event=event)
                
                          
                
    def run(self):
        """
        @brief Starts the Calamity application once initial 
            1. The window appears.
            2. Binded functions are now in action.
        """
        
        self.__app.mainloop()
        
    def close(self):
        """
        @brief Closes the Calamity window.
        @todo Possibly run in background like MSN does when it's "closed"
        """
        self.__app.destroy()
        
    def about(self):
        """
        @brief Says a little info about the application.
        """
        gui.PopUp(self.__window, "About", "Calamity (Chris and Aaron Launch A Message Instantly To You)\n\n Its the cool way to IM!")
        
        
