# MyPassBank
Desktop app to store passwords securely using sha 256 encryption.

Currently working on the gui and better encapsulation. 
Tkinter right now, but looking into something prettier like Kivy. 

When started PassBank asks for a password which it creates an encryption key from, if there isn't already a password, then the program will take a new one, encrypt the password string with the key it just created and save that encrypted password to a file with shelve. If there is already an access key file, it prompts for the password, attempts to decrypt the saved encrypted password and if they match, the main program is started.  
