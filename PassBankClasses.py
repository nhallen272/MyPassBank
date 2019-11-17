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
    
    def isKeyFile(self):
        # get keyfile path from a toplevel on init interface
        self.interface.keyPath()
        try:
            keyfile_path = self.interface.getKeypath()
            keyfile_path = keyfile_path + "/access.key"
            
        # attempts to open the shelve 'access.key' file
        # if the file exists, return true
        except TypeError:
            print("No key given!")
            self.interface.keyPath()
        
        keyFile = shelve.open(keyfile_path)
        keyname = 'accesskey'
        if keyname in keyFile:
            if keyFile[keyname] != "":
                return True
                keyFile.close()
            else:
                return False
                keyFile.close()
        else:
            return False
            keyFile.close()

        #OLD if os.path.isfile(keyfile_path) == True:
            #return True
        #else:
            #return False
        
    def run(self):
        # check if keyfile exists
        if self.isKeyFile():
            i = 0
            while i < 3:
                self.interface.verifyAccess()
                self.root.wait_window()
                if self.interface.verified == True:
                    # set access pass to variable
                    self.key = self.interface.getKey()
                    # exit out of loop
                    break
                    
                else:
                    i += 1
                    self.interface.incorrect() # display a msg box saying  wrong password
                
            if i >= 3:
                # out of attempts, display error and exit program.
                self.interface.denied()
                exit()
                    
        else:
            # create keyfile and Key
            self.interface.makeNewAccess()
            self.key = self.interface.getKey()
        




    
    #def __makePassDict(self):
     #   """Read all shelve keys and data into
      #  a dict."""
       # try:
        #    datfile = shelve.open(self.fname)
         #   passwordDict = dict(datfile)     
        #except:
         #   pass
        
       # return passwordDict







            
