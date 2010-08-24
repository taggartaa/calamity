"""
@file Login.py
@date 8/19/2010
@version 0.1
@author Aaron Taggart

@brief This holds the implementation of the function which logs into the server
using the password and username from the client.
"""

from Network import msnConnect

def login():
    """
    @brief Get the password and username from the client, and 
    """
    email = raw_input("email: ")
    password = raw_input("password: ")
    sock = msnConnect(email, password)
    return sock