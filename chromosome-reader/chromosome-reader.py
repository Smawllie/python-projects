class Chromosome:
    '''A class to represent a chromosome'''
    def __init__(self):
        ''' (Chromosome) -> NoneType
        Creates an instance of Chromosome
        '''
        # Create a dictionary with the keys representing the positions (int)
        # and the values retreived being the chromosome pairs (str)
        self._pos_to_pair = {}

    def __str__(self):
        ''' (Chromosome) -> str
        Returns a string representation of the data within this chromosome
        '''
        # Grab the list of tuples (pos_num, pair_str) using get_data method
        info_list = self.get_data()
        # Create an output to return how many chromosome pairs exist within
        # this chromosome
        output = ("This chromosome contains " + str(len(info_list)) +
                  " pair(s)" + " at position(s)")
        for pos_pair in info_list:
            (pos_num, pair_str) = pos_pair
            pos_str = str(pos_num)
            output += ", " + pos_str + "->" + pair_str
        return output

    def set_by_pos(self, pos_num, pair_str):
        ''' (Chromosome, int, str) -> NoneType
        Sets the position of a given chromosome position (pos_num) to a given
        chromosome pair (pair_str). Chromosomes start counting from 0 and the
        position starts counting from 0
        REQ: pos_num >= 0
        '''
        # If chromosome position already exists in dictionary, functionality is
        # as wanted because the old pair value is removed and new pair value is
        # used
        self._pos_to_pair[pos_num] = pair_str

    def get_by_pos(self, pos_num):
        ''' (Chromosome, int) -> str
        Returns a chromosome pair given a chromosome position (pos_num)
        REQ: pos_num >= 0
        '''
        return self._pos_to_pair[pos_num]

    def get_data(self):
        ''' (Chromosome) -> list of tuple (int, str)
        Returns all chromosome information as a list of tuples (chromosome
        position, chromosome pair)
        '''
        info_list = []
        # Loop through all positions in Chromosome
        for pos_num in self._pos_to_pair:
            # Obtain position number and chromosome pair from dictionary
            pair_str = self._pos_to_pair[pos_num]
            # Create tuple and put in list
            info_list.append((pos_num, pair_str))
        return info_list


class Animal:
    ''' A class to represent an animal'''
    def __init__(self, id_number):
        ''' (Animal, str) -> NoneType
        Creates an instance of animal given an id_number
        REQ: id_number must be a length of at least 4 characters (e.g. '4132')
        '''
        self._id = id_number
        # Initialize a dictionary with keys being the chromosome number and the
        # values being an instance of Chromosome
        self._chromnum_to_chrom = {}
        # Initialize a dictionary with keys being the marker id and the values
        # being a tuple of a Chromosome, a position, and the chromosome #:
        # (Chromosome, pos_num, chrom_num)
        self._marker_to_chrompos = {}

    def __str__(self):
        ''' (Animal) -> str
        Returns a string representation of a given animal
        '''
        # Obtain animal's data
        info_list = self.get_data()
        # Create an output for how many chromosome pairs there are
        output = ("This animal contains " + str(len(info_list)) +
                  " chromosome pair(s) at position(s)")
        # Loop through all the chromosome pairs and add them to the output
        for chrom_pos_pair in info_list:
            (chrom_num, pos_num, pair_str) = chrom_pos_pair
            output += (", " + str(chrom_num) + "-" + str(pos_num) + "->" +
                       pair_str)
        return output

    def set_id(self, new_id):
        '''(Animal, str) -> NoneType
        Sets the id of animal to new_id
        REQ: new_id must be a length of at least 4 characters
        '''
        self._id = new_id

    def get_id(self):
        ''' (Animal) -> str
        Returns the id number of an animal
        '''
        return self._id

    def set_by_pos(self, chrom_num, pos_num, pair_str):
        ''' (Animal, int, int, str) -> NoneType
        Sets the given position (pos_num) at the given chromosome number
        (chrom_num) to the given chromosome pair (pair_str).
        REQ: pos_num >= 0
        REQ: chrom_num >= 0
        REQ: length of pair_str must be 2 (e.g. 'AT' or 'CG')
        '''
        # Check if the chromosome already exists in this animal, and obtain the
        # chromosome if it does
        if chrom_num in self._chromnum_to_chrom:
            chrom = self._chromnum_to_chrom[chrom_num]
        # If not, create a new chromosome
        else:
            chrom = Chromosome()

        # First store chromosome pair in Chromosome class at given position
        chrom.set_by_pos(pos_num, pair_str)
        # Then store chromosome in dictionary, or re-store if chromosome
        # already existed
        self._chromnum_to_chrom[chrom_num] = chrom

    def get_by_pos(self, chrom_num, pos_num):
        ''' (Animal, int, int) -> str
        Returns a chromosome pair (str) when given a chromosome number
        (chrom_num) and a position (pos_num)
        REQ: chrom_num >= 0
        REQ: pos_num >= 0
        '''
        # Retrieve the chromosome from the dictionary using the chromosome
        # number
        chrom = self._chromnum_to_chrom[chrom_num]
        return chrom.get_by_pos(pos_num)

    def set_marker(self, marker_id, chrom_num, pos_num):
        ''' (Animal, str, int, int) -> NoneType
        Sets a given marker (marker_id) to point to a given position (pos_num)
        in a given chromosome number (chrom_num)
        REQ: chrom_num >= 0
        REQ: pos_num >= 0
        '''
        # Check for the chromosome existing, so that it doesn't
        # have to be done later in set_by_marker
        # Check if the chromosome already exists in this animal, and obtain the
        # chromosome if it does
        if chrom_num in self._chromnum_to_chrom:
            chrom = self._chromnum_to_chrom[chrom_num]
        # If not, create a new chromosome
        else:
            chrom = Chromosome()

        # If marker already exists, it will be overwritten which is wanted
        # functionality
        self._marker_to_chrompos[marker_id] = (chrom, pos_num, chrom_num)

    def set_by_marker(self, marker_id, pair_str):
        ''' (Animal, str, str) -> NoneType
        Sets a given marker (marker_id) to point to a given chromosome pair
        (pair_str)
        REQ: length of pair_str must be 2 (e.g. 'AT' or 'CG')
        '''
        # Grab the saved Chromosome, position and chromosome number from
        # dictionary
        (chrom, pos_num, chrom_num) = self._marker_to_chrompos[marker_id]
        # Set the chromosome position to the given chromosome pair
        chrom.set_by_pos(pos_num, pair_str)
        # Then save chromosome in dictionary
        self._chromnum_to_chrom[chrom_num] = chrom

    def get_by_marker(self, marker_id):
        ''' (Animal, str) -> str
        Returns a chromosome pair given a marker (marker_id)
        '''
        # Grab saved Chromosome, position and chromosome number
        (chrom, pos_num, chrom_num) = self._marker_to_chrompos[marker_id]
        return chrom.get_by_pos(pos_num)

    def get_chromosome(self, chrom_num):
        ''' (Animal, int) -> Chromosome
        Returns a Chromosome given a chromosome number (chrom_num)
        REQ: chrom_num >= 0
        '''
        # Return the chromosome using chrom_num as the key
        return self._chromnum_to_chrom[chrom_num]

    def set_chromosome(self, chrom_num, chromosome):
        '''(Animal, int, Chromosome) -> NoneType
        Sets a given chromosome to the chromosome number (chrom_num) of Animal
        REQ: chrom_num >= 0
        '''
        # Now the chromosome is shared between this object and the object where
        # chromosome came from
        self._chromnum_to_chrom[chrom_num] = chromosome

    def test(self, query):
        '''(Animal, Query) -> bool
        Returns True or False if the given query of chromosome pairs matches
        the Animal's chromosome pairs
        '''
        match = False
        sex_chromosome = 22
        # Create an empty dictionary to hold memory nucleotides
        num_to_nuc = {}
        # Obtain all data list (holds tuple of: (chrom_num, pos_num,
        # pair_str) in given Query
        data_list = query.get_data()
        list_index = 0
        # First continue run variable is for the next loop. It is initialized
        # here, so that it can be changed to False, if there are no valid
        # queries for this Animal
        cont_run_query = True
        # This continue run variable is for the current loop which checks if
        # the query's chromosome pair exists in the animal
        cont_run_anim_pair = True
        while(cont_run_anim_pair):
            # Obtain the chromosome pair at given chromosome number and pos
            # Animal chromosomes  will have the added word of animal and query
            # chromosomes will have no additional words
            try:
                (chrom_num, pos_num, pair_str) = data_list[list_index]
                animal_pair_str = self.get_by_pos(chrom_num, pos_num)
                cont_run_anim_pair = False
            except KeyError:
                # If no chromosome pair exists in chromosome 23 (index 22) and
                # Animal is Male then query is rejected. Otherwise, query
                # continues
                if chrom_num == sex_chromosome and type(self) is Male:
                    cont_run_query = False
                    cont_run_anim_pair = False
                else:
                    list_index += 1
                    # If data_list ends, then there are no pairs to check, but
                    # query is not rejected
                    if list_index >= len(data_list):
                        cont_run_anim_pair = False
                        cont_run_query = False
                        match = True
            except IndexError:
                # If there's an index error, that means there's no questions to
                # check, so loops end and test should return True
                cont_run_anim_pair = False
                cont_run_query = False
                match = True
        # Loop through each tuple (chrom_num, pos_num, pair_str)
        # While loop because want to stop when one of the questions fail
        while(cont_run_query):
            # Chromosome pairs split into single nucleotides for clarity
            (first_animal_nuc, second_animal_nuc) = animal_pair_str
            (first_nuc, second_nuc) = pair_str
            # Check if first and second nucleotide of query's chromosome pair
            # are digits
            is_first_digit = first_nuc.isdigit()
            is_second_digit = second_nuc.isdigit()
            if is_first_digit:
                # If first nucleotide is a digit and it's not in memory
                # nuc dictionary, add it to the dictionary, otherwise continue
                if not (first_nuc in num_to_nuc):
                    # Set the memory nucleotide to the key and the animal's
                    # chromosome's nucleotide to the value. This memory nuc
                    # will point to this value for the entire test and cannot
                    # be changed
                    num_to_nuc[first_nuc] = first_animal_nuc
                # Now set the memory nucleotide to the nucleotide it's pointing
                # to in the dictionary
                first_nuc = num_to_nuc[first_nuc]
            # Do the same for the second digit
            if is_second_digit:
                if not (second_nuc in num_to_nuc):
                    num_to_nuc[second_nuc] = second_animal_nuc
                second_nuc = num_to_nuc[second_nuc]
            # This should now only consist of proper nucleotides (no digits)
            pair_str = first_nuc + second_nuc
            # If Query's chromosome pair matches Animal's chromosome pair,
            # check the next pair. Otherwise, no match and stop the loop
            if pair_str == animal_pair_str:
                list_index += 1
                # Also need to check if data list has ended
                if list_index == len(data_list):
                    # No more data to check, so if the loop has gotten this far
                    # that means all the chromosome pairs matched
                    match = True
                    cont_run_query = False
                else:
                    # If data list has not ended
                    cont_run_anim_pair = True
                    while(cont_run_anim_pair):
                        # Obtain the chromosome pair at given chromosome number
                        # Animal chromosomes will have the added word of animal
                        # and query chromosomes will have no additional words
                        try:
                            (chrom_num, pos_num, pair_str) = data_list[
                                list_index]
                            animal_pair_str = self.get_by_pos(
                                chrom_num, pos_num)
                            cont_run_anim_pair = False
                        except KeyError:
                            # If no chromosome pair exists in chromosome 23
                            # (index 22) and Animal is Male then query is
                            # rejected. Otherwise, query continues
                            # We don't check for index error here because,
                            # index is checked for in the previous code
                            if (chrom_num == sex_chromosome and
                                type(
                                    self) is Male):
                                cont_run_query = False
                                cont_run_anim_pair = False
                            else:
                                list_index += 1
                                # If data_list ends, then there are no pairs to
                                # check, but query is not rejected
                                if list_index >= len(data_list):
                                    cont_run_anim_pair = False
                                    cont_run_query = False
                                    match = True
            else:
                cont_run_query = False
        return match

    def get_data(self):
        ''' (Animal) -> list of tuples (int, int, str)
        Returns all animal information as a list of tuples (chromosome number,
        chromosome position, chromosome pair) in a given Animal
        '''
        info_list = []
        # Loop through all chromosomes in Animal
        for chrom_num in self._chromnum_to_chrom:
            # Obtain chromosome number and Chromosome from dictionary
            chrom = self._chromnum_to_chrom[chrom_num]
            # Obtain list of tuples of position number and chromosome pair from
            # Chromosome
            pos_pair_list = chrom.get_data()
            # Loop through all positions in each chromosome
            for pos_pair_tuple in pos_pair_list:
                # Create tuple and put in list
                (pos_num, pair_str) = pos_pair_tuple
                info_list.append((chrom_num, pos_num, pair_str))
        return info_list


class Human(Animal):
    '''A class to represent a human'''
    def __str__(self):
        ''' (Human) -> str
        Returns a string representation of a given human
        '''
        # Obtain human's data
        info_list = self.get_data()
        # Create an output for how many chromosome pairs there are
        output = ("This human contains " + str(len(info_list)) +
                  " chromosome pair(s) at position(s)")
        # Loop through all the chromosome pairs and add them to the output
        for chrom_pos_pair in info_list:
            (chrom_num, pos_num, pair_str) = chrom_pos_pair
            output += (", " + str(chrom_num) + "-" + str(pos_num) + "->" +
                       pair_str)
        return output


class Male(Human):
    '''A class to represent a male human'''
    def __str__(self):
        ''' (Male) -> str
        Returns a string representation of a given male
        '''
        # Obtain male's data
        info_list = self.get_data()
        # Create an output for how many chromosome pairs there are
        output = ("This male contains " + str(len(info_list)) +
                  " chromosome pair(s) at position(s)")
        # Loop through all the chromosome pairs and add them to the output
        for chrom_pos_pair in info_list:
            (chrom_num, pos_num, pair_str) = chrom_pos_pair
            output += (", " + str(chrom_num) + "-" + str(pos_num) + "->" +
                       pair_str)
        return output


class Female(Human):
    '''A class to represent a female human'''
    def __str__(self):
        ''' (Female) -> str
        Returns a string representation of a given female
        '''
        # Obtain female's data
        info_list = self.get_data()
        # Create an output for how many chromosome pairs there are
        output = ("This female contains " + str(len(info_list)) +
                  " chromosome pair(s) at position(s)")
        # Loop through all the chromosome pairs and add them to the output
        for chrom_pos_pair in info_list:
            (chrom_num, pos_num, pair_str) = chrom_pos_pair
            output += (", " + str(chrom_num) + "-" + str(pos_num) + "->" +
                       pair_str)
        return output

    def procreate(self, male, binder):
        ''' (Female, Male, Binder) -> Male or Female
        Returns a child (Male or Female) given a dad (male), a mom (self) and a
        binding chromosome (binder)
        '''
        # Retrieve tuple data from binder (chrom_num, pos_num, maternal_str)
        # and child's sex
        (binder_list, sex) = binder.get_data()
        # Create child based on sex given. For the child's id, the first 3
        # numbers will be taken from the mom's id and the rest from the dad's
        # All children from these two parents will have the same id. If they
        # want to be changed, they need to be changed manually
        mom_id = self.get_id()
        dad_id = male.get_id()
        child_id = mom_id[0:3] + dad_id[3:]
        if sex == 'F':
            child = Female(child_id)
        else:
            child = Male(child_id)
        # This continue run variable is for the loop that sets the chromosomes
        # for the child
        cont_run_build_child = True
        # If the chromosome in binder does not exist in both the male and
        # female, the binder will skip over that chromosome.
        # Will use a while loop to find if the chromosome exists in both
        # parents
        list_index = 0
        cont_run_chrom_found = True
        while(cont_run_chrom_found):
            try:
                # Set the variables in the tuple of the binder data
                (chrom_num, pos_num, maternal_str) = binder_list[list_index]
                # Finds the chromosome pair at the given position for parents
                mom_pair = self.get_by_pos(chrom_num, pos_num)
                dad_pair = male.get_by_pos(chrom_num, pos_num)
                # If both pairs are found, chromosome is found, so loop stops
                cont_run_chrom_found = False
            except IndexError:
                # If an index error occurs, the binder list is empty, so child
                # is finished building
                cont_run_build_child = False
                cont_run_chrom_found = False
            except KeyError:
                # If a key error occurs, either a mom or dad chromosome was not
                # found, so we move on to the next binder pair
                list_index += 1
                if list_index >= len(binder_list):
                    # If binder has no more chromosome to check, child is
                    # finished being created
                    cont_run_build_child = False
                    cont_run_chrom_found = False
        # Once both the mom and dad chromosome pairs are found, this loop
        # places the chromosomes in the appropriate position based on
        # left/right maternality. We need 2 loops at the start and end, so that
        # we can stop running the loops as soon as possible
        while(cont_run_build_child):
            if maternal_str == 'LM':
                # If this chromosome pair is left maternal, we care only about
                # the left nucleotide in the mom and the right nucleotide in
                # the dad
                left_mom = mom_pair[0]
                right_dad = dad_pair[1]
                # Concatening the two nucleotides will create the child pair
                # based on left maternality
                child_pair_str = left_mom + right_dad
                # Chromosome pair set
                child.set_by_pos(chrom_num, pos_num, child_pair_str)
            else:
                # If chromosome is right maternal, we care only about the
                # right nucleotide in the mom and the left nucleotide in the
                # dad
                left_dad = dad_pair[0]
                right_mom = mom_pair[1]
                child_pair_str = left_dad + right_mom
                child.set_by_pos(chrom_num, pos_num, child_pair_str)
            # Now the next chromosome in the binder needs to be found. We will
            # use the same loop we used before
            cont_run_chrom_found = True
            while(cont_run_chrom_found):
                list_index += 1
                if list_index >= len(binder_list):
                    # If binder has no more chromosome to check, child is
                    # finished being created
                    cont_run_build_child = False
                    cont_run_chrom_found = False
                else:
                    try:
                        # Set the variables in the tuple of the binder data
                        (chrom_num, pos_num, maternal_str) = binder_list[
                            list_index]
                        # Finds the chromosome pair at the given position for
                        # parents
                        mom_pair = self.get_by_pos(chrom_num, pos_num)
                        dad_pair = male.get_by_pos(chrom_num, pos_num)
                        # Chromosome fining loop stops when chromosome is found
                        cont_run_chrom_found = False
                    except KeyError:
                        # If a key error occurs, either a mom or dad chromosome
                        # was not found, so we move on to the next binder pair
                        pass

        return child


class Query():
    '''A class to represent a query for animals' chromosomes'''
    # Not inheritting from Animal because don't want the functionality of
    # Animals being able to test Queries or being inputted without ids
    def __init__(self):
        ''' (Query) -> NoneType
        Creates an instance of a query
        '''
        # Initialize a dictionary with keys being the chromosome number and the
        # values being an instance of Chromosome
        self._chromnum_to_chrom = {}
        # Initialize a dictionary with keys being the marker id and the values
        # being a tuple of a Chromosome, a position, and the chromosome #:
        # (Chromosome, pos_num, chrom_num)
        self._marker_to_chrompos = {}

    def __str__(self):
        ''' (Query) -> str
        Returns a string representation of the chromosome pairs in the query
        '''
        # Obtain query's data
        info_list = self.get_data()
        # Create an output for how many chromosome pairs there are
        output = ("This query contains " + str(len(info_list)) +
                  " chromosome pair(s) at position(s)")
        # Loop through all the chromosome pairs and add them to the output
        for chrom_pos_pair in info_list:
            (chrom_num, pos_num, pair_str) = chrom_pos_pair
            output += (", " + str(chrom_num) + "-" + str(pos_num) + "->" +
                       pair_str)
        return output

    def set_by_pos(self, chrom_num, pos_num, pair_str):
        ''' (Query, int, int, str) -> NoneType
        Sets the given position (pos_num) at the given chromosome number
        (chrom_num) to the given chromosome pair (pair_str).
        REQ: pos_num >= 0
        REQ: chrom_num >= 0
        REQ: length of pair_str must be 2 (e.g. 'AT' or 'CG')
        '''
        # Check if the chromosome already exists in this query, and obtain the
        # chromosome if it does
        if chrom_num in self._chromnum_to_chrom:
            chrom = self._chromnum_to_chrom[chrom_num]
        # If not, create a new chromosome
        else:
            chrom = Chromosome()

        # First store chromosome pair in Chromosome class at given position
        chrom.set_by_pos(pos_num, pair_str)
        # Then store chromosome in dictionary, or re-store if chromosome
        # already existed
        self._chromnum_to_chrom[chrom_num] = chrom

    def get_by_pos(self, chrom_num, pos_num):
        ''' (Query, int, int) -> str
        Returns a chromosome pair (str) when given a chromosome number
        (chrom_num) and a position (pos_num)
        REQ: chrom_num >= 0
        REQ: pos_num >= 0
        '''
        # Retrieve the chromosome from the dictionary using the chromosome
        # number
        chrom = self._chromnum_to_chrom[chrom_num]
        return chrom.get_by_pos(pos_num)

    def set_marker(self, marker_id, chrom_num, pos_num):
        ''' (Query, str, int, int) -> NoneType
        Sets a given marker (marker_id) to point to a given position (pos_num)
        in a given chromosome number (chrom_num)
        REQ: chrom_num >= 0
        REQ: pos_num >= 0
        '''
        # Check for the chromosome existing, so that it doesn't
        # have to be done later in set_by_marker
        # Check if the chromosome already exists in this query, and obtain the
        # chromosome if it does
        if chrom_num in self._chromnum_to_chrom:
            chrom = self._chromnum_to_chrom[chrom_num]
        # If not, create a new chromosome
        else:
            chrom = Chromosome()

        # If marker already exists, it will be overwritten which is wanted
        # functionality
        self._marker_to_chrompos[marker_id] = (chrom, pos_num, chrom_num)

    def set_by_marker(self, marker_id, pair_str):
        ''' (Query, str, str) -> NoneType
        Sets a given marker (marker_id) to point to a given chromosome pair
        (pair_str)
        REQ: length of pair_str must be 2 (e.g. 'AT' or 'CG')
        '''
        # Grab the saved Chromosome, position and chromosome number from
        # dictionary
        (chrom, pos_num, chrom_num) = self._marker_to_chrompos[marker_id]
        # Set the chromosome position to the given chromosome pair
        chrom.set_by_pos(pos_num, pair_str)
        # Then save chromosome in dictionary
        self._chromnum_to_chrom[chrom_num] = chrom

    def get_by_marker(self, marker_id):
        ''' (Query, str) -> str
        Returns a chromosome pair given a marker (marker_id) and Query
        '''
        # Grab saved Chromosome, position and chromosome number
        (chrom, pos_num, chrom_num) = self._marker_to_chrompos[marker_id]
        return chrom.get_by_pos(pos_num)

    def get_data(self):
        ''' (Query) -> list of tuples (int, int, str)
        Returns all query information as a list of tuples (chromosome number,
        chromosome position, chromosome pair) in a given Query
        '''
        info_list = []
        # Loop through all chromosomes in Query
        for chrom_num in self._chromnum_to_chrom:
            # Obtain chromosome number and Chromosome from dictionary
            chrom = self._chromnum_to_chrom[chrom_num]
            # Obtain list of tuples of position number and chromosome pair from
            # Chromosome
            pos_pair_list = chrom.get_data()
            # Loop through all positions in each chromosome
            for pos_pair_tuple in pos_pair_list:
                # Create tuple and put in list
                (pos_num, pair_str) = pos_pair_tuple
                info_list.append((chrom_num, pos_num, pair_str))
        return info_list


class Binder:
    " A class to represent a binding chromosome"
    def __init__(self):
        ''' (Binder) -> NoneType
        Creates an instance of Binder
        '''
        # List of tuples (chrom_num, pos_num, maternal_str) which represent
        # chromosome pairs and whether they are right or left maternal
        self._chrom_list = []
        # As of now, this can either be 'M' (Male) or 'F' (Female)
        self._sex = ''

    def __str__(self):
        ''' (Binder) -> str
        Returns a string representation of the chromosome pairs in the binder
        '''
        # Obtain binder's data
        info_tuple = self.get_data()
        # Obtain the list of chromosome pairs and sex from the data
        (chrom_list, sex) = info_tuple
        if sex == 'F':
            sex_str = 'female'
        else:
            sex_str = 'male'
        # Create an output for how many chromosome pairs there are
        output = ("This binder creates a " + sex_str + " and contains " +
                  str(len(chrom_list)) +
                  " chromosome pair(s) at position(s)")
        # Loop through all the chromosome pairs and add them to the output
        for chrom_pos_maternal in chrom_list:
            (chrom_num, pos_num, maternal_str) = chrom_pos_maternal
            output += (", " + str(chrom_num) + "-" + str(pos_num) + "(" +
                       maternal_str + ")")
        return output

    def set_by_pos(self, chrom_num, pos_num, maternal_str):
        ''' (Binder, int, int, str) -> NoneType
        Sets a Binder to be either right or left maternal (maternal_str) for a
        given chromosome pair (chrom_num, pos_num)
        REQ: chrom_num >= 0
        REQ: pos_num >= 0
        REQ: maternal_str is 'LM' (left maternal) or 'RM' (right maternal)
        '''
        self._chrom_list.append((chrom_num, pos_num, maternal_str))

    def set_sex(self, sex):
        ''' (Binder, str) -> NoneType
        Sets a Binder to produce either male or female offspring
        REQ: sex is 'F' (female) or 'M' (male)
        REQ: set_sex needs to be called before a Female can call procreate
        '''
        self._sex = sex

    def get_data(self):
        ''' (Binder) -> tuple of list of tuples (chromosome number, chromosome
        position, left or right maternal) and sex
        Returns the chromosome data of a given Binder
        '''
        return (self._chrom_list, self._sex)

# main test function
if(__name__ == "__main__"):
    # create a new Male client with ID 12345
    father = Male('12345')
    # create a new Female client with ID 67890
    mother = Female('67890')
    # set chromosome pair 12 position 45 to be AG
    father.set_by_pos(12, 45, 'AG')
    mother.set_by_pos(12, 45, 'CT')
    # set chromosome marker rs12345 to refer to chromosome
    # pair 3, position 97
    father.set_marker('rs12345', 3, 97)

    # set marker rs12345 to be GT
    father.set_by_marker('rs12345', 'GT')
    # this should return "AG"
    result_str = father.get_by_pos(12, 45)
    # this should return "GT"
    result_str2 = father.get_by_marker('rs12345')
    c = father.get_chromosome(3)
    # This will set father's pair 3-85 to be "TA"
    c.set_by_pos(85, 'TA')
    # Now mother and father share a chromosome pair, updating
    # one will update the other
    mother.set_chromosome(7, c)

    # create a new query object
    query = Query()
    query.set_by_pos(12, 45, 'AG')
    # this should return True since 12-45 in the query matches
    # with 12-45 in father
    result = father.test(query)
    query.set_by_pos(12, 45, 'A1')
    query.set_marker('rs12345', 3, 97)
    # now the query will only work if 12-45 is AX and 3-97 is XT for
    # some value of X
    query.set_by_marker('rs12345', '1T')

    # create a new binder object
    binder = Binder()
    # set chromosome pair position 45 to be left maternal
    # (this means that the offspring will have 12-45 equal to CG
    # e.g., gets the left C from mother and the right G from father)
    binder.set_by_pos(12, 45, 'LM')

    # this means any offspring created with this binder will be female
    binder.set_sex("F")
    child = mother.procreate(father, binder)
