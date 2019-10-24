#Imports
import socket
from ipcqueue import sysvmq
import struct
import memory_manager

#Imports
page_table = dict()

def malloc_maravilloso(sensorId, teamId):
		global page_table
		page = memory_manager.create_page()
		page_table[(sensorId, teamId)] = ProcessInfo()
		page_table[(sensorId, teamId)].last = page
		page_table[(sensorId, teamId)].list.append(page)

def store(sensorId, teamId, date, data, dataType):
	if (sensorId, teamId) not in page_table.keys():
		malloc_maravilloso(sensorId, teamId)
	if(page_table[(sensorId, teamId)].off_set + 8 >= 1024)
		page = memory_manager.create_page()
		page_table[(sensorId, teamId)].last = page
		page_table[(sensorId, teamId)].list.append(page)
		page_table[(sensorId, teamId)].off_set = 0
	memory_manager.store(date, teamId, sensorId, dataType, data, page_table[(sensorId, teamId)].last)
	page_table[(sensorId, teamId)].off_set += 8

def get_info(sensorId, teamId):


class ProcessInfo():
	def __init__(self, *args, **kwargs):
		self.last = None
		self.off_set = 0
		self.list = []