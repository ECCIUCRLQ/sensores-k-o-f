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

def malloc_maravilloso(sensorId, teamId):
		global page_table
		page = memory_manager.create_page()
		page_table[str((sensorId + teamId))] = PageCreation()
		print("Se creo pagina para: "+str((sensorId + teamId)+" con el id: "+str(page)))
		page_table[str((sensorId + teamId))].pages_list[page] = 1024
		page_table[str((sensorId + teamId))].last = page

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
	pages = page_table[str((sensorId + teamId))].list
	for i in range(0, len(page_table[str((sensorId + teamId))].list)):
		packet = memory_manager.get_page(pages[i])
		for j in range(0, len(packet), 2):
			info = []
			info[0] = (packet[j])
			info[1] = (packet[j+1])
			packetInfo = s.pack(int(info[0]),int(float(info[1])))
			plotter_queue.put(packetInfo, msg_type=1)




class PageCreation():
	def __init__(self, *args, **kwargs):
		self.last 
		self.pages_list = {}

def main(self):		
	while True:
		packet = server_queue.get(block=True, msg_type=1)
		packetU = ss.unpack(packet)
		local_last = self.page_table[str((packetU[1])+(packetU[2]))].last
		local_offset = self.page_table[str((packetU[1])+(packetU[2]))].pages_list[local_last]
		if(packetU[0]==0):
			if str((packetU[1])+(packetU[2])) not in page_table.keys():
				malloc_maravilloso((packetU[1]), (packetU[2]))	
			elif(local_offset > 1019):
				malloc_maravilloso((packetU[1]), (packetU[2]))
			else:
				data = []
				data[0] = packetU[3]
				data[1] = packetU[4]
				memory_manager.store(local_last, local_offset, data)
		else:
			get_info(packetU[2], packetU[3])

main()