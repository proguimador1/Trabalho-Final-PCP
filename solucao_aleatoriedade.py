from solucao import Solucao
import time
import random

class SolucaoAleatoriedade(Solucao):
    def __init__(self, grafo, filosofos, rodadas_necessarias):
        super().__init__(grafo, filosofos, rodadas_necessarias)
        
        # Fator de backoff inicial
        self.backoff_min = 0.5
        self.backoff_max = 2.0
    
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
            
            # Marca o momento que ficou com sede
            inicio_sede = time.time()
            
            # Loop até conseguir todas as garrafas
            while True:
                # 3. Tenta pegar garrafas
                ids_garrafas = []
                for vizinho in filosofo.garrafas_escolhidas:
                    id_garrafa = self.grafo.get_id_aresta(filosofo.id, vizinho)
                    ids_garrafas.append(id_garrafa)
                
                filosofo.garrafas_pegadas = []
                conseguiu_todas = True
                
                for id_garrafa in ids_garrafas:
                    # Tenta pegar sem bloquear (non-blocking)
                    if self.locks_garrafas[id_garrafa].acquire(blocking=False):
                        filosofo.garrafas_pegadas.append(id_garrafa)
                        print(f"  Filósofo {filosofo.id} pegou garrafa {id_garrafa}")
                    else:
                        # Não conseguiu uma garrafa
                        conseguiu_todas = False
                        print(f"  Filósofo {filosofo.id} não conseguiu garrafa {id_garrafa}")
                        break
                
                # 4. Se conseguiu todas, sai do loop
                if conseguiu_todas:
                    break
                
                # 5. Não conseguiu todas: libera as que pegou
                for id_garrafa in filosofo.garrafas_pegadas:
                    self.locks_garrafas[id_garrafa].release()
                    print(f"   Filósofo {filosofo.id} liberou garrafa {id_garrafa}")
                
                filosofo.garrafas_pegadas = []
                
                # Espera um tempo aleatório (backoff)
                tempo_backoff = random.uniform(self.backoff_min, self.backoff_max)
                print(f"   Filósofo {filosofo.id} esperando {tempo_backoff:.2f}s (backoff)")
                time.sleep(tempo_backoff)
            
            # 6. Conseguiu todas as garrafas
            tempo_espera = time.time() - inicio_sede  # Tempo total desde que ficou com sede
            filosofo.tempo_espera_total += tempo_espera
            filosofo.tempo_com_sede += tempo_espera
            
            # 7. Beber
            print(f" Filósofo {filosofo.id} começou a beber (esperou {tempo_espera:.2f}s)")
            filosofo.beber()
            
            # 8. Liberar garrafas
            for id_garrafa in filosofo.garrafas_pegadas:
                self.locks_garrafas[id_garrafa].release()
                print(f"  Filósofo {filosofo.id} liberou garrafa {id_garrafa}")
            
            filosofo.garrafas_pegadas = []
            print(f"--- Filósofo {filosofo.id} completou {filosofo.rodadas_feitas}/{filosofo.rodadas_necessarias} rodadas ---")