###########################################################
#
#
#                   Node Element
#
#
###########################################################

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

###########################################################
#
#
#                   Automata Element
#
#
###########################################################


class automata():
    def __init__(self,file:str) -> None:
        self.nodes=[]
        self.labels=[]
        with open(file,'r') as file:
            file_content=file.readlines()
        for i in range(len(file_content)):
            file_content[i]=file_content[i][:-1]
        [number_of_initial_states,self.start]=file_content[2].split(" ")
        [number_of_final_states,self.finish]=file_content[3].split(" ")
        for i in range(int(file_content[1])):
            if str(i) in self.finish:
                is_terminal=True
            else:
                is_terminal=False
            if str(i) in self.start:
                is_initial=True
            else:
                is_initial=False
            self.nodes.append(node(i,is_initial,is_terminal))
        for elem in file_content[5:]:
            if elem[1] not in self.labels:
                self.labels.append(elem[1])
            self.nodes[int(elem[0])].add_path(elem[1],elem[2])


    def is_standard(self):
        initial_states=self.start
        if len(self.start)>1:
            return False
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
    
    def determinize(self):
        if self.is_deterministic():
            return
        if not self.is_complete():
            self.complete()
        new_nodes=[]
        dones=[]
        paths={label:"" for label in self.labels}
        finish=False
        name=""
        for elem in self.start:
            name+=elem
            for label in self.labels:
                if self.nodes[int(elem)].paths[label][0] not in paths[label]:
                    paths[label]+="".join(self.nodes[int(elem)].paths[label])
            if self.nodes[int(elem)].finish:
                finish=True
        start_node=node("".join(sorted(name)),True,finish)
        to_compute=[]
        for key,value in paths.items():
            start_node.add_path(key,value)
            if name!=value:
                to_compute.append(value)
        dones.append(name)
        new_nodes.append(start_node)
        while(len(to_compute)>1):
            paths={label:"" for label in self.labels}
            finish=False
            name="".join(sorted(to_compute[0]))
            for elem in name:
                for label in self.labels:
                    if "".join(self.nodes[int(elem)].paths[label]) not in paths[label]:
                        paths[label]+="".join(self.nodes[int(elem)].paths[label])
                if self.nodes[int(elem)].finish:
                    finish=True
            new_node=node(name,False,finish)
            dones.append(name)
            for key,value in paths.items():
                new_node.add_path(key,"".join(sorted(value))) 
            for key,value in paths.items():
                if value not in to_compute and value not in dones:
                    to_compute.append(value)
            to_compute.pop(0)
            new_nodes.append(new_node)
        states=[]
        for state in new_nodes:
            states.append(state.number)
        for state in new_nodes:
            state.number=states.index(state.number)
            for key,value in state.paths.items():
                state.paths[key]=[states.index("".join(sorted(value[0])))]



        self.nodes=new_nodes


    
        


    

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

automate1=automata("automate1.txt")
automate1.determinize()
print_automata(automate1)


