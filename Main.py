# /***********************************************************************
#
# 	This file is part of KEEL-software, the Data Mining tool for regression,
# 	classification, clustering, pattern mining and so on.
#
# 	Copyright (C) 2004-2010
#
# 	F. Herrera (herrera@decsai.ugr.es)
# 	L. S谩nchez (luciano@uniovi.es)
# 	J. Alcal谩-Fdez (jalcala@decsai.ugr.es)
# 	S. Garc铆a (sglopez@ujaen.es)
# 	A. Fernandez (alberto.fernandez@ujaen.es)
# 	J. Luengo (julianlm@decsai.ugr.es)
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
# **********************************************************************

from ParseParameters import ParseParameters
from Fuzzy_Chi import Fuzzy_Chi
from Farchd import Farchd
from os import listdir
from os.path import isfile, join
import sys
from pathlib import Path


# * <p>It reads the configuration file (data-set files and parameters) and launch the algorithm</p>
# *
# * @author Written by Alberto Fern谩ndez (University of Granada) 14/10/2007
# * @version 1.0
# * @since JDK1.5

class Main:
    # config_files_folder = Path("C:\phd_algorithms\chi-scikit-granularity-rules-experiments\few_disjuncts_1")
    # file_to_open = None

    # Default Constructor

    # * It launches the algorithm
    # * @param confFile String it is the filename of the configuration file.


    def execute(file_setup):
        # print("file_setup is " + file_setup)
        # print("Main execute begin...")
        parameters = ParseParameters()
        parameters.parse_configuration_file(file_setup)
        farc_hd = Farchd(parameters)
        farc_hd.execute()

    def executeMultiFiles(self,file_setup):
        # print("MaultiMain execute begin...")
        parameters = ParseParameters()
        parameters.parseConfigurationFile(file_setup)
        farc_hd = Farchd(parameters)
        farc_hd.execute()

    # * Main Program
    # * @param args It contains the name of the configuration file
    # * Format:
    # * algorithm = ;algorithm name>
    # * inputData = "training file" "validation file" "test file"
    # * outputData = "training file" "test file"
    # *
    # * seed = value (if used)
    # Parameter1; value1
    # Parameter2&gt; value2

    if __name__ == '__main__':
        # print("Executing Algorithm.")

        # print("sys.argv: " + sys.argv[1])
        execute(sys.argv[1])
