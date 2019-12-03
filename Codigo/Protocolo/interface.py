#Imports
import socket
from ipcqueue import sysvmq
import struct
import memory_manager as memory_manager
#Imports

page_table = dict()
server_queue = sysvmq.Queue(2)
plotter_queue = sysvmq.Queue(15)

s = struct.Struct("II")
ss = struct.Struct("BIBBf")

values = []

lastId = 0

def malloc_maravilloso(sensorId, teamId):
		global page_table
		global lastId
		lastId += 1
		page = memory_manager.create_page(lastId)
		page_table[str((sensorId + teamId))] = ProcessInfo()
		print(str((sensorId + teamId)))
		page_table[str((sensorId + teamId))].last = page
		page_table[str((sensorId + teamId))].list.append(page)

# def store(sensorId, teamId, date, data):
# 	global lastId
# 	if str((sensorId + teamId)) not in page_table.keys():
# 		malloc_maravilloso(sensorId, teamId)
# 	else:
# 		page = memory_manager.create_page(lastId)
# 		lastId += 1
# 		page_table[str((sensorId + teamId))].last = page
# 		page_table[str((sensorId + teamId))].list.append(page)
# 		#page_table[str((sensorId + teamId))].off_set = 0
# 	memory_manager.store(date, teamId, sensorId, data, page_table[str((sensorId + teamId))].last)
# 	page_table[str((sensorId + teamId))].off_set += 8

def get_info(sensorId, teamId):
	for i in range(0, len(page_table[str((sensorId + teamId))].list)):
		packet = memory_manager.read(sensorId, teamId, i)
		for j in packet:
			info = j.split(" ")
			info1 = info[1].replace("\n", "")
			packetInfo = s.pack(int(info[0]),int(float(info1)))
			plotter_queue.put(packetInfo, msg_type=1)




class ProcessInfo():
	def __init__(self, *args, **kwargs):
		self.last = None
		self.off_set = 0
		self.list = []

def main():		
	while True:
		packet = server_queue.get(block=True, msg_type=1)
		packetU = ss.unpack(packet)
		if(packetU[0]==0):
			if str((packetU[1])+(packetU[2])) not in page_table.keys():
				malloc_maravilloso((packetU[1]), (packetU[2]))	
			memory_manager.store(packetU[1], packetU[2], packetU[3], packetU[4], page_table[str((packetU[1])+(packetU[2]))].last)
		else:
			get_info(packetU[2], packetU[3])

main()