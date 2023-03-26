# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Mathis LAIR, Maxime GUIBERT, Audrey DAMIBA, Melissa LACHEB
# Created Date: 2023-03-25
# version ='1.0'
# ---------------------------------------------------------------------------
""" This module as for objective to do somes operations to automata 
    Operations availables are:
        -standardize
        -complete
        -determinize
        -recognize a word

    The module is composed of 3 classes:
        -state: a state of the automata
        -automata: the automata

    The module is also composed of one global constants:
        -characters: a list of all the characters that can be used in the automata
    
    This project is a part of the course SM402I from EFREI Paris (2022-2023)
        
        """

###########################################################
#
#
#                   Global constants
#
#
###########################################################

characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
              'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '&', '@', '!', '#', '$', '%', '^', '*', '(', ')', '_', '+', '-', '=', '{', '}', '[', ']', '|', ':', ';', '"', '<', '>', '?', '/', '~', '`', '.', ',', ' ']

###########################################################
#
#
#                   Utility Functions
#
#
###########################################################


def readword() -> str:
    """
    read a word from the user
    """
    c = input("Enter the word you want to read")
    return c


def group_by_value(d: dict) -> list:
    """
    return a list of list of keys of the dictionary d grouped by value
    """
    result = {}
    for key, value in d.items():
        if value not in result:
            result[value] = [key]
        else:
            result[value].append(key)
    return list(result.values())

###########################################################
#
#
#                   Node Element
#
#
###########################################################


class State():
    def __init__(self, number, start, finish) -> None:
        """
        number: str, the name of the state
        paths: dict of list of str, the key is the label of the path and the value is the list of the target States
        start: bool, True if the State is an initial state
        finish: bool, True if the State is a final state
        """
        self.number = number
        self.paths = {}
        self.finish = finish
        self.start = start

    def add_path(self, label, target):
        """
        add a path to the state
        """
        try:
            # if the state doesn't already have this label we add it
            if target not in self.paths[label]:
                self.paths[label].append(target)
        except:
            self.paths[label] = [target]

###########################################################
#
#
#                   Automata Element
#
#
###########################################################


class automata():
    def __init__(self, file: str) -> None:
        """
        states: list of State, the list of the states of the automata
        labels: list of str, the list of the labels of the automata
        start: str, composed of the name of the initial states
        finish: str, composed of the name of the final states

        -file: str, the name of the file that contains the automata

        -if file is empty, the automata is empty

        functions:
            -is_standard: return True if the automata is standard
            -is_complete: return True if the automata is complete
            -is_deterministic: return True if the automata is deterministic
            -recognize: return True if the word is recognized by the automata
            -standardize: return the standard automata
            -complete: return the complete automata
            -determinize: return the deterministic automata
            -complement: return the complement automata
            -minimize: return the minimized automata

        """
        self.states = []
        self.labels = []
        if file == '':
            return
        with open(file, 'r') as file:
            file_content = file.readlines()
        for i in range(len(file_content)):
            file_content[i] = file_content[i][:-1]
        # we get the number of initial states and the name of the initial states
        [number_of_initial_states, self.start] = file_content[2].split(" ")
        # we get the number of final states and the name of the final states
        [number_of_final_states, self.finish] = file_content[3].split(" ")
        for elem in characters[:int(file_content[1])]:
            if str(characters.index(elem)) in self.finish:
                is_terminal = True  # if the state is a final state we set is_terminal to True
            else:
                is_terminal = False  # if the state is not a final state we set is_terminal to False
            if str(characters.index(elem)) in self.start:
                is_initial = True  # if the state is an initial state we set is_initial to True
            else:
                is_initial = False
            self.states.append(State(elem, is_initial, is_terminal))
        for elem in file_content[5:]:
            if elem[1] not in self.labels:
                # we add the label to the list of labels
                self.labels.append(elem[1])
            self.states[characters.index(str(elem[0]))].add_path(
                elem[1], elem[2])

    def is_standard(self) -> bool:
        """
        return True if the automata is standard
        return False if the automata is not standard
        """
        initial_states = self.start
        if len(self.start) > 1:  # if there is more than one initial state the automata is not standard
            return False
        for elem in self.states:
            for paths, target in elem.paths.items():
                for state in target:
                    # if there is a path that goes to an initial state the automata is not standard
                    if str(state) in initial_states:
                        return False
        return True  # otherwise the automata is standard

    def is_complete(self) -> bool:
        """
        return True if the automata is complete
        return False if the automata is not complete
        """
        for elem in self.states:
            for label in self.labels:
                if label not in elem.paths.keys():
                    # if there is a state that doesn't have a path for each label the automata is not complete
                    return False
        return True  # otherwise the automata is complete

    def is_deterministic(self) -> bool:
        """
        return True if the automata is deterministic
        return False if the automata is not deterministic
        """
        if len(self.start) > 1:
            return False  # if there is more than one initial state the automata is not deterministic
        for elem in self.states:
            for paths, target in elem.paths.items():
                if len(target) > 1:
                    return False  # if there is a path that goes to more than one state the automata is not deterministic
        return True  # otherwise the automata is deterministic

    def complete(self):
        """
        complete the automata
        It will add a new sink state and add a path to it for each label that doesn't have a path
        """
        last_node_number = characters[len(
            self.states)]  # the name of the new state we will add
        self.states.append(
            State(characters[characters.index(last_node_number)+1], False, False))  # we add the new state to the automaton
        for elem in self.states:
            for label in self.labels:
                if label not in elem.paths.keys():  # we look if each label of the alphabet is in the paths of the state
                    elem.paths[label] = ['{}'.format(
                        characters[characters.index(last_node_number)])]  # if not we add a path to the sink state
        return self  # we return the automata with the new state

    def recognise_word(self, word: str) -> bool:
        """
        return True if the word is recognized by the automata
        return False if the word is not recognized by the automata
        recursive function that will look if the word is recognized by the automata

        It take care of the empty word wich is represented by the symbol '&' in the file
        and it take care of the facts that sometimes there are more than one path for a label
        it takes care of the fact that sometimes the automata is not standard and has many initial states
        """
        if word == '&':
            if self.start in self.finish:
                return True
            else:
                return False
        if word == '':
            if self.start in self.finish:
                return True
            else:
                return False
        if self.is_standard() == False:
            for elem in self.states:
                if elem.number in self.start:
                    for paths, target in elem.paths.items():
                        for state in target:
                            if self.recognise_word(word[1:]) == True:
                                return True
            return False
        else:
            for paths, target in self.states[characters.index(self.start)].paths.items():
                if paths == word[0]:
                    for state in target:
                        if self.recognise_word(word[1:]) == True:
                            return True
            return False

    def recognise_words(self, words: list) -> list:
        """
        return a list of booleans that correspond to the list of words
        """
        return [self.recognise_word(word) for word in words]

    def complement(self):
        """
        return the complement of the automata
        It will change the finish state to non final state and vice versa
        """
        new_finish = ""  # we create a new string that will contain the name of the new final states
        for elem in self.states:
            if elem.number not in self.finish:  # if the state is not a final state we add it to the string of the new final states
                new_finish += elem.number
        self.finish = new_finish  # we change the string of the final states

        for elem in self.states:  # we invert for each state if it is final or not
            if elem.finish == True:
                elem.finish = False  # true->false
            else:
                elem.finish = True  # false->true
        return self

    def standardise(self):
        """
        standardise the automata
        """
        if self.is_standard():  # if the automata is already standard we return it
            return
        # we create a new state that will be the new initial state
        new_nodes = State("{}".format(
            characters[len(self.states)]), True, False)
        for elem in self.start:
            for key, value in self.states[int(characters.index(elem))].paths.items():
                for elem in value:
                    # we add the paths of the old initial state to the new initial state
                    new_nodes.add_path(key, elem)

            self.states[int(characters.index(elem))].start = False
            # if the old initial state was final we make the new initial state final
            if self.states[int(characters.index(elem))].finish:
                new_nodes.finish = True
        for elem in self.states:  # we remove the paths that go to the old initial state
            elem.start = False
        # we add the new initial state to the automata
        self.states.append(new_nodes)
        # we change the string of the initial state
        self.start = "{}".format(characters[len(self.states)])

    def determinize(self):
        """
        determinize the automata
        """
        if self.is_deterministic():  # if the automata is already deterministic we
            return
        if not self.is_complete():
            self.complete()  # if the automata is not complete we complete it
        new_nodes = []
        dones = []
        # we create a dictionary that will contain the paths of the new states
        paths = {label: "" for label in self.labels}
        finish = False
        name = ""  # we create a string that will contain the name of the new state
        for elem in self.start:  # we add the paths of the initial state to the dictionary
            name += elem
            for label in self.labels:
                if str(self.states[int(characters.index(elem))].paths[label][0]) not in paths[label]:
                    paths[label] += "".join(
                        self.states[int(characters.index(elem))].paths[label])
            if self.states[int(characters.index(elem))].finish:
                finish = True
        # we create the new initial state
        start_node = State("".join(sorted(name)), True, finish)
        to_compute = []  # we create a list that will contain the states that we will have to compute
        for key, value in paths.items():
            start_node.add_path(key, value)
            if name != value:
                # we add the paths of the initial state to the list
                to_compute.append(value)
        dones.append("".join(sorted(name)))
        new_nodes.append(start_node)
        while(len(to_compute) > 0):  # while there is still states to compute
            paths = {label: "" for label in self.labels}
            finish = False  # we reset the finish variable
            name = "".join(sorted(to_compute[0]))
            for elem in name:  # we compute the paths of the new state
                for label in self.labels:
                    # we add the paths of the old states to the new state
                    if "".join(self.states[int(characters.index(elem))].paths[label]) not in paths[label]:
                        paths[label] += "".join(
                            self.states[int(characters.index(elem))].paths[label])  # we add the paths of the old states to the new state
                # if one of the old state is final the new state is final
                if self.states[int(characters.index(elem))].finish:
                    finish = True
            new_node = State(name, False, finish)
            dones.append(name)
            for key, value in paths.items():  # we add the paths of the new state to the automata
                new_node.add_path(key, "".join(sorted(value)))
            for key, value in paths.items():
                if value not in to_compute and value not in dones:  # if the path is not already in the list we add it
                    to_compute.append(value)
            to_compute.pop(0)
            new_nodes.append(new_node)  # we add the new state to the automata
        states = []
        for state in new_nodes:
            state.number = str(characters[dones.index(state.number)])
        for state in new_nodes:  # we change the paths of the new states
            for key, value in state.paths.items():
                # we change the paths of the new states
                state.paths[key] = [dones.index("".join(sorted(value[0])))]

        self.start = "a"
        self.states = new_nodes

    def minimized(self):
        """
        return a new automata which is the minimal version of the automata
        """
        if not self.complete():
            self.complete()
        if not self.is_deterministic():
            self.determinize()  # if the automata is not complete we complete it
        partitions = [[i for i, state in enumerate(self.states) if not state.finish], [
            i for i, state in enumerate(self.states) if state.finish]]  # we create the partitions
        partition2 = []
        partition3 = []
        working = True  # we create a variable that will be used to know if we have to continue the algorithm
        while working:  # while we have to continue the algorithm
            for elem in partitions:  # we create the new partitions
                if len(elem) == 1:
                    new_partitions = [elem]
                else:
                    partitions_target = {number: "" for number in elem}
                    for number in elem:
                        for label in self.labels:
                            target = self.states[number].paths[label][0]
                            for j in range(len(partitions)):
                                if int(target) in partitions[j]:
                                    partitions_target[number] += str(j)
                    new_partitions = group_by_value(partitions_target)
                for elem in new_partitions:
                    partition2.append(elem)
            if partition2 != partitions:    # if the new partitions are different from the old ones we continue the algorithm
                partitions = partition2
                partition2 = []
            else:
                working = False  # if the new partitions are the same as the old ones we stop the algorithm
        new_nodes = []
        for i, elem in enumerate(partitions):  # we create the new automata
            node_to_add = State(i, False, False)
            # we choose a representative of the partition
            representative = elem[0]
            for label in self.labels:
                # we add the paths of the representative to the new state
                target = self.states[representative].paths[label][0]
                # we add the paths of the representative to the new state
                for j, partition in enumerate(partitions):
                    if int(target) in partition:
                        # we add the paths of the representative to the new state
                        node_to_add.add_path(label, j)
            if any(str(x) in self.start for x in elem):
                # if one of the old state is the start state the new state is the start state
                node_to_add.start = True
            for i in elem:
                # if one of the old state is a finish state the new state is a finish state
                if self.states[i].finish:
                    node_to_add.finish = True
            new_nodes.append(node_to_add)
        self.states = new_nodes  # we change the states of the automata
        self.start = '0'
        # we change the start and finish states of the automata
        self.finish = [i for i, state in enumerate(
            self.states) if state.finish]

###########################################################
#
#
#                   Automata functions
#
#
###########################################################


def print_automata(automata: automata):
    """
    print the automata as a table
    exremple:
      | a | b | c |
      -------------
    0 | 0 | 1 | 2 |
      -------------
    1 | 0 | 1 | 2 |
      -------------
    2 | 0 | 1 | 2 |
      -------------
    """
    # print the first line of the table with the labels
    print("      ", end='')
    size = {}
    for elem in automata.labels:
        size[elem] = 0
    for state in automata.states:
        for key, value in state.paths.items():
            if len(value) > size[key]:
                size[key] = len(value)
    for elem in automata.labels:
        print("| ", end='')
        print(elem, end='')
        print(" "*(2*(size[elem])-1), end='')
    print("|", end='')
    print("\n      ", end='')

    # print the line of dashes

    for key, value in size.items():
        for i in range(value):
            print("____", end='')
    print('')
    for elem in automata.states:
        if elem.finish:
            print("<", end='')  # if the state is a finish state, print a <
        else:
            print(" ", end='')
        if elem.start or elem.finish:
            print("-", end='')
        else:
            print(" ", end='')
        if elem.start:
            print(">", end='')  # if the state is a start state, print a >
        else:
            print(" ", end='')
        print(" ", end='')
        # print the name of the state
        print(characters.index(str(elem.number)), end='')
        print(" ", end='')
        print("|", end='')
        for label in automata.labels:  # print the target of the state for each label
            s = 0
            print(" ", end='')
            if label in elem.paths:
                for target in elem.paths.get(label):
                    print(characters.index(str(target)), end='')
                    # Print a space between each target to make the table more readable
                    print(" ", end='')
                    s += 1

            else:
                print(' ', end='')
                print(" ", end='')
                s += 1
            for i in range(size[label]-s):
                print(" "*2, end='')
            print("|", end='')
        print("\n      ", end='')
        for key, value in size.items():  # print the line of dashes
            for i in range(value):
                print("____", end='')
        print('')


def informations(automate: automata):
    """
    print informations about the automata
    """
    print_automata(automate)
    print("════════════════════════")
    print("Informations about your automata:")
    print("Standard: {}".format(automate.is_standard()))
    print("Complete: {}".format(automate.is_complete()))
    print("Deterministic: {}".format(automate.is_deterministic()))
    print("════════════════════════")

###########################################################
#
#
#                   Menu functions
#
#
###########################################################


def automate_manager(file_name: str):
    """
    User interface to manage an automata from a file
    """
    automate = automata(file_name)
    choice = 0
    choices = []
    while choice <= len(choices)+1:  # while the user doesn't choose to exit
        choices = []
        informations(automate)  # print the automata and its informations
        i = 0
        if not automate.is_standard():  # if the automata is not standard, add the option to standardise it to the menu
            i += 1
            choices.append("sta")
            print("{}-Standardise it".format(i))
        if not automate.is_complete():  # if the automata is not complete, add the option to complete it to the menu
            i += 1
            choices.append("com")
            print("{}-Complete it".format(i))
        if not automate.is_deterministic():  # if the automata is not deterministic, add the option to determinize it to the menu
            i += 1
            choices.append("det")
            print("{}-Determinize it".format(i))
        i += 1
        # add the option to complementarize it to the menu
        choices.append("cop")
        print("{}-Complementarize it".format(i))
        i += 1
        choices.append("min")  # add the option to minimize it to the menu
        print("{}-Minimize it".format(i))
        # add the option to test if a word is recognized by it to the menu
        choices.append("rec")
        i = i+1
        print("{}-Test if a word is recognized by it".format(i))
        choice = int(input())

        # apply the choice

        if choices[choice-1] == "sta":
            automate.standardise()
        if choices[choice-1] == "com":
            automate.complete()
        if choices[choice-1] == "det":
            automate.determinize()
        if choices[choice-1] == "cop":
            automate.complement()
        if choices[choice-1] == "min":
            automate.minimized()
        if choices[choice-1] == "rec":
            x = readword()
            if automate.recognise_word(x):
                print("-----------------------------------")
                print("\n\n The word: {}is recognized \n\n".format(x))
                print("-----------------------------------")
            else:
                print("-----------------------------------")
                print("\n\n The word: {} is not recognized\n\n".format(x))
                print("-----------------------------------")


def main():
    """
    User interface to choose the automata to use
    It looks like this:

    ════════════════════════ ❀•°❀°•❀ ════════════════════════
    Welcome to Your Automata manager
    ════════════════════════ ❀•°❀°•❀ ════════════════════════
    -If you want to import an automata tap 1
    -If you want to use one of the default automata tap 2
    -If you want to create a new automata tap 3
    -If you want to exit tap 4
    """
    choice = 0
    while(choice < 1 or choice > 4):  # while the user doesn't choose a valid option or exit
        print("════════════════════════ ❀•°❀°•❀ ════════════════════════\n\n\n Welcome to Your Automata manager \n\n\n════════════════════════ ❀•°❀°•❀ ════════════════════════")
        print("     -If you want to import an automata tap 1")
        print("     -If you want to use one of the default automata tap 2")
        print("     -If you want to create a new automata tap 3")
        print("     -If you want to exit tap 4")
        choice = int(input())
    if choice == 4:
        return
    if choice == 2:
        print("════════════════════════════════════════════════════════════")
        # ask the user to choose an automata from the default automata list
        x = input("enter the number of the automata you want to use (1-42)")
        automate_manager("{}.txt".format(x))
    if choice == 1:  # ask the user to enter the path to the file he wants to import, if he want to import an automaton that was not in the default automata list
        working = False
        while(not working):
            print("Enter the path to the file you want to import")
            path = input()
            print([path])
            # if the file is not a .txt file, ask the user to enter a valid filename
            if not path.endswith(".txt"):
                print("This is not a .txt file, please enter a valid filename")
            else:
                try:    # try to open the file, if it fails, ask the user to enter a valid path
                    with open(path, 'r') as file:
                        working = True
                except:
                    print("The path you entered is not valid")
        automate_manager(path)  # if the file is valid, open it

###########################################################
#
#
#                   Save functions
#                   (save the automata in a file)
#                   Was used to create all the traces
#
###########################################################


def save_as_automata(source_file):
    """
    save the automata in a file
    """
    automate = automata(source_file)
    automate.complement()
    # write to destination file
    with open(source_file[:-4]+"\\"+source_file[:-4]+"_complement.txt", 'w') as f:
        # write number of symbols
        f.write(str(len(automate.labels)) + '\n')
        # write number of states
        f.write(str(len(automate.states)) + '\n')
        # write initial states
        f.write(str(len(automate.start)) + ' ' + automate.start + '\n')
        # write final states
        f.write(str(len(automate.finish)) + ' ' + automate.finish + '\n')
        # write transitions
        f.write(str(4) + '\n')
        for elem in automate.states:
            for label in automate.labels:
                if label in elem.paths:
                    for target in elem.paths.get(label):
                        f.write(str(elem.number) + label + str(target) + '\n')


def save_as_table(source_file):
    """
    save the automata in a file as a table
    """
    automate = automata(source_file)
    automate.minimized()
    # write to destination file
    char = "      "
    size = {}
    for elem in automate.labels:
        size[elem] = 0
    for state in automate.states:
        for key, value in state.paths.items():
            if len(value) > size[key]:
                size[key] = len(value)
    for elem in automate.labels:
        char += "| "
        char += elem
        char += " "*(2*(size[elem])-1)
    char += "|"
    char += "\n      "
    for key, value in size.items():
        for i in range(value):
            char += "____"
    char += '\n'
    for elem in automate.states:
        if elem.finish:
            char += "<"
        else:
            char += " "
        if elem.start or elem.finish:
            char += "-"
        else:
            char += " "
        if elem.start:
            char += ">"
        else:
            char += " "
        char += " "
        char += str(characters.index(str(elem.number)))
        char += " "
        char += "|"
        for label in automate.labels:
            s = 0
            char += " "
            if label in elem.paths:
                for target in elem.paths.get(label):
                    char += str(characters.index(str(target)))
                    char += " "
                    s += 1

            else:
                char += ' '
                char += " "
                s += 1
            for i in range(size[label]-s):
                char += " "*2
            char += "|"
        char += "\n      "
        for key, value in size.items():
            for i in range(value):
                char += "____"
        char += '\n'
    with open(source_file[:-4]+"\\"+source_file[:-4]+"_minimized.txt", 'w') as f:
        f.write(char)


###########################################################
#
#
#                   Main program
#
#
###########################################################
if __name__ == "__main__":
    main()
