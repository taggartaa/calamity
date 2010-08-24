"""
@file Network.py
@date 8/17/2010
@version 0.1
@author Aaron Taggart

@brief This file holds the implementation of the classes needed to communicate with various servers and other members.
"""

import socket
import ssl

def getMsnTicket(challange, password, email):
    """
    @brief returns the 32-digit hex value needed to login to the MSN Server.
    
    @var challange: Challange string sent by the MSN Server
    @var password: The login password of the user.
    @var email: The email address of the user.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    nexus = ssl.wrap_socket(s)
    nexus.connect(("nexus.passport.com", 443))
    
    nexus.send("GET /rdr/pprdr.asp HTTP/1.0\n\n")
    redirect = nexus.recv(4096)
    
    x = redirect.find("DALogin=")+8
    y = redirect[x:].find(",") + x
    DALogin = redirect[x:y].split("/")
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    DAlogin = ssl.wrap_socket(s)
    DAlogin.connect((DALogin[0], 443))
    
    #email = email.replace("@", "%40")
    DAlogin.send("GET /" + DALogin[1] + " HTTP/1.1\nAuthorization: Passport1.4 OrgVerb=GET,OrgURL=http%3A%2F%2Fmessenger%2Emsn%2Ecom,sign-in="+email+",pwd="+password+","+challange+"\nHOST: "+DALogin[0]+"\n\n")
    
    received = False
    rec = ""
    while not received:
        rec = DAlogin.recv(4096)
        if rec.split("\r\n")[0] == "HTTP/1.1 200 OK":
            received = True
        else:
            print "FAIL: ",rec
            return False
        
    x = rec.find("from-PP='")+9
    y = rec[x:].find("'") + x
    
    print rec
    return rec[x:y]

def msnRecv(map, sock, waitfor = -1):
    """
    @brief Receives from the socket and maps the responses by TID in the map.
    
    @var map: Where the responses are stored.
    @var sock: Where the responses are read from.
    @var waitfor: Wait for a specific TID message before continuing
    """
    recieved = False
    while not recieved:
        for line in sock.recv(4096).split("\n"):
            if line != "":
                map[int(line.split(" ")[1])]= line
                print "recv: " + line
            
        if waitfor != -1:
            try:
                test = map[waitfor]
                print "Got it: ", test
                recieved = True
            except:
                pass
        else:
            recieved = True
                
            

def msnConnect(email, password):
    """
    @brief Connects to the msn server.
    
    @var email: The amial address of the user (msn login id),
    @var passord: The password of the user.
    
    @return socket connected to msn.
    """
    
    # Maps TID to responses
    responses = {}
    TID = 1
        
    # Authentication server.
    authServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    authServer.connect(("messenger.hotmail.com", 1863))
            
    authServer.send("VER %d MSNP8 CVR0\n" %TID)
    TID += 1
        
    #msnRecv(responses, authServer, TID-1)

    authServer.send("CVR %d 0x0409 win 4.10 i386 MSNMSGR 6.2.0208 MSMSGS %s\n" %(TID, email))
    TID+=1
        
    #msnRecv(responses, authServer)
        
    authServer.send("USR %d TWN I ajtaggs@hotmail.com\n" %TID)
    TID+=1
        
    msnRecv(responses, authServer, TID-1)
    
    # Notification Server
    busy = True
    notServer = None
    
    while busy:
        ipInfo = responses[3].split(" ")[3].split(":")
    
        notServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        notServer.connect((ipInfo[0], int(ipInfo[1])))
        
        notServer.send("VER %d MSNP8 CVR0\n" %TID)
        TID += 1
        
        #msnRecv(responses, notServer)
        
        notServer.send("CVR %d 0x0409 win 4.10 i386 MSNMSGR 6.2.0208 MSMSGS %s\n" %(TID, email))
        TID+=1
        
        #msnRecv(responses, notServer)
        
        notServer.send("USR %d TWN I %s\n" %(TID, email))
        TID+=1
        
        msnRecv(responses, notServer, TID-1)
        
        if responses[TID-1].split(" ")[0] != "XFR":
            busy = False
            
    # msn challenges me!
    challenge = responses[TID-1].split(" ")[4]   
    ticket = getMsnTicket(challenge, password, email)
    print "ticket: ", ticket
    notServer.send("USR %d TWN S %s\n" %(TID, ticket))
    TID+=1
    msnRecv(responses, notServer, TID-1)
    
    return notServer
    
    # Connect to and return the dispatch server!
        
        