#########################################################################
#########################################################################
# In the name of Allah                                      #############
# GROUP 5                                                   #############
# NeginLava - HengameNesarizadeh - RoozbehIzadian - RezaGhanbari ########
#########################################################################
# ENVIRONMENT INFO                                          #############
# kali linux distribution                                   #############
# pycharm 2016.1 IDE                                        #############
# Written and tested using Python 2.5.                      #############
# prerequisite python packages:  (numpy, scipy)             #############
# USE pip install numpy and pip install scipy for installation###########
#########################################################################
#########################################################################
# All documentation files have been attached in main folder #############
# Generates a random web link structure, and finds the      #############
# corresponding PageRank vector.  The number of inbound     #############
# links for each page is controlled by a power law          #############
# distribution.                                             #############
# WE USE S PARAMETER (S=.085) LIKE WHAT IS IN MAIN PAGERANK ARTICLE  ####
#########################################################################
# This code should work for up to a few million pages on a  #############
# modest machine.                                           #############
#########################################################################


import numpy
import random


class Web:
    def __init__(self, number):
        self.size = number
        self.in_links = {}
        self.number_out_links = {}
        self.dangling_pages = {}
        for item in xrange(number):  # we use xrange() instead of range() for using low memory
            self.in_links[item] = []
            self.number_out_links[item] = 0
            self.dangling_pages[item] = True


def pareto(number, power=2.0):
    '''This function returns a Pareto distribution that truncated at l = n
    probability mass function is p(l) proportional to 1/l^power.'''
    trunc = number + 1
    while trunc > number:
        trunc = numpy.random.zipf(power)

    return trunc


def randomizedWeb(number=1000, power=2.0):
    '''web object with 1000 pages,each page k is linked to by L_k random other pages.'''
    graph = Web(number)
    for item in xrange(number):
        linked = pareto(number+1, power) - 1
        values = random.sample(xrange(number),linked)

        graph.in_links[item] = values
        for iterate in values:
            if graph.number_out_links[iterate] == 0:
                graph.dangling_pages.pop(iterate)

            graph.number_out_links[iterate] +=1

    return graph


def step(graph, p, s=0.85):

    n = graph.size
    v = numpy.matrix(numpy.zeros((n, 1)))
    inner_product = sum([p[j] for j in graph.dangling_pages.keys()])
    for j in xrange(n):
        v[j] = s * sum([p[k] / g.number_out_links[k]
                        for k in graph.in_links[j]]) + s * inner_product / n + (1 - s) / n

    return v / numpy.sum(v)


def pagerank(graph, s=0.85, tolerance=0.00001):

    n = graph.size
    p = numpy.matrix(numpy.ones((n, 1)))/n
    iteration = 1
    change = 2
    while change > tolerance:
        print "Iteration: %s" % iteration
        new_p = step(graph, p, s)
        change = numpy.sum(numpy.abs(p-new_p))
        print "Change of new_p is : %s \n\n" % change
        p = new_p
        iteration += 1
    return p


g = randomizedWeb(10000, 2.0)
pr = pagerank(g, 0.85, 0.0001)




