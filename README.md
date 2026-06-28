# Trabalho Final PCP - Bar dos Filósofos

## Descrição

Este projeto implementa o **Bar dos Filósofos** (*Drinking Philosophers Problem*), uma generalização do clássico Problema do Jantar dos Filósofos. O objetivo é simular a coordenação de filósofos em um grafo para acessar garrafas compartilhadas, comparando diferentes algoritmos de sincronização concorrente quanto à eficiência e justiça.

## O Problema

Em um grafo não direcionado:
- **Vértices** → filósofos
- **Arestas** → garrafas compartilhadas entre dois filósofos vizinhos

Cada filósofo executa ciclos de:
1. **Pensar** (estado tranquilo) por tempo aleatório (0 a n segundos, onde n é seu grau)
2. **Ficar com sede** e escolher aleatoriamente de 2 até n garrafas
3. **Adquirir todas** as garrafas escolhidas
4. **Beber** por 1 segundo
5. Repetir até completar N rodadas (6 para grafos pequenos, 3 para grafos grandes)

**Desafios:**
- Evitar **deadlock** (filósofos travados indefinidamente)
- Evitar **starvation** (filósofos que nunca conseguem beber)
- Garantir **justiça** no acesso às garrafas
- Minimizar **tempo de espera**

## Estrutura do Projeto

```
Trabalho-Final-PCP/
├── main.py                    # Ponto de entrada do programa
├── grafo.py                   # Representação do grafo (matriz e lista de adjacência)
├── filosofo.py                # Classe Filosofo com estados e comportamentos
├── simulacao.py               # Gerenciador de simulação com threads
├── solucao.py                 # Classe base abstrata para soluções
├── solucao_numeracao.py       # Solução por numeração de recursos
├── solucao_arbitro.py         # Solução com árbitro (semáforo)
├── solucao_chandy_misra.py    # Solução Chandy-Misra (algoritmo distribuído)
├── solucao_aleatoriedade.py   # Solução com backoff exponencial aleatório
├── relatorio.py               # Geração de relatórios comparativos
├── arquivo_caso1.txt          # Caso de teste 1 (5 vértices, 6 rodadas)
├── arquivo_caso2.txt          # Caso de teste 2 (6 vértices, 6 rodadas)
├── arquivo_caso3.txt          # Caso de teste 3 (12 vértices, 3 rodadas)
└── arquivo_caso*_resultado.txt # Resultados gerados automaticamente
```

## Algoritmos Implementados

### 1. Numeração de Recursos (`solucao_numeracao.py`)

**Estratégia:** Ordena as garrafas por ID numérico e adquire os locks sempre na mesma ordem.

**Funcionamento:**
- Cada garrafa recebe um ID único
- O filósofo ordena suas garrafas desejadas por ID
- Adquire os locks em ordem crescente
- Evita deadlock por ordering (ordenação global)

**Vantagens:**
- Simples de implementar
- Garante ausência de deadlock
- Baixo overhead

**Desvantagens:**
- Pode causar contenção (muitos filósofos competindo pela mesma garrafa)
- Não é justo por natureza

### 2. Árbitro (`solucao_arbitro.py`)

**Estratégia:** Usa um semáforo que permite no máximo N-1 filósofos tentando adquirir garrafas simultaneamente.

**Funcionamento:**
- Semáforo inicializado com N-1 (onde N é o número de filósofos)
- Filósofo adquire permissão do árbitro antes de pegar garrafas
- Pelo menos um filósofo sempre consegue todas as suas garrafas
- Libera o árbitro após beber

**Vantagens:**
- Garante ausência de deadlock (teorema do árbitro)
- Simples e eficiente
- Bom desempenho em grafos densos

**Desvantagens:**
- Pode causar contenção no árbitro
- Limita paralelismo a N-1 filósofos

### 3. Chandy-Misra (`solucao_chandy_misra.py`)

**Estratégia:** Algoritmo distribuído baseado em mensagens entre filósofos.

**Funcionamento:**
- Cada garrafa tem um estado (CHEIA ou VAZIA) e um dono
- Filósofos enviam pedidos de garrafas para vizinhos
- Quem tem a garrafa VAZIA a entrega (marca como CHEIA e transfere posse)
- Se o dono está bebendo, enfileira o pedido
- Se não consegue todas as garrafas, libera e tenta novamente

**Vantagens:**
- Algoritmo clássico e bem estudado
- Distribui a carga entre os filósofos
- Evita deadlock e starvation

**Desvantagens:**
- Overhead de mensagens
- Complexidade de implementação
- Pode ter alta contenção em grafos densos

### 4. Aleatoriedade com Backoff (`solucao_aleatoriedade.py`)

**Estratégia:** Tenta pegar garrafas sem bloqueio; se falhar, libera tudo e espera um tempo aleatório.

**Funcionamento:**
- Tenta adquirir cada garrafa com `acquire(blocking=False)`
- Se não consegue todas, libera as que pegou
- Aguarda tempo aleatório entre 0.1s e 1.0s (backoff)
- Repete até conseguir todas as garrafas

**Vantagens:**
- Muito simples
- Baixa contenção
- Justo probabilisticamente

**Desvantagens:**
- Tempo de espera imprevisível
- Pode ter alto overhead em situações de contenção

## Métricas de Avaliação

### Índice de Jain (Jain's Fairness Index)
Mede a equidade na distribuição dos tempos de espera.
J = (Σ x_i)² / (n * Σ x_i²)


- **J = 1.0** → Perfeitamente justo (todos esperaram o mesmo tempo)
- **J próximo de 1.0** → Alta justiça
- **J próximo de 0** → Baixa justiça (starvation)

### Coeficiente de Variação (CV)
Mede a dispersão relativa dos tempos de espera.
CV = (Desvio Padrão / Média) × 100%
- **CV < 30%** → Baixa dispersão (tempos equilibrados)
- **CV > 70%** → Alta dispersão (baixa equidade)
## Como Executar

### Pré-requisitos

- Python 3.7+
- Nenhuma dependência externa (usa apenas biblioteca padrão)

### Execução

```bash
# Executar com caso de teste 1 (5 vértices, 6 rodadas)
python main.py arquivo_caso1.txt

# Executar com caso de teste 2 (6 vértices, 6 rodadas)
python main.py arquivo_caso2.txt

# Executar com caso de teste 3 (12 vértices, 3 rodadas)
python main.py arquivo_caso3.txt
```

### Formato dos Arquivos de Entrada

Arquivos `.txt` contendo matriz de adjacência separada por vírgulas:

```
0,1,0,0,1
1,0,1,0,0
0,1,0,1,0
0,0,1,0,1
1,0,0,1,0
```

- `1` indica aresta entre vértices
- `0` indica ausência de aresta
- Matriz deve ser simétrica (grafo não direcionado)

### Saída

O programa gera:
1. **Console:** Logs detalhados do progresso de cada filósofo
2. **Arquivo de resultado:** `arquivo_caso*_resultado.txt` com estatísticas comparativas

Exemplo de saída no console:
```
============================================================
ARQUIVO: arquivo_caso1.txt | VÉRTICES: 5 | RODADAS: 6
============================================================

 Numeração
------------------------------------------------------------
Filósofo 0 quer 2 garrafas: 0(v1),3(v4)
Filósofo 0 tentando pegar garrafas: [0, 3]
Filósofo 0 pegou garrafa 0
Filósofo 0 pegou garrafa 3
Filósofo 0 começou a beber (esperou 0.00s)
...
```

Exemplo de saída no arquivo:


============================================================
ARQUIVO: arquivo_caso1.txt | VÉRTICES: 5 | RODADAS: 6
============================================================

SOLUÇÃO: Chandy-Misra
------------------------------------------------------------
Tempo total de execução: 17.29 segundos
Média de espera geral: 0.65s

Detalhes por filósofo:
------------------------------------------------------------
Filósofo 0 (grau 2):
  Rodadas: 6
  Tempo tranquilo: 8.32s
  Tempo com sede (espera): 2.49s
  Tempo bebendo: 6.00s
  Tempo médio de espera: 0.41s
...

============================================================
RESUMO COMPARATIVO
============================================================
Solução              Tempo Total     Espera Média    Jain       CV(%)
--------------------------------------------------------------------------------
Numeração            18.49           0.70            0.884      36.2
Árbitro              16.24           0.51            0.934      26.6
Chandy-Misra         17.29           0.65            0.968      18.0
Aleatoriedade        22.93           1.29            0.958      20.9

## Resultados e Métricas

Cada solução é avaliada por:

- **Tempo Total:** Tempo de execução da simulação
- **Espera Média:** Tempo médio que filósofos esperam desde que ficam com sede até conseguirem beber
- **Rodadas Completadas:** Número de ciclos pensamento-sede-beber realizados
- **Tempo por Estado:** Tempo gasto em cada estado (tranquilo, com sede, bebendo)

## Casos de Teste

### Caso 1 (`arquivo_caso1.txt`)
- **5 vértices** (grafo ciclo/caminho)
- **6 rodadas** por filósofo
- Grafo esparso, baixo grau médio

### Caso 2 (`arquivo_caso2.txt`)
- **6 vértices**
- **6 rodadas** por filósofo
- Grafo médio, complexidade moderada

### Caso 3 (`arquivo_caso3.txt`)
- Configuração diferente de grafo (12 vértices)
- **3 rodadas** por filósofo
- Testa robustez em diferentes topologias

## Análise Comparativa

| Solução | Complexidade | Garantia de Ausência de Deadlock | Overhead | Justiça |
|---------|-------------|----------------------------------|----------|---------|
| Numeração | O(E log E) | Evita | Baixo | Moderada |
| Árbitro | O(1) |  Evita | Médio | Alta |
| Chandy-Misra | O(E) |  Evita | Alto | Muito Alta |
| Aleatoriedade | O(1) |  Pratico* | Baixo | Alta |

*Na prática, starvation é extremamente raro devido ao backoff exponencial.


## Trabalho Acadêmico

**Disciplina:** Programação Concorrente  
**Instituição:** Universidade Estadual do Ceará  
**Objetivo:** Implementar e comparar algoritmos de sincronização para o problema dos filósofos com garrafas em grafos.

## Autores
- Guilherme Souto De Andrade
- Joao Victor Dos Santos Sales
- Maurílio Salvaterra Cordeiro Neto
- Pedro Otávio De Sousa Bezerra

Desenvolvido como trabalho final da disciplina de Programação Concorrente.

## Licença

Este projeto é de caráter educacional e acadêmico.