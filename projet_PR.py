from instance import *
from random import *
from itertools import *
from time import time
from copy import deepcopy
import sys
import matplotlib.pyplot as plt


#####################################################
#                    EXERCICE 1                     #
#####################################################

def select_p_percent(filename, percent):
    f = open(filename, 'r')
    lines = f.readlines()
    nb_photos = len(lines) * percent / 100  # Number of lines we will read

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

def output(solution, out_file):  # Writes the solution in the output file
    sol = open(out_file, 'w+')

    sol.write(str(len(solution)) + "\n")
    for slide in solution:
        sol.write(str(slide) + "\n")


#####################################################
#                    EXERCICE 3                     #
#####################################################

def glouton(inst, max_time = -1):
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

    a = time()
    b = time()

    while len(solution) < len_solution :  # While there are not enough slides to make a solution
        if b-a > max_time and max_time > 0:
            break
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
        b = time()
    return solution


def glouton_opti(inst, n, max_time = -1):
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

    a = time()
    b = time()

    while len(solution) < len_solution :
        if b-a > max_time and max_time > 0:
            break
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
        b = time()
    return solution


#####################################################
#                    EXERCICE 4                     #
#####################################################

def desc_best(sol, max_time = -1):
    x = evaluate(sol)
    a = time()
    b = time()
    while True:
        if b-a > max_time and max_time > 0:
            break
        print("Best solution BEFORE looking at neighbors =", x)

        h_slide = []
        v_slide = []
        for i in range(len(sol)):
            if sol[i].p2.p_id == -1:  # If it is an horizontal picture
                h_slide.append(i)
            else:
                v_slide.append(i)

        sol_glouton = x  # Best solution before looking at the neighbors
        alea = randint(0,1)  # 0 for horizontal permuation, 1 for vertical permutation

        if alea == 0:  # 1st way of defining neighbors -> permutation of 2 horizontal pictures
            slides, res = first_neighbors(sol, h_slide, x)

        else:  # 2nd way of defining neighbors -> permutation of 1 of the 2 vertical picture inside a slide with another vertical slide
            slides, res = second_neighbors(sol, v_slide, x)

        if res > 0:
            x = res
            sol = slides
        b = time()
        print("Better solution AFTER looking at neighbors =", x)
        print()

        if x == sol_glouton:
            break
    return x, sol


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


def algo_g(nb_species, nb_generations, inst, n, max_time = -1, mutation = 1):
    populations = create_species(inst, n, nb_species)  # Initialise the population
    print("Population initialized")
    a = time()
    b = time()
    for i in range(nb_generations):  # For each generation
        if max_time > 0 and b - a > max_time:
            break
        print("Generation", i, ":")
        populations = selection_mu_lambda(populations, 0.8, int(len(populations)*0.2))  # Select 80% of species among the bests of them
        creation = create_species(inst, n, int(nb_species * 0.2))  # Fill the missing 20% with totally new species
        for j in creation:
            populations.append(j)
        for k in populations:
            if random() > 0.5:  # Each specie has a 50% probability to mutate
                if mutation == 1 :
                    mutate(k)
                elif mutation == 2:
                    mutate2(k)
            print("Fitness of specie", k.name, "is :", k.eval)
        b = time()
        print()

    return max(populations, key = lambda x: x.eval)  # Return the specie with the highiest fitness


def create_species(inst, n, nb):
    species = []
    for i in range(nb):  # For each specie with create
        instance = deepcopy(inst)
        s = Specie(glouton_opti(instance, n))  # we calculate his solution
        s.eval = evaluate(s.slides)  # Then evaluate this solution
        s.name = str(i)  # Give him a name
        species.append(s)  # Add it to the list of new species
    return species


def selection_mu_lambda(s, p, l):
    new_species = []
    pourcentage = int(p * len(s))  # Number of species we have to select
    s = sorted(s, key=lambda x: x.eval, reverse=True)[0:l]  # We only keep the l better species

    for i in s:  # We add them all, once
        new_species.append(i)

    while len(new_species) < pourcentage:  # Then while we didn't select enough we select new specie
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

    if alea == 0:  # permutation of 2 horizontal pictures
        l = list(combinations(h_slide, 2))  # All possible permutations
        rand = l[randint(0,len(l)-1)]  # We choose one of them randomly
        t = s.slides[rand[0]]  # Then we do the permutation
        s.slides[rand[0]] = s.slides[rand[1]]
        s.slides[rand[1]] = t

    else:  # permutation of 1 of the 2 vertical picture inside a slide with another vertical slide
        alea = randint(0,1)  # Allow us to decide if we switch the 1st picture of the first slide with the 1st or with the second picture of the second slide
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

    s.eval = evaluate(s.slides)  # We recalculate the score of the presentation of our specie
    s.name = s.name + str(rand[0]) + str(rand[1])  # We change his name


#####################################################
#                    EXERCICE 5                    #
#####################################################
def solveurPL(vignettes):
    # Range of plants and warehouses
    m = Model("mogplex")

    # declaration variables de decision
    x = []
    z = []

    for i in range(0,len(vignettes)):
        for j in range(0,len(vignettes)):
            # xi correspond a une transition entre vi et vj
            x.append(m.addVar(vtype=GRB.BINARY, lb=0, name="x%d" % (i*len(vignettes)+j)))

    for i in range(0,len(vignettes)):
        for j in range(0,len(vignettes)):
            #Variable zi : elimination des sous tours par les flots
            z.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="x%d" % (i*len(vignettes)+j)))

    m.update()

    obj = LinExpr();
    obj =0

    #Un seul arc sortant d'un sommet
    for i in range(0,len(vignettes)):
        m.addConstr(quicksum(x[i*len(vignettes)+j] for j in range(0,len(vignettes)))==1)
        m.addConstr(quicksum(x[j*len(vignettes)+i] for j in range(0,len(vignettes)))==1)

    #Contrainte du premier sommet
    m.addConstr(quicksum(z[j] for j in range(1,len(vignettes))) == len(vignettes)-1)

    for i in range(1,len(vignettes)):
        i1 = np.arange(0,len(vignettes))
        i1=np.delete(i1,i)
        i1=np.delete(i1,0)
        i2 = np.arange(0,len(vignettes))
        i2=np.delete(i2,i)
        m.addConstr(quicksum([z[i*len(vignettes)+j] for j in i1])+1 == quicksum([z[j*len(vignettes)+i] for j in i2]))

    for i in range(0,len(vignettes)):
        for j in range(0,len(vignettes)):
            if(j != i and j != 0):
                m.addConstr(z[i*len(vignettes)+j]+z[j*len(vignettes)+i] <= (len(vignettes)-1)*(x[i*len(vignettes)+j]+x[j*len(vignettes)+i]))


    for i in range(0,len(vignettes)):
        for j in range(0,len(vignettes)):
            if(j != i and j != 0):
                m.addConstr(z[i*len(vignettes)+j]>=0)

    m.update()

    obj = LinExpr();
    obj =0
    for i in range(0,len(vignettes)):
        for j in range(0,len(vignettes)):
            obj+= score_transition(vignettes[i].key_words,vignettes[j].key_words)*x[i*len(vignettes)+j]

    m.setObjective(obj,GRB.MAXIMIZE)
    m.optimize()

    print("")
    print('Solution optimale:')
    print("")
    return x


#####################################################
#                    EXERCICE 7                     #
#####################################################

def graph(inst, n):
    time = [300, 1200, 2100]
    score = {}
    for i in time:
        print("Debut de la phase avec temps =", i)
        score[i] = []
        score[i].append(evaluate(glouton(deepcopy(inst), i)))
        print("Glouton OK", score[i][0])
        a = glouton_opti(deepcopy(inst), n, i)
        score[i].append(evaluate(a))
        print("Glouton opti OK", score[i][1])
        score[i].append(desc_best(a, i)[0])
        print("Descente stochastique OK", score[i][2])
        score[i].append(algo_g(30, 1000, deepcopy(inst), n, i).eval)
        print("Algo genetique OK", score[i][3])
    print(score)


#####################################################
#                    EXERCICE 8                     #
#####################################################

def mutate2(s):
    s.slides = desc_best(s.slides)[1]
    s.eval = evaluate(s.slides)  # We recalculate the score of the presentation of our specie
    s.name = s.name + str(randint(0, 100))  # We change his name


#####################################################
#                        MAIN                        #
#####################################################

def main(argv):
    f = "Inputs\\c_memorable_moments.txt"
    #f = "Inputs\\b_lovely_landscapes.txt"
    #f = "Inputs\\a_example.txt"
    instance = select_p_percent(f, 40)

    #graph(instance, 100)
    #solveurPL(inst.tabH)

    """
    #GLOUTON
    sol = glouton(instance)
    output(sol, 'glouton.sol')
    """

    """
    #GLOUTON OPTIMISE
    sol = glouton_opti(instance, 100)
    output(sol, 'glouton_opt.sol')
    """

    """
    #DESCENTE STOCHASTIQUE
    g = glouton_opti(instance, 100)
    sol = desc_best(g)[1]
    output(sol, 'desc.sol')
    """

    """
    #ALGORITHME GENETIQUE
    sol = algo_g(50, 20, instance, 100).slides
    output(sol, 'algo_g.sol')
    """


    #ALGORITHME GENETIQUE + DESCENTE STOCHASTIQUE
    s = algo_g(10, 20, instance, 100, max_time = 300, mutation = 2)
    sol = s.slides
    print(s.eval)
    output(sol, 'algo_g_desc.sol')





if __name__ == "__main__":
    main(sys.argv[1:])
