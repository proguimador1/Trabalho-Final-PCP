from solucao import Solucao
import time
import threading
from enum import Enum
from collections import deque

class EstadoGarrafa(Enum):
    CHEIA = "cheia"
    VAZIA = "vazia"

class SolucaoChandyMisra(Solucao):
    def __init__(self, grafo, filosofos, rodadas_necessarias):
        super().__init__(grafo, filosofos, rodadas_necessarias)
        
        # Estado de cada garrafa: inicialmente VAZIA
        self.estado = {}
        self.dono = {}
        for aresta in grafo.arestas:
            self.estado[aresta['id']] = EstadoGarrafa.VAZIA
            self.dono[aresta['id']] = None
        
        # Fila de pedidos para cada garrafa (ordem de chegada)
        self.fila_pedidos = {}
        for aresta in grafo.arestas:
            self.fila_pedidos[aresta['id']] = deque()
        
        self.lock_garrafa = {}
        for aresta in grafo.arestas:
            self.lock_garrafa[aresta['id']] = threading.Lock()
        
        # Fila de mensagens para cada filósofo
        for f in filosofos:
            f.fila_mensagens = deque()
            f.lock_mensagens = threading.Lock()
            f.esta_bebendo = False
    
    def enviar_pedido(self, filosofo, id_garrafa, vizinho_id):
        """Filósofo envia pedido para o vizinho"""
        vizinho = None
        for f in self.filosofos:
            if f.id == vizinho_id:
                vizinho = f
                break
        
        with vizinho.lock_mensagens:
            vizinho.fila_mensagens.append({
                'tipo': 'pedido',
                'de': filosofo.id,
                'garrafa': id_garrafa
            })
    
    def processar_mensagens(self, filosofo):
        with filosofo.lock_mensagens:
            while filosofo.fila_mensagens:
                msg = filosofo.fila_mensagens.popleft()
                
                if msg['tipo'] == 'pedido':
                    id_garrafa = msg['garrafa']
                    solicitante = msg['de']
                    
                    with self.lock_garrafa[id_garrafa]:
                        if filosofo.esta_bebendo:
                            filosofo.fila_mensagens.append(msg)
                            continue
                        
                        if self.estado[id_garrafa] == EstadoGarrafa.VAZIA:
                            # Apenas registra que vai entregar
                            self.estado[id_garrafa] = EstadoGarrafa.CHEIA
                            self.dono[id_garrafa] = solicitante
                            print(f" Filósofo {filosofo.id} vai enviar garrafa {id_garrafa} para {solicitante}")
    
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
            
            # 3. Envia pedidos para todos os vizinhos
            ids_garrafas = []
            for vizinho_id in filosofo.garrafas_escolhidas:
                id_garrafa = self.grafo.get_id_aresta(filosofo.id, vizinho_id)
                ids_garrafas.append(id_garrafa)
                self.enviar_pedido(filosofo, id_garrafa, vizinho_id)
                print(f"Filósofo {filosofo.id} pediu garrafa {id_garrafa} para {vizinho_id}")
            
            # 4. Tenta adquirir as garrafas
            filosofo.garrafas_pegadas = []
            
            for id_garrafa in ids_garrafas:
                # Tenta pegar (pode bloquear até receber)
                if self.locks_garrafas[id_garrafa].acquire(blocking=True):
                    filosofo.garrafas_pegadas.append(id_garrafa)
                    with self.lock_garrafa[id_garrafa]:
                        self.dono[id_garrafa] = filosofo.id
                        self.estado[id_garrafa] = EstadoGarrafa.CHEIA
                    print(f"Filósofo {filosofo.id} pegou garrafa {id_garrafa}")
            
            # 5. Se não pegou todas, libera e tenta de novo
            if len(filosofo.garrafas_pegadas) < len(ids_garrafas):
                for id_garrafa in filosofo.garrafas_pegadas:
                    with self.lock_garrafa[id_garrafa]:
                        self.estado[id_garrafa] = EstadoGarrafa.VAZIA
                        self.dono[id_garrafa] = None
                    self.locks_garrafas[id_garrafa].release()
                filosofo.garrafas_pegadas = []
                time.sleep(0.1)
                continue
            
            # 6. Registra tempo de espera
            tempo_espera = time.time() - inicio_espera
            filosofo.tempo_espera_total += tempo_espera
            filosofo.tempo_com_sede += tempo_espera
            
            # 7. Beber
            filosofo.esta_bebendo = True
            print(f"Filósofo {filosofo.id} começou a beber (esperou {tempo_espera:.2f}s)")
            filosofo.beber()
            filosofo.esta_bebendo = False
            
            # 8. Processa mensagens que chegaram durante a bebida
            self.processar_mensagens(filosofo)
            
            # 9. Coloca todas as garrafas em VAZIA
            for id_garrafa in filosofo.garrafas_pegadas:
                with self.lock_garrafa[id_garrafa]:
                    self.estado[id_garrafa] = EstadoGarrafa.VAZIA
                    self.dono[id_garrafa] = None
                self.locks_garrafas[id_garrafa].release()
                print(f"Filósofo {filosofo.id} liberou garrafa {id_garrafa} (vazia)")
            
            # 10. Processa mensagens novamente (após liberar)
            self.processar_mensagens(filosofo)
            
            filosofo.garrafas_pegadas = []
            print(f"--- Filósofo {filosofo.id} completou {filosofo.rodadas_feitas}/{filosofo.rodadas_necessarias} rodadas ---")