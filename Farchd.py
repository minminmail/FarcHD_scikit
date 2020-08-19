# ***********************************************************************

#  * <p>Title: Farchd</p>
#  * <p>Description: It contains the implementation of the Farchd algorithm</p>
#  * <p>Company: KEEL </p>
#  * @author Written by Jesus Alcala (University of Granada) 09/02/2011

# **********************************************************************/
from DataBase import DataBase
from RuleBase import RuleBase
from MyDataSet import MyDataSet
from Apriori import Apriori
from Populate import Populate
import datetime
import random
import time
import os.path


# * <p>It contains the implementation of the Chi algorithm</p>
# *
# * @author Written by Alberto Fern谩ndez (University of Granada) 02/11/2007
# * @version 1.0
# * @since JDK1.5

class Farchd:
    train_mydataset = None
    val_mydataset = None
    test_mydataset = None

    output_tr = ""
    output_tst = ""

    file_db = ""
    file_rb = ""
    file_time = ""
    file_hora = ""
    data_string = ""
    file_rules = ""
    evolution = ""

    rules_stage1 = 0
    rules_stage2 = 0
    rules_stage3 = 0

    data_base = None
    rule_base = None

    apriori = None

    pop = None
    start_time = 0
    total_time = 0

    # algorithm parameters
    # int
    nlabels = 0
    population_size = 0
    depth = 0
    k_parameter = 0
    max_trials = 0
    type_inference = 0
    bits_gen = 0

    minsup = 0.0
    minconf = 0.0
    alpha = 0.0

    # bool
    something_wrong = False  # to check if everything is correct.

    def __init__(self, parameters):
        print("__init__ of Fuzzy_Chi begin...")
        self.start_time = datetime.datetime.now()

        self.train_mydataset = MyDataSet()
        self.val_mydataset = MyDataSet()
        self.test_mydataset = MyDataSet()


        try:

            input_training_file = parameters.get_input_training_files()
            print("Reading the training set: " + input_training_file)

            self.train_mydataset.read_classification_set(input_training_file, True, parameters.file_path)
            print("Reading the validation set: ")
            input_validation_file = parameters.get_validation_input_file()
            self.train_mydataset.read_classification_set(input_validation_file, True, parameters.file_path)
            print("Reading the test set: ")
            self.test_mydataset.read_classification_set(parameters.get_input_test_files(), False, parameters.file_path)
            print(" ********* test_mydataset.myDataSet read_classification_set finished !!!!!! *********")
        except IOError as ioError:
            print("I/O error: " + str(ioError))
            self.something_wrong = True
        except Exception as e:
            print("Unexpected error:" + str(e))
            self.something_wrong = True

        self.something_wrong = self.something_wrong or self.train_mydataset.has_missing_attributes()
        self.output_tr = parameters.get_training_output_file()
        self.output_tst = parameters.get_test_output_file()

        self.file_db = parameters.get_output_file(0)
        self.file_rb = parameters.get_output_file(1)
        self.data_string = parameters.get_input_training_files()

        output_file = parameters.get_output_file(1)
        self.file_time = output_file + "/time.txt"
        self.file_hora = output_file + "/hora.txt"
        self.file_rules = output_file + "/rules.txt"
        # Now we parse the parameters long
        seed = int(float(parameters.get_parameter(0)))
        para1 = parameters.get_parameter(1)
        self.nlabels = int(parameters.get_parameter(1))
        self.minsup = float(parameters.get_parameter(2))
        self.minconf = float(parameters.get_parameter(3))
        self.depth = int(parameters.get_parameter(4))
        self.k_parameter = int(parameters.get_parameter(5))
        self.max_trials = int(parameters.get_parameter(6))
        self.population_size = int(parameters.get_parameter(7))
        if self.population_size % 2 > 0:
            self.population_size = self.population_size + 1
        self.alpha = float(parameters.get_parameter(8))
        self.bits_gen = int(parameters.get_parameter(9))
        self.type_inference = int(parameters.get_parameter(10))
        random.seed(seed)

    def execute(self):
        if self.something_wrong:  # We do not execute the program
            print("An error was found, the data-set have missing values")
            print("Please remove the examples with missing data or apply a MV preprocessing.")
            print("Aborting the program")
        # We should not use the statement: System.exit(-1);
        else:
            print("No errors, Execute in FarcHD execute :")
            self.data_base = DataBase()
            self.data_base.init_with_three_parameters(self.nlabels, self.train_mydataset)
            self.rule_base = RuleBase()
            self.rule_base.init_with_five_parameters(self.data_base, self.train_mydataset, self.k_parameter,
                                                     self.type_inference)
            self.apriori = Apriori()
            self.apriori.multiple_init(self.rule_base, self.data_base, self.train_mydataset, self.minsup, self.minconf,
                                       self.depth)
            self.apriori.generate_rb()
            self.rules_stage1 = self.apriori.get_rules_stage1()
            self.rules_stage2 = self.rule_base.get_size()

            self.pop = Populate()

            self.pop.init_with_multiple_parameters(self.train_mydataset, self.data_base, self.rule_base,
                                                   self.population_size, self.bits_gen, self.max_trials, self.alpha)
            self.pop.generation()

            print("Building classifier")
            self.rule_base = self.pop.get_best_RB()

            self.rules_stage3 = int(self.rule_base.get_size())

            self.data_base.saveFile(self.file_db)
            self.rule_base.saveFile(self.file_rb)

            #  Finally we should fill the training and test  output files
            self.do_output(self.val, self.output_tr)
            self.do_output(self.test, self.output_tst)

            current_millis = int(round(time.time() * 1000))
            self.total_time = current_millis - self.start_time
            self.write_time()
            self.write_rules()
            print("Algorithm Finished")

    """ 
     * Add all the rules generated by the classifier to fileRules file.
     """

    def write_rules(self):

        string_out = "" + self.rules_stage1 + " " + self.rules_stage2 + " " + self.rules_stage3 + "\n"

        file = open(self.file_rules, "a+")
        file.write(string_out)

    def write_time(self):
        aux = None  # int
        seg = None  # int
        min_value = None  # int
        hor = None  # int

        string_out = "" + self.total_time / 1000 + "  " + self.data_string + "\n"
        file = open(self.file_time, "a+")
        file.write(string_out)
        self.total_time /= 1000
        seg = self.total_time % 60
        self.total_time = self.total_time / 60
        min_value = self.total_time % 60
        hor = self.total_time / 60
        string_out = ""
        if hor < 10:
            string_out = string_out + "0" + hor + ":"
        else:
            string_out = string_out + hor + ":"
        if min_value < 10:
            string_out = string_out + "0" + min_value + ":"
        else:
            string_out = string_out + min_value + ":"

        if seg < 10:
            string_out = string_out + "0" + seg
        else:
            string_out = string_out + seg

        string_out = string_out + "  " + self.data_string + "\n"

        file = open(self.file_hora, "a+")
        file.write(string_out)

    # """
    #    * It generates the output file from a given dataset and stores it in a file
    #    * @param dataset myDataset input dataset
    #    * @param filename String the name of the file
    #    *
    #    * @return The classification accuracy
    # """

    def do_output(self, mydataset, filename):
        output = ""
        output = mydataset.copy_header()  # we insert the header in the output file
        # We write the output for each example
        for i in range(0, mydataset.get_ndata()):
            # for classification:
            output = output + mydataset.get_output_as_string(i) + " " + self.classification_output(
                mydataset.get_example(i)) + "\n"

        if os.path.isfile(filename):
            print("File exist")
            output_file = open(filename, "a+")
        else:
            print("File not exist")
            output_file = open(filename, "w+")

        output_file.write(output)

    # * It returns the algorithm classification output given an input example
    # * @param example double[] The input example
    # * @return String the output generated by the algorithm

    def classification_output(self, example):
        output = "?"
        # Here we should include the algorithm directives to generate the
        # classification output from the input example

        class_out = self.rule_base.FRM(example)

        if class_out >= 0:
            output = self.train_mydataset.get_output_value(class_out)

        return output
