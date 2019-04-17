from instance import *
from random import *
from itertools import *
from copy import deepcopy
import sys


#####################################################
#                    EXERCICE 1                        #
#####################################################

def select_p_percent(filename, percent):
    f = open(filename, 'r')
    lines = f.readlines()
    nb_photos = len(lines) * percent // 100  # Number of lines we will read

    inst = Instance()

    for i in range(len(lines)):
        if i > nb_photos:  # If we read enough line we stop
            break
        if i > 0:
            if lines[i][3] in "1234567890":  # Sometimes pictures have more than 9 keyword
                arg = lines[i][5:len(lines[i]) - 1].split(" ")
            else:
                arg = lines[i][4:len(lines[i]) - 1].split(" ")
            p = Photo(lines[i][0], arg, i-1)
            inst.add_photo(p)
    return inst
    

def evaluate(slides):
    score = 0
    for i in range(len(slides)-1):  # For each transition we calculate the score
        kw1 = slides[i].key_words
        kw2 = slides[i+1].key_words
        score += score_transition(kw1, kw2)
    return score


def score_transition(kw1, kw2):  # Return the minimum as asked in the subject
    return len(min([kw1.difference(kw2), kw2.difference(kw1), kw1.intersection(kw2)], key=lambda x: len(x)))


def h_before_v(inst):  # Solution with all horizontal slides before vertical slides
    slides = []
    inst.sort()
    for pH in inst.tabH:
        slides.append(Slide(pH))

    for i in range(0, len(inst.tabV), 2):
        if(i != len(inst.tabV)-1):  # This way there are no problems even if there is an odd number of vertical pictures
            slides.append(Slide(inst.tabV[i], inst.tabV[i+1]))
    return slides
    

#####################################################
#                    EXERCICE 3                        #
#####################################################

def glouton(inst):
    solution = []
    h_or_v = randint(0, 1)  # Randomly choose to pick a horizontal or vertical picture
    len_solution = len(inst.tabH) + len(inst.tabV)//2
    if (h_or_v == 0 or not inst.tabV) and inst.tabH:  # If their is no vertical pictures or we choose to pick an horizontal picture and there are horizontal pictures
        alea = randint(0, len(inst.tabH) - 1)
        solution.append(Slide(inst.tabH[alea]))
        inst.tabH.remove(inst.tabH[alea])  # Once we choose a picture, we remove it from the list
    else:
        alea1 = randint(0, len(inst.tabV) - 1)
        alea2 = randint(0, len(inst.tabV) - 1)
        while alea1 == alea2:
            alea2 = randint(0, len(inst.tabV) - 1)
        solution.append(Slide(inst.tabV[alea1], inst.tabV[alea2]))
        if alea1 > alea2:  # We remove both pictures used for the slide
            inst.tabV.remove(inst.tabV[alea1])
            inst.tabV.remove(inst.tabV[alea2])
        else:
            inst.tabV.remove(inst.tabV[alea2])
            inst.tabV.remove(inst.tabV[alea1])

    all_permutation = deepcopy(list(combinations(inst.tabV, 2)))  # Allow to have all possible combinations for vertical pictures without double (there are not (1,2) (2,1) only (1,2)

    while len(solution) < len_solution :  # While there are not enough slides to make a solution
        maxi = -1  
        max_photo = None
        for i in inst.tabH:  # for all horizontal pictures, we will keep the one that maximise the score of the transition
            s = score_transition(solution[len(solution) - 1].key_words, Slide(i).key_words)
            if s > maxi:
                maxi = s
                max_photo = Slide(i)
        for i,j in all_permutation:  # for all permutations possible for vertical pictures, we will keep the one that maximise the score of the transition if its score is better than the horizontal one
            slide = Slide(i, j)
            s = score_transition(solution[len(solution) - 1].key_words, slide.key_words)
            if s > maxi:
                maxi = s
                max_photo = slide
        if max_photo.p2.p_id == -1:
            inst.tabH.remove(max_photo.p1)  # Once we choose a picture, we remove it from the list
        else:
            to_remove = []
            for i,j in all_permutation:  # We remove all permutations where at least one of the chosen pictures appears
                if i == max_photo.p1 or j == max_photo.p1 or i== max_photo.p2 or j == max_photo.p2 :
                    to_remove.append((i,j))
            for i,j in to_remove:
                all_permutation.remove((i,j))
        solution.append(max_photo)
    return solution
    
    
def glouton_opti(inst, n):
    solution = []
    h_or_v = randint(0, 1)
    len_solution = len(inst.tabH) + len(inst.tabV)//2
    if (h_or_v == 0 or not inst.tabV) and inst.tabH:
        alea = randint(0, len(inst.tabH) - 1)
        solution.append(Slide(inst.tabH[alea]))
        inst.tabH.remove(inst.tabH[alea])
    else:
        alea1 = randint(0, len(inst.tabV) - 1)
        alea2 = randint(0, len(inst.tabV) - 1)
        while alea1 == alea2:
            alea2 = randint(0, len(inst.tabV) - 1)
        solution.append(Slide(inst.tabV[alea1], inst.tabV[alea2]))
        if alea1 > alea2:  # Necessary to avoid out of range exception
            inst.tabV.remove(inst.tabV[alea1])
            inst.tabV.remove(inst.tabV[alea2])
        else:
            inst.tabV.remove(inst.tabV[alea2])
            inst.tabV.remove(inst.tabV[alea1])

    all_permutation = list(combinations(inst.tabV, 2))

    while len(solution) < len_solution :
        maxi = -1
        max_photo = None
        for i in sample(inst.tabH, min(len(inst.tabH), n)):  # We will take the best horizontal pictures among "n" of them
            s = score_transition(solution[len(solution) - 1].key_words, Slide(i).key_words)
            if s > maxi:
                maxi = s
                max_photo = Slide(i)
        for i,j in sample(all_permutation, min(len(all_permutation), n)):  # We will take the best permutations of vertical pictures among "n" of them and if its score is better than the horizontal one
            slide = Slide(i, j)
            s = score_transition(solution[len(solution) - 1].key_words, slide.key_words)
            if s > maxi:
                maxi = s
                max_photo = slide
        if max_photo.p2.p_id == -1:
            inst.tabH.remove(max_photo.p1)
        else:
            to_remove = []
            for i,j in all_permutation:
                if i == max_photo.p1 or j == max_photo.p1 or i== max_photo.p2 or j == max_photo.p2 :
                    to_remove.append((i,j))
            for i,j in to_remove:
                all_permutation.remove((i,j))
        solution.append(max_photo)
    return solution
    

#####################################################
#                    EXERCICE 4                        #
#####################################################

def desc_best(sol):
    x = sol.eval
            
    while True:
        print("Best solution BEFORE looking at neighbors =", x)
        
        h_slide = []
        v_slide = []
        for i in range(len(sol.slides)):
            if sol.slides[i].p2.p_id == -1:  # If it is an horizontal picture
                h_slide.append(i)
            else:
                v_slide.append(i)
        
        sol_glouton = x  # Best solution before looking at the neighbors
        alea = randint(0,1)  # 0 for horizontal permuation, 1 for vertical permutation
        
        if alea == 0:  # 1st way of defining neighbors -> permutation of 2 horizontal pictures 
            slides, res = first_neighbors(sol.slides, h_slide, x)
                    
        else:  # 2nd way of defining neighbors -> permutation of 1 of the 2 vertical picture inside a slide with another vertical slide
            slides, res = second_neighbors(sol.slides, v_slide, x)
            
        if res > 0:
            x = res
            sol.slides = slides
            
        print("Better solution AFTER looking at neighbors =", x)
        print()
        
        if x == sol_glouton:
            break
    return x

    
def first_neighbors(s, h, x):
    to_permute = list(combinations(h, 2))
    for i,j in to_permute:
        slides = deepcopy(s)
        t = slides[i]
        slides[i] = slides[j]
        slides[j] = t
        res = evaluate(slides)
                
        if res > x :  # We found a better solution we stop here
            return slides, res
            
    return None, -1

def second_neighbors(s, v, x):
    to_permute = list(combinations(v, 2))
    for i,j in to_permute:
        slides = deepcopy(s)  # We permute 1st picture of 1st slide with 2nd picture of 2nd slide
        t = slides[i].p1
        slides[i] = Slide(slides[i].p2, slides[j].p1)
        slides[j] = Slide(slides[j].p2, t)
        res = evaluate(slides)
        
        if res > x :  # We found a better solution we stop here
            return slides, res
            
        slides = deepcopy(s)  # We permute 1st picture of 1st slide with 1st picture of seconde slide
        t = slides[i].p1
        slides[i] = Slide(slides[j].p2, slides[i].p2)
        slides[j] = Slide(slides[j].p1, t)
        res = evaluate(slides)
        
        if res > x :  # We found a better solution we stop here
            return slides, res
    
    return None, -1
    
    
def algo_g(nb_species, nb_generations, inst, n):
    populations = create_species(inst, n, nb_species)
    for i in range(nb_generations):
        print("Generation", i, ":")
        populations = selection_mu_lambda(populations, 0.8, int(len(populations)*0.2))
        creation = create_species(inst, n, int(nb_species * 0.2))
        for j in creation:
            populations.append(j)
        for k in populations:
            if random() > 0.5:
                mutate(k)
            print("Fitness of specie", k.name, "is :", k.eval)
        print()

    return max(populations, key = lambda x: x.eval)
    
    
def create_species(inst, n, nb):
    species = []
    for i in range(nb):
        instance = deepcopy(inst)
        s = Specie(glouton_opti(instance, n))
        s.eval = evaluate(s.slides)
        s.name = str(i)
        species.append(s)
    return species
        

def selection_mu_lambda(s, p, l):
    new_species = []
    pourcentage = int(p * len(s))
    s = sorted(s, key=lambda x: x.eval, reverse=True)[0:l]

    for i in s:
        new_species.append(i)
        
    while len(new_species) < pourcentage:
        new_species.append(deepcopy(s[randint(0, len(s) - 1)]))
        
    return new_species
    
    
def mutate(s):
    h_slide = []
    v_slide = []
    for i in range(len(s.slides)):
        if s.slides[i].p2.p_id == -1:  # If it is an horizontal picture
            h_slide.append(i)
        else:
            v_slide.append(i)
            
    alea = randint(0,1)  # 0 for horizontal permuation, 1 for vertical permutation
        
    if alea == 0:  # 1st way of defining neighbors -> permutation of 2 horizontal pictures 
        l = list(combinations(h_slide, 2))
        rand = l[randint(0,len(l)-1)]
        t = s.slides[rand[0]]
        s.slides[rand[0]] = s.slides[rand[1]]
        s.slides[rand[1]] = t
                
    else:  # 2nd way of defining neighbors -> permutation of 1 of the 2 vertical picture inside a slide with another vertical slide
        alea = randint(0,1)
        l = list(combinations(v_slide, 2))
        rand = l[randint(0,len(l)-1)]
        if alea == 0:
            t = s.slides[rand[0]].p1
            s.slides[rand[0]] = Slide(s.slides[rand[0]].p2, s.slides[rand[1]].p1)
            s.slides[rand[1]] = Slide(s.slides[rand[1]].p2, t)
        else:
            t = s.slides[rand[0]].p1
            s.slides[rand[0]] = Slide(s.slides[rand[1]].p2, s.slides[rand[0]].p2)
            s.slides[rand[1]] = Slide(s.slides[rand[1]].p1, t)

    s.eval = evaluate(s.slides)
    s.name = s.name + str(rand[0]) + str(rand[1])
    
    


#####################################################
#                        MAIN                        #
#####################################################

def main(argv):
    f = "Inputs/c_memorable_moments.txt"
    #f = "Inputs\\b_lovely_landscapes.txt"
    #f = "Inputs\\a_example.txt"
    instance = select_p_percent(f, 20)
    #sol = Solution(instance, h_before_v, 0, "H_puis_V.sol")
    #sol = Solution(instance, glouton, 0, "glouton.sol")
    #sol = Solution(instance, glouton_opti, 5, "glouton_opt.sol")
    #sol.eval = evaluate(sol.slides)
    #print("Évaluation de la solution de", f, ":", sol.eval)
    #res = desc_best(sol)
    #print("Meilleur score apres descente stochastique :", res)
    b = algo_g(100, 200, instance, 10)
    print(b)
    #sol.output()
    



if __name__ == "__main__":
    main(sys.argv[1:])
