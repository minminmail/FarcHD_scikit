#  /***********************************************************************
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

#  * <p>It reads the configuration file (data-set files and parameters)</p>
#  *
#  * @author Written by Alberto Fern谩ndez (University of Granada) 15/10/2007
#  * @Modified by Rui Min 28/09/2018
#  * @version 1.0
#  * @since Python 3

import logging
import re
from pathlib import Path


class ParseParameters:
    algorithm_name = ""
    training_file = ""
    validation_file = ""
    test_file = ""

    input_files = []
    output_tr_file = ""
    output_ts_file = ""
    output_files = []
    file_path = None

    parameters = []

    # * Default constructor

    def __init__(self):
        self.input_files = []
        self.output_files = []
        self.parameters = []
        self.file_path = None

        # * It obtains all the necesary information from the configuration file.<br/>
        # * First of all it reads the name of the input data-sets, training, validation and test.<br/>
        # * Then it reads the name of the output files, where the training (validation) and test outputs will be stored<br/>
        # * Finally it read the parameters of the algorithm, such as the random seed.<br/>
        # *
        # * @param fileName Name of the configuration file
        # *

    def parse_configuration_file(self, file_name):

        logging.info("fileName in parseParameters = " + file_name)
        logging.info("before open file")
        # print(fileName)
        # print("file in parseConfigurationFile is :" + str(fileName))
        self.file_path = '\\'.join(file_name.split('\\')[0:-1])
        # print("file_path in parseConfigurationFile is :" + self.file_path)
        file = open(file_name, "r")

        # file is an string containing the whole file
        file_string = file.read()
        line = file_string.splitlines()

        for line_number in range(0, len(line)):
            # print("In line " + str(lineNumber) + ", the str is:begin ***   " + line[lineNumber] + "   ***end")
            if line_number == 0:
                self.read_name(line[line_number])
            elif line_number == 1:
                self.read_input_files(line[line_number])  # We read all the input files
            elif line_number == 2:
                self.read_output_files(line[line_number])  # We read all the output files
            else:  # read parameters and save into map
                self.read_all_parameters(line[line_number])  # We read all the possible parameters
        # print("********* Summary for readAllParameters :" + " *********")
        # for key, value in self.__parameters:
            # print("********* parameters are : (" + key + ", " + value + " ) *********")

    # """
    #     * It reads the name of the algorithm from the configuration file
    #     * @param line StringTokenizer It is the line containing the algorithm name.
    # """
    def read_name(self, line):
        # print("In side the readName method the parameter pass is :" + str(line))
        name = line.rpartition("=")[2]
        name = name.strip()
        # print("In side the readName method after split =, we get:" + str(name))
        self.algorithm_name = name

    # """
    #     * We read the input data-set files and all the possible input files
    #     * @param line StringTokenizer It is the line containing the input files.
    # """
    def read_input_files(self, line):
        # print("Inside the readInputFiles mehtod, we get parameter is:" + str(line))
        first_parts = line.split()
        line_number = len(first_parts)
        file_list = []
        for i in range(0, line_number):
            whole_name = first_parts[i]
            # print("Inside readInputFiles, line " + str(lineNumber) + ",wholeName: " + str(wholeName))
            file_name_with_str = whole_name.rpartition('/')[2]
            # print("Inside readInputFiles, line " + str(fileNameWithStr) + ",fileNameWithStr: " + str(fileNameWithStr))
            file_name = file_name_with_str[:-1]
            # print("Inside readInputFiles, line " + str(lineNumber) + ",fileName: " + str(fileName))

            file_type = file_name[-3:]
            if file_type == "dat" or file_type == "tra" or file_type == "tst":
                file_list.append(file_name)

        file_number = len(file_list)
        # print("file_number :" + str(file_number))
        for i in range(0, file_number):
            if i == 0:
                self.training_file = file_list[i]
            elif i == 1:
                self.validation_file = file_list[i]
            elif i == 2:
                self.test_file = file_list[i]
            else:
                self.input_files.append(file_list[i])

        # print("The other remaining Input files number is :" + str(len(self.input_files)))

        # for file in self.input_files:
            # print("input file is :" + file)

        # print("********* Summary for readInputFiles :" + " *********")
        # print("********* The Input training file  is :" + str(self.training_file) + " *********")
        # print("********* The Input validation file  is :" + str(self.validation_file) + " *********")
        # print("********* The Input test file  is :" + str(self.test_file) + " *********")

    # """
    #     * We read the output files for training and test and all the possible remaining output files
    #     * @param line StringTokenizer It is the line containing the output files.
    # """
    def read_output_files(self, line):
        # print("Inside the readInputFiles method, we get parameter is:" + str(line))
        first_parts = line.split()
        file_list = []
        line_number = len(first_parts)
        for i in range(0, line_number):
            whole_name = first_parts[i]
            # print("Inside readOutputFiles, line " + str(lineNumber) + ",wholeName: " + str(wholeName))
            file_name_with_str = whole_name.rpartition('/')[2]
            # print("Inside readOutputFiles, line " + str(fileNameWithStr) + ",fileNameWithStr: " + str(fileNameWithStr))
            file_name = file_name_with_str[:-1]
            # print("Inside readOutputFiles, line " + str(lineNumber) + ",fileName: " + str(fileName))

            file_type = file_name[-3:]
            if file_type == "txt" or file_type == "tra" or file_type == "tst":
                file_list.append(file_name)

        file_number = len(file_list)
        # print("file_number" + str(file_number))
        for i in range(0, file_number):
            if i == 0:
                self.output_tr_file = file_list[i]
            elif i == 1:
                self.output_ts_file = file_list[i]
            else:
                self.output_files.append(file_list[i])

        # print("********* Summary for readOutputFiles :" + " *********")
        # print("*********  The output training file  is :" + str(self.__outputTrFile) + " *********")
        # print("*********  The output test file  is :" + str(self.__outputTstFile) + " *********")

        for file in self.output_files:
            print("********* output file is :" + file + " *********")

    # """
    #     * We read all the possible parameters of the algorithm
    #     * @param line StringTokenizer It contains all the parameters.
    # """
    def read_all_parameters(self, line):

        # print("readAllParameters begin,  line is :" + line)
        key = line.rpartition("=")[0]
        # print("The parameter key is :" + key)
        value = line.rpartition("=")[2]
        # print("The parameter value is :" + value)
        # remove the space in key and value of parameters and save into dictionary
        if key != "":
            self.parameters.append((key, value))

    # If the algorithm is non-deterministic the first parameter is the Random SEED

    # """
    # * It returns the algorithm name
    # *
    # * @return the algorithm name
    # """

    def get_algorithm_name(self):
        return self.algorithm_name

    # """
    # * It returns the name of the parameters
    # *
    # * @return the name of the parameters
    # """
    def get_parameters(self):
        param = self.parameters

        return param

    # """
    # * It returns the name of the parameter specified
    # *
    # * @param key the index of the parameter
    # * @return the value of the parameter specified
    # """
    def get_parameter(self, pos):

        return self.parameters[pos][1]

    # """
    # * It returns the input files
    # *
    # * @return the input files
    # """

    def get_input_files(self):
        return str(self.input_files)

    # """
    # * It returns the input training files
    # *
    # * @return the input training files
    # """

    def get_input_training_files(self):
        return self.training_file

    # """
    #  * It returns the input test files
    #  *
    #  * @return the input test files
    #  """

    def get_input_test_files(self):
        return self.test_file

    # * It returns the validation input file
    # *
    # * @return the validation input file

    def get_validation_input_file(self):
        return self.validation_file

    # /**
    #  * It returns the training output file
    #  *
    #  * @return the training output file
    #  */
    def get_training_output_file(self):
        return self.output_tr_file

    # * It returns the test output file
    # *
    # * @return the test output file

    def get_test_output_file(self):
        return self.output_ts_file

    # * It returns the algorithm name
    # *
    # * @return the algorithm name

    def get_algorithm_name(self):
        return self.algorithm_name

    # * It returns the name of the parameters
    # *
    # * @return the name of the parameters

    def get_parameters(self):
        return self.parameters

    # * It returns the input files
    # *
    # * @return the input files

    def get_input_files(self):
        return self.input_files

    # """
    # * It returns the input file of the specified index
    # *
    # * @param pos index of the file
    # * @return the input file of the specified index
    # """
    def get_input_file(self, pos):
        return self.input_files[pos]

    # """
    # * It returns the output files
    # *
    # * @return the output files
    # """
    def get_output_files(self):
        return self.output_files

    # """
    # * It returns the output file of the specified index
    # *
    # * @param pos index of the file
    # * @return the output file of the specified index
    # """
    def get_output_file(self, pos):
        return self.output_files[pos]
