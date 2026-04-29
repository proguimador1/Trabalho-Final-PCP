import threading
import time

def create_forks(matrix):
    forks = {}
    arestas = []
    for linha in matrix:
        i = matrix.index(linha)
        for element in linha:
            j = linha.index(element)
            if element and not (j,i) in forks:
                forks[(i,j)] = threading.Lock()
                arestas.append((i,j))
    return forks, arestas

class Filosofo():
    def __init__(self, ID):
        self.ID = ID
        self.state = 'pensando'
        self.refeicoes = 0

    def set_left_fork(self, fork):
        self.left_fork = fork

    def set_right_fork(self, fork):
        self.right_fork = fork

    def set_state(self, state):
        self.state = state
    
    def inc_refeicoes(self):
        self.refeicoes += 1
    
    def get_state(self):
        return self.state
    
    def get_ID(self):
        return self.ID
    
    def get_refeicoes(self):
        return self.refeicoes
    
mutex = threading.Lock()

def jantar(filosofo:Filosofo, mutex):
    ...

matrix = []

with open('dinner_graph.txt', 'r') as file:
    for i in range(5):
        matrix.append(file.readline())

forks, arestas = create_forks(matrix)

filosofos = [Filosofo(ID) for ID in range(1,6)]

for i in range(len(arestas)):
    right = arestas[i]
    left = arestas[-1-i]
    filosofos[i].set_right_fork(forks[right])
    filosofos[i].set_left_fork(forks[left])

for filosofo in filosofos:
    threading.Thread(target=jantar, args=(filosofo.get_ID(), filosofo)).start()
