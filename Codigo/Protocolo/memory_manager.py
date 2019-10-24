#Imports
import pickle
import file_manager
import os
import team_interpreter
import sensor_interpreter
#Imports

num_pages = 0
pages_list = {}


def create_page():
	global num_pages
	global pages_list
	id = create_id
	pages_list[id] = PageInfo()
	return id

def create_id():
	global num_pages
	id = hex(num_pages)
	num_pages += 1
	return id

def store(date, teamId, sensorId, dataType, data, pageId):
	team = team_interpreter.interpret(teamId)
	sensor = sensor_interpreter.interpret(sensorId)
	path = "pages/" + team
	if(os.path.exists(path)==False):
		os.makedirs(path)
	file = open(path + sensor + str(pageId), "a")
	file.write("%i" % str(date) + "%f" % str(data))
	file.close()

def  new_page(id):
	global pages_list

	pass

class PageInfo(): #Need to analice more that
    def __init__(self, *args, **kwargs):
        self.size = 0
        self.content = []