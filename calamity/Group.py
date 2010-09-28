"""
@file Group.py
@date 8/2/2010
@version 0.1
@author Aaron Taggart

@brief The file that contains the implementation for the Group class.

A Group is set of "like" Members specified by the user. Members are organized
first by  their status, then their nickname via descending alphabetical.

@note TabSize and FontSize must be globally defined before this file is imported.
"""

# Used for in-order inserting into a list
import bisect

import gui

import Globals
from Member import Member

class Group:
    """
    @brief A set of like Members
    """
    
    def __init__(self, name, position = (0,0)):
        """
        @brief Constructor for the Group
        
        @param name: A string that represents the name of the Group
        @param members: An optional list of Members (or just a member) to initialize the group. 
        @todo change over to dictionaries for efficiency.
        """

        self.__layer = gui.Layer(pos=position)
        self.__layer.setBorderWidth(Globals.GROUP_BORDER_WIDTH)
        self.__layer.setBorderType("flat")
        self.__name = gui.TextBox(text=name, pos=(0,0))
        self.__name.setBorderType("raised")
        self.__name.setBorderWidth(2)
        self.__layer.add(self.__name)
        
        self.__hColor = "white"
        
        self.__members = []
        
    def getBlend(self):
        """
        @brief Gets the blended color of the background
        
        @return Blended background color
        """
        return self.__layer.getBlend()
        
    def getLayer(self):
        """
        @breif Used to add the Group to the screen
        
        @return The drawable layer that can be added to the screen.
        """
        return self.__layer
        
    def add(self, item):
        """
        @brief Adds a Member to the Group in the proper position
        
        @param item: The Member to be inserted
        """

        position = bisect.bisect(self.__members, item)
        bisect.insort(self.__members, item)
        item.setGroup(self)
        self.reOrder(position)
        self.__layer.add(item.getLayer())
        
    def reOrder(self, startFrom=0):
        """
        @brief Sort the array from StartFrom, to the end.
        
        @param startFrom: Where to start from when sorting (inclusive)
        """
        i = startFrom
        for member in self.__members[startFrom:]:
            member.setPostition((i+1, 0))
            member.setBorderColor(self.__hColor)
            if i%2 == 1:
                member.setBackgroundColor(Globals.MEMBER_ODD_COLOR)
            else:
                member.setBackgroundColor(Globals.MEMBER_EVEN_COLOR)
            i+=1
        

                
    def setPosition(self, position):
        """
        @brief Sets the position of the Group
        
        @position A tuple of size 2 that indicates where the Group should be positioned i.e. (10,50)
        """
        self.__layer.setPosition(position)
        
    def getPosition(self):
        """
        @brief Gets the position of the Group object
        
        @return Tuple of size 2 indicating the position of the Group i.e. (10,20)
        """
        return self.__layer.getPosition()
    
    def setBackgroundColor(self, color):
        """
        @brief Sets the background color of the Group.
        
        @var color: New background color of the group.
        """
        self.__layer.setBackgroundColor(color)
        
    def getBackgroundColor(self):
        """
        @brief Gets the background color of the Group.
        
        @var The background color of the group.
        """
        return self.__layer.getBackgroundColor(False)
    
    def setHighlightColor(self, color):
        """
        @brief Color members of this group will be highlighted with.
        
        @var color: The color to highlight members with.
        """
        self.__hColor = color
        
        for member in self.__members:
            member.setBorderColor(color)
            
    def tab(self, direction):
        """
        @brief Highlights next member in the group.
        
        @var direction: Whether the next member is up or down.
        @return True/False Whether or not the tab was successful.
        """
        if len(self) == 0:
            return False
        
        try:
            i = self.__members.index(Member.focus[0])
        except:
            i = -1
            
        if direction == gui.Globals.UP:
            
            if i == -1:
                self.__members[-1].clicked("")
                return True
            
            if self.__members[0] != Member.focus[0]:
                self.__members[i-1].clicked("")
                return True
            else:
                return False
            
        elif direction == gui.Globals.DOWN:
            
            if i == -1:
                self.__members[0].clicked("")
                return True
            
            if self.__members[-1] != Member.focus[0]:
                self.__members[i+1].clicked("")
                return True
            else:
                return False
        
    def find(self, email):
        """
        @brief Returns the index of a Member with the email of the parameter
        
        @var email: The email of the Member to search for.
        @return The index of the member, -1 if not found. 
        """
        index = 0
        for member in self.__members:
            if member.getEmail() == email:
                return index
            index+=1
        return -1
    
    def sort(self):
        """
        @brief Sorts the members list.
        """
        self.__members.sort()
        self.reOrder()
                
    def __getitem__(self, index):
        """
        @brief Indexing a Group gives you the member the group is in.
        
        @var index: The index of the Member you want.
        @return The Member at position index
        """
        return self.__members[index]
        
            
    def __eq__(self, other):
        """
        @brief Groups are equal if they have the same name.
        
        @return True/False Whether or not they have the same name.
        """
        
        return self.__name == other.__name

    def __len__(self):
        """
        @brief Returns how many members are in the group.
        
        @return The number of members in the group.
        """
        return len(self.__members)
        
        