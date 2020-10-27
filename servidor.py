#HTTP/1.1 server template
import socket
from datetime import datetime


#array with name that will be posted on the site
visitante = ''
visitantes = []
def retVisitantes():
    result = ''
    for v in visitantes:
        result = result + f'{v}<br>'
    return result

def removePlusSign(post_string):
    for character in post_string:
        if character == '+':
            post_string = post_string[:post_string.find('+')]+' '+post_string[post_string.find('+')+1:]
    return post_string

#listening to socket...
serverPort = 8081

#source code of the webpage hosted in the server
page = f'<!DOCTYPE HTML>\n<html><body><h1>This is THE WEB PAGE</h1><br><form name="name" method="POST">Digite o seu nome:<input type="text" name="your_name"><br><input type="submit" value="Submit"></form><br>Visitantes:<br>{retVisitantes()}</body></html>\r\n\r\n'

page404 = '<!DOCTYPE HTML>\n<html><body><h1>ERRO 404<br>Pagina nao encontrada</h1></body></html>\r\n\r\n'
page_bar = f'<!DOCTYPE HTML>\n<html><body><h1>A pagina que voce procura foi movida para <a href="http://localhost:{serverPort}/index.html">/index.html</a><br>Digite /index.html na sua solicitacao GET</h1></body></html>\r\n\r\n'
#get current time
currentTime = datetime.now()

#formatted date and time
d = currentTime.ctime()
date_array = d.split()
date_formatted = f'Date: {date_array[0]}, {d[4:]} BRT\r\n'


#create socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind socket to a specific port
serverSocket.bind(('', serverPort))

#start listening
serverSocket.listen(1)

print("Server HTTP/1.1 Initialized")
print(f'Listening to port {serverPort}')

#loop for receiving clients' requests

while True:
    connectionSocket, addr = serverSocket.accept()
    print("Client {} connected to server".format(addr))
    
    #Receives clients' requests
    request = connectionSocket.recv(1024).decode('utf-8')

    #breaks each word in the request
    splitted_request = request.split()
    if len(splitted_request) > 0 and splitted_request[0] == 'GET':
       # performs action pertaining to the GET command
       params = splitted_request[1]
       if splitted_request[1] == '/index.html' and len(splitted_request) > 4:
           params = splitted_request[4]+f'{splitted_request[1]}'
       print(splitted_request)
       if splitted_request[1] == '/index.html' and len(splitted_request) == 3:
           params = f'localhost:{serverPort}{splitted_request[1]}'
      
       if splitted_request[1] == '/' and (len(splitted_request) > 4 or len(splitted_request) == 3):
           params = f'localhost:{serverPort}{splitted_request[1]}'  
       print("Get type request, searching for {} resource".format(params[params.find('/'):]))
       #assuming the request was successful
       if params == f'localhost:{serverPort}/index.html':
           response = "\nHTTP/1.1 200 OK\r\n"
       else:
           if params == f'localhost:{serverPort}/':
               response = "\nHTTP/1.1 200 OK"
           else:
               response = "\nHTTP/1.1 404\r\n"
       response += 'Transfer-Encoded: chunked\r\n'
       response += date_formatted 
       response += "Content-Type:text/html; charset=UTF-8\r\n\r\n"
       if params == f'localhost:{serverPort}/index.html':
          response += f'<!DOCTYPE HTML>\n<html><body><h1>This is THE WEB PAGE</h1><br><form name="name" method="POST">Digite o seu nome:<input type="text" name="your_name"><br><input type="submit" value="Submit"></form><br>Visitantes:<br><h2>{retVisitantes()}</h2></body></html>\r\n\r\n'
       else:
           if params == f'localhost:{serverPort}/':
               response += page_bar
           else:
               response += page404
       connectionSocket.send(response.encode())

   
    if len(splitted_request) > 0 and splitted_request[0] == "POST":
       # performs action pertaining to the GET command
       params = splitted_request[1]
       if splitted_request[1] == '/index.html' and len(splitted_request) > 4:
           params = splitted_request[4]+f'{splitted_request[1]}'
       print(splitted_request)
       params2 = splitted_request[-1]
       params_post = params2[params2.find('=') + 1:]
       visitante = params_post
       visitante = removePlusSign(visitante)
       visitantes.append(visitante)
       print("Post type request, posting to {}".format(params[params.find('/'):]))
       #assuming the request was successful
       if params == f'localhost:{serverPort}/index.html':
           response = "\nHTTP/1.1 200 OK\r\n"
       else:
           response = "\nHTTP/1.1 404\r\n"
       response += date_formatted 
       response += "Content-Type:text/html; charset=UTF-8\r\n\r\n"
       if params == f'localhost:{serverPort}/index.html':
           response += f'<!DOCTYPE HTML>\n<html><body><h1>This is THE WEB PAGE</h1><br><form name="name" method="POST">Digite o seu nome:<input type="text" name="your_name"><br><input type="submit" value="Submit"></form><br>Visitantes:<br><h2>{retVisitantes()}</h2></body></html>\r\n\r\n'
       else:
           response += page404
       connectionSocket.send(response.encode())

    if len(splitted_request) > 0 and splitted_request[0] == "OPTIONS":
       # performs action pertaining to the GET command
       params = splitted_request[2]
       print(splitted_request)
       if splitted_request[2] == 'HTTP/1.1': 
           response = "\nHTTP/1.1 200 OK\r\n"
           response += 'Transfer-Encoded: chunked\r\n'
           response += date_formatted
           response += "Content-Type:text/html; charset=UTF-8\r\n\r\n"
           response += f"GET function:\n\tGET localhost:{serverPort}/index.html\nOPTIONS function:\n\tOPTIONS / HTTP/1.1\nHEAD function:\n\tHEAD / HTTP/1.1\nPOST function:\n\t*Available only through browser\r\n\r\n"
       connectionSocket.send(response.encode())
   
    if len(splitted_request) > 0 and splitted_request[0] == "HEAD":
       # performs action pertaining to the HEAD command
       params = splitted_request[2]
       print(splitted_request)
       if splitted_request[2] == 'HTTP/1.1': 
           response = "\nHTTP/1.1 200 OK\r\n"
           response += 'Transfer-Encoded: chunked\r\n'
           response += date_formatted
           response += "Content-Type:text/html; charset=UTF-8\r\n\r\n"
       connectionSocket.send(response.encode())


    connectionSocket.close()

