"""
@file Login.py
@date 8/19/2010
@version 0.1
@author Aaron Taggart

@brief This holds the implementation of the function which logs into the server
using the password and username from the client.
"""

import msn

def login(email, password):
    """
    @brief Get the password and username from the client, and 
    """
    
    if email.find('\n') != -1:
        raise ValueError("Email cannot contain newline (\n) characters!")
    
    try:
        server = email.split('@')
        if len(server) != 2:
            raise ValueError("To the exception!!")
        
        server = server[1]
        
    except:
        raise ValueError("Email address needs to be in format: name@place.com")
    
    if server == "hotmail.com" or server == "msn.com" or "live.com":
        connection = msn.Connection(email=email, password=password)
        return connection
    