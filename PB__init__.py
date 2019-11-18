# class definition for password bank

from cryptography.fernet import Fernet
import shelve
import os
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import tkinter as tk
from PB_Key import Key
from PB_interfaces import init_Interface
import getpass
# default key loc C:/Users/["Current-User"]/Documents/PassBank//access.key


class init_program:
    """Program initialization, checks for an access.key file by prompting for it's location,
           if it exists, prompts for password 3 times, starts main program if password is verified,
           quits if not."""
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.interface = init_Interface(self.root)

    def getAccessKey(self):
        return self.key
    
    def getDirectories(self):
        """Returns the PassBank folder directory and the keyfile path"""
        return self.PB_Path

    def checkPath(self):
        # check if the directory where shelves are stored exists
        user = getpass.getuser()
        self.PB_Path = "C:\\Users\\" + user + "\\Documents\\PassBank"
        self.default_keyfile_path = self.PB_Path + "\\access.key"

        if not os.path.exists(self.PB_Path):
            os.makedirs(self.PB_Path)
            self.wasPath = False
        else:
            self.wasPath = True

    def isKeyFile(self, keyfile_path):

        # attempts to open the shelve 'access.key' file
        keyFile = shelve.open(keyfile_path)
        keyname = 'accesskey'
        if keyname in keyFile:
            if keyFile[keyname] != "":
                return True
                keyFile.close()
                self.keyfile_path = keyfile_path
            else:
                return False
                keyFile.close()
        else:
            return False
            keyFile.close()


    def verificationLoop(self):
        i = 0
        while i < 3:
            self.interface.verifyAccess()
            self.root.wait_window()
            if self.interface.verified == True:
                self.key = self.interface.getKey()
                self.attempts = i
                break
            else:
                i += 1
                self.interface.incorrect()
        # check if i(attempts) > 3
        if i >= 3:
            self.interface.denied()
            exit()         
        
    def newAccess(self):
        # create keyfile and Key
        self.interface.makeNewAccess()
        self.key = self.interface.getKey()

    def run(self):
        # check if passbank directory exists
        self.checkPath()
        if self.wasPath == True:
            # check for keyfile in its 'default location first'
            if self.isKeyFile(self.default_keyfile_path):
                # set keyfile path
                self.interface.setkeyfilePath(self.default_keyfile_path) # probably can move this down a level later?
                self.verificationLoop()

            else:
                # if keyfile does not exist at its 'default' location
                self.interface.keyPath()
                keyfile_path = self.interface.getKeypath()
                keyfile_path = keyfile_path + "\\access.key"
                if self.isKeyFile(keyfile_path):
                    self.interface.setkeyfilePath(keyfile_path)
                    self.verificationLoop()
                else: # if the user defined keyfile path doesn't exist, make a new access
                    self.newAccess()



        else:
            # create keyfile and Key
            self.newAccess()
        




    
    #def __makePassDict(self):
     #   """Read all shelve keys and data into
      #  a dict."""
       # try:
        #    datfile = shelve.open(self.fname)
         #   passwordDict = dict(datfile)     
        #except:
         #   pass
        
       # return passwordDict







            
