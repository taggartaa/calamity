"""
@file Network.py
@date 8/17/2010
@version 0.1
@author Aaron Taggart

@brief This file holds the implementation of the classes needed to communicate with various servers and other members.
"""

import socket
import ssl
import hashlib

import calamity 

def getTicket(challange, password, email):
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
            return False
        
    x = rec.find("from-PP='")+9
    y = rec[x:].find("'") + x
    
    return rec[x:y]

def recv(map, sock, waitfor = -1):
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
            
        if waitfor != -1:
            try:
                test = map[waitfor]
                recieved = True
            except:
                pass
        else:
            recieved = True
                
class Connection:
    """
    @brief Connection to the msn server
    """
    
    def __init__(self, email, password):
        """
        @brief Sets up the connection to the MSN Server
        
        @var email: The email address of the person signing in.
        @var password: The password of the person signing in.
        """
        # Number to keep me in sync with MSN server
        self.__sync = 0
        self.__tid = 1
        self.__received = {}
        self.__socket = None
        self.__email = email
        self.__password = password
        self.__data = ""
        self.__connect()
        self.__app = None
        self.__socket.send("SYN %d %d\n"%(self.__tid, self.__sync))
        self.__tid+=1
        self.__socket.send("CHG %d HDN 0\n"%self.__tid)
        self.__tid+=1
        self.__socket.setblocking(False)
        
    def setApp(self, app):
        """
        @brief This is necessary for adding the groups and members to the app.
        @note There has got to be a better way to do this... I don't like it much.
        
        @var app: The app that the members and groups will be added to.
        """
        self.__app = app
        
    def updateStatus(self, status="online"):
        """
        @brief Sets the status
        
        @param status: New status (online, offline, away ,or busy)
        """
        tmp = "NLN"
        if status == "offline":
            tmp = "HDN"
        elif status == "away":
            tmp = "AWY"
        elif status == "busy":
            tmp = "BSY"
            
        self.__socket.send("CHG %d %s 0\n"%(self.__tid, tmp))
        self.__tid += 1
        
    def listen(self):
        """
        @brief Listens for changes from the server.
        """
        
        # TCP doesn't have to give me all the stuff together, so I make sure I have the full command.
        
        updates = []
        try:
            self.__data += self.__socket.recv(4096).replace("\r", "")
            if self.__data[-1] == '\n':
                updates = self.__data.split('\n')
                self.__data = ""
            else:
                updates = self.__data.split('\n')
                self.__data = updates[-1]
                updates.pop()         
        except:
            pass
        
        for update in updates:
            tmp = update.split(' ')
            
            # Lists
            if tmp[0] == "LSG":
                self.__app.add(calamity.Group(tmp[2].replace("%20", " ")))
                
            elif tmp[0] == "LST":
                member = calamity.Member(email=tmp[1], name=tmp[2].replace("%20", " "))
                
                groups = []
                
                if len(tmp) >= 5:
                    groups = tmp[4].split(',')
                    
                if len(groups) == 0:
                    self.__app[0].add(member)
                else:
                    for group in groups:
                        self.__app[int(group)+1].add(member)
                        
            elif tmp[0] == "SYN":
                self.__sync = int(tmp[2])
                
            elif tmp[0] == "CHL":
                payload = hashlib.md5(tmp[2] + "Q1P7W2E4J9R8U3S5").hexdigest()
                message = "QRY %d msmsgs@msnmsgr.com 32\n%s"%(self.__tid,payload)
                self.__socket.send(message)
                self.__tid+=1
                
            # Status updates    
            elif tmp[0] in ["NLN", "ILN"]:
                for group in self.__app:
                    index = group.find(email=tmp[3])
                    if index != -1:
                        if tmp[2] == "NLN":
                            group[index].setStatus("online")
                        elif tmp[2] == "AWY" or tmp[2] == "BRB" or tmp[2] == "IDL":
                            group[index].setStatus("away")
                        elif tmp[2] == "BSY" or tmp[2] == "PHN" or tmp[2] == "LUN":
                            group[index].setStatus("busy")
                        else:
                            print tmp
                        group.sort()
            
            elif tmp[0] == "FLN":
                for group in self.__app:
                    group[group.find(email=tmp[1])].setStatus("offline")
                
            else:
                print update
    

    def __connect(self):
        """
        @brief Connects to the msn server.
        """
        
        # Authentication server.
        authServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        authServer.connect(("messenger.hotmail.com", 1863))
            
        authServer.send("VER %d MSNP8 MSNP9 CVR0\n" %self.__tid)
        self.__tid += 1

        authServer.send("CVR %d 0x0409 win 4.10 i386 MSNMSGR 6.2.0208 MSMSGS %s\n" %(self.__tid, self.__email))
        self.__tid+=1
        
        authServer.send("USR %d TWN I %s\n" %(self.__tid, self.__email))
        self.__tid+=1
        
        recv(self.__received, authServer, self.__tid-1)
    
        # Notification Server
        busy = True
        
        while busy:
            ipInfo = self.__received[3].split(" ")[3].split(":")
        
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.connect((ipInfo[0], int(ipInfo[1])))
            
            self.__socket.send("VER %d MSNP8 CVR0\n" %self.__tid)
            self.__tid += 1
            
            self.__socket.send("CVR %d 0x0409 win 4.10 i386 MSNMSGR 6.2.0208 MSMSGS %s\n" %(self.__tid, self.__email))
            self.__tid+=1
            
            self.__socket.send("USR %d TWN I %s\n" %(self.__tid, self.__email))
            self.__tid+=1
            
            recv(self.__received, self.__socket, self.__tid-1)
            
            if self.__received[self.__tid-1].split(" ")[0] != "XFR":
                busy = False
                
        # msn challenges me!
        challenge = self.__received[self.__tid-1].split(" ")[4]   
        ticket = getTicket(challenge, self.__password, self.__email)
        self.__socket.send("USR %d TWN S %s\n" %(self.__tid, ticket))
        self.__tid+=1
        recv(self.__received, self.__socket, self.__tid-1)
        
        if self.__received[self.__tid-1].split(" ")[0] == "911":
            raise ValueError("Invalid Email or Password!")
        
            
            