"""
@file Globals.py
@date 8/9/2010
@version 0.1
@author Aaron Taggart

@brief This file holds all the global variables that many modules need
"""

# Width of the Status icon
MEMBER_STATUS_WIDTH = 2

# Width of the nickname for members
MEMBER_NAME_WIDTH = 20

# Width of a members message
MEMBER_MESSAGE_WIDTH = 30

# Width of an entire member
MEMBER_WIDTH = MEMBER_STATUS_WIDTH + MEMBER_NAME_WIDTH + MEMBER_MESSAGE_WIDTH

MEMBER_ODD_COLOR = "white"
MEMBER_EVEN_COLOR = "darkgrey"

# Maximum characters for a message
MAX_MESSEGE_LENGTH = 40

# Maximum nickname length
MAX_NICKNAME_LENGTH = 25

GROUP_ODD_COLOR = "black"
GROUP_EVEN_COLOR = "darkblue"
GROUP_BORDER_WIDTH = 4

HIGHLIGHT_BORDER_WIDTH = 5
HIGHLIGHT_BORDER_COLOR_EVEN = GROUP_ODD_COLOR
HIGHLIGHT_BORDER_COLOR_ODD = GROUP_EVEN_COLOR

CONVERSATION_EVEN_COLOR = GROUP_EVEN_COLOR
CONVERSATION_ODD_COLOR = GROUP_ODD_COLOR
CONVERSATION_GROUP_COLOR = "darkgreen"
