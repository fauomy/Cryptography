import os
import socket

# initializing the main network aspects to connect client and server
IP = socket.gethostbyname(socket.gethostname())
port = 8080
size = 1024
Format = "utf-8"
serverData = "ServerData"


def main():
    print("Initializing Server. \n")

    # identify the use of IPv4 and TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(IP, port)
    server.listen()
    print("Server is waiting for client data transfer. \n")

    while True:
        # server accepts connection from client
        conn, address = server.accept()
        print(f" {address} connected successfully. \n")

        # recieving folder data from client
        folderToRecieve = conn.recv(size).decode(Format)

        # creating the folder on the server from client
        folderPath = os.path.join(serverData, folderToRecieve)
        # if the file exists it says that it already does and if it doesnt the makedirs function creates it
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
            conn.send(f"({folderToRecieve}) has been created.".encode(Format))
        else:
            conn.send(f"({folderToRecieve}) exists.".encode(Format))

        # recieving the files components from the client
        while True:
            message = conn.recv(size).decode(Format)
            cmd, data = message.split(":")

            if cmd == "name of the file":
                # Recieve the file name from client
                print(f"Filename has been recieved: {data}.")

                filePath = os.path.join(folderPath, data)
                file = open(filePath, "w")
                conn.send("Filename acquired.".encode(Format))

            elif cmd == "Data of the file":

                # Recieve the file name from client
                print(f"Receiving the file data.")
                file.write(data)
                conn.send("File data has been recieved successfully.".encode(Format))

            elif cmd == "End Transfer":
                file.close()
                print(f"{data}. \n")
                conn.send("Data has been appended to location".encode(Format))

            elif cmd == "End connection to client":
                conn.close()
                print(f"{data}")
                break

if __name__ == "__main__":
    main()
