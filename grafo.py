class Grafo:
    def __init__(self, matriz_adjacencia):
        """Inicializa o grafo a partir da matriz de adjacência"""
        self.matriz = matriz_adjacencia
        self.num_vertices = len(matriz_adjacencia)
        self.lista_adjacencia = self._construir_lista_adjacencia()
        self.arestas = self._construir_arestas()
        
    def _construir_lista_adjacencia(self):
        """Converte matriz para lista de adjacência"""
        lista = {}
        for i in range(self.num_vertices):
            vizinhos = []
            for j in range(self.num_vertices):
                if self.matriz[i][j] == 1:
                    vizinhos.append(j)
            lista[i] = vizinhos
        return lista
    
    def _construir_arestas(self):
        """Cria lista de arestas com IDs únicos"""
        arestas = []
        id_aresta = 0
        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                if self.matriz[i][j] == 1:
                    arestas.append({
                        'id': id_aresta,
                        'vertices': (i, j)
                    })
                    id_aresta += 1
        return arestas
    
    def get_vizinhos(self, vertice):
        """Retorna lista de vizinhos de um vértice"""
        return self.lista_adjacencia[vertice]
    
    def get_grau(self, vertice):
        """Retorna o grau de um vértice"""
        return len(self.lista_adjacencia[vertice])
    
    def get_id_aresta(self, v1, v2):
        """Retorna o ID da aresta entre dois vértices"""
        for aresta in self.arestas:
            if (aresta['vertices'][0] == v1 and aresta['vertices'][1] == v2) or \
               (aresta['vertices'][0] == v2 and aresta['vertices'][1] == v1):
                return aresta['id']
        return None