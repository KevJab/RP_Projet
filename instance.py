from random import *

class Photo:
    def __init__(self, ori, key_words, p_id):
        self.ori = ori  # Orientation of the picture (H or V)
        self.key_words = set(key_words)  # List of key words
        self.p_id = p_id  # Picture ID (unique)

    def __lt__(self, other):  # Needed for sort
        return self.p_id < other.p_id

    def __eq__(self, other):
        return self.p_id == other.p_id

    def __gt__(self, other):  # Just in case
        return self.p_id > other.p_id


class Instance:
    def __init__(self, photosH = [], photosV = []):
        self.tabH = photosH  # A list of horizontal pictures
        self.tabV = photosV  # A list of vertical pictures
        self.nb_photos = len(photosH) + len(photosV)

    def add_photo(self, p):  # Adds a picture, and re-sorts both lists by p_id
        if p.ori == "H":
            self.tabH.append(p)
        else:
            self.tabV.append(p)

    def sort(self):
        self.tabH.sort()
        self.tabV.sort()


class Slide:
    def __init__(self, p1, p2 = Photo("", [], -1)):
        self.p1 = p1  # The first picture in the slide
        self.p2 = p2  # The 2nd vertical picture, or -1 of the first one was horizontal
        if self.p2.p_id == -1:
            self.key_words = set(p1.key_words)  # A set made of the first picture's keywords
        else:
            self.key_words = set(p1.key_words).union(set(p2.key_words))  # A set of the union of both pictures' keywords

    def __str__(self):  # Redefining str(Slide) for easier way of writing
        if self.p2.p_id == -1:
            return str(self.p1.p_id)
        return str(self.p1.p_id) + " " + str(self.p2.p_id)


class Solution:
    def __init__(self, instance, func, n, out_file="output.sol"):
        self.instance = instance  # The instance to solve
        self.func = func  # The slide-sorting function
        self.out_file = out_file  # The file to write (has to be .sol)
        self.slides = []  # The list of slides
        self.arg = n  # Arg for self.func
        self.find_solution()  # Finds the solution according to self.func
        self.eval = 0  # Score of the solution
        #self.output()

    def find_solution(self):
        if self.arg == 0:
            self.slides = self.func(self.instance)
        else:
            self.slides = self.func(self.instance, self.arg)

    def output(self):  # Writes the solution in the output file
        sol = open(self.out_file, 'w+')

        sol.write(str(len(self.slides)) + "\n")
        for slide in self.slides:
            sol.write(str(slide) + "\n")


class Specie:
    def __init__(self, s):
        self.slides = s
        self.eval = 0
        self.name = ""
    
    def __str__(self):
        return "My name is " + self.name + " and my score is " + str(self.eval)
