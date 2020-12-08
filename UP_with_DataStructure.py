
"""
##############################################################################
##############################################################################
########               Planning and Reasoning                  ###############
########                   Prof.Liberatore                     ###############
########                                                       ###############
########              Student: FRANCESCO CASSINI               ###############
########              Sapienza ID:       785771                ###############
########     Master in Roboics and Artificial Intelligence     ###############
##############################################################################
##############################################################################
"""

# No Python library required to run this example 
#   of Unit Propagation with Data Structure :) 

##############################################################################
##############                                                ################
##############                      OPTIONS                   ################
##############                                                ################
##############################################################################
##############################################################################

example_with_satisfiable_cnf_via_UP = False   # Boolean : True or False

##############################################################################





class CNF_generator():
    def __init__(self, 
        lenght_cnf = 4, 
        lenght_clause = 4, 
        lenght_clause_random = False, 
        satisfiable = True,
        horn = True, 
        binary = True,
        verbose = False):

        self.cnf_dict = {}
        self.lenght_cnf = lenght_cnf
        self.lenght_clause = lenght_clause
        self.lenght_clause_random = lenght_clause_random
        self.satisfiable = satisfiable
        self.horn = horn
        self.binary = binary
            
        if not(lenght_clause_random) and self.binary:
            self.lenght_clause = 2
        # else:
        #   pass

        self.create_new_cnf()
        if verbose:
            print()
            print('******************')
            print('        CNF       ')
            print('******************')
            self.print_cnf()
        

    def create_new_cnf(self):
        for i in range(self.lenght_cnf):
            clause_name = "C"+str(i)
            clause_dict = {}
            variable_value = True
            for j in range(self.lenght_clause):
                variable_name = "X"+str(i+j)
                clause_dict[variable_name] = variable_value
                variable_value = not(variable_value)
            self.cnf_dict[clause_name] = clause_dict

        clause_name = "C"+str(self.lenght_cnf)
        clause_dict = {}
        variable_value = self.satisfiable
        variable_name = "X"+str(self.lenght_cnf)
        clause_dict[variable_name] = variable_value
        self.cnf_dict[clause_name] = clause_dict


    def print_cnf(self):
        print(' CNF = {  ')
        for key_cnf, value_cnf in self.cnf_dict.items():
            clause = self.cnf_dict[key_cnf]
            string_clause = ''
            for key, value in clause.items():
                variable_key = key
                variable_value = value
                if variable_value:
                    string_clause = string_clause + variable_key + ' OR '
                else:
                    string_clause = string_clause + 'NOT(' + variable_key + ') OR '
            string_clause = string_clause[:-4] + ','
            print('clause', key_cnf,':  ', string_clause)

        print(' }  ')


    def print_cnf_dict(self):
        print('*******')
        print(self.cnf_dict)
        print('*******')


    def get_items(self):
        if key_cnf in self.cnf_dict:
            clause = self.cnf_dict[key_cnf]
        else:
            clause = None
        return clause


    def get_clause(self, key_cnf):
        if key_cnf in self.cnf_dict:
            clause = self.cnf_dict[key_cnf]
        else:
            clause = None
        return clause

    def get_clause_variable(self, key_cnf, key_variable):
        variable = {}
        if key_variable in self.cnf_dict[key_cnf]:
            variable[key_variable] = self.cnf_dict[key_cnf][key_variable] 
        else:
            variable = None
        return variable

        
    def delete_clause(self, key_cnf):
        self.cnf_dict.pop(key_cnf)

    def delete_clause_variable(self, key_cnf, key_variable):
        self.cnf_dict[key_cnf].pop(key_variable)

    def check_clause(self, key_cnf):
        if key_cnf in self.cnf_dict:
            return True
        else:
            return False

    def check_clause_variable(self, key_cnf, key_variable):
        if key_variable in self.cnf_dict[key_cnf]:
            return True
        else:
            return False

    def __setitem__(self, key, item):
        self.cnf_dict[key] = item

    def __getitem__(self, key):
        return self.cnf_dict[key]

    def __repr__(self):
        return repr(self.cnf_dict)

    def __len__(self):
        return len(self.cnf_dict)

    def __delitem__(self, key):
        del self.cnf_dict[key]

    def clear(self):
        return self.cnf_dict.clear()

    def copy(self):
        return self.cnf_dict.copy()

    def has_key(self, k):
        return k in self.cnf_dict

    def update(self, *args, **kwargs):
        return self.cnf_dict.update(*args, **kwargs)

    def keys(self):
        return self.cnf_dict.keys()

    def values(self):
        return self.cnf_dict.values()

    def items(self):
        return self.cnf_dict.items()

    def pop(self, *args):
        return self.cnf_dict.pop(*args)

    def __cmp__(self, cnf_dict_):
        return self.__cmp__(self.cnf_dict, cnf_dict_)

    def __contains__(self, item):
        return item in self.cnf_dict

    def __iter__(self):
        return iter(self.cnf_dict)

    def __unicode__(self):
        return unicode(repr(self.cnf_dict))








class Unit_Propagation_with_DataStructure():
    def __init__(self, 
                cnf):
    
        self.Interpretation = []
        self.Interpretation_I = []

        # 1 step: create the array with the lists
        self.data_structure = self.Build_Data_Structure(verbose = True)

        print('')
        print(' * * * * * * * * * * * * * * * * * * * * ')
        print('')

        # 2 step:  scan the CNF to find unitary clauses
        self.scan_cnf_to_find_unit_clauses(cnf)

        # 3 step:  accumulate partial interpretations
        self.Interpretation = self.Interpretation_I

        # 4..n steps: repeat simplification of CNF by propagation on new unitary 
        #              variable found, else 
        while len(self.Interpretation_I)>0:
            self.delete_cnf_clauses()
            if len(self.Interpretation_I)>0:
                self.Interpretation.append(self.Interpretation_I)
        
        if len(self.Interpretation) == len(self.data_structure):
            print()
            print('******************************************')
            print('         Satisfiable Model found          ')
            print('******************************************')
            print('Model: ', self.Interpretation)
        elif len(self.Interpretation) > 0:
            print()
            print('******************************************')
            print('         Partial interpretation           ')
            print('  No more unitary variable in this CNF    ')
            print('******************************************')
            print('Partial intepretation: ', self.Interpretation)
        else:
            print()
            print('******************************************')
            print('  No unitary variable found in this CNF   ')
            print('******************************************')
            print('Partial intepretation set is EMPTY')
            


    ####################################################################
    ####################################################################
    ##### THIS FUNCTION CREATES THE DATA_STRUCTURE TO LINEARISE  #######
    #####                THE UNIT PROPAGATION ALGORITHM          #######
    #################################################################### 

    def Build_Data_Structure(self, verbose = False):
        self.data_structure = {}
        for key_cnf, value_cnf in cnf.items():
            clause = cnf[key_cnf]
            for key, value in clause.items():
                if key in self.data_structure:
                    self.data_structure[key].append(key_cnf)
                else:
                    self.data_structure[key] = [key_cnf]

        if verbose:
            print()
            print(' * * * * * * * * * * * * * * * * * * * * ')
            print('  First Step:  Buid the Data Structure   ')
            print(' * * * * * * * * * * * * * * * * * * * * ')
            for key, value in self.data_structure.items():
                stringa = ''
                for i in range(len(value)):
                    stringa += ' ' + value[i]

                print(key,':  ', stringa)

        return self.data_structure

    ####################################################################
    ####################################################################


    def scan_cnf_to_find_unit_clauses(self,cnf):
        for key_cnf, value_cnf in cnf.items():
            if len(value_cnf) == 1:
                self.Interpretation_I.append(value_cnf)

    def delete_cnf_clauses(self):
        if len(self.Interpretation_I) != 0: 
            self.Interpretation_II = []
            print('Unitary variable(s) found: ', self.Interpretation_I)
            
            for i in range(len(self.Interpretation_I)):
                variable_cnf = list(self.Interpretation_I[i].keys())[0]
                variable_value_cnf = self.Interpretation_I[i][variable_cnf]
                print('Found',variable_cnf, 'in following clause(s): ',  self.data_structure[variable_cnf])
                for j in range(len(self.data_structure[variable_cnf])):
                    key_clause = self.data_structure[variable_cnf][j]
                    if (variable_value_cnf == cnf.get_clause_variable(key_clause,variable_cnf)[variable_cnf]):
                        cnf.delete_clause(key_clause)
                        print('Simplify CNF by eliminating', variable_cnf,'in', key_clause, 'and eliminates clause from CNF')
                        cnf.print_cnf()
                    else:
                        cnf.delete_clause_variable(key_clause,variable_cnf)
                        print('Simplify ', key_clause, 'by eliminating', variable_cnf,'in', key_clause)
                        cnf.print_cnf()
                        if len(cnf[key_clause]) == 1:
                            self.Interpretation_II.append(cnf[key_clause])
            
            self.Interpretation_I = self.Interpretation_II
            print('***********************************')

        else:
            pass




cnf = CNF_generator(lenght_cnf = 10, satisfiable = example_with_satisfiable_cnf_via_UP, verbose = True)

print()
print('******************************************')
print('    Unit propagation with Data Structure    ')
print('******************************************')

Unit_Propagation_with_DataStructure(cnf=cnf)

print('')


# A SCOPO DI TEST PER I METODI DELLA CLASSE CNF_generator
# if cnf.check_clause('C80'):
#     print('clause C0:' , cnf.get_clause('C80'))
# else:
#     print('this value is not present')

# if cnf.check_clause_variable('C1', 'X20'):
#     print('variable :' , cnf.get_clause_variable('C1', 'X2'))
# else:
#     print('this value is not present')  

# print('Delete C0') 
# cnf.delete_clause('C0')
# print('Delete C1 X2') 
# cnf.delete_clause_variable('C1', 'X2')

# cnf.print_cnf()
# cnf.print_cnf_dict()



