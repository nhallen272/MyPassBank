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
from PB_interfaces import *



class init_program:
    """Program initialization, checks for an access.key file by prompting for it's location,
           if it exists, prompts for password 3 times, starts main program if password is verified,
           quits if not."""
    def __init__(self, init_interface):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.interface = init_Interface(self.root)
    
    def getAccessKey(self):
        return self.access_pass
    
    def isKeyFile(self):
        keyfile_path = input("Enter directory of access.key file: ")
        keyfile_path = keyfile_path + "/access.key"
        
        return os.path.isfile(keyfile_path)
        
    def run(self):
        if self.isKeyFile():
            self.interface.mainloop()
            i = 0
            while i < 3:
                # run verification
                if self.interface.verified == True:
                    # continue to main program, transfer correct access password to main program
                    self.access_pass = self.interface.getAccess()
                    
                else:
                    i += 1
        else:
            self.interface.top.mainloop()
            self.access_pass = self.interface.getAccess()
            # make new keyfile
            mykey = Key(self.access_pass)
            mykey.createKeyFile()
            
            


class MainUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)



class PassBank:

    def __init__(self, access_password, interface):
        self.fname = 'passbank.db'
        # key is generated
        self.key = Key(access_password)
        self.passDict = self.__makePassDict()
        self.interface = interface # need to implement this. An interface between the main program's logic and a gui also, can easily make different versions of this interface.
        # anytime new information must be shown to the user, a suitable method from interface will be invoked

    def getAccessKeyfromUI(self):
        access_key = self.interface.getUserInputAccessKey()
        self.key = Key(access_key)   
    
    def run(self):
        """Runs the main program"""

        # get program function
        
                

    def __encrypt(self, password):
        """Internal encryption function using Fernet"""
        f = Fernet(self.key)
        password = password.encode()
        password = f.encrypt(password)
        return password


    def __decrypt(self, password):
        f = Fernet(self.key)
        password = f.decrypt(password)
        password = str(password)
        password = password[2:-1]
        return password


    def add(self, passname, password):
        """Add an encryopted password to the shelve database file"""
        encryptedpassword = self.__encrypt(password)
        datfile = shelve.open(self.fname)
        datfile[passname] = encryptedpassword
        datfile.close()


    def update(self, pass_to_update, new_password):
        """Update an existing password, given its name and a new password string"""
        encryptedpassword = self.__encrypt(new_password)
        datfile = shelve.open('passbank.db')
        flag = pass_to_update in datfile
        if flag:
            datfile[pass_to_update] = encryptedpassword
            datfile.close()

        else:
            print("Name not found in password database.")
            todo = input("Use anyway and add new password to database?(y/n): ")
            if todo == 'y' or todo == 'Y':
                datfile[pass_to_update] = encryptedpassword
                datfile.close()

            else:
                pass


    def delete(self, passname):
        """Deletes a shelve key and its data. """
        sure = input("Are you sure you want to delete {0} password(y/n)? ")
        if sure == 'Y' or sure == 'y':
            datfile = shelve.open('passbank.db')
            del datfile[passname]
            datfile.close()


    def showpass(self, name):
        """Show a specific password in the database"""
        try:
            if name in self.passDict:
                password = self.passDict[name]
                password = self.__decrypt(password)
                self.interface.ShowEntry(name, password) # need to implement this!
            else: 
                self.interface.ShowMsg("Password name not found in database!") # need to implement this!
        except:
            self.interface.ShowMsg()

    def getHelp(self):
        self.interface.ShowHelp()





    def showall(self):
        """Show all password in the password database"""
        try:
            datfile = shelve.open(self.fname)
            pList = datfile.keys()
            for name in pList:
                showpass = datfile[name]
                showpass = self.__decrypt(showpass)
                print("Name:", name)
                print("Password:", showpass)
        except:
            pass
    
    
    def __makePassDict(self):
        """Read all shelve keys and data into
        a dict."""
        try:
            datfile = shelve.open(self.fname)
            passwordDict = dict(datfile)     
        except:
            pass
        
        return passwordDict







            
