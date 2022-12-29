# Cryptography

First the user needs to add both the executable and the db file in one folder. Followed by that, the user runs the program where they are displayed with the main page that includes signup, and login. When the user chooses to sign up, they are required to fill in the username, name , and a password with minimum length 8 characters. No 2 users can have the same username.

When the user chooses to login, they are required to enter the registered credentials, if the credentials don’t exist, the user is displayed with an error message. Then the machine starts.

The user is displayed with their private key, and they input text, which we then press the encrypt button to do it. Then we copy the encrypted output, paste it into the encrypted input, then press decrypt to display it to the user in the end like the original message. 


First of all I generated keypair from the RSA key and from the pair I generated public and private keys are created. Encryption: For Encryption I take the input from the user and encode it, then I generated a key with the help of Public key, and encrypted the input string with the help of generated key and then convert the encrypted string into the readable  hex format with the help of binascii.hexlify. Decryption: I take the encrypted string from the user and convert it into bytes from hex format, Generate the key with the help of private key form at the first step. then decrypt the byte format to original string. Onethin g to keep in mind, is that if the private key is changed your data can't be decrypted at anny cost make sure it stays same.
