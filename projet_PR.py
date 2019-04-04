from instance import *
from random import *

import sys

#############################
# 
#  EXERCICE 1
#
#############################


# Fonction de sélection de percent % des photos du fichier filename
# (pour l'instant, seulement les percent premiers % sont pris. Randomiser?)
def select_p_percent(filename, percent):
	f = open(filename, 'r')
	nb_photos = int(int(f.readline())*percent / 100.)
	
	inst = Instance()
	
	for i in range(nb_photos):
		arg = [word.rstrip('\n') for word in f.readline().split(' ')]
		p = Photo(arg[0], arg[2:], i)
		inst.add_photo(p)
		
	return inst

# Méthode créant une présentation dont les photos H sont avant toutes les photos V
# toutes les photos sont cependant prises dans l'ordre de leur p_id
def h_before_v(inst):
	
	slides = []
	
	for pH in inst.tabH:
		slides.append(Slide(pH))
		
	for i in range(0, len(inst.tabV), 2):
		if(i != len(inst.tabV)-1):
			slides.append(Slide(inst.tabV[i], inst.tabV[i+1]))
	
	return slides

# Fonction d'évaluation d'une solution
# Vérifier que son résultat est égal au retour de Checker
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



#############################
# 
#  EXERCICE 3
#
#############################


def glouton(instance):
	
	slides = []
	
	
	# Ajouter la 1re slide aléatoirement
	
	# r est un id de photo random
	r = randint(instance.nb_photos)
	
	p1 = instance.take_photo(r)
	if p1.ori == "H":
		slides.append(Slide(p1))
	else:
		r2 = randint(instance.nb_photos)
		while r2 == r:
			r = randint(instance.nb_photos)
		
		p2 = instance.take_photo(r2)
		slides.append(Slide(p1, p2))
			
	
	while(instance.is_ok()):
		




		
def main(argv):
	# Sélection de p% des images de l'instance
	instance = select_p_percent(argv[0], 100)
	
	# Calcule le score de l'instance, en utilisant la méthode passée en 2e paramètre
	sol = Solution(instance, h_before_v, "H_puis_V.sol")
	
	print("Évaluation de la solution de %s : %d" %(argv[0],evaluate(sol)))
	
	

if __name__ == "__main__":
	main(sys.argv[1:])
	
	
	
