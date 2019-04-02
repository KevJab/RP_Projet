from instance import *

import sys

def select_p_percent(filename, percent):
	f = open(filename, 'r')
	nb_photos = int(int(f.readline())*percent / 100.)
	
	inst = Instance()
	
	for i in range(nb_photos):
		arg = [word.rstrip('\n') for word in f.readline().split(' ')]
		p = Photo(arg[0], arg[2:], i)
		inst.add_photo(p)
		
	return inst
	
def h_before_v(inst):
	
	slides = []
	
	for pH in inst.tabH:
		slides.append(Slide(pH))
		
	for i in range(0, len(inst.tabV), 2):
		if(i != len(inst.tabV)-1):
			slides.append(Slide(inst.tabV[i], inst.tabV[i+1]))
	
	return slides

def evaluate(sol):
	score = 0
	for i in range(len(sol.slides)-1):
		kw1 = sol.slides[i].key_words
		kw2 = sol.slides[i+1].key_words
		
		communs = kw1.intersection(kw2)
		si = kw1.difference(kw2)
		sii = kw2.difference(kw1)
		
		#print("\t"+" ".join(map(str, [communs, si, sii])))
		nb_communs = len(communs)
		nb_si = len(si)
		nb_sii = len(sii)
		#print("\tcommuns: %d, seulmt sur la slide: %d, seulmt sur la suivante: %d"%(nb_communs, nb_si, nb_sii))
		score += min(min(nb_si, nb_sii), nb_communs)
	return score

		
def main(argv):
	instance = select_p_percent(argv[0], 100)
	sol = Solution(instance, h_before_v, "H_puis_V.sol")
	print("Évaluation de la solution de %s : %d" %(argv[0],evaluate(sol)))
	
	

if __name__ == "__main__":
	main(sys.argv[1:])
	
	
	
