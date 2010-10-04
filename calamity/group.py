"""
@file Group.py
@date 8/2/2010
@version 0.1
@author Aaron Taggart

@brief The file that contains the implementation for the Group class.

A Group is set of "like" Members specified by the user. Members are organized
first by  their status, then their nickname via descending alphabetical.

@note TabSize and FontSize must be globally defined before this file 
can be imported.
"""

# Used for in-order inserting into a list
import bisect

import gui

import globals
from member import Member

class Group:
    """
    @brief A set of like Members
    """
    
    def __init__(self, name, position = (0,0)):
        """
        @brief Constructor for the Group
        
        @param name: A string that represents the name of the Group.
        @param position: where the Group is relative to other Groups.
        @todo change over to dictionaries for efficiency.
        """

        self._layer = gui.Layer(pos=position)
        self._layer.set_border_width(globals.GROUP_BORDER_WIDTH)
        self._layer.set_border_type("flat")
        self._name = gui.TextBox(text=name, pos=(0,0))
        self._name.set_border_type("raised")
        self._name.set_border_width(2)
        self._layer.add(self._name)
        
        self._highlight_color = "white"
        
        self._members = []
        
    def get_blend(self):
        """
        @brief Gets the blended color of the background
        
        @return Blended background color
        """
        return self._layer.get_blend()
        
    def get_layer(self):
        """
        @breif Used to add the Group to the screen
        
        @return The drawable layer that can be added to the screen.
        """
        return self._layer
        
    def add(self, item):
        """
        @brief Adds a Member to the Group in the proper position
        
        @param item: The Member to be inserted
        """

        position = bisect.bisect(self._members, item)
        bisect.insort(self._members, item)
        item.set_group(self)
        self.reorder(position)
        self._layer.add(item.get_layer())
        
    def reorder(self, startFrom=0):
        """
        @brief Sort the array from StartFrom, to the end.
        
        @param startFrom: Where to start from when sorting (inclusive)
        """
        i = startFrom
        for member in self._members[startFrom:]:
            member.set_postition((i+1, 0))
            member.set_border_color(self._highlight_color)
            if i%2 == 1:
                member.set_background_color(globals.MEMBER_ODD_COLOR)
            else:
                member.set_background_color(globals.MEMBER_EVEN_COLOR)
            i+=1
        

                
    def set_position(self, position):
        """
        @brief Sets the position of the Group
        
        @position A tuple of size 2 that indicates where the Group should be 
        positioned i.e. (10,50)
        """
        self._layer.set_position(position)
        
    def get_position(self):
        """
        @brief Gets the position of the Group object
        
        @return Tuple of size 2 indicating the position of the Group 
        i.e. (10,20)
        """
        return self._layer.get_position()
    
    def set_background_color(self, color):
        """
        @brief Sets the background color of the Group.
        
        @var color: New background color of the group.
        """
        self._layer.set_background_color(color)
        
    def get_background_color(self):
        """
        @brief Gets the background color of the Group.
        
        @var The background color of the group.
        """
        return self._layer.get_background_color(False)
    
    def set_highlight_color(self, color):
        """
        @brief Color members of this group will be highlighted with.
        
        @var color: The color to highlight members with.
        """
        self._highlight_color = color
        
        for member in self._members:
            member.set_border_color(color)
            
    def tab(self, direction):
        """
        @brief Highlights next member in the group.
        
        @var direction: Whether the next member is up or down.
        @return True/False Whether or not the tab was successful.
        """
        if len(self) == 0:
            return False
        
        try:
            i = self._members.index(Member.focus[0])
        except:
            i = -1
            
        if direction == gui.globals.UP:
            
            if i == -1:
                self._members[-1].clicked("")
                return True
            
            if self._members[0] != Member.focus[0]:
                self._members[i-1].clicked("")
                return True
            else:
                return False
            
        elif direction == gui.globals.DOWN:
            
            if i == -1:
                self._members[0].clicked("")
                return True
            
            if self._members[-1] != Member.focus[0]:
                self._members[i+1].clicked("")
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
        for member in self._members:
            if member.get_email() == email:
                return index
            index+=1
        return -1
    
    def sort(self):
        """
        @brief Sorts the members list.
        """
        self._members.sort()
        self.reorder()
                
    def __getitem__(self, index):
        """
        @brief Indexing a Group gives you the member the group is in.
        
        @var index: The index of the Member you want.
        @return The Member at position index
        """
        return self._members[index]
        
            
    def __eq__(self, other):
        """
        @brief Groups are equal if they have the same name.
        
        @return True/False Whether or not they have the same name.
        """
        
        return self._name == other._name

    def __len__(self):
        """
        @brief Returns how many members are in the group.
        
        @return The number of members in the group.
        """
        return len(self._members)
        