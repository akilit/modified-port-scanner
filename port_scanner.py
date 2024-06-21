#!/bin/python3

import sys
import socket
from datetime import datetime

DEFAULT_START_RANGE = 15
DEFAULT_END_RANGE = 140


#Define our target
if len(sys.argv) == 2 or len(sys.argv) == 4: #if command does not have exactly 2 or 4 commands
	if len(sys.argv) == 4: # setting start and end ranges if user does specify port range
		START_RANGE = sys.argv[2]
		END_RANGE = sys.argv[3]
	else:
		START_RANGE = DEFAULT_START_RANGE # setting default values if user does not specify
		END_RANGE = DEFAULT_END_RANGE 
	try:
		target = socket.gethostbyname(sys.argv[1]) # translate hostname to ipv4
	except socket.gaierror:
		print("Hostname could not be resolved")
		print("Syntax: python3 scanner.py <IP> <port start range> (default=15) <port end range> (default=140")
		sys.exit()
	else:
		print("-" * 50)
		print("Scanning target: "+ target)
		print(f"Range: port {START_RANGE} to port {END_RANGE}")
		print("Time started: " + str(datetime.now()))
		print("-" * 50)
else:
	print("invalid amount of arguments.")
	print("Syntax: python3 scanner.py <IP> <port start range> (default=15) <port end range> (default=140")
	sys.exit()

no_open_ports = True

try: 
	for port in range(int(START_RANGE), int(END_RANGE)):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # (ipv4, port #)
		socket.setdefaulttimeout(1) # 
		result = s.connect_ex((target, port)) # connect_ex is error indicator. if port is open, returns 0. if closed, returns 1
		if result == 0:
			print(f"Port {port} is open")
			no_open_ports = False
		s.close()
	if no_open_ports:
		print("No open ports")

except ValueError:
	print("Not a valid port range")
	print("Syntax: python3 scanner.py <IP> <port start range> (default=15) <port end range> (default=140")
	sys.exit()
except KeyboardInterrupt: # say person using '^C'
	print("\nExiting program.")
	sys.exit() # allows graceful exit of program
	
except socket.gaierror: # if hostname could not be resolved. if someone typed 'python3 scanner.py etoisneth
	print("Hostname could not be resolved.")
	sys.exit()
	
except socket.error: # if server is not online/talking back
	print("Could not connect to server")
	sys.exit()

