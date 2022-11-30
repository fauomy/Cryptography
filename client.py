import os
import socket

# initializing the main network aspects to connect client and server
IP = socket.gethostbyname(socket.gethostname())
port = 8080
size = 1024
Format = "utf-8"
clientData = "ClientData"

def main():
    print("Initializing Server. \n")

    # identify the use of IPv4 and TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(IP, port)

    #the path of the client data
    pathOfTransfer = os.pathOfTransfer.join(clientData, "files")
    folder = pathOfTransfer.split("/")[-1]

    # sending the folder name to server
    message = f"{folder}"
    print(f" Sending folder name to server: {folder}")
    client.send(message.encode(Format))

    # notifying the user that data has been achnowledged from the server
    message = client.recv(size).decode(Format)
    print(f"{message} \n")

    # sending files to the server
    components = sorted(os.listdir(pathOfTransfer))

    for fileName in components:

        #send the file names to the server
        message = f"File name: {fileName}"
        print(f" Transferring file name to server: {fileName}")
        client.send(message.encode(Format))

        # recieving reply from server
        message = client.recv(size).decode(Format)
        print(f"{message}")

        #sending the data to the server
        transfer = open(os.path.join(pathOfTransfer, fileName), "r")
        fileComponents = transfer.read()

        message = f"{fileComponents}"
        client.send(message.encode(Format))
        message = client.recv(size).decode(Format)
        print(f"{message}")

        #closing function
        message = f"Data sent successfully."
        client.send(message.encode(Format))
        message = client.recv(size).decode(Format)
        print(f" {message}")

    # Ending connection to server
    message = f"File transfer complete"
    client.send(message.encode(Format))
    client.close()

if __name__ == "__main__":
    main()
