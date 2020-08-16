# /***********************************************************************
#
# 	This file is part of KEEL-software, the Data Mining tool for regression,
# 	classification, clustering, pattern mining and so on.
#
# 	Copyright (C) 2004-2010
#
# 	F. Herrera (herrera@decsai.ugr.es)
#     L. S谩nchez (luciano@uniovi.es)
#     J. Alcal谩-Fdez (jalcala@decsai.ugr.es)
#     S. Garc铆a (sglopez@ujaen.es)
#     A. Fern谩ndez (alberto.fernandez@ujaen.es)
#     J. Luengo (julianlm@decsai.ugr.es)
#
# 	This program is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU General Public License as published by
# 	the Free Software Foundation, either version 3 of the License, or
# 	(at your option) any later version.
#
# 	This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# 	GNU General Public License for more details.
#
# 	You should have received a copy of the GNU General Public License
# 	along with this program.  If not, see http://www.gnu.org/licenses/
#
# **********************************************************************/
from Fuzzy import Fuzzy
from DataBase import DataBase
from Rule import Rule
import Fuzzy_Chi
from data_row import data_row
from MyDataSet import MyDataSet
from ExampleWeight import ExampleWeight
import gc


# * This class contains the representation of a Rule Set
# *
# * @author Written by Alberto Fern谩ndez (University of Granada) 29/10/2007
# * @version 1.0
# * @since JDK1.5

class RuleBase:
    rule_base_array = []
    train_myDataSet = None
    # added by rui for negative rule
    granularity_rule_Base = []
    granularity_prune_rule_base = []
    data_base = DataBase()
    n_variables = None
    n_labels = None
    ruleWeight = None
    inferenceType = None
    compatibilityType = None
    names = []
    classes = []
    data_row_array = []
    fitness = None
    k_value = None
    default_rule = None
    nuncover = None
    nuncover_class_array = []

    # /**
    #  * Rule Base Constructor
    #  * @param dataBase DataBase the Data Base containing the fuzzy partitions
    #  * @param inferenceType int the inference type for the FRM
    #  * @param compatibilityType int the compatibility type for the t-norm
    #  * @param ruleWeight int the rule weight heuristic
    #  * @param names String[] the names for the features of the problem
    #  * @param classes String[] the labels for the class attributes
    #  */
    def __init__(self):
        print("This is the empty init of RuleBase() ......")

    def init_with_five_parameters(self, data_base_pass, train_myDataset_pass, K_int, inferenceType_pass):
        self.rule_base_array = []
        self.data_base = data_base_pass
        self.train_myDataSet = train_myDataset_pass
        self.n_variables = self.data_base.num_variables()
        self.fitness = 0.0
        self.k_value = K_int
        self.inferenceType = inferenceType_pass
        self.default_rule = -1
        self.nuncover = 0
        self.nuncover_class_array = [0 for x in range(self.train_myDataSet.get_nclasses())]

    def set_six_parameter_init(self, data_base, inferenceType, compatibilityType, ruleWeight, names, classes):
        print("RuleBase init begin...")
        self.rule_base_array = []
        self.granularity_rule_Base = []
        # added by rui for negative rule
        self.negative_rule_base_array = []
        self.granularity_prune_rule_base = []
        self.data_base = data_base
        self.n_variables = data_base.numVariables()
        self.n_labels = data_base.numLabels()
        self.inferenceType = inferenceType
        self.compatibilityType = compatibilityType
        self.ruleWeight = ruleWeight
        self.names = names
        self.classes = classes
        self.data_row_array = []
        self.granularity_data_row_array = []
        print("set_six_parameter_init the length of classes is" + str(len(self.classes)))

    # * It checks if a specific rule is already in the rule base
    # * @param r Rule the rule for comparison
    # * @return boolean true if the rule is already in the rule base, false in other case

    def duplicated(self, rule):
        i = 0
        found = False
        while (i < len(self.rule_base_array)) and (not found):
            found = self.rule_base_array[i].comparison(rule)
            i = i + 1
        return found

    def duplicated_granularity_rule(self, rule):
        i = 0
        found = False
        while (i < len(self.granularity_rule_Base)) and (not found):
            found = self.granularity_rule_Base[i].comparison(rule)
            i = i + 1
        return found

    def duplicated_negative_rule(self, rule):
        i = 0
        found = False
        while (i < len(self.negative_rule_base_array)) and (not found):
            found = self.negative_rule_base_array[i].comparison(rule)
            i = i + 1
        return found

    # * Rule Learning Mechanism for the Chi et al.'s method
    # * @param train myDataset the training data-set

    def generation(self, train):
        print("In generation, the size of train is :" + str(train.size()))
        for i in range(0, train.size()):
            rule = self.searchForBestAntecedent(train.getExample(i), train.getOutputAsIntegerWithPos(i))
            self.data_row_array.append(rule.data_row_here)
            rule.assingConsequent(train, self.ruleWeight)

            if not (self.duplicated(rule)) and (rule.weight > 0):
                # print("normal rule before append , the rule weight is " + str(rule.weight ) )

                self.rule_base_array.append(rule)
        print("The total data_row is " + str(len(self.data_row_array)))

    # * This function obtains the best fuzzy label for each variable of the example and assigns
    # * it to the rule
    # * @param example double[] the input example
    # * @param clas int the class of the input example
    # * @return Rule the fuzzy rule with the highest membership degree with the example

    def searchForBestAntecedent(self, example, clas):
        ruleInstance = Rule()
        ruleInstance.setTwoParameters(self.n_variables, self.compatibilityType)
        # print("In searchForBestAntecedent ,self.n_variables is :" + str(self.n_variables))
        ruleInstance.setClass(clas)
        # print("In searchForBestAntecedent ,self.n_labels is :" + str(self.n_labels))
        example_feature_array = []
        for f_variable in range(0, self.n_variables):
            # print("The f_variable is :"+str(f_variable))
            # print("The example is :" + str(example))
            example_feature_array.append(example[f_variable])
        label_array = []

        for i in range(0, self.n_variables):
            max_value = 0.0
            etq = -1
            per = None
            for j in range(0, self.n_labels):
                # print("Inside the second loop of searchForBestAntecedent......")
                per = self.data_base.membershipFunction(i, j, example[i])
                if per > max_value:
                    max_value = per
                    etq = j
            if max_value == 0.0:
                # print("There was an Error while searching for the antecedent of the rule")
                # print("Example: ")
                for j in range(0, self.n_variables):
                    print(example[j] + "\t")

                print("Variable " + str(i))
                exit(1)
            # print(" The max_value is : " + str(max_value))
            # print(" ,the j value is : " + str(j))
            ruleInstance.antecedent[i] = self.data_base.clone(i, etq)  # self.data_base[i][j]
            label_array.append(etq)
        data_row_temp = data_row()
        data_row_temp.set_three_parameters(clas, example_feature_array, label_array)
        ruleInstance.data_row_here = data_row_temp

        return ruleInstance

    # * It prints the rule base into an string
    # * @return String an string containing the rule base

    def printString(self):
        i = None
        j = None
        cadena_string = ""
        cadena_string += "@Number of rules: " + str(len(self.rule_base_array)) + "\n\n"
        for i in range(0, len(self.rule_base_array)):
            rule = self.rule_base_array[i]
            cadena_string += str(i + 1) + ": "
            for j in range(0, self.n_variables - 1):
                cadena_string += self.names[j] + " IS " + rule.antecedent[j].name + " AND "
            j = j + 1
            cadena_string += self.names[j] + " IS " + rule.antecedent[j].name + ": " + str(
                self.classes[rule.class_value]) + " with Rule Weight: " + str(rule.weight) + "\n"
        print("rule_base_array cadena_string is:" + cadena_string)

        # added negative rule print into file
        cadena_string += "\n\n"
        cadena_string += "@Number of negative rules: " + str(len(self.negative_rule_base_array)) + "\n\n"
        for i in range(0, len(self.negative_rule_base_array)):
            negative_rule = self.negative_rule_base_array[i]
            cadena_string += str(i + 1) + ": "
            for j in range(0, self.n_variables - 1):
                cadena_string += self.names[j] + " IS " + negative_rule.antecedent[j].name + " AND "
            j = j + 1
            cadena_string += self.names[j] + " IS " + negative_rule.antecedent[j].name + ": " + str(
                self.classes[negative_rule.class_value]) + " with Rule Weight: " + str(negative_rule.weight) + "\n"
        print("negative rules rule_base_array cadena_string is:" + cadena_string)

        return cadena_string

    def print_granularity_rule_string(self):
        # added for granularity rules
        cadena_string = ""
        cadena_string += "@Number of granularity rules: " + str(len(self.granularity_rule_Base)) + "\n\n"
        for i in range(0, len(self.granularity_rule_Base)):
            granularity_rule = self.granularity_rule_Base[i]
            cadena_string += "In negative zone area : " + str(
                granularity_rule.granularity_sub_zone) + " , has rules : " + "\n"
            cadena_string += str(i + 1) + ": "
            for j in range(0, self.n_variables - 1):
                cadena_string += self.names[j] + " IS " + granularity_rule.antecedent[j].name + " AND "
            j = j + 1
            print("granularity_rule.class_value is : " + str(granularity_rule.class_value))
            cadena_string += self.names[j] + " IS " + granularity_rule.antecedent[j].name + ": " + str(
                self.classes[granularity_rule.class_value]) + " with Rule Weight: " + str(
                granularity_rule.weight) + "\n"
        print("granularity rules rule_base_array cadena_string is:" + cadena_string)
        return cadena_string

    def print_pruned_granularity_rule_string(self):
        # added for granularity rules
        cadena_string = ""
        cadena_string += "@Number of pruned granularity rules: " + str(len(self.granularity_prune_rule_base)) + "\n\n"
        for i in range(0, len(self.granularity_prune_rule_base)):
            granularity_prune_rule = self.granularity_prune_rule_base[i]
            cadena_string += "In negative zone area : " + str(
                granularity_prune_rule.granularity_sub_zone) + " , has rules : " + "\n"
            cadena_string += str(i + 1) + ": "
            for j in range(0, self.n_variables - 1):
                cadena_string += self.names[j] + " IS " + granularity_prune_rule.antecedent[j].name + " AND "
            j = j + 1
            cadena_string += self.names[j] + " IS " + granularity_prune_rule.antecedent[j].name + ": " + str(
                self.classes[granularity_prune_rule.class_value]) + " with Rule Weight: " + str(
                granularity_prune_rule.weight) + "\n"
        print("pruned granularity rules rule_base_array cadena_string is:" + cadena_string)
        return cadena_string

    # * It writes the rule base into an ouput file
    # * @param filename String the name of the output file

    def writeFile(self, filename):
        print("rule string to save is: " + self.printString())
        outputString = self.printString()
        file = open(filename, "w+")
        file.write(outputString)
        file.close()

    def write_File_for_granularity_rule(self, filename):
        with open(filename, 'a') as file_append:
            outputString = "\n" + "\n" + self.print_granularity_rule_string()
            file_append.write(outputString)
            file_append.close()

    def write_File_for_pruned_granularity_rule(self, filename):
        with open(filename, 'a') as file_append:
            outputString = "\n" + "\n" + self.print_pruned_granularity_rule_string()
            file_append.write(outputString)
            file_append.close()

    # * Fuzzy Reasoning Method
    # * @param example double[] the input example
    # * @return int the predicted class label (id)

    def FRM(self, example, selected_array_pass):
        if self.inferenceType == 0:

            return self.FRM_WR(example, selected_array_pass)
        else:
            return self.FRM_AC_with_two_parameters(example, selected_array_pass)

    # * Winning Rule FRM
    # * @param example double[] the input example
    # * @return int the class label for the rule with highest membership degree to the example
    def FRM_WR(self, example, selected_array_pass):
        class_value = self.default_rule
        max_value = 0.0

        for i in range(0, len(self.rule_base_array)):
            if selected_array_pass[i] > 0:
                rule = self.rule_base_array[i]
                degree = rule.matching(example)
                if degree > max_value:
                    max_value = degree
                    class_value = rule.get_class()
        return class_value

    '''
       The granularity rules with normal rules, one new row data come, how to choose which rule
       Check if the data meet the granularity rule scope, if yes, go to the granularity rule, else
       go to the normal rules
    '''

    def FRM_Granularity(self, example):
        # print("FRM_Granularity begin :  ")
        class_value = -1
        max_value = 0.0
        produc = 0
        for i in range(0, len(self.granularity_rule_Base)):
            rule = self.granularity_rule_Base[i]
            # print("after get rule of the FRM_Granularity :")
            produc = rule.compatibility(example)
            produc *= rule.weight
            if produc > max_value:
                max_value = produc
                class_value = rule.class_value
        if produc == 0:
            for i in range(0, len(self.rule_base_array)):
                rule = self.rule_base_array[i]
                produc = rule.compatibility(example)
                produc *= rule.weight
                if produc > max_value:
                    max_value = produc
                    class_value = rule.class_value

        return class_value

    def FRM_Pruned_Granularity(self, example):
        # print("FRM_Granularity begin :  ")
        class_value = -1
        max_value = 0.0
        produc = 0
        for i in range(0, len(self.granularity_prune_rule_base)):
            rule = self.granularity_prune_rule_base[i]
            # print("after get rule of the FRM_Granularity :")
            produc = rule.compatibility(example)
            produc *= rule.weight
            if produc > max_value:
                max_value = produc
                class_value = rule.class_value

        return class_value

    # * Additive Combination FRM
    # * @param example double[] the input example
    # * @return int the class label for the set of rules with the highest sum of membership degree per class

    def FRM_AC_with_two_parameters(self, example,selected_array):
        class_value = self.default_rule
        degree = 0
        max_degree = 0
        degrees_class = [0.0 for x in range(self.train_myDataSet.get_nclasses())]
        for i in range(0, self.train_myDataSet.get_nclasses()):
            degrees_class[i]=0.0
        for i in range(0,len(self.rule_base_array)):
            if selected_array[i]>0:
                rule = self.rule_base_array[i]
                degree = rule.matching(example)
                degrees_class[rule.get_class()]+=degree
        max_degree = 0.0
        for i in range(0,self.train_myDataSet.get_nclasses()):
            if degrees_class[i]>max_degree:
                max_degree = degrees_class[i]
                class_value = i
        return class_value

    def FRM_AC(self,example):

        degree = 0.0
        max_degree = 0.0
        class_value = self.default_rule

        degree_class_array = [0.0 for x in range(self.get_nclasses())]
        for i in range(0, self.train_myDataSet.getnClasses()):
            degree_class_array[i] = 0.0

        for i in range (0, len(self.rule_base_array)) :
            rule = self.rule_base_array[i]

            degree = rule.matching(example)
            degree_class_array[rule.getClas()] += degree


        max_degree = 0.0
        for i in range(0, self.train_myDataSet.get_nclasses()):
            if degree_class_array[i] > max_degree:
                max_degree = degree_class_array[i]
                class_value = i



        return class_value






    # added by rui for negative  rules
    def generate_negative_rules(self, train, confident_value_pass, zone_confident_pass):

        class_value_arr = self.get_class_value_array(train)
        for i in range(0, len(self.rule_base_array)):
            rule_negative = Rule()
            rule_negative.antecedent = self.rule_base_array[i].antecedent
            positive_rule_class_value = self.rule_base_array[i].get_class()
            print("the positive rule class value is " + str(positive_rule_class_value) + " ,the i is :" + str(i))
            rule_negative.setClass(positive_rule_class_value)

            for j in range(0, len(class_value_arr)):
                class_type = int(class_value_arr[j])
                if positive_rule_class_value != class_type:  # need to get another class value for negative rule

                    rule_negative.setClass(class_type)  # change the class type in the rule
                    rule_negative.calculate_confident_support(self.data_row_array)
                    print("Negative rule's  confident value is :" + str(rule_negative.confident_value))

                    if rule_negative.confident_value > confident_value_pass and rule_negative.zone_confident > zone_confident_pass:
                        rule_negative.weight = rule_negative.confident_value
                        if not (self.duplicated_negative_rule(rule_negative)):

                            for k in range(0, len(rule_negative.antecedent)):
                                print("antecedent L_ " + str(rule_negative.antecedent[j].label))
                            print("Negative rule's class value " + str(rule_negative.get_class()))
                            print(" Negative rule's weight, confident_vale  " + str(rule_negative.weight))
                            print(" Negative rule's zone confident value   " + str(rule_negative.zone_confident))
                            print("Negative rule's positive_rule_class_value" + str(positive_rule_class_value))
                            print("Negative rule's class_type" + str(class_type))
                            self.negative_rule_base_array.append(rule_negative)

    def get_class_value_array(self, train):
        class_value_array = []
        integer_array = train.getOutputAsInteger()
        for i in range(0, len(integer_array)):
            exist_yes = False
            for j in range(0, len(class_value_array)):
                if integer_array[i] == class_value_array[j]:
                    exist_yes = True
            if not exist_yes:
                class_value_array.append(integer_array[i])
        return class_value_array

    def calculate_confident_support_rulebase(self, train):
        class_value_arr = self.get_class_value_array(train)
        str_print = "Totally there are: " + str(len(self.rule_base_array)) + " rules"
        print(str_print)
        index_number = 1

        for each_rule in self.rule_base_array:
            each_rule.calculate_confident_support(self.data_row_array)
            print(str(index_number) + " -- each_rule.weight :" + str(each_rule.weight) + ",zone_confident :" + str(
                each_rule.zone_confident) + ",calculate_confident :" + str(each_rule.confident_value))
            print(" -- each_rule.support_value :" + str(each_rule.support_value))
            index_number = index_number + 1

    def get_inference_type(self):
        return self.inferenceType

    def get_k_value(self):
        return self.k_value

    """
   * Function to eliminate the rules that are not needed (Redundant, not enough accurate,...) for a given class.
   * @param clas class whose rules are being tested
    """

    def reduce_rules(self, class_value):
        nexamples = 0

        example_weight: ExampleWeight = []
        for i in range(0, self.train_myDataSet.size()):
            example_weight.append(ExampleWeight(self.k_value))
        selected = [0 for x in range(len(self.rule_base_array))]
        for i in range(0, len(self.rule_base_array)):
            selected[i] = 0

        nexamples = self.train_myDataSet.number_instances(class_value)
        nrule_select = 0
        posBestWracc = 0

        while (nexamples > 0 and (nrule_select < len(self.rule_base_array)) and (posBestWracc > -1)):
            bestWracc = -1.0
            posBestWracc = -1
            for i in range(0, len(self.rule_base_array)):
                if selected[i] == 0:
                    rule = self.rule_base_array[i]
                    rule.calculateWracc(self.train, example_weight)
                    if rule.getWracc() > bestWracc:
                        bestWracc = rule.getWracc()
                        posBestWracc = i
            if posBestWracc > -1:
                selected[posBestWracc] = 1
                nrule_select = nrule_select + 1
                rule = self.rule_base_array.get(posBestWracc)
                nexamples = nexamples - rule.reduceWeight(self.train, example_weight)

        for i in range(len(self.rule_base_array) - 1, 0, -1):
            if selected[i] == 0:
                self.rule_base_array.pop(i)

        example_weight.clear()
        gc.collect()

    def add_rule(self, rule):
        self.rule_base_array.append(rule)

    def add_rule_base(self, rule_base_pass):

        for i in range(0, rule_base_pass.get_size()):
            self.rule_base_array.append(rule_base_pass[i].clone)

    def get_size(self):
        return len(self.rule_base_array)

    def clear(self):
        self.rule_base_array.clear()
        self.fitness = 0.0

    """
     * Sets the default rule.
     * The default rule classifies all the examples to the majority class.
    """

    def set_default_rule(self):

        best_rule = 0
        for i in range(1, self.train.getnClasses()):
            if self.train.numberInstances(best_rule) < self.train.numberInstances(i):
                best_rule = i
        self.default_rule = best_rule

    """

   * Function to return the fitness of the rule base

   * @return Fitness of the rule base
    
    """

    def get_accuracy(self):
        return self.fitness

    """
     * Indentifies how many classes are uncovered with a selection of rules.
     * @param selected rules selected to be tested
     * @return number of classes uncovered.
    """

    def has_class_uncovered(self, selected_array_pass):
        i = 0
        count = 0
        cover_array = []
        cover_array = [0 for x in range(self.train_myDataSet.get_nclasses())]
        for i in range(0, len(cover_array)):
            if self.train_myDataSet.number_instances(i) > 0:
                cover_array[i] = 0
            else:
                cover_array[i] = 1

        for i in range(0, len(self.rule_base_array)):
            if selected_array_pass[i] > 0:
                cover_array[self.rule_base_array[i].get_class()] += 1
        count = 0
        for i in range(0, len(cover_array)):
            if cover_array[i] == 0:
                count += 1

        return count

    """
   * Function to evaluate the whole rule base by using the training dataset.
     """

    def evaluate(self):
        nhits = 0
        prediction = 0

        self.nuncover = 0
        for j in range(0, self.train_myDataSet.get_nclasses()):
            self.nuncover_class_array[j] = 0

        for j in range(0, self.train_myDataSet.size()):
            prediction = self.FRM(self.train_myDataSet.getExample(j))
            if self.train_myDataSet.get_output_as_integer_with_pos(j) == prediction:
                nhits += 1
            if prediction < 0:
                self.nuncover += 1
                self.nuncover_class_array[self.train.getOutputAsInteger(j)]

        self.fitness = (100.0 * nhits) / (1.0 * self.train_myDataSet.size())

    """
     * Function to evaluate the selected rules by using the training dataset and the fuzzy functions stored in the gene given.
     * @param gene Representation where the fuzzy functions needed to evaluate are stored
     * @param selected Selection of rules to be evaluated
     */
    """

    def evaluate_with_two_parameters(self, gene_array_pass, selected_array_pass):
        nhits = 0
        prediction = 0

        self.data_base.decode(gene_array_pass)

        nhits = 0
        self.nuncover = 0
        for j in range(0, self.train_myDataSet.get_nclasses()):
            self.nuncover_class_array[j] = 0

        for j in range(0, self.train_myDataSet.size()):
            prediction = self.FRM(self.train_myDataSet.get_example(j), selected_array_pass)
            if self.train_myDataSet.get_output_as_integer_with_pos(j) == prediction:
                nhits += 1
            if prediction < 0:
                self.nuncover += 1
                self.nuncover_class_array[self.train_myDataSet.get_output_as_integer_with_pos(j)] += 1

        self.fitness = (100.0 * nhits) / (1.0 * self.train_myDataSet.size())

    """
     /**
     * Returns the number of examples uncovered by the rules
     * @return Number of examples uncovered
     */
    """
    def get_uncover(self) :
        return self.nuncover




