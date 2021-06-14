import socket
from datetime import datetime
from netifaces import interfaces, ifaddresses, AF_INET


def getAPIP():
    for ifaceName in interfaces():
        addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
        if ifaceName == "en0":
            return ', '.join(addresses)

def sendAPIP(IP):
	print("IP: " + IP)
	APIP = getAPIP()
	send_message = "AP:" + APIP
	server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    # server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.settimeout(0.2)
	message = str.encode(send_message)
	server.sendto(message, (IP, 3000))
	return



def sendqueue(queue, IP):
	send_ID = "List: "
	for i in range(len(queue)):
		if i > 0:
			send_ID += " "
		send_ID += queue[i][2]
	server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    # server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	server.settimeout(0.2)
	print("sned queue message is : ", send_ID, "  to this IP : ", IP)
	message = str.encode(send_ID)
	server.sendto(message, (IP, 3000))
	print("queue sent!")
	return 




def check_one_hour(dic, queue):
	while len(queue) != 0:
		d = queue[-1][1].split('-')
		interval = datetime.now() - datetime(int(d[0]), int(d[1]), int(d[2]), int(d[3]))
		if interval.seconds < 3600: # less than one hour
			break
		if dic[queue[-1][0]] == queue[-1][1]:  # if IP and time is both the same
			# check the IP is alive
			# send check message
			server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
			server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
			# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			server.settimeout(0.2)
			message = str.encode("Here?")
			server.sendto(message, (queue[-1][0], 3000))

    		# listen to 
			try:
				client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket. IPPROTO_UDP)
				client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
				client.bind(("", 37020))
				client.settimeout(10)
				data, addr = client.recvfrom(1024)
				print(data)
				queue.insert(0, queue[-1])
			except:
				print("Can't recvform")
		
		queue.pop(-1)





def sendID(ID):
	server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
	# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	server.settimeout(0.2)
	message = str.encode(ID)
	server.sendto(message, ('<broadcast>', 3000))
	print("message sent!")


def reqID(dic, queue):
	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket. IPPROTO_UDP)
	client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
	# client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	client.bind(("", 37020))
	data, addr = client.recvfrom(1024)
	data = data.decode("utf-8") 
	IP = data.split(" ")[0]
	ID = data.split(" ")[1]
	now_time = datetime.now().strftime("%Y-%m-%d-%H")
	dic[IP] = now_time
	queue.insert(0, [IP, now_time, ID])
	return ID, IP


if __name__ == '__main__':

	dic = {}
	queue = []
	while True:
		# print("I need ID and IP")
		new_clientID, new_clientIP = reqID(dic, queue)
		# print("now the new client's ID is " + new_clientID + " and new_client's IP is " + new_clientIP)
		# print("I need to broacast ID")
		sendID(new_clientID)
		# print("I want to check the queue")
		check_one_hour(dic, queue)
		# print("I want to send APIP to the client")
		sendAPIP(new_clientIP)
		# print("I want to sen queue to client")
		sendqueue(queue, new_clientIP)
		

	
	

