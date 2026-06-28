import threading

class Solucao:
    """Classe base para todas as soluções do Bar dos Filósofos"""
    
    def __init__(self, grafo, filosofos, rodadas_necessarias):
        self.grafo = grafo
        self.filosofos = filosofos
        self.rodadas_necessarias = rodadas_necessarias
        self.executando = True
        
        # Cria locks para cada garrafa (aresta)
        self.locks_garrafas = {}
        for aresta in grafo.arestas:
            self.locks_garrafas[aresta['id']] = threading.Lock()
            
        # Atribui locks aos filosofos
        for f in filosofos:
            f.locks_garrafas = self.locks_garrafas
            f.rodadas_necessarias = rodadas_necessarias
            
    def ciclo_filosofo(self, filosofo):
        """Cada solução deve implementar este método"""
        raise NotImplementedError("Cada solução deve implementar este método")