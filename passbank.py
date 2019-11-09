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
from PassBankClasses import *
from PB_interfaces import *
from PB_Key import Key



def initialize():
    init_TkRoot = tk.Tk()
    initInterface = init_Interface(init_TkRoot)
    init = init_program(initInterface)
    init.run()
    return init.getAccessKey()



def main():
    # Run initialization program to get string for access key
    access_key = initialize()
    # Run main passback program
    main_TkRoot = tk.Tk()
    PB_main = PassBank(init.getAccessKey(), MainUI(main_TkRoot))
    PB_main.run()


if __name__ == "__main__":
    main()