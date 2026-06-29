import time
import sys
from grafo import Grafo
from simulacao import Simulacao
from solucao_numeracao import SolucaoNumeracao
from solucao_arbitro import SolucaoArbitro
from solucao_chandy_misra import SolucaoChandyMisra
from solucao_aleatoriedade import SolucaoAleatoriedade
from relatorio import Relatorio

def ler_matriz(arquivo):
    matriz = []
    with open(arquivo, 'r') as f:
        for linha in f:
            linha = linha.strip()
            if linha:
                valores = [int(x.strip()) for x in linha.split(',')]
                matriz.append(valores)
    return matriz

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo.txt>")
        print("Opções: arquivo_caso1.txt, arquivo_caso2.txt, arquivo_caso3.txt")
        sys.exit(1)
    
    nome_arquivo = sys.argv[1]
    matriz = ler_matriz(nome_arquivo)
    
    grafo = Grafo(matriz)
    rodadas = 3 if len(matriz) == 12 else 6
    
    solucoes = [
        ("Numeração", SolucaoNumeracao),
        ("Árbitro", SolucaoArbitro),
        ("Chandy-Misra", SolucaoChandyMisra),
        ("Aleatoriedade", SolucaoAleatoriedade)
    ]
    
    print("="*60)
    print(f"ARQUIVO: {nome_arquivo} | VÉRTICES: {grafo.num_vertices} | RODADAS: {rodadas}")
    print("="*60)
    
    # Cria relatório
    relatorio = Relatorio(nome_arquivo, grafo, rodadas)
    
    for nome, classe in solucoes:
        print(f"\n {nome}")
        print("-"*60)
        
        inicio = time.time()
        sim = Simulacao(grafo, classe, rodadas)
        sim.executar()
        tempo_total = time.time() - inicio
        
        media_espera = sum(d['tempo_medio_espera'] for d in sim.resultados.values()) / len(sim.resultados)
        
        dados = {
            'tempo_total': tempo_total,
            'media_espera': media_espera,
            'resultados': sim.resultados
        }
        
        relatorio.adicionar_solucao(nome, dados)
        
        print(f"Tempo total: {tempo_total:.2f}s")
        print(f"Média de espera: {media_espera:.2f}s")
    
    # Salva relatório
    nome_saida = nome_arquivo.replace('.txt', '_resultado.txt')
    relatorio.salvar(nome_saida)
    print(f"\n Resultados salvos em: {nome_saida}")
    
    # Mostra resumo na tela
    print("\n" + "="*60)
    print("RESUMO COMPARATIVO")
    print("="*60)
    print(f"{'Solução':<20} {'Tempo Total':<15} {'Espera Média':<15}")
    print("-"*60)
    
    for nome, dados in relatorio.resultados.items():
        print(f"{nome:<20} {dados['tempo_total']:<15.2f} {dados['media_espera']:<15.2f}")

if __name__ == "__main__":
    main()