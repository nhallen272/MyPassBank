#passbank.py
#a program that stores encrypted passwords and decrypts them

import sys
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import shelve

# specialized modules for this program
from PassBankClasses import init_program
from PB_interfaces import *
from PB_Key import Key
import tkinter as tk


# C:/Users/Admin/Documents/Python Projects

def main():
    # Run initialization program to get a verified access key
    init = init_program()
    init.run()

    key = init.getAccessKey()
    root = tk.Tk()
    PBMain = PB_MainUI(root, key)
    PBMain.mainloop()


if __name__ == "__main__":
    main()