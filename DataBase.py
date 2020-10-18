

import numpy as np
from numpy import array
from Fuzzy import Fuzzy


class DataBase:
    n_variables = 0
    partitions = 0
    # not use in FarcHD
    n_labels = 0

    nlabels_array: int = []
    varreal_array: bool = []
    database = []
    database_ini = []
    names = []
    # not use in FarcHD
    cadena = None

    # Default constructor
    def __init__(self):
        print("init DataBase class")


        # Constructor with parameters. It performs a homegeneous partition of the input space for
        # a given number of fuzzy labels.
        # @param n_variables int Number of input variables of the problem
        # @param n_labels int Number of fuzzy labels
        # @param rangos double[][] Range of each variable (minimum and maximum values)
        # @param names String[] Labels for the input attributes


    # '''
    #      * @return int the number of input variables
    # '''
    # modified at 2020-08-14
    def init_with_three_parameters(self, n_labels_pass, train_my_dataset):

        ranks = train_my_dataset.get_ranges()

        self.n_variables = train_my_dataset.get_ninputs()
        self.names = train_my_dataset.get_names()
        # int array
        self.nlabels_array = [0 for x in range(self.n_variables)]

        # bool array
        self.varreal_array = [True for x in range(self.n_variables)]
        self.database = [[Fuzzy() for y in range(n_labels_pass)] for x in range(self.n_variables)]
        self.database_ini = [[Fuzzy() for y in range(n_labels_pass)] for x in range(self.n_variables)]

        for i in range(0, self.n_variables):

            rank = abs(ranks[i][1] - ranks[i][0])
            self.varreal_array[i] = False

            if train_my_dataset.is_nominal(i):
                self.nlabels_array[i] = int(rank) + 1
            elif train_my_dataset.is_integer(i) and (rank + 1) <= n_labels_pass:
                self.nlabels_array[i] = int(rank) + 1
            else:
                self.nlabels_array[i] = n_labels_pass
                self.varreal_array[i] = True

            self.database[i] = [Fuzzy() for x in range(self.nlabels_array[i])]
            self.database_ini[i] = [Fuzzy() for x in range(self.nlabels_array[i])]

            mark = rank / (self.nlabels_array[i] - 1.0)

            for j in range(0, self.nlabels_array[i]):
                self.database[i][j] = Fuzzy()
                self.database_ini[i][j] = Fuzzy()
                value = ranks[i][0] + mark * (j - 1)
                self.database_ini[i][j].x0 = self.database[i][j].x0 = self.set_value(value, ranks[i][0], ranks[i][1])
                value = ranks[i][0] + mark * j
                self.database_ini[i][j].x1 = self.database[i][j].x1 = self.set_value(value, ranks[i][0], ranks[i][1])
                value = ranks[i][0] + mark * (j + 1)
                self.database_ini[i][j].x3 = self.database[i][j].x3 = self.set_value(value, ranks[i][0], ranks[i][1])
                self.database_ini[i][j].y = self.database[i][j].y = 1.0
                self.database[i][j].name = "L_" + str(j) + "(" + str(self.nlabels_array[i]) + ")"
                self.database_ini[i][j].name = "L_" + str(j) + "(" + str(self.nlabels_array[i]) + ")"

    # 2020-08-14
    def set_value(self, val, min_value, max_value):
        if min_value - 1e-4 < val < min_value + 1e-4:
            return min_value
        if max_value < val < max_value + 1e-4:
            return max_value
        return val

    """
     * Decode the gene representation for the GA into the DataBase one based on the Triangular Membership Functions 
     * @param gene Gene representation of the individual being decoded.
     */
    """

    def decode(self, gene_array):
        i = 0
        j = 0
        pos = 0
        displacement = 0.0
        pos = 0

        """
          for (i=0; i < n_variables; i++) {
		  if (varReal[i]) {
			  for (j=0; j < this.nLabels[i]; j++, pos++) {
				  if (j == 0)  
				  displacement = (gene[pos] - 0.5) * (this.dataBaseIni[i][j+1].x1 - this.dataBaseIni[i][j].x1);
				  else if (j == (this.nLabels[i]-1))  
				  displacement = (gene[pos] - 0.5) * (this.dataBaseIni[i][j].x1 - this.dataBaseIni[i][j-1].x1);
				  else {
					  if ((gene[pos] - 0.5) < 0.0)  
					  displacement = (gene[pos] - 0.5) * (this.dataBaseIni[i][j].x1 - this.dataBaseIni[i][j-1].x1);
					  else  
					  displacement = (gene[pos] - 0.5) * (this.dataBaseIni[i][j+1].x1 - this.dataBaseIni[i][j].x1);
				  }
				  
				  this.dataBase[i][j].x0 = this.dataBaseIni[i][j].x0 + displacement;
				  this.dataBase[i][j].x1 = this.dataBaseIni[i][j].x1 + displacement;
				  this.dataBase[i][j].x3 = this.dataBaseIni[i][j].x3 + displacement;
			  }
		  }
	  }
        
        """
        for i in range(0, self.n_variables):
            if self.varreal_array[i]:
                for j in range(0, self.nlabels_array[i]):

                    if j == 0:
                        displacement = (gene_array[pos] - 0.5) * (
                                self.database_ini[i][j + 1].x1 - self.database_ini[i][j].x1)
                    elif j == (self.nlabels_array[i] - 1):
                        displacement = (gene_array[pos] - 0.5) * (
                                self.database_ini[i][j].x1 - self.database_ini[i][j - 1].x1)
                    else:
                        if (gene_array[pos] - 0.5) < 0.0:
                            displacement = (gene_array[pos] - 0.5) * (
                                    self.database_ini[i][j].x1 - self.database_ini[i][j - 1].x1)
                        else:
                            displacement = (gene_array[pos] - 0.5) * (
                                    self.database_ini[i][j + 1].x1 - self.database_ini[i][j].x1)
                    self.database[i][j].x0 = self.database_ini[i][j].x0 + displacement
                    self.database[i][j].x1 = self.database_ini[i][j].x1 + displacement
                    self.database[i][j].x3 = self.database_ini[i][j].x3 + displacement
                    j += 1
                    pos += 1

    """
   * It returns the number of input attributes in the examples
   * @return The number of input attributes
    """

    def num_variables(self):
        return self.n_variables

    """
       * It returns the number of different labels that a specific input attribute can hold
       * @param variable The input attribute which we want to know the number of different labels it can have
       * @return The number of labels 
    """

    def num_labels(self, variable):
        return self.n_labels[variable]

    # '''
    #      * It computes the membership degree for a input value
    #      * @param i int the input variable id
    #      * @param j int the fuzzy label id
    #      * @param X double the input value
    #      * @return double the membership degree
    #      */
    # '''
    def membership_function(self, i, j, X):
        # print("len(self.database[0])" + str(len(self.database)))
        value = self.database[i][j].fuzzify(X)
        # print("Get value form Fuzzy setX is :" + str(value))
        return value

    # '''
    #      * It makes a copy of a fuzzy label
    #      * @param i int the input variable id
    #      * @param j int the fuzzy label id
    #      * @return Fuzzy a copy of a fuzzy label
    # '''
    def clone(self, i, j):
        return self.database[i][j]

    # '''
    #      * It prints the Data Base into an string
    #      * @return String the data base
    # '''
    def printString(self):
        self.cadena = "@Using Triangular Membership Functions as antecedent fuzzy sets\n"
        self.cadena += "@Number of Labels per variable: " + str(self.n_labels) + "\n"
        numrows = len(self.database)
        # print("numrows: " + str(numrows))
        numcols = len(self.database[0])

        # print("numrows: " + str(numrows) + "numcols:" + str(numcols))
        if self.database.size != 0:
            # print("cadena: " + self.cadena)
            for i in range(0, self.n_variables):
                # print("i = " + str(i))
                # print("cadena: " + self.cadena)
                self.cadena += "\n" + " " + self.names[i] + ":\n"
                for j in range(0, self.n_labels):
                    # print("i = " + str(i))
                    self.cadena += "      " + " L_" + str(int(j + 1)) + ": (" + str(self.database[i][j].x0) + "," + str(
                        self.database[i][j].x1) + "," + str(self.database[i][j].x3) + ")\n"
        else:
            print("self.dataBase is None")
        self.cadena += "\n"
        return self.cadena

    """

    # '''
    #      * It writes the Data Base into an output file
    #      * @param filename String the name of the output file
    #      w+ to save all the database
    # '''
    def writeFile(self, filename, who_call, zone_number):

        if who_call == "1":
            outputString = "normal rule area" + "\n" + "\n" + self.printString()
            file = open(filename, "w+")
            file.write(outputString)
            file.close()
        else:
            with open(filename, 'a') as file_append:
                outputString = "granularity rule of negative zone area " + str(zone_number)
                outputString = outputString + "\n" + "\n" + self.printString()
                file_append.write(outputString)
                file_append.close()
                
    """

    def set_value(self, val_pass: float, min_value: float, max_value: float) -> object:
        """
        :rtype: float
        """
        if min_value - 1e-4 < val_pass < min_value + 1e-4:
            return min_value
        if max_value - 1e-4 < val_pass < max_value + 1e-4:
            return max_value
        return val_pass

    def num_labels(self, index_value):

        return self.nlabels_array[index_value]

    """
        * It return the whole array of number of labels for every attribute
        * @return the whole array of number of labels for every attribute
    
    """

    def get_nlabels_array(self):

        return self.nlabels_array
    """
   * Returns the number of total real labels held by the input attributes.
   * @return The number of real labels
    """
    def get_nlabels_real(self):
        count = 0
        for i in range (0, self.n_variables):
            if self.varreal_array[i]:
              count += self.n_labels[i]
        return count





    def matching(self, variable, label, value):
        if (variable < 0) or (label < 0):
            # do not care
            return 1
        else:
            return self.database[variable][label].fuzzify(value)

    def get_nlabels_real(self):

        count = 0

        for i in range(0, self.n_variables):
            if self.varreal_array[i]:
                count = count + self.nlabels_array[i]
        return count

    """
     * Return a String representation of the Triangular Membership Functions of the variable and its label given as arguments. 
     * @param var Index of the variable given.
     * @param label Index of the label given.
     * @return String representation of the Triangular Membership Function.
   """

    def print_triangle(self, var_value, label):

        dfuzzy = self.database[var_value][label]
        cadena = dfuzzy.name + ": \t" + dfuzzy.x0 + "\t" + dfuzzy.x1 + "\t" + dfuzzy.x3 + "\n"
        return cadena

    """
   * It prints an attribute with its label in a string way
   * @param var Attribute to be printed
   * @param label Attribute's label to be printed
   * @return A string which represents the "string format" of the given input
    """

    def print_here(self, var, label):
        return self.database[var][label].get_name()

    """
     
   * It prints the whole database
   * @return The whole database
    """

    def print_string(self):
        information = "@Using Triangular Membership Functions as antecedent fuzzy sets"
        for i in range(0, self.n_variables):
            information += "\n\n@Number of Labels in Variable " + str(i + 1) + ": " + str(self.nlabels_array[i])
            information += "\n" + self.names[i] + ":\n"
            for j in range(0, self.nlabels_array[i]):
                information += self.database[i][j].name + ": (" + str(self.database[i][j].x0) + "," + str(self.database[i][
                    j].x1) + "," + str(self.database[i][j].x3) + ")\n"

        return information

    """
   * It stores the data base in a given file
   * @param filename Name for the database file
    """
    def save_file(self, filename):
        string_out = ""
        string_out = self.print_string()
        file = open(filename, "w+")
        file.write(string_out)
        file.close()





