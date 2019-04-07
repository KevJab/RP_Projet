from instance import *
from random import randint
from itertools import combinations

import sys

def select_p_percent(filename, percent):
	f = open(filename, 'r')
	lines = f.readlines()
	nb_photos = len(lines) * percent // 100

	inst = Instance()

	#print(nb_photos)

	for i in range(len(lines)):
		if i > nb_photos:
			break
		if i > 0:
			if lines[i][3] in "1234567890":
				arg = lines[i][5:len(lines[i]) - 1].split(" ")
			else:
				arg = lines[i][4:len(lines[i]) - 1].split(" ")
			p = Photo(lines[i][0], arg, i-1)
			inst.add_photo(p)
	return inst

def h_before_v(inst):

	slides = []

	inst.sort()

	for pH in inst.tabH:
		slides.append(Slide(pH))

	for i in range(0, len(inst.tabV), 2):
		if(i != len(inst.tabV)-1):
			slides.append(Slide(inst.tabV[i], inst.tabV[i+1]))

	return slides

def glouton(inst):
	solution = []
	already_taken = []
	h_or_v = randint(0, 1)
	if (h_or_v == 0 or not inst.tabV) and inst.tabH:
		alea = randint(0, len(inst.tabH) - 1)
		solution.append(Slide(inst.tabH[alea]))
		already_taken.append(inst.tabH[alea].p_id)
	else:
		alea1 = randint(0, len(inst.tabV) - 1)
		alea2 = randint(0, len(inst.tabV) - 1)
		while alea1 == alea2:
			alea2 = randint(0, len(inst.tabV) - 1)
		solution.append(Slide(inst.tabV[alea1], inst.tabV[alea2]))
		already_taken.append(inst.tabV[alea1].p_id)
		already_taken.append(inst.tabV[alea2].p_id)

	all_permutation = list(combinations(inst.tabV, 2))

	while len(solution) < len(inst.tabH) + len(inst.tabV)//2:
		maxi = -1
		max_photo = None
		for i in inst.tabH:
			if i.p_id not in already_taken:
				s = score_transition(solution[len(solution) - 1].key_words, Slide(i).key_words)
				if s > maxi:
					maxi = s
					max_photo = Slide(i)
		for i,j in all_permutation:
			if i.p_id not in already_taken and j.p_id not in already_taken:
				slide = Slide(i, j)
				s = score_transition(solution[len(solution) - 1].key_words, slide.key_words)
			if s > maxi:
				maxi = s
				max_photo = slide
		if max_photo.p2.p_id == -1:
			already_taken.append(max_photo.p1.p_id)
		else:
			already_taken.append(max_photo.p1.p_id)
			already_taken.append(max_photo.p2.p_id)
		solution.append(max_photo)
	print(len(solution))
	for i in solution:
		print(i)
	return solution

def evaluate(sol):
	score = 0
	for i in range(len(sol.slides)-1):
		kw1 = sol.slides[i].key_words
		kw2 = sol.slides[i+1].key_words
		score += score_transition(kw1, kw2)
		#print("Tour",i,"score",score)
	return score

def score_transition(kw1, kw2):
	communs = kw1.intersection(kw2)
	si = kw1.difference(kw2)
	sii = kw2.difference(kw1)

	"""print("kw1", kw1, "kw2", kw2)
	print("communs", communs)
	print("si", si)
	print("sii", sii)
	print()"""
	nb_communs = len(communs)
	nb_si = len(si)
	nb_sii = len(sii)
	#print("\tcommuns: %d, seulmt sur la slide: %d, seulmt sur la suivante: %d"%(nb_communs, nb_si, nb_sii))
	return min([nb_si, nb_sii, nb_communs])


def main(argv):
	instance = select_p_percent("Inputs\\b_lovely_landscapes.txt", 1)
	#instance = select_p_percent("Inputs\\a_example.txt", 100)
	#sol = Solution(instance, h_before_v, "H_puis_V.sol")
	sol = Solution(instance, glouton, "glouton.sol")
	sol.output()
	print("Évaluation de la solution de %s : %d" %("Inputs\\b_lovely_landscapes.txt",evaluate(sol)))



if __name__ == "__main__":
	main(sys.argv[1:])
