from socket import *
import datetime
import os

BUFFER_SIZE = 1024 * 4 #4KB

serverPort = 13000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print("The server is ready to receive")

while True:
    connectionSocket, addr = serverSocket.accept()

    request = connectionSocket.recv(1024).decode() 


    fileName = request.split(' ')[1]
    fileName = fileName[1:]

    #if file exist
    if os.path.isfile(fileName):                                         #https://www.guru99.com/python-check-if-file-exists.html

        #response code
        connectionSocket.send('HTTP/1.0 200 OK\r\n'.encode())            #https://stackoverflow.com/questions/8315209/sending-http-headers-with-python
        
        #date header
        date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")     #https://pynative.com/python-datetime-format-strftime/
        date = "Date: " + date + "\n"
        connectionSocket.send(date.encode())

        #content-length header
        contentLength = str(os.path.getsize(fileName))
        contentLength = "Content-Length: " + contentLength + "\n"
        connectionSocket.send(contentLength.encode())

        #last-modified header
        lastModified = datetime.datetime.fromtimestamp(os.path.getmtime(fileName)).strftime("%d-%m-%Y %H:%M:%S") #https://stackoverflow.com/questions/237079/how-to-get-file-creation-and-modification-date-times/237084#237084
        lastModified = "Last-Modified: " + lastModified + "\n"
        connectionSocket.send(lastModified.encode())

        #connection header
        connectionHeader = "Connection: close\n"
        connectionSocket.send(connectionHeader.encode())
        
        #content-type header
        contentType = fileName.split('.')[1]
        contentType = "Content-Type: " + contentType + "\n\n"
        connectionSocket.send(contentType.encode())
        
        with open(fileName, "rb") as f:                                  #https://www.thepythoncode.com/code/send-receive-files-using-sockets-python
            while True:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in 
                # busy networks
                connectionSocket.sendall(bytes_read)


    else:
        movedFile = open("moved", "r") #https://www.geeksforgeeks.org/python-how-to-search-for-a-string-in-text-files/
        readfile = movedFile.read()
        
        #if file has been moved
        if fileName in readfile: 
            movedFile.close()

            #response code
            connectionSocket.send('HTTP/1.0 301 Moved Permanently\r\n'.encode())
            
            #date header
            date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            date = "Date: " + date + "\n"
            connectionSocket.send(date.encode())

            # Content-Location Header
            movedFile = open("moved", "r")
            locationLine = ""
            for line in movedFile:
                if fileName in line:
                    locationLine = line
                    break
            url = locationLine.split(' ')[1]
            url = url.replace("\n", "")
            
            message = "Location: " + url
            connectionSocket.send(message.encode())

        #if file does not exist
        else: 
            #response code
            connectionSocket.send('HTTP/1.0 404 Not Found\r\n'.encode())
           
            #date header
            date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            date = "Date: " + date + "\n"
            connectionSocket.send(date.encode())

        movedFile.close()
    

    connectionSocket.close()
