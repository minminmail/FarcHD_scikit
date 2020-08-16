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
from RuleBase import RuleBase
import numpy as np
import math
import random


class Individual:

    gene_array: float = []
    geneR_array: int = []
    fitness: float = None
    accuracy: float = None
    w1_value: float = None

    n_e = None
    ngenes = None
    rule_base: RuleBase = None

    def __init__(self):
        print("Individual init")

    """
    * @param ruleBase Rule set
    * @param dataBase Database
    * @param w1 Weight for the fitness function
    """

    def init_with_parameter(self, rule_base, database, w1_value):
        self.rule_base = rule_base
        self.w1_value = w1_value
        self.fitness = float('-inf')
        self.accuracy = 0.0
        self.n_e = 0
        self.ngenes = database.get_nlabels_real()
        rules_number = self.rule_base.get_size()
        if self.ngenes > 0:
            self.gene_array = [0.0 for x in range(self.ngenes)]
        self.geneR_array = [0 for x in range(rules_number)]

    """
    * @return A copy of the individual
    """

    def clone(self):
        ind = Individual()

        ind.rule_base = self.rule_base
        ind.w1_value = self.w1_value
        ind.fitness = self.fitness
        ind.accuracy = self.accuracy
        ind.n_e = self.n_e
        ind.ngenes = self.ngenes

        if self.ngenes > 0:
            ind.gene = [0.0 for x in range(self.ngenes)]
            for j in range(0, self.ngenes):
                ind.gene_array[j] = self.gene_array[j]

        ind.geneR_array = [0 for x in range(len(self.geneR_array))]
        for j in range(0, len(self.geneR_array.length)):
            ind.geneR_array[j] = self.geneR_array[j]

        return ind

    """
     * Resets the gene with the same value.
    """

    def reset(self):
        if self.ngenes > 0:
            for i in range(0, self.ngenes):
                self.gene_array[i] = 0.5
        for i in range(0, len(self.geneR_array)):
            self.geneR_array[i] = 1

    """
    * Initialization of the individual with random values.
    """

    def random_values(self):
        if self.ngenes > 0:
            for i in range(0, self.ngenes):
                self.gene_array[i] = np.random.rand()

        for i in range(0, len(self.gene_array)):
            if np.random.rand() < 0.5:
                self.gene_array[i] = 0
            else:
                self.gene_array[i] = 1

    """
       * It returns the number of rules in the rule base
       * @return int Rule base's size
    """

    def size(self):
        return len(self.gene_array)

    """
         * Returns the number of genes selected.
     * @return the number of genes selected.
     */
    """

    def get_nselected(self):
        count = 0
        for i in range(0, len(self.geneR_array)):
            if self.geneR_array[i] > 0:
                count = count + 1
        return count

    """
    * Function to return if this individual is new in the population
    * @return boolean true = it is-, false = it isn't
    """

    def is_new(self):
        return self.n_e == 1

    """
     * Modifies the new flag to true. 
    """

    def on_new(self):
        self.n_e = 1

    """
     * Modifies the new flag to false. 
    """

    def off_new(self):
        self.n_e = 0

    """
     * Sets the value of w1 with the given argument. 
     * @param value value given to set w1.
    """

    def set_w1(self, value):
        self.w1_value = value

    """

   * Function to return the accuracy of the individual

   * @return double The accuracy of the individual
    """

    def get_accuracy(self):
        return self.accuracy

    """
    * Function to return the fitness of the individual
    * @return double The fitness of the individual
    """

    def get_fitness(self):
        return self.fitness

    """
    /*************************************************************************/
    /* Translations between string representation and floating point vectors */
    /*************************************************************************/
    """

    def string_rep(self, indiv, bits_gen):
        i = 0
        j = 0
        pos = 0
        length = 0
        count = 0
        n_value = 0
        last = ''
        incremento = 0.0

        indiv1_str_array = []
        indiv2_str_array = []
        aux_str_array = []

        length = self.ngenes * bits_gen

        indiv1_str_array = ['' for x in range(length)]
        indiv2_str_array = ['' for x in range(length)]
        aux_str_array = ['' for x in range(length)]

        incremento = 1.0 / (math.pow(2.0, float(bits_gen)) - 1.0)

        pos = 0
        for i in range(0, self.ngenes):
            n_value = int((self.gene[i] / incremento + 0.5))

            for j in range(bits_gen - 1, 0, -1):
                aux_str_array[j] = str('0' + (n & 1));
                n_value >>= 1

            last = '0'
            for j in range(0, bits_gen):
                j += 1
                pos += 1
                if aux_str_array[j] != last:
                    indiv1_str_array[pos] = str('0' + 1)
                else:
                    indiv1_str_array[pos] = str('0' + 0)
                last = aux_str_array[j]
        pos = 0

        for i in range(0, self.ngenes):
            if incremento != 0:
                n_value = int(indiv.gene_array[i] / incremento + 0.5)
            else:
                print("Exception happened, the incremento is 0 !")

            for j in range(bits_gen - 1, 0, -1):
                aux_str_array[j] = str('0' + (n & 1))
                n_value >>= 1

            last = '0'
            for j in range(0, bits_gen):
                j += 1
                pos += 1
                if aux_str_array[j] != last:
                    indiv2_str_array[pos] = str('0' + 1)
                else:
                    indiv2_str_array[pos] = str('0' + 0)
                last = aux_str_array[j]

        count = 0
        for i in range(0, length):
            if indiv1_str_array[i] != indiv2_str_array[i]:
                count += 1

        return count

    """
             /**
             * Computes the Hamming distance with the Individual given as a argument.
             * In case a transformation from float representation to string is needed, the argument BITS_GEN will guide the process.
             * @param ind Individual given to compute the distance.
             * @param BITS_GEN Number of bits to guide the transformation of representation.
             * @return Hamming distance with the Individual given.
             */
    """

    def dist_hamming(self, ind, bits_gen):
        count = 0
        for i in range(0, len(self.geneR_array)):
            if self.geneR_array[i] != ind.geneR_array[i]:
                count += 1
        if self.nGenes > 0:
            count += self.string_rep(ind, bits_gen)
        return count

    """
      /**
     * Crosses the individuals using the HUX operator.
     * Exactly half of the different bits are flipped.
     * The results are stored in each Individual object, the method caller and the argument.
     * @param indiv Individual to cross with.
     */
    """

    def hux(self, indiv):
        i = 0
        dist = 0
        random_value = 0
        aux = 0
        npos = 0
        position_array = [0 for x in range(len(self.geneR_array))]
        dist = 0

        for i in range(0, len(self.geneR_array)):
            if self.geneR_array[i] != indiv.geneR[i]:
                position_array[dist] = i
                dist += 1

        npos = dist / 2

        for i in range(0, npos):
            random_value = random.randit(0, dist)

            aux = self.geneR_array[position_array[random]]
            self.geneR_array[position_array[random]] = indiv.geneR[position_array[random]]
            indiv.geneR_array[position_array[random]] = aux

            dist -= 1

            aux = position_array[dist]
            position_array[dist] = position_array[random];
            position_array[random] = aux

    """
     /**
     * Crosses the individuals using the BLX operator.
     * The results are stored in each Individual object, the method caller and the argument.
     * @param indiv Individual to cross with.
     * @param d proportion of the diference of each gene that BLX will allow to exceed.
     */
    """

    def xpc_blx(self, indiv, d_value):
        i_value = 0.0
        a1 = 0.0
        c1 = 0.0

        for i in range(0, self.ngenes):
            i_value = d_value * math.abs(self.gene_array[i] - indiv.gene_array[i])
            a1 = self.gene_array[i] - i_value

            if a1 < 0.0:
                a1 = 0.0
            c1 = self.gene_array[i] + i_value
            if c1 > 1.0:
                c1 = 1.0
            self.gene_array[i] = a1 + random.rand() * (c1 - a1)
            a1 = indiv.gene[i] - i_value
            if a1 < 0.0:
                a1 = 0.0
            c1 = indiv.gene_array[i] + i_value
            if c1 > 1.0:
                c1 = 1.0
            indiv.gene_array[i] = a1 + random.rand() * (c1 - a1)

    """
       * Generates the Rule Base with adjusted to the optimization done.
       * @return RuleBase The whole FARCHD rule set
    """

    def generate_rb(self):
        i = 0
        best_rule = 0
        rule_base = self.rule_base.clone()

        rule_base.evaluate(self.gene, self.geneR)
        rule_base.setDefaultRule()

        for i in range(len(self.gene_array) - 1, 0, -1):
            if self.gene_array[i] < 1:
                rule_base.remove(i)

        return rule_base

    """
    * Evaluate this individual (fitness function)
    """

    def evaluate(self):
        self.rule_base.evaluate_with_two_parameters(self.gene_array, self.geneR_array)
        self.accuracy = self.rule_base.get_accuracy()

        self.fitness = self.accuracy - (self.w1_value / (self.rule_base.get_size()- self.get_nselected() + 1.0)) - (
                    5.0 * self.rule_base.get_uncover()) - (5.0 * self.rule_base.has_class_uncovered(self.geneR_array))

    def compare_to(self, a_object):
        if Individual(a_object).fitness < self.fitness:
            return -1

        if Individual(a_object).fitness > self.fitness:
            return 1
        return 0

    """
       * Function to return if this individual is new in the population
       * @return boolean true = it is-, false = it isn't
    """

    def is_new(self):
        return self.n_e == 1

    """
     Modifies the new flag to false. 
    """

    def off_new(self):
        self.n_e = 0

    """
    /**
     * Sets the value of w1 with the given argument. 
     * @param value value given to set w1.
     */
    """

    def set_w1(self, value):
        self.w1_value = value
