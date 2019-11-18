# Interfaces for use with the PassBank program
import tkinter as tk
from PB_Key import Key
import tkinter.simpledialog
import tkinter.ttk
from itertools import cycle
import shelve
from MultiListBox2 import *
from cryptography.fernet import Fernet
# keyfile directory C:/Users/Admin/Documents/Python Projects


class init_Interface:

    def __init__(self, master):
        self.master = master
        self.master.title("Verify Access")
        self.master.geometry('240x80')
        # Check for access.key file
        
    def verifyAccess(self):
        self.button = tk.Button(self.master, text="Done", command=self.__verifyAccess)
        self.button.grid(row = 2, column = 1, padx=2, pady=2 )
        self.label = tk.Label(self.master, text = "Enter Password:" )
        self.label.grid(row = 1, column = 0, padx=2, pady=2)
        self.entry = tk.Entry(self.master, show="*")
        self.entry.grid(row = 1, column = 1, padx=2, pady=2)
    
    def setkeyfilePath(self, path):
        self.keyfilePath = path

    

    def __verifyAccess(self):
        """Internal method, when button is pressed, the  string in self.entry is saved in 
           variable, then a Key object is made with it and Key.verified
           is called. The bool value is stored in self.verified"""
        trypass = self.entry.get()
        KFPath = self.keyfilePath
        trykey = Key(trypass) # add key file path as second arg
        trykey.updatePath(KFPath)
        if trykey.verified():
            self.truepass = trypass
            self.key = trykey
            self.verified = True
            self.master.destroy()
        else:
            self.verified = False

    
    def denied(self):
        """Opens a popup msg box if out of attempts at gaining access."""
        popup = tk.messagebox.showerror("Access Denied!", "Wrong Password")

    def incorrect(self):
        """Opens a popup when a password attempt is incorrect."""
        popup = tk.messagebox.showwarning("Incorrect Password", "Password entered is incorroect, try again.")


    def makeNewAccess(self):
        """Internal method. Creates pop-up window with entry to create 
           a new access password, for like the first time using the program."""
        self.master.withdraw()
        while True:
            newpass = tkinter.simpledialog.askstring("Create New Access Key", "Enter new access key password:", show="*")
            np2 = tkinter.simpledialog.askstring("New Access Key", "Enter new access key again to verify:", show="*")
            if newpass == np2:
                self.truepass = newpass
                self.key = Key(self.truepass)
                self.key.createKeyFile(self.keyfilePath)
                self.master.destroy()
                break
            else:
                np2 = tk.messagebox.showwarning("New Access Key", "Passwords did not match!")
                continue
        
    
    def keyPath(self):
        """Creates pop-up window with entry to enter 
           keyfile path."""
        self.master.withdraw()
        keyfilepath = tkinter.simpledialog.askstring("Keyfile path", "Enter access.key folder path: ")
        self.master.deiconify()
        self.keyfilePath = keyfilepath

    

    def getKeypath(self):
        return self.keyfilePath
    
        
    def getKey(self):
        return self.key




class ToolBar:
    """Toolbar with 3 buttons that perform
       functions defined in constructor"""
    def __init__(self, master, AddBtnCommand, EditBtnCommand, DelBtnCommand):
        self.toolbar = tk.Frame(master, height='40')
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        # define photo icons
        add_ico = tkinter.PhotoImage(file = "C:/Users/Admin/Documents/Python Projects/Cryptography/PassBank/new.png")
        edit_ico = tkinter.PhotoImage(file = "C:/Users/Admin/Documents/Python Projects/Cryptography/PassBank/edit.png")
        del_ico = tkinter.PhotoImage(file = "C:/Users/Admin/Documents/Python Projects/Cryptography/PassBank/delete.png")

        # make buttons,
        self.add_Button = tk.Button(self.toolbar, image=add_ico, command=AddBtnCommand ) # need to fix the commands
        self.add_Button.pack(side=tk.LEFT, padx=2, pady=2)
        self.addImage = add_ico
        self.edit_Button = tk.Button(self.toolbar, image=edit_ico, command=EditBtnCommand )
        self.edit_Button.pack(side=tk.LEFT, padx=2, pady=2)
        self.editImage = edit_ico
        self.del_Button = tk.Button(self.toolbar, image=del_ico, command=DelBtnCommand )
        self.del_Button.pack(side=tk.LEFT, padx=2, pady=2)
        self.DelImage = del_ico
    
    def getPassData(self):
        passname = tkinter.simpledialog.askstring("Add Password", "Enter a Password Name:")
        username = tkinter.simpledialog.askstring("Add Password", "Enter Username")
        password = tkinter.simpledialog.askstring("Add Password", "Enter password")
        password2 = tkinter.simpledialog.askstring("Add Password", "Re-enter password to verify")
        if password == password2:
            return passname, username, password
        else:
            password = tkinter.simpledialog.askstring("Add Password", "Re-enter password")
            return passname, username, password



class PB_MainUI(tk.Frame):
    """User interface for main PassBank program."""
    def __init__(self, root, Key_object, directory):
        root.title("PassBank Pasword Manager")
        tk.Frame.__init__(self, root, height=500, width=600)
        self.root = root
        self.directory = directory
        self.passbank_db = self.directory + "\\passbankDB"
        # add encryption functions, save verified Key object in crypter
        self.crypter = Crypter(Key_object)
        
        # create dictionary from the passbank database
        self.PB_Dict = self.__makePassbankDict()

        # initialize the toolbar
        self.toolbar = ToolBar(root, self.AddPassword, self.EditPassword, self.DelPassword)
        
        # init the listbox that contains passname, username, password...
        self.MainListBox(root)

    
    def getPassData(self, addORedit):
        if addORedit == "ADD":
            passname = tkinter.simpledialog.askstring("Add Password", "Enter a Password Name:")
            username = tkinter.simpledialog.askstring("Add Password", "Enter Username")
            while True:
                password = tkinter.simpledialog.askstring("Add Password", "Enter password")
                password2 = tkinter.simpledialog.askstring("Add Password", "Re-enter password to verify")
                if password == password2:
                    return passname, username, password
                    break
                else:
                    continue

        elif addORedit == "EDIT":
            username = tkinter.simpledialog.askstring("Edit Password", "Enter Username") 
            while True:
                password = tkinter.simpledialog.askstring("Edit Password", "Enter Password")
                password2 = tkinter.simpledialog.askstring("Add Password", "Re-enter password to verify")
                if password == password2:
                    return username, password
                    break
                else:
                    continue
        #if addORedit == "ADD":
           # top = tk.Toplevel(self.root, master, )


    def AddPassword(self):
        """Add a password to the database."""
        while True:
            passname, username, password = self.getPassData("ADD")
            if type(passname) != str or type(username) != str or type(password) != str:
                tk.messagebox.showwarning("Error", "Passwords cannot start with b'")
                break
            else:
                # encrypt username and password
                username = self.crypter.encrypt(username)
                password = self.crypter.encrypt(password)
                # add {passname:[username, password]} to passbank database
                passbankDB = shelve.open(self.passbank_db)
                passbankDB[passname] = [username, password]
                passbankDB.close()
                #  update the mainlistbox
                self.populateLB()
                break


    def EditPassword(self):
        """Edit the selected password."""
        while True:
            if self.selected is None:
                tk.messagebox.showerror("Error", "Nothing Selected!")
                break

            else:
                newUsername, newPassword = self.getPassData("EDIT")
                if type(newUsername) != str or type(newPassword) != str: # make sure given character don't come up as type bytes
                    tk.messagebox.showwarning("Error", "Passwords cannot start with b'")
                    break
                else:
                    passdata = self.selected
                    passname = passdata[0]
                    newUsername = self.crypter.encrypt(newUsername)
                    newPassword = self.crypter.encrypt(newPassword)
                    # change data at shelve key [username]
                    passBank = shelve.open(self.passbank_db)
                    # update values at that password name (key)
                    passBank[passname] = [newUsername, newPassword]
                    passBank.close()
                    self.populateLB()
        
            



    def DelPassword(self):
        """Delete a selected password by
           confirming with a popup."""
        if self.selected is None:
            tk.messagebox.showwarning("Warning", "No row selected!") # show an error popup
        else:
            if tk.messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete?"):
                passdata = self.selected
                passname = passdata[0]
                passBank = shelve.open(self.passbank_db)
                del passBank[passname]
                passBank.close()
                # lastly update multilistbox
                self.populateLB() 
            else:
                pass


    def MainListBox(self, root): # root or frame?
        self.multiList = Multicolumn_Listbox(root, ["Password Name/URL", "Username", "Password"], stripped_rows = ("white","#f2f2f2"), command=self.getLBValue, cell_anchor='center' )
        self.multiList.interior.pack(fill=tk.BOTH) # pack in the widget,able to fill in extra space BOTH horizontally and vertically when root is resized
        if self.isData == True:
            self.populateLB()
        else:
            pass
    
    def getLBValue(self, data):
        """Command Called when a row is selected."""
        self.selected = data

    def populateLB(self):
        PB_Dict = self.__makePassbankDict()
        AllpassNames = PB_Dict.keys()
        self.multiList.clear()
        for passname in AllpassNames:
            # make a blank list that will hold passname, username, password that represents data for a single password
            passdata = []
            # add passname(dict key) first
            passdata.append(passname)
            # get username and password saved at that key in the dict
            user_pass = PB_Dict[passname]
            # decrypt username
            username = self.crypter.decrypt(user_pass[0])
            # add username to passdata list
            passdata.append(username)
            password = self.crypter.decrypt(user_pass[1])
            # add decrypted password
            passdata.append(password)
            # now add this 3-item list to the multi-listbox
            self.multiList.insert_row(passdata)



    def __makePassbankDict(self):
        passbank_DB = shelve.open(self.passbank_db)
        passbankdict = dict(passbank_DB)
        passbank_DB.close()
        if len(passbankdict) == 0:
            self.isData = False
        else:
            self.isData = True
        return passbankdict
    

        
class Crypter:

    def __init__(self, keyObject):
        bytes_key = keyObject.getKey() #
        self.f = Fernet(bytes_key)
    
    def encrypt(self, string):
        byteStr = string.encode()
        byteStr = self.f.encrypt(byteStr)
        return byteStr
    
    def decrypt(self, encryptedbytes_Str):
        decrypted = self.f.decrypt(encryptedbytes_Str)
        decrypted = str(decrypted)
        decrypted = decrypted[2:-1]
        return decrypted

