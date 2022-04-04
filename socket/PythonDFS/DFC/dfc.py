#! /usr/bin/env python3


import re 
import os
import sys
import glob
import time
import pickle
import socket
import hashlib 

def check_args():
	if len(sys.argv) != 2:
		print("ERROR: Must supply an argument \nUSAGE: py dfc.py dfc.conf")
		sys.exit()

	elif sys.argv[1].lower() != 'dfc.conf':
		print("ERROR: Must supply a valid argument \nUSAGE: py dfc.py dfc.conf")
		sys.exit()
	elif os.path.isfile(sys.argv[1]) != True:
		print("ERROR: dfc.conf not found.")
		sys.exit()	
	else:
		return sys.argv[1]
def user_auth():
	
	fh = open('dfc.conf', mode='r', encoding='cp1252')
	users=re.findall(r'Username: .*', fh.read())
	usernames=list()
	for i in range(0, len(users)):
		usernames.append(str(users[i]).split()[1])
	fh.close()
		
	fh = open('dfc.conf', mode='r', encoding='cp1252')
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

def authenticate():
	user_auth()
	
	auth_status = ''
	
	for i in range(0, 4):
		if auth_status == 'Valid username.':
		
			pass
		
		else:
			
			username = input('username: ')
		
			
			username_auth = []
			ct = 0
			for key, value in auth_dict.items():
				ct += 1
				if username == key:
					
					username_auth.append(ct)
				else:
					username_auth.append(0)
							
			if i < 2:
				if sum(username_auth) > 0:
					auth_status = 'Valid username.'
					continue
				else:
					print('Username does not exist. You have ' +str(3-i) + ' attempts left.')
					continue 
			elif i == 2:
				if sum(username_auth) > 0:
					auth_status = 'Valid username.'
					continue
				else:
					print('Username does not exist. You have ' +str(3-i) + ' attempt left.')
					continue 				
			else:
				if sum(username_auth) > 0:
					auth_status = 'Valid username.'
					continue
				else:
					print('Username does not exist. You have no more attempts.\nExiting now....')
					sys.exit()
	
	
	user_index = sum(username_auth)

	auth_status = ''
	for i in range(0, 4):
		if auth_status == 'Valid password.':
			
			pass
			
		else:
			
			password = input('password: ')
			
			hash=hashlib.md5()
			hash.update(password.encode())
			password = hash.hexdigest()
					
			password_auth = []
			ct = 0
			for key, value in auth_dict.items():
				ct += 1
				if password == value:
					password_auth.append(ct)
				else:
					password_auth.append(0)
			
			if i < 2:
				if sum(password_auth) > 0:

					if user_index == sum(password_auth):
						auth_status = 'Valid password.'
						continue
					else:
						print('Wrong password. You have ' +str(3-i) + ' attempts left.')
						continue
				else:
					print('Wrong password. You have ' +str(3-i) + ' attempts left.')
					continue
			elif i == 2:
				if sum(password_auth) > 0:
					if user_index == sum(password_auth):
						auth_status = 'Valid password.'
						continue
					else:
						print('Wrong password. You have ' +str(3-i) + ' attempt left.')
						continue 				
				else:
					print('Wrong password. You have ' +str(3-i) + ' attempt left.')
					continue 
			else:
				if user_index == sum(password_auth):
					auth_status = 'Valid password.'
					continue
				else:
					print('Wrong password. You have no more attempts.\nExiting now....')
					sys.exit()
					
	
	print('Authorization Granted.')					
	global final_authorization
	final_authorization = (username, password)
	return final_authorization

	
def server_conf():	
	fh = open('dfc.conf', mode='r', encoding='cp1252')
	params = re.findall(r'DFS.*', fh.read())

	s_names = list()
	for i in range(0, len(params)):
		s_names.append(str(params[i]).split()[1].split(":")[0])
	
	s_ports = list()
	for i in range(0, len(params)):
		s_ports.append(str(params[i]).split()[1].split(":")[1])

	s_names_dict = {}
	for i in range(0, len(params)):
		entry={'server' +str(i+1):s_names[i]}
		s_names_dict.update(entry)
		
	s_ports_dict = {}
	for i in range(0, len(params)):
		entry={'server' +str(i+1):s_ports[i]}
		s_ports_dict.update(entry)
	
	global server_list
	server_list = list()
	ct = 0
	for i in range(0, len(params)):
		ct += 1
		server_list.append((s_names_dict['server' +str(ct)],\
							int(s_ports_dict['server' + str(ct)])))
	return server_list

	
def split_files(filename, chunksize):

	with open(filename + '.txt', 'rb') as bytefile:
		content = bytearray(os.path.getsize(filename + '.txt'))
		bytefile.readinto(content)
		
		for count, i in enumerate(range(0, len(content), chunksize)):
			with open(filename + '_' + str(count+1) + '.txt.', 'wb') as fh:
				fh.write(content[i: i + chunksize])

				
def chunk_pairs(filename):
		
	# group chunks in paired lists							# per table:
	pair1 = [filename +'_1.txt', filename +'_2.txt']    	# 1,2
	pair2 = [filename +'_2.txt', filename +'_3.txt'] 		# 2,3
	pair3 = [filename +'_3.txt', filename +'_4.txt']		# 3,4 
	pair4 = [filename +'_4.txt', filename +'_1.txt']		# 4,1


	hash=hashlib.md5()
	with open(filename +'.txt', 'rb') as fh:
		buffer = fh.read()
		hash.update(buffer)
		
		storeval = int(hash.hexdigest(), 16) % 4

	if storeval == 0:
		dfs1 = pair1
		dfs2 = pair2
		dfs3 = pair3
		dfs4 = pair4
	elif storeval == 1:
		dfs1 = pair4
		dfs2 = pair1
		dfs3 = pair2
		dfs4 = pair3
	elif storeval == 2:
		dfs1 = pair3
		dfs2 = pair4
		dfs3 = pair1
		dfs4 = pair2
	else:
		dfs1 = pair2
		dfs2 = pair3
		dfs3 = pair4
		dfs4 = pair1
	
	return dfs1, dfs2, dfs3, dfs4 
	

def get_command():

	global command
	command = ''
	for i in range(0, 4):
		if command != '':
			return command
			break
		else:
			comm = input('Please specify a command [get, list, put]: ')
			if i < 2:
				if comm.lower() == 'get':
					command = 'get'
					continue
				elif comm.lower() == 'list':
					command = 'list'
					continue
				elif comm.lower() == 'put':
					command = 'put'
					continue
				else:
					print('There is no such command. You have ' +str(3-i) + ' attempts left.')
					continue
			elif i == 2:
				if comm.lower() == 'get':
					command = 'get'
					continue
				elif comm.lower() == 'list':
					command = 'list'
					continue
				elif comm.lower() == 'put':
					command = 'put'
					continue
				else:
					print('There is no such command. You have ' +str(3-i) + ' attempt left.')
					continue
			else:
				print('There is no such command. You have no more attempts.\nExiting now....')
				sys.exit()
			
def get_filename():
	for i in range(0, 2):
		if i == 0:
			txtfiles = []
			print('Current files: ')
			print('-' * 15)
			for file in glob.glob("*.txt"):
				txtfiles.append(file)
				print(file.split(".")[0])
			print('\n')
			filename = input('Please specify a file: ')
			
			try:
				statinfo = os.stat(filename + '.txt')
				break
			except FileNotFoundError:
				print('There is no such file in the directory.\nPlease try again.\n')
				continue 
		else:
			txtfiles = []
			print('Current files: ')
			print('-' * 15)
			for file in glob.glob("*.txt"):
				txtfiles.append(file)
				print(file.split(".")[0])
			print('\n')
			filename = input('Please specify a file: ')
			
			try:
				statinfo = os.stat(filename + '.txt')
			except FileNotFoundError:
				print('There is no such file in the directory.\nExiting now...')
				sys.exit()
	
	global filename_statinfo
	filename_statinfo = (filename, statinfo)
	return filename_statinfo


	
def client():
	
	authenticate()
	username = final_authorization[0]
	password = final_authorization[1]
	
	server_conf()

	try:
		client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket1.connect(server_list[0])
		status1 = ('Connected to server', 'DFS1')
		print(status1[0], status1[1])
		time.sleep(1)
	except ConnectionRefusedError:
		status1 = ('Could not connect to server', 'DFS1')
		print(status1[0], status1[1])
		
	try:
		client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket2.connect(server_list[1])
		status2 = ('Connected to server', 'DFS2')
		print(status2[0], status2[1])
		time.sleep(1)
	except ConnectionRefusedError:
		status2 = ('Could not connect to server', 'DFS2')
		print(status2[0], status2[1])
		
	try:
		client_socket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket3.connect(server_list[2])
		status3 = ('Connected to server', 'DFS3')
		print(status3[0], status3[1])
		time.sleep(1)
	except ConnectionRefusedError:
		status3 = ('Could not connect to server', 'DFS3')
		print(status3[0], status3[1])
		
	try:
		client_socket4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket4.connect(server_list[3])
		status4 = ('Connected to server', 'DFS4')
		print(status4[0], status4[1])
		time.sleep(1)
	except ConnectionRefusedError:
		status4 = ('Could not connect to server', 'DFS4')
		print(status4[0], status4[1])	


	if status1[0] == 'Could not connect to server' and status2[0] == 'Could not connect to server' \
		and status3[0] == 'Could not connect to server' and status4[0] == 'Could not connect to server':
		print('All servers are down.\nExiting now...')
		sys.exit()
	else:
		pass
	conns = (client_socket1, client_socket2, client_socket3, client_socket4)
	DFSS = ('DFS1', 'DFS2', 'DFS3', 'DFS4')	

	

	for i in range(0,4):
		try:
			conns[i].send(username.encode())
			time.sleep(1)
		except OSError:
			pass 
	for i in range(0,4):
		try:
			conns[i].send(password.encode())
		except OSError:
			pass 		
				
	for i in range(0,4):
		try:
			response = conns[i].recv(1024)
			print('From ' +DFSS[i] +': ' +response.decode())
		except OSError:
			pass

	get_command()
		
	if command.lower() == 'put':
		for i in range(0,4):
			try:
				conns[i].send(command.encode())
			except OSError:
				pass

		get_filename()
		filename = filename_statinfo[0]
		statinfo = filename_statinfo[1]
		filesize = statinfo.st_size	
		buffersize = round(float(filesize)/4) +4
			
		split_files(filename, buffersize)
				
		dfs1, dfs2, dfs3, dfs4 = chunk_pairs(filename)
		
		dfss = (dfs1, dfs2, dfs3, dfs4)	
		
		
		for i in range(0,4):
			try:
				conns[i].send(str(buffersize).encode())
			except OSError:
				pass 
		
		for i in range(0,4):
			try:
				conns[i].send(dfss[i][0].encode())
				time.sleep(0.5)
				chunk1=open(dfss[i][0], 'rb').read()
				conns[i].send(chunk1)
				print('\nSending ' +str(dfss[i][0]) +'...\n')
			except OSError:
				pass
		for i in range(0,4):
			try:
				response=conns[i].recv(1024).decode()
				if response == 'Chunk 1 successfully transferred.\n':
					print(DFSS[i] +' Chunk 1 transfer complete.')
				else:
					print(DFSS[i] +' Chunk 1 transfer failed.')
			except OSError:
				pass
			
		for i in range(0,4):
			try:
				conns[i].send(dfss[i][1].encode())
				time.sleep(0.5)				
				chunk2=open(dfss[i][1], 'rb').read()
				conns[i].send(chunk2)
				print('\nSending ' +str(dfss[i][1]) +'...\n')
			except OSError:
				pass
		
		for i in range(0,4):
			try:
				response=conns[i].recv(1024).decode()
				if response == 'Chunk 2 successfully transferred.\n':
					print(DFSS[i] +' Chunk 2 transfer complete.')
				else:
					print(DFSS[i] +' Chunk 2 transfer incomplete.')
			except OSError:
				pass
			
	
		os.remove(str(dfs1[0]))
		os.remove(str(dfs1[1]))
		os.remove(str(dfs3[0]))
		os.remove(str(dfs3[1]))
		
		print('\nExiting now...')
		sys.exit()
			
	# LIST
	elif command.lower() == 'list':
			
		for i in range(0,4):
			try:
				conns[i].send(command.encode())
			except OSError:
				pass
		
		for i in range(0,4):		
			try:
				file_names=conns[i].recv(4096).decode()
				
				print('\nCurrent ' +DFSS[i] +'\%s files:' %username)
				print('-' * 27)
				print(file_names)
			except OSError:
				pass
		
		
		print('\nWould you like to get files, put files, or exit?')
		answer = input('[get, put, exit]: ')
		
		for i in range(0,4):
			try:
				conns[i].send(answer.encode())
			except OSError:
				pass
		
		if answer.lower() == 'put':

			get_filename()
			filename = filename_statinfo[0]
			statinfo = filename_statinfo[1]
						
			filesize = statinfo.st_size	
			buffersize = round(float(filesize)/4) +4
				
			split_files(filename, buffersize)
					
			dfs1, dfs2, dfs3, dfs4 = chunk_pairs(filename)
			
			dfss = (dfs1, dfs2, dfs3, dfs4)	
			
			for i in range(0,4):
				try:
					conns[i].send(str(buffersize).encode())
				except OSError:
					pass 
			
			for i in range(0,4):
				try:
					conns[i].send(dfss[i][0].encode())
					time.sleep(0.5)
					chunk1=open(dfss[i][0], 'rb').read()
					conns[i].send(chunk1)
					print('\nSending ' +str(dfss[i][0]) +'...\n')
				except OSError:
					pass
			
			for i in range(0,4):
				try:
					response=conns[i].recv(1024).decode()
					if response == 'Chunk 1 successfully transferred.\n':
						print(DFSS[i] +' Chunk 1 transfer complete.')
					else:
						print(DFSS[i] +' Chunk 1 transfer failed.')
				except OSError:
					pass
				
			for i in range(0,4):
				try:
					conns[i].send(dfss[i][1].encode())
					time.sleep(0.5)					
					chunk2=open(dfss[i][1], 'rb').read()
					conns[i].send(chunk2)
					print('\nSending ' +str(dfss[i][1]) +'...\n')
				except OSError:
					pass
			for i in range(0,4):
				try:
					response=conns[i].recv(1024).decode()
					if response == 'Chunk 2 successfully transferred.\n':
						print(DFSS[i] +' Chunk 2 transfer complete.')
					else:
						print(DFSS[i] +' Chunk 2 transfer incomplete.')
				except OSError:
					pass
				
			os.remove(str(dfs1[0]))
			os.remove(str(dfs1[1]))
			os.remove(str(dfs3[0]))
			os.remove(str(dfs3[1]))
			
			print('\nExiting now...')
			sys.exit()

			
		elif answer.lower() == 'get':
		
			new_dir_path = os.getcwd() +'/' +username

			if os.path.isdir(new_dir_path) == False:
				try:  
					os.mkdir(new_dir_path)
					print ("Successfully created the directory %s " % new_dir_path)	
					pass
				except OSError:
					print ("Creation of the directory %s failed" % new_dir_path)
			else:
				pass
			
			filename = input('Please specify a file: ')
			
			for i in range(0,4):
				try:
					conns[i].send(filename.encode())
				except OSError:
					pass
			
			for i in range(0,4):
				try:
					answer=conns[i].recv(1024).decode()
				except OSError:
					pass
			
			for i in range(0,4):
				if answer == 'Server is preparing file transfer...':
					try:
						buffersize=int(conns[i].recv(1024).decode())
					except OSError:
						pass
				else:
					try:
						print(answer)
						sys.exit()
					except OSError:
						pass			
			
			chunk_list = []
			for i in range(0,4):
				try:
					name=conns[i].recv(1024).decode()
					chunk_list.append(name)
				except OSError:
					pass
			
			
			for i in range(0,len(chunk_list)):
				try:
					chunk1=conns[i].recv(buffersize).decode()
					with open(os.path.join(new_dir_path, chunk_list[i]), 'w') as fh:
						fh.write(chunk1)
					print('File chunks successfully transferred.')
				except OSError:
					pass			
					
			arrived = chunk_list
			num_chunks = len(arrived)
			
			if num_chunks < 4:

				NACK = 'Transfer incomplete'
				print(NACK +'\nOnly ' +str(num_chunks) +' out of 4 chunks arrived.')
				for i in range(0,4):
					try:
						conns[i].send(NACK.encode())
					except OSError:
						pass 			

				chunk2_list = []
				for i in range(0,4):
					try:
						name2=conns[i].recv(1024).decode()
						chunk2_list.append(name2)
					except OSError:
						pass
					
				print('Receiving second batch...')
				for i in range(0,len(chunk2_list)):
					try:
						chunk2=conns[i].recv(buffersize).decode()
						with open(os.path.join(new_dir_path, chunk2_list[i]), 'w') as fh:
							fh.write(chunk2)
						print('File chunks successfully transferred.')
					except OSError:
						pass
				
			
				arrived2 = os.listdir(new_dir_path)

				arrived2_clean = []
				for i in range(0, len(arrived2)):
					if arrived2[i].split('_')[0] == filename:
						arrived2_clean.append(arrived2[i])
					else:
						pass 
					
				arrived2_intlist = []
				for i in range(0,len(arrived2_clean)):
					arrived2_intlist.append(int(arrived2_clean[i].split('_')[1].split('.')[0]))

				if arrived2_intlist == [1,2,3,4]:
					print('Chunks 1 through 4 are present.')
					
					FIN = 'Transfer successful.'
					for i in range(0,4):
						try:
							conns[i].send(FIN.encode())
						except OSError:
							pass 
							
					final_filename = arrived2_clean[0].split('_')[0] +'.txt'	
					
					with open(username +'/' +final_filename, 'wb') as outfile:		
						for chunk_name in arrived2_clean:
							with open(username +'/' +chunk_name, 'rb') as infile:
								outfile.write(infile.read())
					
					print('File successfully reconstructed.')
					
					for i in range(0,len(arrived2_clean)):
						try:
							os.remove(str(username +'/' +arrived2_clean[i]))
						except IndexError:
							pass
						
					print('Exiting now...')
					sys.exit()
					
				else:

					FIN = 'Transfer failed.\nExiting now...'
					for i in range(0,4):
						try:
							conns[i].send(FIN.encode())
						except OSError:
							pass
							
					print(FIN)
					sys.exit()
				
			else:
				print('A total of ' +str(num_chunks) +' chunks arrived.')
				
				arrived_ordered = []
				for i in range(0,4):
					arrived_ordered.append(int(arrived[i].split('_')[1].split('.')[0]))
				
				arrived_ordered.sort()
			
				if arrived_ordered == [1,2,3,4]:
				
					print('All four chunks are present.')
					
					FIN = 'Transfer successful.'
					for i in range(0,4):
						try:
							conns[i].send(FIN.encode())
						except OSError:
							pass 
							
					chunk_list.sort()
					final_filename = chunk_list[0].split('_')[0] +'.txt'	
					
					with open(username +'/' +final_filename, 'wb') as outfile:		
						for chunk_name in chunk_list:
							with open(username +'/' +chunk_name, 'rb') as infile:
								outfile.write(infile.read())
					
					print('File successfully reconstructed.')
					
					for i in range(0,4):
						try:
							os.remove(str(username +'/' +chunk_list[i]))
						except IndexError:
							pass
						
					sys.exit()
					
				else:
					# if the ordered list is not [1,2,3,4]
					FIN = 'Transfer failed.\Exiting now...'
					for i in range(0,4):
						try:
							conns[i].send(FIN.encode())
						except OSError:
							pass
							
					print(FIN)
					sys.exit()
					
		
			
		elif answer.lower() == 'exit':
			print('Exiting now...')
			sys.exit()
			
		
		else:
			print('This method does not exist.\nExiting now...')
			sys.exit()		
			

	else:
		
		for i in range(0,4):		
			try:
				conns[i].send(command.encode())
			except OSError:
				pass
		
		
		
		new_dir_path = os.getcwd() +'/' +username

		if os.path.isdir(new_dir_path) == False:
			try:  
				os.mkdir(new_dir_path)
				print ("Successfully created the directory %s " % new_dir_path)	
				pass
			except OSError:
				print ("Creation of the directory %s failed" % new_dir_path)
		else:
			pass
		
		
		filename = input('Please specify a file: ')
		
		
		for i in range(0,4):
			try:
				conns[i].send(filename.encode())
			except OSError:
				pass	
		
	
		for i in range(0,4):
			try:
				answer=conns[i].recv(1024).decode()
			except OSError:
				pass
		
		
		for i in range(0,4):
			if answer == 'Server is preparing file transfer...':
				try:
					buffersize=int(conns[i].recv(1024).decode())
					print(answer)
				except OSError:
					pass

			else:
				try:
					print(answer)
					sys.exit()
				except OSError:
					pass			
							
	 
		chunk_list = []
		for i in range(0,4):
			try:
				name=conns[i].recv(1024).decode()
				chunk_list.append(name)
			except OSError:
				pass
		
				
		for i in range(0,len(chunk_list)):
			try:
				chunk1=conns[i].recv(buffersize).decode()
				with open(os.path.join(new_dir_path, chunk_list[i]), 'w') as fh:
					fh.write(chunk1)
				print('File chunks successfully transferred.')
			except OSError:
				pass

		arrived = chunk_list
		num_chunks = len(arrived)
		
		if num_chunks < 4:

			NACK = 'Transfer incomplete'
			print(NACK +'\nOnly ' +str(num_chunks) +' out of 4 chunks arrived.')
			for i in range(0,4):
				try:
					conns[i].send(NACK.encode())
				except OSError:
					pass 			

			chunk2_list = []
			for i in range(0,4):
				try:
					name2=conns[i].recv(1024).decode()
					chunk2_list.append(name2)
				except OSError:
					pass
				
			print('Receiving second batch...')
			for i in range(0,len(chunk2_list)):
				try:
					chunk2=conns[i].recv(buffersize).decode()
					with open(os.path.join(new_dir_path, chunk2_list[i]), 'w') as fh:
						fh.write(chunk2)
					print('File chunks successfully transferred.')
				except OSError:
					pass
			
			
			arrived2 = os.listdir(new_dir_path)

			arrived2_clean = []
			for i in range(0, len(arrived2)):
				if arrived2[i].split('_')[0] == filename:
					arrived2_clean.append(arrived2[i])
				else:
					pass 
					
			arrived2_intlist = []
			for i in range(0,len(arrived2_clean)):
				arrived2_intlist.append(int(arrived2_clean[i].split('_')[1].split('.')[0]))

			
			if arrived2_intlist == [1,2,3,4]:
				print('Chunks 1 through 4 are present.')
					
				
				FIN = 'Transfer successful.'
				for i in range(0,4):
					try:
						conns[i].send(FIN.encode())
					except OSError:
						pass 
						
				
				final_filename = arrived2_clean[0].split('_')[0] +'.txt'	
				
				with open(username +'/' +final_filename, 'wb') as outfile:		
					for chunk_name in arrived2_clean:
						with open(username +'/' +chunk_name, 'rb') as infile:
							outfile.write(infile.read())
				
				print('File successfully reconstructed.')
				
			
				for i in range(0,len(arrived2_clean)):
					try:
						os.remove(str(username +'/' +arrived2_clean[i]))
					except IndexError:
						pass
					
				print('Exiting now...')
				sys.exit()
				
			else:

				FIN = 'Transfer failed.\nExiting now...'
				for i in range(0,4):
					try:
						conns[i].send(FIN.encode())
					except OSError:
						pass
							
				print(FIN)
				sys.exit()
			
		
		else:
			
			print('A total of ' +str(num_chunks) +' chunks arrived.')
			
		
			arrived_ordered = []
			for i in range(0,4):
				arrived_ordered.append(int(arrived[i].split('_')[1].split('.')[0]))
			
			arrived_ordered.sort()
		
			if arrived_ordered == [1,2,3,4]:
			
				print('All four chunks are present.')
				
				FIN = 'Transfer successful.'
				for i in range(0,4):
					try:
						conns[i].send(FIN.encode())
					except OSError:
						pass 
						
				chunk_list.sort()
				final_filename = chunk_list[0].split('_')[0] +'.txt'	
				
				with open(username +'/' +final_filename, 'wb') as outfile:		
					for chunk_name in chunk_list:
						with open(username +'/' +chunk_name, 'rb') as infile:
							outfile.write(infile.read())
				
				print('File successfully reconstructed.')
				
				for i in range(0,4):
					try:
						os.remove(str(username +'/' +chunk_list[i]))
					except IndexError:
						pass
					
				print('Exiting now...')
				sys.exit()
				
			else:
				FIN = 'Transfer failed.\Exiting now...'
				for i in range(0,4):
					try:
						conns[i].send(FIN.encode())
					except OSError:
						pass
						
				print(FIN)
				sys.exit()			
							
			
if __name__=='__main__':
	check_args()
	client()