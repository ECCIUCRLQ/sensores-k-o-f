#Imports
import socket
from ipcqueue import sysvmq
import struct
import memory_manager as memory_manager

#Imports
page_table = dict()
queueR = sysvmq.Queue(2)
queueS = sysvmq.Queue(15)
s = struct.Struct("II")
ss = struct.Struct("BIBBf")
values = []
lastId = 0 

def malloc_maravilloso(sensorId, teamId):
		global page_table
		global lastId
		page = memory_manager.create_page(lastId)
		lastId += 1
		page_table[(sensorId, teamId)] = ProcessInfo()
		page_table[(sensorId, teamId)].last = page
		page_table[(sensorId, teamId)].list.append(page)

def store(sensorId, teamId, date, data):
	if (sensorId, teamId) not in page_table.keys():
		malloc_maravilloso(sensorId, teamId)
	if(page_table[(sensorId, teamId)].off_set + 8 >= 1024):
		page = memory_manager.create_page(lastId)
		lastId += 1
		page_table[(sensorId, teamId)].last = page
		page_table[(sensorId, teamId)].list.append(page)
		page_table[(sensorId, teamId)].off_set = 0
	memory_manager.store(date, teamId, sensorId, data, page_table[(sensorId, teamId)].last)
	page_table[(sensorId, teamId)].off_set += 8

def get_info(sensorId, teamId):
	for i in range(0, len(page_table[(sensorId, teamId)].list)):
		packet = memory_manager.read(sensorId, teamId, i)
		for j in packet:
			info = j.split(" ")
			packetInfo = s.pack(info[0],info[1])
			queueS.put(packetInfo, msg_type=1)




class ProcessInfo():
	def __init__(self, *args, **kwargs):
		self.last = None
		self.off_set = 0
		self.list = []
		
while True:
	packet = queueR.get(block=True, msg_type=1)
	packetU = ss.unpack(packet)
	if(packetU[0]==0):
		store(packetU[2], packetU[3], packetU[1], packetU[4])
	else:
		get_info(packetU[2], packetU[3])
