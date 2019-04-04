from random import *

class Photo:
	def __init__(self, ori, key_words, p_id):
		self.ori = ori				# orientation of the picture (H or V)
		self.key_words = key_words	# list of key words
		self.p_id = p_id			# picture ID (unique)
		
	def __lt__(self, other):	#needed for sort
		return self.p_id < other.p_id
	
	def __eq__(self, other):
		return self.p_id == other.p_id
	
	def __gt__(self, other):	#just in case
		return self.p_id > other.p_id



class Instance:
	def __init__(self, photosH = [], photosV = []):
		self.tabH = photosH		# a list of horizontal pictures
		self.tabV = photosV		# a list of vertical pictures
		self.nb_photos = len(photosH) + len(photosV)
		self.sort()
	
	def add_photo(self, p):	# adds a picture, and re-sorts both lists by p_id
		if p.ori == "H":
			self.tabH.append(p)
		else:
			self.tabV.append(p)
		self.sort()
	
	def sort(self):
		self.tabH.sort()
		self.tabV.sort()
	
	# retire de l'instance la photo d'identifiant _id
	def take_photo(self, _id):
		# parcours des photos horizontales pour trouver la photo d'id _id
		for i in range(len(self.tabH)):
			if self.tabH[i].p_id == _id:
				return self.tabH.pop(i)
			elif self.tabH[i].p_id > _id:
				break
		
		# parcours des photos verticales
		for i in range(len(self.tabV)):
			if self.tabV[i].p_id == _id:
				return self.tabV.pop(i)
				
	def best_photo(self, slide):
		# trouver la photo maximisant la transition
		pass
	
	def best_photo2(self, slide):
		# trouver une 2e photo V maximisant la transition
		pass
	
	# une instance est OK tant qu'il reste des photos horizontales, ou plus d'une photo verticale
	def is_ok(self): 
		return (len(self.tabH) != 0) or (len(self.tabV) > 1)
			
class Slide:
	def __init__(self, p1, p2 = -1):
		self.p1 = p1		# the first picture in the slide
		self.p2 = p2		# the 2nd vertical picture, or -1 of the first one was horizontal
		if p2 == -1:
			self.key_words = set(p1.key_words) # a set made of the first picture's keywords
		else:
			self.key_words = set(p1.key_words).union(set(p2.key_words)) # a set of the union of both pictures' keywords
	
	def __str__(self):		# redefining str(Slide) for easier way of writing
		if self.p2 == -1:
			return str(self.p1.p_id) + "\n"
		return str(self.p1.p_id) + " " + str(self.p2.p_id) + "\n"			
	
class Solution:
	def __init__(self, instance, func, out_file="output.sol"):
		self.instance = instance	# the instance to solve
		self.func = func			# the slide-sorting function
		self.out_file = out_file	# the file to write (has to be .sol)
		self.slides = []			# the list of slides
		self.find_solution()		# finds the solution according to self.func
		#self.output()
		
	def find_solution(self):
		self.slides = self.func(self.instance)
		
	def output(self):		#writes the solution in the output file
		sol = open(self.out_file, 'w')
	
		sol.write(str(len(self.slides)) + "\n")
		for slide in self.slides:
			sol.write(str(slide))
	
	
	
	
	
	
	
	
	
	
	
	
