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
                name = member.getNickname()
            except:
                name = "Chat"
        
        # GUI stuff
        self.__window = gui.Window(title=name)
        self.__window.rowGrowthRate(row=0, growthRate=1)
        self.__window.columnGrowthRate(column=0, growthRate=1)
        
        self.__layer = gui.Layer()
        self.__layer.setBackgroundColor(bg)
        self.__layer.setGrowth(height=True, width=True)
        self.__layer.rowGrowthRate(row=0, growthRate=1)
        self.__layer.columnGrowthRate(column=0, growthRate=1)
        self.__layer.setPosition((0,0))
        
        self.__messages = gui.MessageBox()
        self.__messages.setPosition((0,0))
        self.__messages.setGrowth(height=True, width=True)
        self.__messages.setPadding(x=10, y=10)
        self.__messages.setBorderType("sunken")
        self.__messages.setBorderWidth(4)
        
        self.__entry = gui.EntryBox()
        self.__entry.setPosition((1,0))
        self.__entry.setGrowth(height=False, width=True)
        self.__entry.setPadding(x=10, y=10)
        
        #self.__send = Button(text="Send")
        #self.__send.setPosition((2,0))
        
        self.__layer.add(self.__messages)
        self.__layer.add(self.__entry)
        #self.__layer.add(self.__send)
        
        self.__window.add(self.__layer)
        
        # Member stuff
        self.__members = []
        self.add(member)
        for m in members:
            self.add(m)
        
        
        #bindings
        self.__window.bind(gui.Globals.ENTER, self.send)
        #self.__send.bind(GUIglobals.CLICKED, self.send)
            
    def add(self, member):
        """
        @brief Adds a member to the conversation.
        
        @var member: The new member to be added to the conversation.
        """
        self.__members.append(member)
        
    def send(self, event):
        """
        @brief Sends the message within the entry box to all other members in the conversation.
        """
        
        self.__messages.append("Me: " + self.__entry.getMessage() + "\n")
        self.__entry.setMessage("")
            