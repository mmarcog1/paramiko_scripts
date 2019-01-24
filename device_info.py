#!/usr/bin/python3

import paramiko, getpass, time, json

#Reads the file with the devices and their respective ip addresses
with open('devices.json', 'r') as f:
    devices = json.load(f)
#Reads the file with the commands to be executed
with open('commands.txt', 'r') as f: 
    commands = [line for line in f.readlines()]

max_buffer = 65535

def clear_buffer(connection):
    #Clear the buffer to get only the execution prompt in the file later
    if connection.recv_ready():
        return connection.recv(max_buffer)

#Starts the loop for devices
for device in devices.keys():
    username = input(f'Username for {device}: ')
    password = getpass.getpass('Password: ')
    outputFileName = device + '_output.txt'
    connection = paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connection.connect(devices[device]['ip'], username=username, password=password, look_for_keys=False, allow_agent=False)
    new_connection = connection.invoke_shell()
    output = clear_buffer(new_connection)
    time.sleep(2)
    output = clear_buffer(new_connection)
    with open(outputFileName, 'wb') as f:
        for command in commands:
            new_connection.send(command)
            time.sleep(2)
            output = new_connection.recv(max_buffer)
            print(output)
            f.write(output)
    
    new_connection.close()
    

