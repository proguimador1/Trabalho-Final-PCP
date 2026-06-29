from enum import Enum
import random
import time

class EstadoFilosofo(Enum):
    TRANQUILO = "tranquilo"
    COM_SEDE = "com sede"
    BEBENDO = "bebendo"

class Filosofo:
    def __init__(self, id, grafo):
        self.id = id
        self.grafo = grafo
        self.estado = EstadoFilosofo.TRANQUILO
        self.vizinhos = grafo.get_vizinhos(id)
        self.grau = len(self.vizinhos)
        self.rodadas_necessarias = 0  # 6 ou 3
        self.rodadas_feitas = 0
        
        # Garrafas escolhidas na rodada atual
        self.garrafas_escolhidas = []
        self.garrafas_pegadas = []
        
        # Estatísticas
        self.tempo_tranquilo = 0
        self.tempo_com_sede = 0
        self.tempo_bebendo = 0
        self.tempo_espera_total = 0
        self.tempos_espera = []
        self.inicio_sede = 0
        
    def pensar(self):
        """Fica tranquilo por 0 a n segundos"""
        tempo = random.uniform(0, self.grau)
        self.estado = EstadoFilosofo.TRANQUILO
        time.sleep(tempo)
        self.tempo_tranquilo += tempo
        
    def ficar_com_sede(self):
        """Escolhe garrafas e fica com sede"""
        self.estado = EstadoFilosofo.COM_SEDE
        self.inicio_sede = time.time()
        
        # Escolhe de 2 até grau garrafas
        quantidade = random.randint(2, self.grau)
        self.garrafas_escolhidas = random.sample(self.vizinhos, quantidade)
        
    def beber(self):
        """Bebe por 1 segundo"""
        self.estado = EstadoFilosofo.BEBENDO
        time.sleep(1.0)
        self.rodadas_feitas += 1
        self.tempo_bebendo += 1.0