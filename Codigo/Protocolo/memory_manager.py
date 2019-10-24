#Imports
import pickle
import os
import team_interpreter
import sensor_interpreter
import time
#Imports

num_pages = 0
pages_list = {}


def create_page(identifier):
	# ~ global num_pages
	# ~ global pages_list
	identifier = identifier + 1
	pages_list[identifier] = PageInfo()
	return identifier
	

# ~ def create_id():
	# ~ global num_pages
	# ~ identifier = hex(num_pages)
	# ~ num_pages += 1
	# ~ return identifier
	
#pageID como quinto argumento de lo de abajo
def store(date, teamId, sensorId, data, pageId):
	# ~ team = ""
	# ~ if (teamId == '1'):
		# ~ team = "Whitenoise"
	# ~ elif (teamId == '2'):
		# ~ team = "FlamingoBlack"
	# ~ elif (teamId == '3'):
		# ~ team = "GISSO"
	# ~ elif (id == '4'):
		# ~ team = "KOF"
	# ~ elif (id == '5'):
		# ~ team = "Equipo404"
	# ~ elif (id == '6'):
		# ~ team = "Poffis"
		
	team = str(team_interpreter.interpret(teamId))
	sensor = str(sensor_interpreter.interpret(sensorId))
	path = "./pages/" + team
	if(os.path.exists(path)==False):
		os.makedirs(path)
		
	path = path + sensor + ".txt"
	file = open(str(path), "a")
	file.write("%d" % int(date) + " " + "%f" % float(data) + "\n")
	file.close()

def  new_page(identifier):
	global pages_list

	pass

def read(teamId, sensorId, pageId):
	vector = []
	team = team_interpreter.interpret(teamId)
	sensor = sensor_interpreter.interpret(sensorId)
	path = "./pages/" + team
	with open(path+sensor+str(pageId)+".txt", "rt") as myfile:
		for myline in myfile:
			vector.append(myline)
	return vector


class PageInfo(): #Need to analice more that
    def __init__(self, *args, **kwargs):
        self.size = 0
        self.content = []
