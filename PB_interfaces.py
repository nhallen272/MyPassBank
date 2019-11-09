# Interfaces for use with the PassBank program
import tkinter as tk
from PB_Key import Key


class init_Interface(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.button = tk.Button(self, text="Done", command=self.__verifyAccess)
        self.button.grid(row = 2, column = 1)
        self.label = tk.Label(self, text = "Enter Password:" )
        self.label.grid(row = 1, column = 0, pady = 2)
        self.entry = tk.Entry(self)
        self.entry.grid(row = 1, column = 1, pady = 2)
        



    def __verifyAccess(self):
        """Internal method, when button is pressed, the password string entered
           is saved in variable,  then a Key object is made with it and Key.verified
           is called. The bool value is stored in self.verified"""
        trypass = self.entry.get()
        trykey = Key(trypass)
        if trykey.verified():
            self.truepass = trypass
            self.verified = True

        else:
            self.verified = False

    def __createNewAccessKey(self):
        """Internal method. Creates pop-up window with entry to create 
           a new access password, for like the first time using the program."""
        self.top = tk.Toplevel(self.master)
        self.top.title("Create New Access Key")
        self.tL = tk.Label(self.top, text = "Enter a Password:")
        self.tL.grid(row = 1, column = 0)
        self.tE = tk.Entry(self.top)
        self.tE.grid(row = 1, column = 1)
        self.tB = tk.Button(self.top, text="Create Key", command=self.__newAccessKey)
        self.tB.grid(row = 2, column = 1)
        
    
    def __newAccessKey(self):
        self.truepass = self.tE.get()

        
    def getAccess(self):
        return self.truepass