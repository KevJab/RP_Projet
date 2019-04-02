class Photo:
	def __init__(self, ori, key_words, p_id):
		self.ori = ori
		self.key_words = key_words
		self.p_id = p_id
		
	def __lt__(self, other):
		return self.p_id < other.p_id
	
	def __gt__(self, other):
		return self.p_id > other.p_id



class Instance:
	def __init__(self, photosH = [], photosV = []):
		self.tabH = photosH
		self.tabV = photosV
		self.sort()
	
	def add_photo(self, p):
		if p.ori == "H":
			self.tabH.append(p)
		else:
			self.tabV.append(p)
		self.sort()
	
	def sort(self):
		self.tabH.sort()
		self.tabV.sort()
			
class Slide:
	def __init__(self, p1, p2 = -1):
		self.p1 = p1
		self.p2 = p2
		if p2 == -1:
			self.key_words = set(p1.key_words)
		else:
			self.key_words = set(p1.key_words).union(set(p2.key_words))
	
	def __str__(self):
		if self.p2 == -1:
			return str(self.p1.p_id) + "\n"
		return str(self.p1.p_id) + " " + str(self.p2.p_id) + "\n"			
	
class Solution:
	def __init__(self, instance, func, out_file="output.sol"):
		self.instance = instance
		self.func = func
		self.out_file = out_file
		self.slides = []
		self.find_solution()
		#self.output()
		
	def find_solution(self):
		self.slides = self.func(self.instance)
		
	def output(self):
		sol = open(self.out_file, 'w')
	
		sol.write(str(len(self.slides)) + "\n")
		for slide in self.slides:
			sol.write(str(slide))
	
	
	
	
	
	
	
	
	
	
	
	
