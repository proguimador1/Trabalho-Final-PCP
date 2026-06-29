from solucao import Solucao
import time

class SolucaoArbitro(Solucao):
    def __init__(self, grafo, filosofos, rodadas_necessarias):
        super().__init__(grafo, filosofos, rodadas_necessarias)
        # Árbitro: só permite N-1 filósofos tentando ao mesmo tempo
        import threading
        self.arbitro = threading.Semaphore(len(filosofos) - 1)
        
    def ciclo_filosofo(self, filosofo):
        while self.executando and filosofo.rodadas_feitas < filosofo.rodadas_necessarias:
            # 1. Pensar
            filosofo.pensar()
            
            # 2. Ficar com sede
            filosofo.ficar_com_sede()
            
            garrafas_str = []
            for vizinho in filosofo.garrafas_escolhidas:
                id_garrafa = self.grafo.get_id_aresta(filosofo.id, vizinho)
                garrafas_str.append(f"{id_garrafa}(v{vizinho})")
            
            print(f" Filósofo {filosofo.id} quer {len(filosofo.garrafas_escolhidas)} garrafas: {garrafas_str}")
            inicio_espera = time.time()
            
            # 3. Pede permissão ao árbitro
            print(f"Filósofo {filosofo.id} aguardando permissão do árbitro")
            self.arbitro.acquire()
            print(f"Filósofo {filosofo.id} recebeu permissão do árbitro")
            
            try:
                # 4. Tenta pegar garrafas
                ids_garrafas = []
                for vizinho in filosofo.garrafas_escolhidas:
                    id_aresta = self.grafo.get_id_aresta(filosofo.id, vizinho)
                    ids_garrafas.append(id_aresta)
                
                print(f" Filósofo {filosofo.id} tentando pegar garrafas: {ids_garrafas}")
                
                # Pega todas as garrafas (agora com permissão do árbitro)
                for id_garrafa in ids_garrafas:
                    self.locks_garrafas[id_garrafa].acquire()
                    filosofo.garrafas_pegadas.append(id_garrafa)
                    print(f"Filósofo {filosofo.id} pegou garrafa {id_garrafa}")
                
                # 5. Registra tempo de espera
                tempo_espera = time.time() - inicio_espera
                filosofo.tempo_espera_total += tempo_espera
                filosofo.tempo_com_sede += tempo_espera
                
                # 6. Beber
                print(f"Filósofo {filosofo.id} começou a beber (esperou {tempo_espera:.2f}s)")
                filosofo.beber()
                
            finally:
                # 7. Liberar garrafas (sempre executa, mesmo com exceção)
                print(f"Filósofo {filosofo.id} liberando garrafas {filosofo.garrafas_pegadas}")
                for id_garrafa in filosofo.garrafas_pegadas:
                    self.locks_garrafas[id_garrafa].release()
                
                filosofo.garrafas_pegadas = []
                
                # 8. Libera árbitro (sempre executa, mesmo com exceção)
                self.arbitro.release()
                print(f"--- Filósofo {filosofo.id} completou {filosofo.rodadas_feitas}/{filosofo.rodadas_necessarias} rodadas ---")
