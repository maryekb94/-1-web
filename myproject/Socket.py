import socket 
import os.path
 
buffer_size = 2048
PORT = 8000

server_address = ('localhost',8000)
http_ok = """HTTP/1.1 200 OK\nContent-Type: text/html\n\n\n"""
print ('Serving HTTP on port %s ...' % PORT )

if __name__ == "__main__":
	
	sock_obj = socket.socket()
	sock_obj.bind(server_address)
	sock_obj.listen(10)
	while True:
		conn,addr = sock_obj.accept()
		request = conn.recv(buffer_size)
		filePath = ''
		
		result = request.split('\n')[0].split(' ')[1]
		filePath = './' + result
		if not os.path.isfile(filePath):
			filePath ='./index.html' 
		
		
		fd = open(filePath,'r')
		fileContent = http_ok + fd.read()
		conn.send(fileContent)
		fd.close()
		conn.close()
	sock_obj.close()	
