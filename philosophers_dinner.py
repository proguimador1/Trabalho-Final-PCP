import threading
import time

def create_forks(matrix):
    forks = {}
    for linha in matrix:
        i = matrix.index(linha)
        for element in linha:
            j = linha.index(element)
            if element and not (j,i) in forks:
                forks[(i,j)] = threading.Lock()
    return forks

class Filosofo():
    def __init__(self, ID):
        self.ID = ID
        self.state = 'pensando'
        self.refeicoes = 0
        
    def set_state(self, state):
        self.state = state
    
    def inc_refeicoes(self):
        self.refeicoes += 1
    
    def get_state(self):
        return self.state
    
    def get_refeicoes(self):
        return self.refeicoes
    
mutex = threading.Lock()

def jantar(i, filosofo:Filosofo):
    counter = 0
    while filosofo.get_refeicoes() < 5:
        filosofo.set_state('faminto')
        print(f'---Iteração {...}---')
        mutex.acquire()
        filosofo.set_state('comendo')
        filosofo.inc_refeicoes()
        print(f'Filosofo {i} comeu')
        mutex.release()
        
        filosofo.set_state('pensando')
        counter += 1
        
        time.sleep(5)

matrix = []

with open('dinner_graph.txt', 'r') as file:
    for i in range(5):
        matrix.append(file.readline())

forks = create_forks(matrix)

#for i, filosofo in enumerate(filosofos):
    #threading.Thread(target=jantar, args=(i, filosofo)).start()
