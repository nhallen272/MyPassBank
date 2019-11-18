#passbank.py
# a program that stores encrypted passwords and decrypts them

import shelve
import tkinter as tk

# specialized modules for this program
from PB__init__ import init_program
from PB_interfaces import *
from PB_Key import Key



# C:/Users/Admin/Documents/Python Projects

def main():
    # Run initialization program to get a verified access key.
    init = init_program()
    init.run()

    # get key object and program path from init program.
    PBPath = init.getDirectories()
    key = init.getAccessKey()
    root = tk.Tk()

    PBMain = PB_MainUI(root, key, PBPath)
    PBMain.mainloop()


if __name__ == "__main__":
    main()