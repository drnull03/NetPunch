import socket
import threading
import time

VERSION=0.1


"""
TODO: implement a rendezvous using a blackchain smart contract and maybe IPFS?
TODO: error handling
"""



"""
Node 1:
first punch a hole on port 50001 constant
listen on port 50001 (different thread)
send messages on port 50002

Node 2:
first punch a hole on port 50001 constant
listen on port 50001 (different thread)
send messages on port 50002

punch a hole in the sending port (50001)

"""

#get the node public someway may implement autoNAT in the future
#know get them using some public service



other_node_ip = "8.8.8.8" # hard code ur ip here



print(f'punching hole in node: {other_node_ip}')
sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #using udp for holepunching
sock1.bind(('0.0.0.0', 50001))
sock1.sendto(b'0', (other_node_ip, 50002)) #opened port 50001 

#using another thread for listening because the busywait can inturrpt sending
def listen():
	while True:
		data = sock1.recvfrom(1024)
		if(data.decode().strip() != "MAGIC$"):
			print('\rpeer: {}\n> '.format(data.decode()), end='')

listener = threading.Thread(target=listen, daemon=True);
listener.start()








#sending is done on port 50002 udp
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2.bind(('0.0.0.0', 50002))



#implemeting a heartbeat method
def heartBeat():
	while True:
		sock2.sendto(b'MAGIC$',(other_node_ip,50001))
		time.sleep(4) #heartbeat every 4 seconds

heart_beat_thread = threading.Thread(target=heartBeat,daemon=True)
heart_beat_thread.start()


#actual sending
while True:
	msg = input('> ')
	sock2.sendto(msg.encode(), (other_node_ip, 50001))



