# class definitition for password bank key
from cryptography.fernet import Fernet
import shelve
import os
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import tkinter.messagebox

class Key:

    def __init__(self, access_password):
        """Creates a Fernet encryption key, 
           given an access password."""
        
        self.strpass = access_password
        bytes_password = access_password.encode() # converts to type bytes 
        salt = b'\xcaO\xf8\xf8\xab\xd6\xb0\x0b@\xf5\xd5\xaf|\xca\x1b\xc1'
        kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
        )
        # key is generated
        self.key = base64.urlsafe_b64encode(kdf.derive(bytes_password))
        self.keyfile_Name = 'access.key'
        
            
        


    def createKeyFile(self, path):
        """Saves the key in a file called access.key"""
        f = Fernet(self.key)
        password = self.strpass # may need to make new line to do this
        password = password.encode()
        encryptedPass = f.encrypt(password)
        path += "/access.key"
        with shelve.open(path) as keyfile:
            keyfile['accesskey'] = encryptedPass
        keyfile.close()


    def isKeyFile(self):
        keyfile_path = input("Enter directory of access.key file: ")
        keyfile_path = keyfile_path + "/access.key"
        
        return os.path.isfile(keyfile_path)


    def verified(self):
        """Returns true or false depending on if the string access password given in
        constructor corresponds to the password key stored in access.key file"""
        
        key = self.key
        f = Fernet(key) # set the key in Fernet
        # open key file
        truepass = self.__getAccesskeyfromShelf()
        if truepass == self.strpass:
            return True
            
        else:
            return False
    
    def updatePath(self, keyfile_path):
        self.keyfile_path = keyfile_path
    
    def getKey(self):
        """Returns the type bytes encryption key."""
        return self.key
    
    def getAccessPass(self):
        """Returns original access password string."""
        return self.strpass

    def __getAccesskeyfromShelf(self):
        path = self.keyfile_path
        path = path[0:-11] # change directory to the main folder (minus '\\passbank.key')
        os.chdir(path)
        keyfile = shelve.open('access.key')
        truepass = keyfile['accesskey']
        keyfile.close()
        key = self.key
        f = Fernet(key)
        truepass = f.decrypt(truepass)
        truepass = str(truepass)
        truepass = truepass[2:-1]
        return truepass
