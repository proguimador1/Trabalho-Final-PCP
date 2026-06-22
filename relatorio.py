import math

class Relatorio:
    def __init__(self, nome_arquivo, grafo, rodadas):
        self.nome_arquivo = nome_arquivo
        self.grafo = grafo
        self.rodadas = rodadas
        self.resultados = {}
        self.linhas = []
    
    def adicionar_solucao(self, nome, dados):
        self.resultados[nome] = dados
    
    def _add_linha(self, texto=""):
        self.linhas.append(texto)
    
    def _calcular_metricas_starvation(self, tempos):
        """Calcula métricas para análise de starvation"""
        n = len(tempos)
        if n == 0:
            return None
        
        media = sum(tempos) / n
        
        # Desvio padrão
        variancia = sum((t - media) ** 2 for t in tempos) / n
        desvio_padrao = math.sqrt(variancia)
        
        # Coeficiente de Variação (CV)
        cv = (desvio_padrao / media) * 100 if media > 0 else 0
        
        # Índice de Jain
        soma = sum(tempos)
        soma_quadrados = sum(t ** 2 for t in tempos)
        jain = (soma ** 2) / (n * soma_quadrados) if soma_quadrados > 0 else 0
        
        return {
            'media': media,
            'desvio_padrao': desvio_padrao,
            'cv': cv,
            'jain': jain,
            'min': min(tempos),
            'max': max(tempos),
            'variacao_abs': max(tempos) - min(tempos)
        }
    
    def _interpretar_starvation(self, metricas):
        """Interpreta as metricas de starvation"""
        if metricas is None:
            return "Sem dados"
        
        jain = metricas['jain']
        
        # Interpretação baseada no Índice de Jain
        if jain >= 0.9:
            return "Excelente equidade (sem starvation)"
        elif jain >= 0.7:
            return "Equidade moderada (possivel starvation leve)"
        elif jain >= 0.5:
            return "Baixa equidade (starvation provavel)"
        else:
            return "Equidade muito baixa (starvation severo!)"
    
    def _gerar_cabecalho(self):
        self._add_linha("="*60)
        self._add_linha(f"ARQUIVO: {self.nome_arquivo} | VERTICES: {self.grafo.num_vertices} | RODADAS: {self.rodadas}")
        self._add_linha("="*60)
        self._add_linha()
    
    def _gerar_solucao(self, nome, dados):
        self._add_linha(f"SOLUCAO: {nome}")
        self._add_linha("-"*60)
        self._add_linha(f"Tempo total de execução: {dados['tempo_total']:.2f} segundos")
        self._add_linha(f"Media de espera geral: {dados['media_espera']:.2f}s")
        self._add_linha()
        
        self._add_linha("Detalhes por filosofo:")
        self._add_linha("-"*60)
        for id_f, info in dados['resultados'].items():
            self._add_linha(f"Filosofo {id_f} (grau {info['grau']}):")
            self._add_linha(f"  Rodadas: {info['rodadas']}")
            self._add_linha(f"  Tempo tranquilo: {info['tempo_tranquilo']:.2f}s")
            self._add_linha(f"  Tempo com sede (espera): {info['tempo_com_sede']:.2f}s")
            self._add_linha(f"  Tempo bebendo: {info['tempo_bebendo']:.2f}s")
            self._add_linha(f"  Tempo médio de espera: {info['tempo_medio_espera']:.2f}s")
            self._add_linha()
        
        self._gerar_analise_starvation(dados)
        self._add_linha()
        self._add_linha("="*60)
        self._add_linha()
    
    def _gerar_analise_starvation(self, dados):
        self._add_linha("="*60)
        self._add_linha("ANALISE DE STARVATION")
        self._add_linha("="*60)
        
        grupos = {}
        for id_f, info in dados['resultados'].items():
            grau = info['grau']
            if grau not in grupos:
                grupos[grau] = []
            grupos[grau].append(info['tempo_medio_espera'])
        
        for grau, tempos in grupos.items():
            if len(tempos) > 1:
                metricas = self._calcular_metricas_starvation(tempos)
                
                self._add_linha(f"\nFilosofos com grau {grau} ({len(tempos)} filosofos):")
                self._add_linha("-"*40)
                self._add_linha(f"  Tempos de espera: {[f'{t:.2f}' for t in tempos]}")
                self._add_linha(f"  Media: {metricas['media']:.2f}s")
                self._add_linha(f"  Desvio padrao: {metricas['desvio_padrao']:.2f}s")
                self._add_linha(f"  Coeficiente de Variacao (CV): {metricas['cv']:.1f}%")
                self._add_linha(f"  Indice de Jain: {metricas['jain']:.3f} (1 = perfeito)")
                self._add_linha(f"  Variacao: {metricas['min']:.2f}s - {metricas['max']:.2f}s")
                self._add_linha(f"  {self._interpretar_starvation(metricas)}")
            else:
                self._add_linha(f"\nFilosofos com grau {grau}: apenas 1 filosofo (sem comparacao)")
        
        self._add_linha()
    
    def _gerar_resumo(self):
        self._add_linha("="*60)
        self._add_linha("RESUMO COMPARATIVO ENTRE AS SOLUCOES")
        self._add_linha("="*60)
        self._add_linha(f"{'Solucao':<20} {'Tempo Total':<15} {'Espera Média':<15} {'Starvation':<20}")
        self._add_linha("-"*80)
        
        for nome, dados in self.resultados.items():
            # Pega a pior métrica de starvation entre os grupos
            pior_jain = 1.0
            grupos = {}
            for id_f, info in dados['resultados'].items():
                grau = info['grau']
                if grau not in grupos:
                    grupos[grau] = []
                grupos[grau].append(info['tempo_medio_espera'])
            
            for grau, tempos in grupos.items():
                if len(tempos) > 1:
                    metricas = self._calcular_metricas_starvation(tempos)
                    if metricas and metricas['jain'] < pior_jain:
                        pior_jain = metricas['jain']
            
            if pior_jain >= 0.9:
                status = " Excelente"
            elif pior_jain >= 0.7:
                status = " Moderado"
            elif pior_jain >= 0.5:
                status = " Ruim"
            else:
                status = " Severo"
            
            self._add_linha(f"{nome:<20} {dados['tempo_total']:<15.2f} {dados['media_espera']:<15.2f} {status:<20}")
    
    def gerar(self):
        self._gerar_cabecalho()
        for nome, dados in self.resultados.items():
            self._gerar_solucao(nome, dados)
        self._gerar_resumo()
        return "\n".join(self.linhas)
    
    def salvar(self, arquivo_saida):
        conteudo = self.gerar()
        with open(arquivo_saida, 'w') as f:
            f.write(conteudo)
        return arquivo_saida