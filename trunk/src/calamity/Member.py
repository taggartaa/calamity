"""
@file Member.py
@date 8/2/2010
@version 0.1
@author Aaron Taggart

@brief This is the implementation of the Member class.

@note FontSize must be globally defined in order to use this module.
"""


from Conversation import Conversation
import Globals

import gui

class Member:
    """
    @brief A Member is a single user in one of your Groups (or the Default Group)
    
    It represents another instant messenger user (Hopefully Calamity)
    """
    
    focus = []
    
    def __init__(self, name, email, status = "offline", message = ""):
        """
        @brief Constructor of the Member
        
        @param nickname: The name that appears in the window for the user to identify a Member
        @param email: Email address of the Member
        @param status: Current state the friend is in. (offline, online, away, busy) type: string
        @param message: The quote after the users name
        """

        #Used to keep track of the borderwidth when highlighted
        self.__borderWidth = 0
        
        self.__layer = gui.Layer()
        self.__border = gui.Layer()
        
        self.__border.blending(False)
        self.__border.setBackgroundColor("black")
        
        self.__layer.setBorderType("flat")
        
        self.__email = email
        self.__status = gui.TextBox(text="N", pos=(0,0), width = Globals.MEMBER_STATUS_WIDTH)
        
        self.__nick = name
        self.__nickname = gui.TextBox(pos=(0,1), width = Globals.MEMBER_NAME_WIDTH, justify="left")
        self.setNickname(name)
        
        self.__mess = message
        self.__message = gui.TextBox(pos=(0,2), width = Globals.MEMBER_MESSAGE_WIDTH, justify="left")
        self.setMessage(message)
        
        self.__selected = False
        
        self.setStatus(status)
        
        self.__layer.add(self.__status)
        self.__layer.add(self.__nickname)
        self.__layer.add(self.__message)
        
        self.__border.add(self.__layer)
        
        self.__group = ""
        self.__window = None
        
        self.__conv = []
        
        #bindings
        self.__status.bind(gui.Globals.CLICKED, self.clicked)
        self.__nickname.bind(gui.Globals.CLICKED, self.clicked)
        self.__message.bind(gui.Globals.CLICKED, self.clicked)
        
        self.__status.bind(gui.Globals.DBL_CLICKED, self.startConversation)
        self.__nickname.bind(gui.Globals.DBL_CLICKED, self.startConversation)
        self.__message.bind(gui.Globals.DBL_CLICKED, self.startConversation)
        
    def getLayer(self):
        """
        @breif Used to add the member to the screen
        
        @return The drawable layer that can be added to the screen.
        """
        return self.__border
    
    def setGroup(self, group):
        """
        @brief Sets the Group the Member is in. 
        Needs to be set so tab order works properly.
        
        @var group: The Group this Member is in.
        """
        self.__group = group
        
    def getGroup(self):
        """
        @brief Gets the Group this Member is in.
        
        @return The Group this Member is in.
        """
        return self.__group
        
    def setNickname(self, nickname):
        """
        @brief Sets the nickname of the Member
        
        @param nickname: New nickname of the Member
        """
        
        if len(nickname) > Globals.MAX_NICKNAME_LENGTH:
            nick = nickname[0:Globals.MAX_NICKNAME_LENGTH-3]+"..."
        else:
            nick = nickname
            
        self.__nickname.setMessage(nick)
        
    def getNickname(self):
        """
        @brief Gets the nickname of a Member
        
        @return string: nickname of the Member
        """
        return self.__nick
        
    def setStatus(self, status):
        """
        @brief Sets the status of the Member (offline, online, away, busy)
        
        offline - (red) Unable to talk to Member.
        online - (Green) Able to talk to Member.
        away - (Grey) Able to send messages to Member, but don't expect a response.
        busy - (Yellow) Member is there, but will not likely respond.
        
        @param status: New status of the Member
        """
        if status == "offline":
            self.__status.setMessage("N")
            self.__status.setForegroundColor("red")
            
        elif status == "online":
            self.__status.setMessage("Y")
            self.__status.setForegroundColor("Green")
            
        elif status == "away":
            self.__status.setMessage("A")
            self.__status.setForgroudColor("Grey")
            
        elif status == "busy":
            self.__status.setMessage("B")
            self.__status.setForgroundColor("Yellow")
        
    def getStatus(self):
        """
        @brief Returns the status of the Member (Online, Offline, Away, Busy)
        
        @return string: Current status of the Member.
        """
        status = self.__status.getMessage()
        
        if status == "N":
            return "offline"
        
        elif status == "Y":
            return "online"
        
        elif status == "A":
            return "away"
        
        elif status == "B":
            return "busy"
        
    def setMessage(self, message):
        """
        @brief Sets the message that is displayed after the nickname
        
        @param message: The new message of the Member 
        """
        if len(message) > Globals.MAX_MESSEGE_LENGTH:
            mess = message[0:Globals.MAX_MESSEGE_LENGTH-3]+"..."
        else:
            mess = message
        self.__message.setMessage(mess)
        
    def getMessage(self):
        """
        @brief Gets the current message of the Member
        
        @return string: The current message
        """
        return self.__mess
    
    def setPostition(self, position):
        """
        @brief Sets the position of the Member on screen
        
        @param postition: A tuple of size 2 indicating the Member's new position
        """
        self.__border.setPosition(position)
        
    def getPosition(self):
        """
        @brief Gets the position of the Member on screen
        
        @return tuple: tuple of size two indicating the current position of the Member
        """
        return self.__border.getPosition()
    
    def setBackgroundColor(self, color):
        """
        @brief Sets the background color of the member.
        
        @var color: New color of the member.
        """
        self.__layer.setBackgroundColor(color)
        
    def setBorderColor(self, color):
        """
        @brief Sets the border color of the Member
        
        @var color: The color of the border
        """
        self.__border.setBackgroundColor(color)
        
    def setBorderWidth(self, width):
        """
        @brief Sets the width of the border.
        
        @var width: The new width of the border.
        """
        self.__border.setBorderWidth(width)
        self.__borderWidth = width
        
    def select(self, selected = True):
        """
        @brief Used to select or deselect a Member.
        
        @var selected: True/False Should the member be selected or not.
        """
        
        if selected != self.__selected:
            if selected:
                self.__border.setBorderWidth(Globals.HIGHLIGHT_BORDER_WIDTH)
                Member.focus.append(self)
            else:
                self.__border.setBorderWidth(self.__borderWidth)
                Member.focus.remove(self)
            
            self.__selected = selected
        
    def selected(self):
        """
        @brief Determines whether the member is currently selected.
        
        @return True/False Whether or not the Member is selected.
        """
        return self.__selected
        
    def __lt__(self, other):
        """
        @brief operator < (overloaded for sorting)
        
        @return True/False First based on Status, then on nickname (alphebitical decending).
        """
        status = self.getStatus()
        Ostatus = other.getStatus()
        
        if status == Ostatus:
            return self.getNickname() < other.getNickname()
        
        if status == "online":
            return True
        elif status == "away" and Ostatus != "online":
            return True
        elif status == "busy" and Ostatus not in ["online", "away"]:
            return True
        else:
            return False
        
    def __eq__(self, other):
        """
        @brief operator = (overloaded for sorting)
        
        @return True/False Whether the status and nickname are exactly equal.
        """
        return self.getStatus() == other.getStatus() and self.getNickname() == other.getNickname() and self.__email == other.__email
    
    def __le__(self, other):
        """
        @brief operator <= (overloaded for sorting)
        
        @return True/False First based on Status, then on nickname (alphebitical decending).
        """
        return self < other or self == other
    
    def __gt__(self, other):
        """
        @brief operator > (overloaded for sorting)
        
        @return True/False First based on Status, then on nickname (alphebitical decending).
        """
        return not (self <= other)
    
    def __ge__(self, other):
        """
        @brief operator >= (overloaded for sorting)
        
        @return True/False First based on Status, then on nickname (alphebitical decending).
        """
        return not (self < other)
    
    def __ne__(self, other):
        """
        @brief operator != (overloaded for sorting)
        
        @return True/False Whether or not the Members are not exactly equal
        """
        return not (self == other)
    
    def clicked(self, event):
        """
        @brief Select this Member, and deselect all other members.
        """
        for member in Member.focus:
            member.select(False)
            
        self.select()
        
    def startConversation(self, event):
        """
        @brief Start a conversation with this user.
        Creates a top level window.
        """
        if self.__border.getBackgroundColor(False) == Globals.GROUP_ODD_COLOR:
            backgroundColor = Globals.CONVERSATION_EVEN_COLOR
        else:
            backgroundColor = Globals.CONVERSATION_ODD_COLOR
            
        self.__conv.append(Conversation(self, bg=backgroundColor))
        
    