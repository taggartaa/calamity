"""
@file Conversation.py
@date 8/15/2010
@version 0.1
@author Aaron Taggart

@brief This file holds the implementation of the Conversation class.
"""

import gui

class Conversation:
    """
    @brief A window used to comunicate to other users.
    """
    
    def __init__(self, member = None, members = [], bg = "clear"):
        """
        @brief Constructs a chat window between you and some other windows.
        
        @var member: A single member to converse with.
        @var members: A list of members to converse with.
        """
        
        if len(members) > 0:
            name = "Group Chat"
        else:
            try:
                name = member.get_nickname()
            except:
                name = "Chat"
        
        # GUI stuff
        self._window = gui.Window(title=name)
        self._window.row_growth_rate(row=0, growthRate=1)
        self._window.column_growth_rate(column=0, growthRate=1)
        
        self._layer = gui.Layer()
        self._layer.set_background_color(bg)
        self._layer.set_growth(height=True, width=True)
        self._layer.row_growth_rate(row=0, growthRate=1)
        self._layer.column_growth_rate(column=0, growthRate=1)
        self._layer.set_position((0,0))
        
        self._messages = gui.MessageBox()
        self._messages.set_position((0,0))
        self._messages.set_growth(height=True, width=True)
        self._messages.set_padding(x=10, y=10)
        self._messages.set_border_type("sunken")
        self._messages.set_border_width(4)
        
        self._entry = gui.EntryBox()
        self._entry.set_position((1,0))
        self._entry.set_growth(height=False, width=True)
        self._entry.set_padding(x=10, y=10)
        
        #self.__send = Button(text="Send")
        #self.__send.setPosition((2,0))
        
        self._layer.add(self._messages)
        self._layer.add(self._entry)
        #self.__layer.add(self.__send)
        
        self._window.add(self._layer)
        
        # Member stuff
        self._members = []
        self.add(member)
        for m in members:
            self.add(m)
        
        
        #bindings
        self._window.bind(gui.globals.ENTER, self.send)
        #self.__send.bind(GUIglobals.CLICKED, self.send)
            
    def add(self, member):
        """
        @brief Adds a member to the conversation.
        
        @var member: The new member to be added to the conversation.
        """
        self._members.append(member)
        
    def send(self, event):
        """
        @brief Sends the message within the entry box to all other members 
        in the conversation.
        """
        
        self._messages.append("Me: " + self._entry.get_message() + "\n")
        self._entry.set_message("")
            