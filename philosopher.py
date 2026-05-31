import threading

class Filosofo:
    def __init__(self, id:int):
        self.id = id
        self.garrafas = None
        self.state = 'pensando'
        self.count_refeicoes = 0

    def set_state(self, state):
        self.state = state

    def set_garrafas(self, garrafas:list[tuple[int,int]]):
        self.garrafas = garrafas
    
    def get_state(self):
        return self.state
    
    def get_ID(self):
        return self.id
    
    def get_count_refeicoes(self):
        return self.count_refeicoes
    
    def inc_refeicoes(self):
        self.count_refeicoes += 1

def criar_garrafas(matriz:list[list[int]]):
    garrafas = {}

    for i, linha in enumerate(matriz):
        for j, elemento in enumerate(linha):
            if elemento and (j,i) not in garrafas:
                print(f'iteração{i}')
                garrafas[(i,j)] = threading.Lock()

    return garrafas

def atribuir_garrafas(garrafas:dict, filosofos:list[Filosofo]):
    arestas = list(garrafas)
    for filosofo in filosofos:
        id = filosofo.get_ID()
        arestas_filosofo = [aresta for aresta in arestas if (id == aresta[0] or id == aresta[1])]
        filosofo.set_garrafas(arestas_filosofo)
        print(arestas_filosofo)