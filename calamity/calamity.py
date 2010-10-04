
"""
@file Calamity.py
@date 7/31/2010
@version 0.1
@author Aaron Taggart

@brief Contains source code for the Calamity app that should be implementation 
independent for easy porting.
"""

import gui
import network

import globals
from member import Member
from group import Group
from conversation import Conversation

class CalamityApp:
    """
    The entire application in one class object. One instance of this class will
    be one instance of calamity running on your computer.
    """
    
    def __init__(self):
        """
        @brief Constructs the Calamity application
        """
        
        self._app = gui.App()
        
        self._window = gui.Window("Calamity", self._app)
        
        self._connection = False
        
        # Login Screen
        self._sign_in_layer = gui.Layer(align="pack")
        
        self._email_label = gui.TextBox(text="Email:", justify="right")
        self._email = gui.EntryBox()
        self._email.set_position((0,1))
        
        self._password_label = gui.TextBox(text="Password:", 
                                           justify="right", 
                                           pos=(1,0))
        self._password = gui.EntryBox()
        self._password.set_hidden_message()
        self._password.set_position((1,1))
        
        self._sign_in = gui.Button(text="Sign In")
        self._sign_in.set_position((2,1))
        self._sign_in.set_border_type("raised")
        
        self._sign_in_layer.add(self._email_label)
        self._sign_in_layer.add(self._email)
        self._sign_in_layer.add(self._password_label)
        self._sign_in_layer.add(self._password)
        self._sign_in_layer.add(self._sign_in)
        
        # Login Binds
        self._sign_in.bind(gui.globals.CLICKED, self.sign_in)
        self._app.bind(gui.globals.ENTER, self.sign_in)
        
        
        # After Login
        self._layer = gui.Layer(align="pack")
        self._layer.set_visibility(False)
        self._layer.set_background_color("clear")
        
        menu = gui.Menu("File")
        menu.add(gui.MenuItem("About", 
                              "Shows info about the program.", 
                              self.about))
        menu.add(gui.MenuItem("Exit", "Closes the window.", self.close))
        
        menubar = gui.MenuBar()
        menubar.add(menu)
        
        self._groups = []
        
        self.add(Group("Default"))
                
        self._window.add(menubar)
        self._window.add(self._sign_in_layer)
        self._window.add(self._layer)
        
        
    def add(self, item):
        """
        @brief Adds an item (i.e Group) to the window.
        
        @param item: A valid object to be added to the Calamity Window. (Group)
        """
        
        # If its a member, add it to the default group
        try:
            item.get_nickname()
            self._groups[0].add(item)
            return
        except:
            pass
            
        item.set_position((len(self._groups),0))

	# recolor every other group
        if len(self._groups)%2 == 1:
            item.set_background_color(globals.GROUP_ODD_COLOR)
            item.set_highlight_color(globals.HIGHLIGHT_BORDER_COLOR_ODD)
        else:
            item.set_background_color(globals.GROUP_EVEN_COLOR)
            item.set_highlight_color(globals.HIGHLIGHT_BORDER_COLOR_EVEN)

        self._groups.append(item)
        self._layer.add(item.get_layer())
        
        
    def tab(self, event):
        """
        @brief Highlights the next/previous thing in the tab order.
        
        @var event: The event that triggered the tab.
        """
        
        if Member.focus == []:
            self._groups[0].tab(gui.globals.DOWN)
            return
        
        curGroup = Member.focus[0].get_group()
        
        if event.keysym == "Up":
            while not curGroup.tab(gui.globals.UP):
                if curGroup == self._groups[0]:
                    curGroup = self._groups[-1]
                else:
                    curGroup = self._groups[self._groups.index(curGroup)-1]
                    
        elif event.keysym == "Down" or event.keysym == "Tab":
            while not curGroup.tab(gui.globals.DOWN):
                if curGroup == self._groups[-1]:
                    curGroup = self._groups[0]
                else:
                    curGroup = self._groups[self._groups.index(curGroup)+1]
                    
    def enter(self, event):
        """
        @brief Start a conversation with all selected members. 
        (when the enter button is pressed)
        """
        if len(Member.focus) > 1:
            Conversation(members=Member.focus, 
                         bg=globals.CONVERSATION_GROUP_COLOR)
        elif len(Member.focus) == 1:
            Member.focus[0].start_conversation(event=event)
                
                          
                
    def run(self):
        """
        @brief Starts the Calamity application once initial 
            1. The window appears.
            2. Binded functions are now in action.
        """
        
        self._app.mainloop()
        
    def close(self):
        """
        @brief Closes the Calamity window.
        @todo Possibly run in background like MSN does when it's "closed"
        """
        self._app.destroy()
        
    def about(self):
        """
        @brief Says a little info about the application.
        """
        gui.PopUp(self._window, 
                  "About", 
                  "Calamity"+
                  "(Chris and Aaron Launch A Message Instantly To You)"+
                  "\n\n Its the cool way to IM!")
        
    def sign_in(self, event):
        """
        @brief Signs in using the email and password provided
        """
        connected = True
        loggedIn = False
        try:
            self._connection = network.login(email=self._email.get_message(), 
                                          password=self._password.get_message())
            self._connection.set_app(self)
            self.get_updates()
        except ValueError as e:
            print e
            connected = False
                
        if connected:
            
            # Bindings
            self._app.bind(gui.globals.UP, self.tab)
            self._app.bind(gui.globals.DOWN, self.tab)
            self._app.bind(gui.globals.TAB, self.tab)
            
            # Override the previous ENTER bind
            self._app.bind(gui.globals.ENTER, self.enter)
            
            self._sign_in_layer.set_visibility(False)
            self._layer.set_visibility(True)
            
    def get_updates(self):
        """
        @brief Get updates from the server, calls itself every second to check.
        @todo Perhaps threading this process instead to reduce busy waiting and 
        delay, but I foresee to many issues at the moment
        """
        self._connection.listen()
        self._app.after(1000, self.get_updates)
        
        
            
    def __getitem__(self, index):
        """
        @brief Indexing a Calamity app gives you the group at position index.
        
        @var index: The index of the group you want.
        @retur.n The group at position index
        """
        return self._groups[index]