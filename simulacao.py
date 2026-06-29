import threading
from filosofo import Filosofo
from grafo import Grafo

class Simulacao:
    def __init__(self, grafo, classe_solucao, rodadas_necessarias=6):
        self.grafo = grafo
        self.classe_solucao = classe_solucao
        self.rodadas_necessarias = rodadas_necessarias
        self.filosofos = []
        self.resultados = {}
        
    def executar(self):
        # Cria filosofos
        for i in range(self.grafo.num_vertices):
            self.filosofos.append(Filosofo(i, self.grafo))
            
        # Cria solução
        solucao = self.classe_solucao(self.grafo, self.filosofos, self.rodadas_necessarias)
        
        # Inicia threads
        threads = []
        for f in self.filosofos:
            t = threading.Thread(target=solucao.ciclo_filosofo, args=(f,))
            t.daemon = True
            threads.append(t)
            t.start()
            
        # Espera todos terminarem
        for t in threads:
            t.join()
            
        # Coleta resultados
        self._coletar_resultados()
        
    def _coletar_resultados(self):
        for f in self.filosofos:
            self.resultados[f.id] = {
                'rodadas': f.rodadas_feitas,
                'tempo_tranquilo': f.tempo_tranquilo,
                'tempo_com_sede': f.tempo_com_sede,
                'tempo_bebendo': f.tempo_bebendo,
                'tempo_medio_espera': f.tempo_espera_total / f.rodadas_feitas if f.rodadas_feitas > 0 else 0,
                'grau': f.grau
            }