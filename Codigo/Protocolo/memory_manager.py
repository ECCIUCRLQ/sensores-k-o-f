#Imports
import pickle

#Imports

num_pages = 0
pages_list = {}


def create_page():
	global num_pages
	global pages_list
	id = create_id
	pages_list[id] = PageInfo() #Get this idea from Jose
	return id

def create_id():
	global num_pages
	id = hex(num_pages)
	num_pages += 1
	return id

class PageInfo(): #Need to analice more that
    def __init__(self, *args, **kwargs):
        self.current_size = 0
        self.content = []