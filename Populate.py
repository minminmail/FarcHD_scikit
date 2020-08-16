"""
/***********************************************************************

	This file is part of KEEL-software, the Data Mining tool for regression,
	classification, clustering, pattern mining and so on.

	Copyright (C) 2004-2010

	F. Herrera (herrera@decsai.ugr.es)
    L. Sánchez (luciano@uniovi.es)
    J. Alcalá-Fdez (jalcala@decsai.ugr.es)
    S. García (sglopez@ujaen.es)
    A. Fernández (alberto.fernandez@ujaen.es)
    J. Luengo (julianlm@decsai.ugr.es)

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see http://www.gnu.org/licenses/

**********************************************************************/
"""
from Individual import Individual
from DataBase import DataBase
from RuleBase import RuleBase
from MyDataSet import MyDataSet
from random import randrange


class Populate:

    population_list =[]

    alpha:float = None
    w1:float = None
    l_value = None
    lini = None

    n_variables  = None
    pop_size  = None
    maxTrials  = None
    ntrials = None
    bits_gen = None
    best_fitness:float = None
    best_accuracy:float = None
    selected_array =[]

    train_mydataset = None
    data_base = None
    rule_base  = None

    """
    * Maximization
    * @ param a int first number
    * @ param b int second number
    """
    def better(self,value_a, value_b):
        if value_a > value_b:
            return True
        else:
            return False
    """"
    None attribute will be initialized.
    """
    def __init__(self):
        print("Init empty Populate ")
    """
    * @param train Training dataset
    * @param dataBase Data Base
    * @param ruleBase Rule set
    * @param size Population size
    * @param BITS_GEN Bits per gen
    * @param maxTrials Maximum number of evaluacions
    * @param alpha Parameter alpha
    
    """
    def init_with_multiple_parameters(self, train_mydataset, data_base, ruleBase, size, bits_gen, maxtrials, alpha):
        self.data_base = data_base
        self.train_mydataset = train_mydataset
        self.rule_base = ruleBase
        self.bits_gen = bits_gen

        self.n_variables = data_base.num_variables()
        self.pop_size = size
        self.alpha = alpha
        self.maxtrials = maxtrials
        self.lini = ((data_base.get_nlabels_real() * bits_gen) + ruleBase.get_size()) / 4.0
        self.l_value = self.lini
        self.w1 = self.alpha * ruleBase.get_size()

        self.population = []
        self.selected_array = [0 for x in range (self.pop_size)]

        """
        * Run the CHC algorithm (Stage 3) 
        """
    def generation(self):
        self.init()
        self.evaluate(0)

        while True:
            self.selection()
            self.cross_over()
            self.evaluate(self.pop_size)
            self.elitist()
            if not self.has_new():
                self.l_value =  self.l_value - 1
                if self.l_value < 0.0:
                    self.restart()
            if self.nTrials >= self.maxTrials:
                break

    def init(self):
        ind = Individual()
        ind.init_with_parameter(self.rule_base, self.data_base, self.w1)
        ind.reset()
        self.population_list.append(ind)
        for i in range(1, self.pop_size):
            ind = Individual()
            ind.init_with_parameter(self.rule_base, self.data_base, self.w1)
            ind.random_values()
            self.population_list.append(ind)

        self.best_fitness = 0.0
        self.ntrials = 0

    def evaluate(self,pos):
        for i in range(pos,len(self.population_list)):
            self.population_list[i].evaluate()
        self.ntrials = self.ntrials + (len(self.population_list) - pos)


    def selection(self):

        aux =None
        random = None

        for i in range(0,self.pop_size):
            self.selected_array[i] = i

        for i in range(0,self.pop_size):
            random = randrange(0, self.pop_size)
            aux = self.selected_array[random]
            self.selected_array[random] = self.selected_array[i]
            self.selected_array[i] = aux

    def xpc_blx(self,d_value, son1_individual, son2_individual):
        son1_individual.xpc_blx(son2_individual, d_value)


    def hux(self, son1_individual, son2_individual):
        son1_individual.hux(son2_individual)

    def cross_over(self):

        dist = None
        dad_individual = None
        mom_individual = None
        son1_individual = None
        son2_individual = None

        for i in range( 0, self.pop_size, 2) :
            dad_individual = self.population_list[self.selected_array[i]]
            mom_individual = self.population_list[self.selected_array[i + 1]]
            dist = float(dad_individual.dist_hamming(mom_individual, self.bits_gen))
            dist /= 2.0

            if dist > self.l_value:
                son1_individual = dad_individual.clone()
                son2_individual = mom_individual.clone()

                self.xpc_blx(1.0, son1_individual, son2_individual)
                self.hux(son1_individual, son2_individual)

                son1_individual.onNew()
                son2_individual.onNew()

                self.Population.add(son1_individual)
                self.Population.add(son2_individual)


    def elitist(self):
        # need to know which order to sort ,how to sort, if the sort will be saved
        self.population_list.sort()
        while len(self.population_list) > self.pop_size:
            self.population.remove(self.pop_size)
            self.best_fitness = self.population_list[0].getFitness()

    def has_new(self):

        state: bool = None
        ind:Individual = None
        state = False

        for i in range (0, self.pop_size):
            ind = self.population_list[i]
            if ind.is_new():
                ind.off_new()
                state = True

        return state


    def restart(self):

        i = None
        dist = None
        ind = None
        self.w1 = 0.0

        self.population_list.sort()
        ind = self.population_list[0].clone()
        ind.set_w1(self.w1)

        self.population_list.clear()
        self.population_list.append(ind)

        for i in range (1,self.pop_size):
            ind = Individual()
            ind.init_with_parameter(self.rule_base,self.data_base, self.w1)
            ind.randomValues()
            self.population_list.append(ind)

        self.evaluate(0)
        self.l_value = self.lini

    """
    * <p>
    * Return the best individual in the population 
    * </p>

    """
    def get_best_RB(self):

        rule_base = None

        self.population_list.sort()
        rule_base = self.population_list[0].generateRB()

        return rule_base
