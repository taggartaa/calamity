"""
@file Member.py
@date 8/2/2010
@version 0.1
@author Aaron Taggart

@brief This is the implementation of the Member class.

@note FontSize must be globally defined in order to use this module.
"""


from conversation import Conversation
import globals

import gui

class Member:
    """
    @brief A Member is a single user in one of your Groups 
    (or the Default Group)
    
    It represents another instant messenger user (Hopefully Calamity)
    """
    
    focus = []
    
    def __init__(self, name, email, status = "offline", message = ""):
        """
        @brief Constructor of the Member
        
        @param nickname: The name that appears in the window for the user to 
        identify a Member
        @param email: Email address of the Member
        @param status: Current state the friend is in. 
        (offline, online, away, busy) type: string
        @param message: The quote after the users name
        """

        #Used to keep track of the borderwidth when highlighted
        self._border_width = 0
        
        self._layer = gui.Layer()
        self._border = gui.Layer()
        
        self._border.blending(False)
        self._border.set_background_color("black")
        
        self._layer.set_border_type("flat")
        
        self._email = email
        self._status = gui.TextBox(text="N", 
                                   pos=(0,0), 
                                   width = globals.MEMBER_STATUS_WIDTH)
        
        self._nick = name
        self._nickname = gui.TextBox(pos=(0,1), 
                                     width = globals.MEMBER_NAME_WIDTH, 
                                     justify="left")
        self.set_nickname(name)
        
        self._mess = message
        self._message = gui.TextBox(pos=(0,2), 
                                    width = globals.MEMBER_MESSAGE_WIDTH, 
                                    justify="left")
        self.set_message(message)
        
        self._selected = False
        
        self.set_status(status)
        
        self._layer.add(self._status)
        self._layer.add(self._nickname)
        self._layer.add(self._message)
        
        self._border.add(self._layer)
        
        self._group = ""
        self._window = None
        
        self._conv = []
        
        #bindings
        self._status.bind(gui.globals.CLICKED, self.clicked)
        self._nickname.bind(gui.globals.CLICKED, self.clicked)
        self._message.bind(gui.globals.CLICKED, self.clicked)
        
        self._status.bind(gui.globals.DBL_CLICKED, self.start_conversation)
        self._nickname.bind(gui.globals.DBL_CLICKED, self.start_conversation)
        self._message.bind(gui.globals.DBL_CLICKED, self.start_conversation)
        
    def get_layer(self):
        """
        @breif Used to add the member to the screen
        
        @return The drawable layer that can be added to the screen.
        """
        return self._border
    
    def set_group(self, group):
        """
        @brief Sets the Group the Member is in. 
        Needs to be set so tab order works properly.
        
        @var group: The Group this Member is in.
        """
        self._group = group
        
    def get_group(self):
        """
        @brief Gets the Group this Member is in.
        
        @return The Group this Member is in.
        """
        return self._group
        
    def set_nickname(self, nickname):
        """
        @brief Sets the nickname of the Member
        
        @param nickname: New nickname of the Member
        """
        
        if len(nickname) > globals.MAX_NICKNAME_LENGTH:
            nick = nickname[0:globals.MAX_NICKNAME_LENGTH-3]+"..."
        else:
            nick = nickname
            
        self._nickname.set_message(nick)
        
    def get_nickname(self):
        """
        @brief Gets the nickname of a Member
        
        @return string: nickname of the Member
        """
        return self._nick
        
    def set_status(self, status):
        """
        @brief Sets the status of the Member (offline, online, away, busy)
        
        offline - (red) Unable to talk to Member.
        online - (Green) Able to talk to Member.
        away - (Grey) Able to send messages to Member, 
        but don't expect a response.
        busy - (Yellow) Member is there, but will not likely respond.
        
        @param status: New status of the Member
        """
        if status == "offline":
            self._status.set_message("N")
            self._status.set_foreground_color("red")
            
        elif status == "online":
            self._status.set_message("Y")
            self._status.set_foreground_color("Green")
            
        elif status == "away":
            self._status.set_message("A")
            self._status.set_foreground_color("Grey")
            
        elif status == "busy":
            self._status.set_message("B")
            self._status.set_foreground_color("Yellow")
        
    def get_status(self):
        """
        @brief Returns the status of the Member (Online, Offline, Away, Busy)
        
        @return string: Current status of the Member.
        """
        status = self._status.get_message()
        
        if status == "N":
            return "offline"
        
        elif status == "Y":
            return "online"
        
        elif status == "A":
            return "away"
        
        elif status == "B":
            return "busy"
        
    def set_message(self, message):
        """
        @brief Sets the message that is displayed after the nickname
        
        @param message: The new message of the Member 
        """
        if len(message) > globals.MAX_MESSEGE_LENGTH:
            mess = message[0:globals.MAX_MESSEGE_LENGTH-3]+"..."
        else:
            mess = message
        self._message.set_message(mess)
        
    def get_message(self):
        """
        @brief Gets the current message of the Member
        
        @return string: The current message
        """
        return self.__mess
    
    def get_email(self):
        """
        @brief Gets the email of the Member.
        
        @return The email of the Member
        """
        return self._email
    
    def set_postition(self, position):
        """
        @brief Sets the position of the Member on screen
        
        @param postition: A tuple of size 2 indicating the Member's new position
        """
        self._border.set_position(position)
        
    def get_position(self):
        """
        @brief Gets the position of the Member on screen
        
        @return tuple: tuple of size two indicating the current position 
        of the Member
        """
        return self._border.get_position()
    
    def set_background_color(self, color):
        """
        @brief Sets the background color of the member.
        
        @var color: New color of the member.
        """
        self._layer.set_background_color(color)
        
    def set_border_color(self, color):
        """
        @brief Sets the border color of the Member
        
        @var color: The color of the border
        """
        self._border.set_background_color(color)
        
    def set_border_width(self, width):
        """
        @brief Sets the width of the border.
        
        @var width: The new width of the border.
        """
        self._border.set_border_width(width)
        self._border_width = width
        
    def select(self, selected = True):
        """
        @brief Used to select or deselect a Member.
        
        @var selected: True/False Should the member be selected or not.
        """
        
        if selected != self._selected:
            if selected:
                self._border.set_border_width(globals.HIGHLIGHT_BORDER_WIDTH)
                Member.focus.append(self)
            else:
                self._border.set_border_width(self._border_width)
                Member.focus.remove(self)
            
            self._selected = selected
        
    def selected(self):
        """
        @brief Determines whether the member is currently selected.
        
        @return True/False Whether or not the Member is selected.
        """
        return self._selected
        
    def __lt__(self, other):
        """
        @brief operator < (overloaded for sorting)
        
        @return True/False First based on Status, 
        then on nickname (alphebitical decending).
        """
        status = self.get_status()
        Ostatus = other.get_status()
        
        if status == Ostatus:
            return self.get_nickname() < other.get_nickname()
        
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
        return (self.get_status() == other.get_status() and 
                self.get_nickname() == other.get_nickname() and 
                self._email == other._email)
    
    def __le__(self, other):
        """
        @brief operator <= (overloaded for sorting)
        
        @return True/False First based on Status, 
        then on nickname (alphebitical decending).
        """
        return self < other or self == other
    
    def __gt__(self, other):
        """
        @brief operator > (overloaded for sorting)
        
        @return True/False First based on Status, 
        then on nickname (alphebitical decending).
        """
        return not (self <= other)
    
    def __ge__(self, other):
        """
        @brief operator >= (overloaded for sorting)
        
        @return True/False First based on Status, 
        then on nickname (alphebitical decending).
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
        
    def start_conversation(self, event):
        """
        @brief Start a conversation with this user.
        Creates a top level window.
        """
        if self._border.get_background_color(False) == globals.GROUP_ODD_COLOR:
            background_color = globals.CONVERSATION_EVEN_COLOR
        else:
            background_color = globals.CONVERSATION_ODD_COLOR
            
        self._conv.append(Conversation(self, bg=background_color))
        
    