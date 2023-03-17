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
    def __init__(self,file:str) -> None:
        self.nodes=[]
        self.labels=[]
        if file=='':
            return
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
                    if str(node) in initial_states:
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
            if str(i) not in self.finish:
                new_finish+=str(i)
        self.finish=new_finish

        for elem in self.nodes:
            if elem.finish==True:
                elem.finish=False
            else:
                elem.finish=True
        return self

    def standardise(self):
        if self.is_standard():
            return
        new_nodes=node("{}".format(len(self.nodes)),True,False)
        for elem in self.start:
            for key,value in self.nodes[int(elem)].paths.items():
                for elem in value:
                    new_nodes.add_path(key,elem)
                
            self.nodes[int(elem)].start=False
            if self.nodes[int(elem)].finish:
                new_nodes.finish=True
        self.nodes.append(new_nodes)
        self.start="{}".format(len(self.nodes))
            
    
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
                if str(self.nodes[int(elem)].paths[label][0]) not in paths[label]:
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


        self.start="0"
        self.nodes=new_nodes
    def recognise_word(self, word):
        current_nodes = [self.start]  # liste des états courants
        for letter in word:
            next_nodes = []  # liste des états suivants
            for node in current_nodes:
                try:
                    next_nodes.extend(self.nodes[int(node)].paths[letter])
                except KeyError:
                    pass
            if not next_nodes:
                return False  # aucun état suivant n'a été trouvé pour cette lettre
            current_nodes = next_nodes
        return any(node in self.finish for node in current_nodes)  # on renvoie True si au moins un état courant est un état final


    def recognise_words(self, words):
        return [self.recognise_word(word) for word in words]
    
    def recognise_file(self, filename):
        with open(filename, 'r') as file:
            words = file.read().splitlines()
        return self.recognise_words(words)
    
    def recognise_file_and_print(self, filename):
        with open(filename, 'r') as file:
            words = file.read().splitlines()
        for word, result in zip(words, self.recognise_words(words)):
            print(word, result)




    def minimizied(self):
        if not self.complete():
            self.complete()
        if not self.is_deterministic():
            self.determinize()
        initial_partition=[i for i in range (len(self.nodes))]
        partitions=[[i for i in range (len(self.nodes)) if self.nodes[i].finish==False],[i for i in range (len(self.nodes)) if self.nodes[i].finish==True]]       
        partition2=[]
        partition3=[]
        working=True
        while (working==True):
            for elem in partitions:
                if len(elem)==1:
                    new_partitions=[elem]
                else:
                    partitions_target={number : "" for number in elem}
                    for number in elem:
                        for label in self.labels:
                            target=self.nodes[number].paths[label][0]
                            for j in range(len(partitions)):
                                if int(target) in partitions[j]:
                                    partitions_target[number]+=str(j)
                    new_partitions=group_by_value(partitions_target)
                for elem in new_partitions:
                    partition2.append(elem)
            if partition2!=partitions:
                partitions=partition2
                partition2=[]
            else:
                working=False
        i=0
        new_nodes=[]
        for elem in partitions:
            node_to_add=node(i,False,False)
            representative=elem[0]
            for label in self.labels:
                target=self.nodes[representative].paths[label][0]
                for j in range(len(partitions)):
                    if int(target) in partitions[j]:
                        node_to_add.add_path(label,j)
            if any(str(x) in self.start for x in elem):
                node_to_add.start=True
            if any(str(x) in self.finish for x in elem):
                node_to_add.finish=True
            new_nodes.append(node_to_add)
            i+=1
        self.nodes=new_nodes
        self.start='0'
        self.finish=[i for i in range(len(self.nodes)) if self.nodes[i].finish==True]
    

    
        
def group_by_value(d):
    result = {}
    for key, value in d.items():
        if value not in result:
            result[value] = [key]
        else:
            result[value].append(key)
    return list(result.values())

    

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
    c = input("Enter the word you want to read")
    return c

def informations(automate):
    print_automata(automate)
    print("════════════════════════")
    print("Informations about your automata:")
    print("Standard: {}".format(automate.is_standard()))
    print("Complete: {}".format(automate.is_complete()))
    print("Deterministic: {}".format(automate.is_deterministic()))
    print("════════════════════════")


def automate_manager(file_name):
    automate=automata(file_name)
    choice=0
    choices=[]
    while choice<=len(choices)+1:
        choices=[]
        informations(automate)
        i=0
        if not automate.is_standard():
            i+=1
            choices.append("sta")
            print("{}-Standardise it".format(i))
        if not automate.is_complete():
            i+=1
            choices.append("com")
            print("{}-Complete it".format(i))
        if not automate.is_deterministic():
            i+=1
            choices.append("det")
            print("{}-Determinize it".format(i))
        i+=1
        choices.append("cop")
        print("{}-Complementarize it".format(i))
        i+=1
        choices.append("min")
        print("{}-Minimize it".format(i))
        choices.append("rec")
        i=i+1
        print("{}-Test if a word is recognized by it".format(i))
        choice=int(input())
        if choices[choice-1]=="sta":
            automate.standardise()
        if choices[choice-1]=="com":
            automate.complete()
        if choices[choice-1]=="det":
            automate.determinize()
        if choices[choice-1]=="cop":
            automate.complement()
        if choices[choice-1]=="min":
            automate.minimizied()
        if choices[choice-1]=="rec":
            if automate.recognise_word(readword()):
                print("The word is recognized")
            else:
                print("The word is not recognized")
        

    
    

def main():
    choice=0
    while(choice<1 or choice>4):
        print("════════════════════════ ❀•°❀°•❀ ════════════════════════\n\n\n Welcome to Your Automata manager \n\n\n════════════════════════ ❀•°❀°•❀ ════════════════════════")   
        print("     -If you want to import an automata tap 1")
        print("     -If you want to use one of the default automata tap 2")
        print("     -If you want to create a new automata tap 3")
        print("     -If you want to exit tap 4")
        choice=int(input())
    if choice==4:
        return
    if choice==2:
        automate_manager("automate1.txt")
    if choice==1:
        working=False
        while(not working):
            print("Enter the path to the file you want to import")
            path=input()
            print([path])
            if not path.endswith(".txt"):
                print("This is not a .txt file, please enter a valid filename")
            else:
                try: 
                    with open(path,'r') as file:
                        working=True
                except:
                    print("The path you entered is not valid")
        automate_manager(path)



if __name__ == "__main__":

    main()
