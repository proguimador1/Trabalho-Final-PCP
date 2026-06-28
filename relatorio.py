import math

class Relatorio:
    def __init__(self, nome_arquivo, grafo, rodadas):
        self.nome_arquivo = nome_arquivo
        self.grafo = grafo
        self.rodadas = rodadas
        self.resultados = {}
        self.linhas = []
    
    def adicionar_solucao(self, nome, dados):
        """Adiciona os dados de uma solução ao relatório."""
        self.resultados[nome] = dados
    
    def _add_linha(self, texto=""):
        """Adiciona uma linha ao relatório."""
        self.linhas.append(texto)
    
    def _calcular_metricas_starvation(self, tempos):
        """Calcula Índice de Jain, CV e desvio padrão para análise de starvation."""
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
    
    
    def _gerar_cabecalho(self):
        """Gera cabeçalho do relatório."""
        self._add_linha("="*60)
        self._add_linha(f"ARQUIVO: {self.nome_arquivo} | VÉRTICES: {self.grafo.num_vertices} | RODADAS: {self.rodadas}")
        self._add_linha("="*60)
        self._add_linha()
    
    def _gerar_solucao(self, nome, dados):
        """Gera seção de uma solução com detalhes e análise de starvation."""
        self._add_linha(f"SOLUÇÃO: {nome}")
        self._add_linha("-"*60)
        self._add_linha(f"Tempo total de execução: {dados['tempo_total']:.2f} segundos")
        self._add_linha(f"Média de espera geral: {dados['media_espera']:.2f}s")
        self._add_linha()
        
        self._add_linha("Detalhes por filósofo:")
        self._add_linha("-"*60)
        for id_f, info in dados['resultados'].items():
            self._add_linha(f"Filósofo {id_f} (grau {info['grau']}):")
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
        """Agrupa filósofos por grau e analisa starvation com Jain e CV."""
        self._add_linha("="*60)
        self._add_linha("ANÁLISE DE STARVATION")
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
                
                self._add_linha(f"\nFilósofos com grau {grau} ({len(tempos)} filósofos):")
                self._add_linha("-"*40)
                self._add_linha(f"  Tempos de espera: {[f'{t:.2f}' for t in tempos]}")
                self._add_linha(f"  Média: {metricas['media']:.2f}s")
                self._add_linha(f"  Desvio padrão: {metricas['desvio_padrao']:.2f}s")
                self._add_linha(f"  Coeficiente de Variação (CV): {metricas['cv']:.1f}%")
                self._add_linha(f"  Índice de Jain: {metricas['jain']:.3f}")
                self._add_linha(f"  Variação: {metricas['min']:.2f}s - {metricas['max']:.2f}s")
            else:
                self._add_linha(f"\nFilósofos com grau {grau}: apenas 1 filósofo (sem comparação)")
        
        self._add_linha()
    
    def _gerar_resumo(self):
        """Gera tabela comparativa entre todas as soluções."""
        self._add_linha("="*60)
        self._add_linha("RESUMO COMPARATIVO ENTRE AS SOLUÇÕES")
        self._add_linha("="*60)
        self._add_linha(f"{'Solução':<20} {'Tempo Total':<15} {'Espera Média':<15} {'Jain':<10} {'CV(%)':<10}")
        self._add_linha("-"*80)
        
        for nome, dados in self.resultados.items():
            pior_jain = 1.0
            pior_cv = 0.0
            grupos = {}
            for id_f, info in dados['resultados'].items():
                grau = info['grau']
                if grau not in grupos:
                    grupos[grau] = []
                grupos[grau].append(info['tempo_medio_espera'])
            
            for grau, tempos in grupos.items():
                if len(tempos) > 1:
                    metricas = self._calcular_metricas_starvation(tempos)
                    if metricas:
                        if metricas['jain'] < pior_jain:
                            pior_jain = metricas['jain']
                        if metricas['cv'] > pior_cv:
                            pior_cv = metricas['cv']
            
            self._add_linha(f"{nome:<20} {dados['tempo_total']:<15.2f} {dados['media_espera']:<15.2f} {pior_jain:<10.3f} {pior_cv:<10.1f}")
    
    def gerar(self):
        """Gera o relatório completo."""
        self._gerar_cabecalho()
        for nome, dados in self.resultados.items():
            self._gerar_solucao(nome, dados)
        self._gerar_resumo()
        return "\n".join(self.linhas)
    
    def salvar(self, arquivo_saida):
        """Salva o relatório em um arquivo .txt."""
        conteudo = self.gerar()
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        return arquivo_saida