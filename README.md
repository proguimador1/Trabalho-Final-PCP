# Trabalho Final PCP - Problema dos Filósofos com Garrafas

## Descrição

Este projeto implementa uma variação do **Problema dos Filósofos** com garrafas, onde filósofos em um grafo precisam coordenar o acesso a garrafas compartilhadas. O objetivo é comparar diferentes algoritmos de sincronização concorrente para evitar deadlock e garantir acesso justo aos recursos.

## O Problema

Em um grafo não direcionado, cada vértice representa um filósofo e cada aresta representa uma garrafa compartilhada entre dois filósofos vizinhos. Cada filósofo precisa:

1. **Pensar** (estado tranquilo) por um tempo aleatório
2. **Ficar com sede** e escolher aleatoriamente de 2 até o seu grau de vizinhança garrafas
3. **Pegar todas as garrafas** escolhidas simultaneamente
4. **Beber** por 1 segundo
5. Repetir o ciclo por N rodadas

O desafio é garantir que:
- Não ocorra **deadlock**
- Não ocorra **starvation** (inanição)
- O acesso às garrafas seja **justo**
- O tempo de espera seja **minimizado**

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
- Não garante ausência de starvation (embora seja raro)
- Tempo de espera imprevisível
- Pode ter alto overhead em situações de contenção

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
| Numeração | O(E log E) | Sim | Baixo | Baixa |
| Árbitro | O(1) |  Sim | Médio | Média |
| Chandy-Misra | O(E) |  Sim | Alto | Alta |
| Aleatoriedade | O(1) |  Não* | Baixo | Alta |

*Na prática, starvation é extremamente raro devido ao backoff exponencial.

## Conceitos Teóricos

### Deadlock
Ocorre quando dois ou mais filósofos ficam bloqueados indefinidamente, cada um esperando por uma garrafa que está com outro filósofo.

**Condições de Coffman (todas devem ser evitadas):**
1. Exclusão mútua
2. Posse e espera
3. Não preempção
4. Espera circular

### Starvation (Inanição)
Ocorre quando um filósofo nunca consegue beber, apesar de não estar em deadlock.

### Sincronização com Threads
- **Locks (threading.Lock):** Garantem exclusão mútua
- **Semáforos (threading.Semaphore):** Controlam acesso a recursos limitados
- **Threads Daemon:** Encerram automaticamente quando o programa principal termina

## Trabalho Acadêmico

**Disciplina:** Programação Concorrente  
**Instituição:** Universidade Estadual do Ceará  
**Objetivo:** Implementar e comparar algoritmos de sincronização para o problema dos filósofos com garrafas em grafos.

## Autores

Desenvolvido como trabalho final da disciplina de Programação Concorrente.

## Licença

Este projeto é de caráter educacional e acadêmico.