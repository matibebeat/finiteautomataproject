

class node():
    def __init__(self, number,start, finish) -> None:
        self.number = number
        self.paths = {}
        self.finish = finish
        self.start = start

    def add_path(self, label, target):
        try:
            self.paths[label].append(target)
        except:
            self.paths[label] = [target]


class automata():
    def __init__(self) -> None:
        self.labels=['a','b']
        self.nodes=[]


    def is_standard(self):
        initial_states=self.start
        if len(self.start)>1:
            return False
        print(initial_states)
        for elem in self.nodes:
            for paths,target in elem.paths.items():
                for node in target:
                    if node in initial_states:
                        return False
        return True


    def is_complete(self):
        for elem in self.nodes:
            for label in self.labels:
                if label not in elem.paths.keys():
                    return False
        return True
    
    def is_deterministic(self):
        if len(self.start)>1:
            return False
        for elem in self.nodes:
            for paths,target in elem.paths.items():
                if len(target)>1:
                    return False
        return True
    
    def complete(self):
        last_node_number=len(self.nodes)
        self.nodes.append(node(last_node_number,False,False))
        for elem in self.nodes:
            for label in self.labels:
                if label not in elem.paths.keys():
                    elem.paths[label]=['{}'.format(last_node_number)]
        return self
    
    def is_recognizing(self,word):
        current_node=self.start
        for letter in word:
            try:
                current_node=self.nodes[int(current_node)].paths[letter][0]
            except:
                return False
        if current_node in self.finish:
            return True
        else:
            return False
    
    def complement(self):
        new_finish=""
        for i in range(len(self.nodes)):
            if i not in self.finish:
                new_finish+=str(i)
        self.finish=new_finish

        for elem in self.nodes:
            if elem.finish==True:
                elem.finish=False
            else:
                elem.finish=True
        return self

def fill_automata(file:str, automata:automata):
    with open(file,'r') as file:
        file_content=file.readlines()
    for i in range(len(file_content)):
        file_content[i]=file_content[i][:-1]
    [number_of_initial_states,initial_states]=file_content[2].split(" ")
    [number_of_final_states,final_states]=file_content[3].split(" ")
    automata.start=initial_states
    automata.finish=final_states
    for i in range(int(file_content[1])):
        if str(i) in final_states:
            is_terminal=True
        else:
            is_terminal=False
        if str(i) in initial_states:
            is_initial=True
        else:
            is_initial=False
        automata.nodes.append(node(i,is_initial,is_terminal))
    for elem in file_content[5:]:
        automata.nodes[int(elem[0])].add_path( elem[1], elem[2])
    

def print_automata(automata:automata):
    print("    ", end='')
    for elem in automata.labels:
        print(elem, end='')
        print(" ", end='')
    print('\n')
    for elem in automata.nodes:
        print(" ", end='')
        print(elem.number,end='')
        print(" ", end='')
        for label in automata.labels:
            print(" ", end='')
            if label in elem.paths:
                for target in elem.paths.get(label):
                    print(target,end='')
            else:
                print('*',end='')
            print(" ",end='')
        print('\n')


"""
automata=automata()
fill_automata("automate1.txt",automata)
print(automata.is_standard())
print_automata(automata)
automata.complete()
print_automata(automata)
"""

###########################################################
#
#
#                   Usefull functions
#
#
###########################################################


def readword():
    c = input("Enter the letter you want to read")
    return c


string=readword()
print(string)