#! /usr/bin/env python3

import os
import re 
import sys
import time
import socket
import glob
import pickle

def check_args():
	if len(sys.argv) != 2:
		print("ERROR: Must supply port number \nUSAGE: py dfs2.py 10002")
		sys.exit()

	else:
		try:
			if int(sys.argv[1]) != 10002:
				print("ERROR: Port number must be 10002")
				sys.exit()
			else:
				return int(sys.argv[1])
				
		except ValueError:
				print("ERROR: Port number must be a number.")
				sys.exit()

check_args()

def auth_params():

	config_file='dfs.conf'
	fh=open(config_file, mode='r', encoding='cp1252')
	users=re.findall(r'Username: .*', fh.read())
	usernames=list()
	for i in range(0, len(users)):
		usernames.append(str(users[i]).split()[1])
	fh.close()

	fh=open(config_file, mode='r', encoding='cp1252')
	passes=re.findall(r'Password: .*', fh.read())
	passwords=list()
	for i in range(0, len(passes)):
		passwords.append(str(passes[i]).split()[1])
	fh.close()
	global auth_dict 
	auth_dict = {}
	for i in range(0, len(users)):
		entry={usernames[i]:passwords[i]}
		auth_dict.update(entry)

	return auth_dict

def client_auth(auth_dict, username, password):
	ct = 0
	auth_status=''
	for key, value in auth_dict.items():
		ct += 1
		if auth_status != '':
			pass
		else:
			if ct < len(auth_dict):
			
				if username == key:
					print('Correct username.')
					
					if password == value:
						print('Correct password.')
						
						auth_status='Authorization Granted.\n'
						print(auth_status)
						conn.send(auth_status.encode())
						pass
					else:
						print('Incorrect password.')
						auth_status = 'Authorization Denied.\n'
						print(auth_status)
						conn.send(auth_status.encode())
						sys.exit()
				else:
					continue
			
			else:
				if username == key:
					print('Correct username.')
							
					if password == value:
						print('Correct password.')
						
						auth_status='Authorization Granted.\n'
						print(auth_status)
						conn.send(auth_status.encode())
						pass
					else:
						print('Incorrect password.')
						auth_status = 'Authorization Denied.\n'
						print(auth_status)
						conn.send(auth_status.encode())
						sys.exit()
				else:
					print('Incorrect username.')
					auth_status = 'Authorization Denied.\n'
					print(auth_status)
					conn.send(auth_status.encode())
					sys.exit()
				
# put files into servers
def put(new_dir_path):
	
	try:
		buffersize = int(conn.recv(2048).decode())
		print('The buffer size is: ' +str(buffersize))
	except ValueError:
		print('The buffer size is not a number. \nExiting now...')
		sys.exit()
	name1 = conn.recv(1024).decode()
	chunk1 = conn.recv(buffersize).decode()
	print('Receiving ' +name1 +'...\n')

	file_folder = name1.split('_')[0]
	new_folder_path = os.getcwd() +'/' +username +'/' +file_folder
	
	if os.path.isdir(new_folder_path) == False:
		try:  
			os.mkdir(new_folder_path)
			print ("Successfully created the folder %s " % new_folder_path)	
			pass
		except OSError:
			print ("Creation of the folder %s failed" % new_folder_path)
	else:
		pass
	
	fh=open(os.path.join(new_folder_path, name1), 'w')
	fh.write(chunk1)
	fh.close()
		
	exists = new_folder_path +'/' +name1
	if os.path.isfile(exists) == True:
		response = 'Chunk 1 successfully transferred.\n'
		print(response)
		conn.send(response.encode())
	else:
		response = 'Chunk 1 transfer incomplete.\n'
		print(response)
		conn.send(response.encode())		
	name2 = conn.recv(1024).decode()
	chunk2 = conn.recv(buffersize).decode()
	print('Receiving ' +name2 +'...\n')	
	fh=open(os.path.join(new_folder_path, name2), 'w')
	fh.write(chunk2)
	fh.close()
			
	exists = new_folder_path +'/' +name2
	if os.path.isfile(exists) == True:
		response = 'Chunk 2 successfully transferred.\n'
		print(response)
		conn.send(response.encode())
	else:
		response = 'Chunk 2 transfer incomplete.\n'
		print(response)
		conn.send(response.encode())						
	
	print('Exiting now...')
	sys.exit()

# funtion for creating new dir
def new_dir(username):

	global new_dir_path
	new_dir_path = os.getcwd() +'/' +username

	if os.path.isdir(new_dir_path) == False:
		try:  
			os.mkdir(new_dir_path)
			print ("Successfully created the directory %s " % new_dir_path)	
			return new_dir_path
		except OSError:
			print ("Creation of the directory %s failed" % new_dir_path)
	
	else:
		return new_dir_path
		pass

# command to list files in servers	
def list_files(username):

	user_dir = os.getcwd() +'/' +username
	file_dir_list = next(os.walk(user_dir))[1]
	
	if file_dir_list == []:
		response='There are no files yet.'
		print(response)
		conn.send(response.encode())
		
	else:
		file_list = []
		for i in range(0, len(file_dir_list)):
			file_dir = file_dir_list[i]
			file_list.append(os.listdir(user_dir +"/" +file_dir))
	
		if file_list == [[]]:
			response='There are no files yet.'
			print(response)
			conn.send(response.encode())
		
		else:
			with open('filenames.txt', 'w') as fh:
				for list in file_list:
					for file in range(0, len(list)):
						fh.write('%s\n' % list[file])
			
			# send list (the txt file) to client
			file_names=open('filenames.txt', 'rb').read()
			conn.send(file_names)
			print('\nSending file names...\n')	

			os.remove('filenames.txt')
		
		
# gets files from servers
def get(username):

	filename = conn.recv(1024).decode()
	print('User ' +username +' requested: ' +filename)
	
	user_dir = os.getcwd() +'/' +username
	file_dir = os.path.join(user_dir, filename)
	user_dir_filelist = next(os.walk(user_dir))[1]
	
	if user_dir_filelist == []:
		response='Your directory has no files yet.\nExiting now...'
		print('User directory has no file folders.\nExiting now...')
		conn.send(response.encode())
		sys.exit()
		
	else:
		file_dir_chunklist = next(os.walk(file_dir))[2]

		if file_dir_chunklist == []:
			response='You do not have any files in the folder yet.\nExiting now...'
			print('File folder empty.\nExiting now...')
			conn.send(response.encode())
			sys.exit()
		
		else:
			ct = 0
			for chunk in user_dir_filelist:
				ct += 1
				if ct < len(user_dir_filelist):
					# file exists, send file
					if filename == chunk:				
						response='Server is preparing file transfer...'
						print('File found.')
						conn.send(response.encode())
						time.sleep(1)
						break
					else:
						continue
				# if ct == length of list
				else:
					if filename == chunk:
						response='Server is preparing file transfer...'
						print('File found.')
						conn.send(response.encode())
						time.sleep(1)
						pass
					else:
						response='No such file exists.\nExiting now...'
						print(response)
						conn.send(response.encode())
						sys.exit()
						
	# create  chunk paths
	name1, name2 = os.listdir(file_dir)
	chunk1 = username +'/' +chunk +'/' +name1
	chunk2 = username +'/' +chunk +'/' +name2
	
	statinfo=os.stat(chunk1)
	buffersize=round(float(statinfo.st_size)) +4
	conn.send(str(buffersize).encode())
	time.sleep(1)
	
	chunk1_num = name1.split('_')[1]
	chunk2_num = name2.split('_')[1]
	
	if chunk1_num == '1.txt' and chunk2_num == '4.txt':
		
		conn.send(name2.encode())
		time.sleep(0.5)
		chunk2=open(chunk2,'rb').read()
		conn.send(chunk2)
		
		print('Sending chunk 1: ' +name2)
	else:
		
		conn.send(name1.encode())
		time.sleep(0.5)
		chunk1=open(chunk1,'rb').read()
		conn.send(chunk1)
		print('Sending chunk 1: ' +name1)
		
	
	FINACK = conn.recv(1024).decode()
	

	if FINACK == 'Transfer incomplete':
		
		if chunk1_num == '1.txt' and chunk2_num == '4.txt':
			
			conn.send(name1.encode())
			time.sleep(0.5)
			chunk1=open(chunk1,'rb').read()
			conn.send(chunk1)
		
			print('Sending chunk 2: ' +name1)
		else:
			
			conn.send(name2.encode())
			time.sleep(0.5)
			chunk2=open(chunk2,'rb').read()
			conn.send(chunk2)
			print('Sending chunk 2: ' +name2)

			FIN = conn.recv(1024).decode()
			print(FIN)
		
	# iff FIN, exit (FINACK == 'Transfer successful.')
	else: 
		
	
		print(FINACK +'\nExiting now...')
		
	sys.exit()

	

server_name = '127.0.0.1'
server_port = int(sys.argv[1])
	
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_name, server_port))
server_socket.listen(5)
print('Server listening...')

while True:
	conn, client_address = server_socket.accept()
	print('Connected to Client.')
	
	username = conn.recv(2048)
	username = username.decode()
	print('received username')
	
	password = conn.recv(2048)
	password = password.decode()
	print('received password')
	
	auth_params()	
	client_auth(auth_dict, username, password)

	new_dir(username)
	
	command = conn.recv(1024).decode()
	print('The user requested to ' +command + ' files.')
		
	# PUT 
	if command == 'put':
		put(new_dir_path)
						
	# LIST
	elif command == 'list':
		list_files(username)
		
		answer = conn.recv(1024).decode()
		print('The user now requests to ' +answer +' files.')

		if answer == 'put':
			print('Receiving files...')
			put(new_dir_path)

		elif answer == 'get':
			get(username)
			
		else:
			print('Exiting now...')
			sys.exit()	
			
	elif command == 'get':
		get(username)
					 
	else:
		print('Command does not exist.\nExiting now...')
		sys.exit()	

conn.close()