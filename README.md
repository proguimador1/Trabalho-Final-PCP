# Trabalho Final de PCP

Membros:
- Pedro Otávio
- Gulherme
- JV

## Requisitos de Implementação: Problema do Bar dos Filósofos

Este documento detalha os requisitos técnicos e funcionais para a simulação do problema de programação concorrente "Bar dos Filósofos" (Drinking Philosophers Problem).

### 1. Arquitetura e Estrutura de Dados
* **Entrada de Dados:** O sistema deve ler obrigatoriamente um arquivo `.txt` contendo uma matriz de adjacência quadrada.
* **Mapeamento do Grafo:**
    * **Vértices (Nós):** Representam os Filósofos.
    * **Arestas (Conexões):** Representam os recursos compartilhados (Garrafas).
* **Concorrência:** Cada filósofo deve ser implementado como uma unidade de execução independente (**Thread** ou Processo).
* **Sincronização:** As garrafas (arestas) devem ser protegidas por mecanismos de exclusão mútua (**Locks/Mutexes**) para evitar condições de corrida.

### 2. Ciclo de Vida do Filósofo (Máquina de Estados)
Cada instância de Filósofo deve transitar ciclicamente entre os três estados abaixo:

1.  **Tranquilo:**
    * **Duração:** Tempo aleatório entre `0` e `n` segundos (onde `n` é o grau de conectividade do nó).
2.  **Com Sede:**
    * **Ação:** Sortear uma quantidade de garrafas para a sessão (entre `2` e o total de vizinhos).
    * **Seleção:** Escolher aleatoriamente quais vizinhos (arestas) serão solicitados.
    * **Duração:** Tempo de espera variável até obter acesso exclusivo a todos os recursos sorteados.
3.  **Bebendo:**
    * **Duração:** Fixa em `1` segundo.
    * **Ação:** Após o tempo, liberar todas as garrafas e retornar ao estado **Tranquilo**.

### 3. Regras de Simulação
* **Controle de Ciclos:**
    * **Casos 1 e 2:** Cada filósofo deve completar **6 ciclos** de bebida.
    * **Caso 3:** Cada filósofo deve completar **3 ciclos** de bebida.
* **Prevenção de Falhas:** A implementação deve garantir a ausência de:
    * **Deadlock:** Impasse onde nenhum filósofo consegue progredir.
    * **Starvation:** Situação onde um filósofo nunca consegue beber enquanto outros bebem repetidamente.

### 4. Algoritmos de Solução (Mínimo de 2)
Devem ser implementadas e comparadas ao menos duas das seguintes estratégias:
* **Ordenação de Recursos:** Filósofos requisitam garrafas seguindo uma ordem numérica pré-definida.
* **Hierarquia/Árbitro:** Um agente central autoriza ou nega o acesso aos recursos.
* **Chandy-Misra:** Uso de tokens (garrafas sujas/limpas) para coordenar a prioridade.
* **Backoff Aleatório:** Se não conseguir todos os recursos, libera os atuais e aguarda antes de tentar novamente.

### 5. Relatórios e Métricas (Saída)
Ao final da execução, o programa deve exibir:
* **Tempos Individuais:** Log de quanto tempo cada filósofo passou em cada estado.
* **Tempo Total:** Duração total da simulação.
* **Tempo de Espera Médio:** Cálculo da média do estado "Com Sede" por filósofo para avaliação de desempenho e justiça (fairness).