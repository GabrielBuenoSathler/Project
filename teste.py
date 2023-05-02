#!/usr/bin/env python
import socket 
import time 
import struct

#ip a se conectar
ip = "192.168.15.4"

#porta do socket server
port = 8080 

addr = ((ip,port)) 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client_socket.connect(addr) 
msg  = bytearray()
msg.append(49)
msg.append(50)
msg.append(51)
msg.append(52)
#msg.append(10)

def  kommando(i):
    client_socket.send(chr(msg[i]).encode())

name = "not_desliga"

  

while name!= "desliga":
    name = input("What is my name? ")
    if name == "f":
        print("pra frente")
        kommando(0)
    if name == "p":
         kommando(1)

time.sleep(1)

client_socket.close()
