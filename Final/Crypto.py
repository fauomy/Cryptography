import binascii
from tkinter import *
from tkinter import messagebox
import sqlite3
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from tkinter.messagebox import showinfo, showerror

recordsConnection = sqlite3.connect('records.db')


# Designing Main Screen So, first of all, you have to design the main screen.
# two buttons Login and Register.
def main_screen():
    def showSignUpFrame():
        def addUserToDb(name, username, password):
            addUserQuery = "INSERT INTO tbl_user (name,username,password) VALUES (?, ?, ?)"
            user_data = (name, username, password)
            recordsConnection.execute(addUserQuery, user_data)
            recordsConnection.commit()

        def signUpClick():
            if usernameEntry.get() != "" and nameEntry.get() != "" and passwordEntry.get() != "":
                cur = recordsConnection.cursor()
                cur.execute("""SELECT * FROM tbl_user WHERE username=?""", (usernameEntry.get(),))
                row = cur.fetchone()
                if row is None:
                    addUserToDb(nameEntry.get(), usernameEntry.get(), passwordEntry.get())
                    showinfo("Information", "User added Succesfully")
                    nameEntry.delete(0, END)
                    usernameEntry.delete(0, END)
                    passwordEntry.delete(0, END)
                else:
                    showerror("ERROR", 'User already exists.')
                recordsConnection.commit()
            else:
                messagebox.showerror("Error",
                                     "Please Fill the fields appropriately (Password must be 8 characters at least).")

        ##sign up screen
        def closeClick():
            signUpScreen.destroy()
            main_screen()
            mainscreen.mainloop()

        mainscreen.destroy()
        signUpScreen = Tk()  # create a GUI window
        screen_width = signUpScreen.winfo_screenwidth()
        screen_height = signUpScreen.winfo_screenheight()
        window_width = 400
        window_height = 400
        x_coordinate = (screen_width / 2) - (window_width / 2)
        y_coordinate = (screen_height / 2) - (window_height / 2)
        signUpScreen.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))
        signUpScreen.title("SignUp Page")  # set the title of GUI window
        signUpScreen.config(bg='light blue')

        # Use the grid layout manager to position the widgets
        LblName = Label(signUpScreen, text="Name", font=("Helvetica", 16), fg='black', bg='light blue')
        LblName.grid(row=0, column=0, padx=10, pady=10)
        nameEntry = Entry(signUpScreen, bd=5)
        nameEntry.grid(row=0, column=1, padx=10, pady=10)

        LblUsername = Label(signUpScreen, text="UserName: ", font=("Helvetica", 16), fg='black', bg='light blue')
        LblUsername.grid(row=1, column=0, padx=10, pady=10)
        usernameEntry = Entry(signUpScreen, bd=5)
        usernameEntry.grid(row=1, column=1, padx=10, pady=10)

        LblPassword = Label(signUpScreen, text="Password", font=("Helvetica", 16), fg='black', bg='light blue')
        LblPassword.grid(row=2, column=0, padx=10, pady=10)
        passwordEntry = Entry(signUpScreen, bd=5)
        passwordEntry.grid(row=2, column=1, padx=10, pady=10)

        # Use the padx and pady options to add some padding around the buttons
        btnSignUp = Button(signUpScreen, text="SignUp", command=signUpClick, font=("Helvetica", 14), fg='black',
                           bg='green', padx=20, pady=10)
        btnSignUp.grid(row=3, column=0, padx=10, pady=10)
        btnClose = Button(signUpScreen, text="Close", command=closeClick, font=("Helvetica", 14), fg='black', bg='red',
                          padx=20, pady=10)
        btnClose.grid(row=3, column=1, padx=10, pady=10)

        signUpScreen.mainloop()

    def showLoginFrame():
        def openCryptoForm(user_id):
            def addMessageToDb(id, input, encrypted_text):
                addMessageQuery = "INSERT INTO tbl_messages (id,input,encrypted_text) VALUES (?, ?, ?)"
                message_data = (id, input, encrypted_text)
                recordsConnection.execute(addMessageQuery, message_data)
                recordsConnection.commit()

            def encrypt():
                message = input_text.get('1.0', 'end')
                print(message)
                encryptor = PKCS1_OAEP.new(pubKey)
                encrypted = encryptor.encrypt(message.encode())
                print("Encrypted:", binascii.hexlify(encrypted))
                # Insert the encrypted message into the encrypted output text field
                encrypted_output_text.delete('1.0', 'end')
                encrypted_output_text.insert('1.0', (binascii.hexlify(encrypted)))
                addMessageToDb(user_id, message, (binascii.hexlify(encrypted)))
                showinfo("Message", "The input has been encrypted successfully!")

            def decrypt():
                decryptor = PKCS1_OAEP.new(keyPair)
                # Get the encrypted input and PGP private key from the text fields
                encrypted_input = encrypted_input_text.get('1.0', 'end')
                print("encrypt in is", encrypted_input)
                byte_data = bytes.fromhex(encrypted_input)
                print("byte data", byte_data)
                try:
                    decrypted = decryptor.decrypt(byte_data)
                    print('Decrypted:', decrypted)

                    # Insert the decrypted message into the decrypted output text field
                    decrypted_output_text.delete('1.0', 'end')
                    decrypted_output_text.insert('1.0', decrypted)
                except:
                    showerror("Error", 'Invalid Encrypted String.')

            def readme():
                red = Tk()
                screen_width = red.winfo_screenwidth()
                screen_height = red.winfo_screenheight()
                window_width = 500
                window_height = 500
                x_coordinate = (screen_width / 2) - (window_width / 2)
                y_coordinate = (screen_height / 2) - (window_height / 2)
                red.config(bg='light blue')
                red.title("Read me")
                red.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))
                textArea = Text(red, font="lucida 13")
                textArea.pack(expand=True, fill=BOTH)
                textArea.insert(END,"First of all I generated keypair from the RSA key and from the pair I generated "
                                    "public key and private key. \nEncryption:\n\t For Encryption I take the input "
                                    "from the user and encode it, then I generated a key with the help of Public key, "
                                    "and encrypted the input string with the help of generated key and then convert "
                                    "the encrypted string into the readale  hex format with the help of "
                                    "binascii.hexlify.\nDecryption:\n\t I take the encrypted string from the user and "
                                    "convert it into bytes from hex format, Generate the key with the help of private "
                                    "key form at the first step. the decrypte the byte format to original string. One "
                                    "thing keep in mind that if the private key is changed your data can't be "
                                    "decrypted at anny cost make sure it stays same.")

            loginScreen.destroy()
            cryptoScreen = Tk()
            cryptoScreen.config(bg='light blue')
            cryptoScreen.title("Encryption/Decryption Machine")
            screen_width = cryptoScreen.winfo_screenwidth()
            screen_height = cryptoScreen.winfo_screenheight()
            window_width = 1200
            window_height = 800
            x_coordinate = (screen_width / 2) - (window_width / 2)
            y_coordinate = (screen_height / 2) - (window_height / 2)
            cryptoScreen.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

            # Create the label and text widget for the PGP private key
            pgp_private_key_label = Label(cryptoScreen, text="PGP Private Key", font=("Helvetica", 14))
            pgp_private_key_label.grid(row=0, column=0, padx=10, pady=10)
            pgp_private_key_text = Text(cryptoScreen, height=20, width=50, bd=5, bg='white', font=("Helvetica", 14),
                                        fg='black', padx=10, pady=10)
            pgp_private_key_text.grid(row=0, column=1, padx=10, pady=10)

            # Create the label and text widget for the input
            input_label = Label(cryptoScreen, text="Input")
            input_text = Text(cryptoScreen, height=1, width=100, bg='white', font=("Helvetica", 14), fg='black',
                              padx=10, pady=10)
            input_label.grid(row=1, column=0, padx=10, pady=10)
            input_text.grid(row=1, column=1, padx=10, pady=10)

            # Create the label and text widget for the encrypted output
            encrypted_output_label = Label(cryptoScreen, text="Encrypted Output")
            encrypted_output_text = Text(cryptoScreen, height=1, width=100, bd=5)
            encrypted_output_label.grid(row=2, column=0, padx=10, pady=10)
            encrypted_output_text.grid(row=2, column=1, padx=10, pady=10)

            # Create the label and text widget for the encrypted input
            encrypted_input_label = Label(cryptoScreen, text="Encrypted Input")
            encrypted_input_text = Text(cryptoScreen, height=1, width=100, bd=5)
            encrypted_input_label.grid(row=3, column=0, padx=10, pady=10)
            encrypted_input_text.grid(row=3, column=1, padx=10, pady=10)

            # Create the label and text widget for the decrypted output
            decrypted_output_label = Label(cryptoScreen, text="Decrypted Output")
            decrypted_output_text = Text(cryptoScreen, height=1, width=100, bd=5)
            decrypted_output_label.grid(row=4, column=0, padx=10, pady=10)
            decrypted_output_text.grid(row=4, column=1, padx=10, pady=10)

            # Create the encrypt and decrypt buttons
            encrypt_button = Button(cryptoScreen, text="Encrypt", command=encrypt)
            decrypt_button = Button(cryptoScreen, text="Decrypt", command=decrypt)
            encrypt_button.grid(row=5, column=1, columnspan=2, padx=10, pady=10)
            decrypt_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
            Button(cryptoScreen,text='About Machine',command=readme,font='Bahnschrift 11 bold').place(x=20, y=10)
            keyPair = RSA.generate(3072)

            pubKey = keyPair.publickey()
            pubKeyPEM = pubKey.exportKey()
            privKeyPEM = keyPair.exportKey()
            # # Insert the private key into the appropriate text box
            pgp_private_key_text.insert('1.0', privKeyPEM.decode('ascii'))
            cryptoScreen.mainloop()

        def validateUser(name, password):
            cur = recordsConnection.cursor()
            cur.execute("""SELECT * FROM tbl_user WHERE username=? and password=?""", (name, password,))
            row = cur.fetchone()
            if row is None:
                showerror("Error", 'Invalid username or password.')
            else:
                user_id = row[0]
                usernameEntry.delete(0, END)
                passwordEntry.delete(0, END)
                showinfo("Message", "Logged in successfully")
                openCryptoForm(user_id)
            recordsConnection.commit()

        def loginClick():
            if usernameEntry.get() != "" and passwordEntry.get() != "":
                validateUser(usernameEntry.get(), passwordEntry.get())

            else:
                showerror("Error", "Please Fill the fields appropriately (Password must be 8 characters at least).")

        ### login screen
        def closeClick():
            loginScreen.destroy()
            main_screen()
            mainscreen.mainloop()

        mainscreen.destroy()
        loginScreen = Tk()  # create a GUI window
        screen_width = loginScreen.winfo_screenwidth()
        screen_height = loginScreen.winfo_screenheight()
        window_width = 400
        window_height = 400
        x_coordinate = (screen_width / 2) - (window_width / 2)
        y_coordinate = (screen_height / 2) - (window_height / 2)
        loginScreen.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))
        loginScreen.title("Login Page")  # set the title of GUI window
        loginScreen.config(bg='light blue')
        LblUsername = Label(loginScreen, text="UserName: ", font=("Helvetica", 16), fg='black', bg='light blue')
        LblUsername.grid(row=0, column=0, padx=10, pady=10)
        usernameEntry = Entry(loginScreen, bd=5)
        usernameEntry.grid(row=0, column=1, padx=10, pady=10)
        LblPassword = Label(loginScreen, text="Password", font=("Helvetica", 16), fg='black', bg='light blue')
        LblPassword.grid(row=1, column=0, padx=10, pady=10)
        passwordEntry = Entry(loginScreen, bd=5)
        passwordEntry.grid(row=1, column=1, padx=10, pady=10)
        btnLogin = Button(loginScreen, text="Login", command=loginClick, font=("Helvetica", 14), fg='black', bg='green',
                          padx=20, pady=10)
        btnLogin.grid(row=2, column=1, padx=10, pady=10)
        btnClose = Button(loginScreen, text="Close", command=closeClick, font=("Helvetica", 14), fg='black', bg='red',
                          padx=20, pady=10)
        btnClose.grid(row=2, column=0, padx=10, pady=10)

        loginScreen.mainloop()

    ###the main page pop up window

    mainscreen = Tk()  # create a GUI window
    screen_width = mainscreen.winfo_screenwidth()
    screen_height = mainscreen.winfo_screenheight()
    window_width = 400
    window_height = 400
    x_coordinate = (screen_width / 2) - (window_width / 2)
    y_coordinate = (screen_height / 2) - (window_height / 2)
    mainscreen.geometry("%dx%d+%d+%d" % (
        window_width, window_height, x_coordinate, y_coordinate))  # set the configuration of GUI window
    mainscreen.title("Welcome")  # set the title of GUI window
    mainscreen.config(bg='light blue')  # Change the background color to light blue
    Button(mainscreen, text="Login", height="2", width="30", command=showLoginFrame, font=("Helvetica", 14), fg='black',
           bg='light green', padx=20, pady=10).pack(padx=10, pady=10)
    Button(mainscreen, text="Register", height="2", width="30", command=showSignUpFrame, font=("Helvetica", 14),
           fg='black', bg='red', padx=20, pady=10).pack(padx=10, pady=10)
    mainscreen.mainloop()  # start the GUI


main_screen()  # call the main_account_screen() function

