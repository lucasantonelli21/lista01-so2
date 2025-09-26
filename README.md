# Lista 1 - SO2

## Exercício 1: Corrida de Cavalos com Threads

Simulação de corrida onde cada cavalo é uma thread. Implementa largada sincronizada, exclusão mútua e sistema de apostas.

### Funcionalidades
- **Apostas**: Usuário escolhe cavalo antes da largada
- **Largada sincronizada**: Event() coordena início simultâneo
- **Exclusão mútua**: Locks protegem placar e definição do vencedor
- **Empates determinísticos**: Resolvidos por ordem alfabética

## Exercício 2: Buffer Circular Produtores/Consumidores

Buffer circular com múltiplos produtores e consumidores. Analisa impacto do tamanho do buffer no desempenho.

### Funcionalidades
- **Buffer circular**: Array de tamanho N com índices circulares
- **Exclusão mútua**: Mutex protege acesso ao buffer
- **Variáveis de condição**: Eliminam espera ativa (busy-wait)
- **Estatísticas**: Throughput e tempo médio de espera
- **Experimentos**: Testa diferentes tamanhos de buffer (1, 5, 10, 20)
## Exercício 3: Transferências entre Contas

Simulação de várias contas bancárias acessadas por threads. As threads fazem transferências aleatórias preservando a soma global.

### Funcionalidades
- **Contas**: Lista de contas compartilhadas
- **Exclusão mútua**: Locks garantem a segurança das transferências
- **Verificação**: Soma inicial e final comparadas
- **Modo sem trava**: Demonstra condição de corrida


## Exercício 4: Linha de Produção com Filas

Pipeline com três etapas: captura, processamento e gravação. Usa filas limitadas e sinal de encerramento com poison-pill.

### Funcionalidades
- **Captura**: Gera itens e coloca na fila
- **Processamento**: Threads consomem e transformam os dados
- **Gravação**: Consome resultados e imprime
- **Fim limpo**: Poison-pill encerra o fluxo sem travar

## Exercício 5: Pool de Tarefas CPU-Bound

Implementação de um pool fixo de N threads que processa uma fila concorrente de tarefas
de CPU (teste de primalidade). As tarefas são enfileiradas a partir da entrada padrão (stdin) 
e o sistema processa até o EOF. A finalização é feita com sinalização de poison-pill.

### Funcionalidades
- **Leitura de tarefas**: números inteiros lidos da entrada padrão até EOF
- **Fila concorrente**: uso de queue.Queue (thread-safe) para compartilhar tarefas
- **Thread pool**: N threads fixas consomem tarefas da fila
- **CPU-bound**: cada tarefa executa um teste de primalidade
- **Encerramento limpo**: após EOF, a main envia um poison-pill para cada thread
- **Prova de corretude**: cada número lido gera exatamente uma saída antes do término

## Exercício 6: MapReduce com Threads para Soma e Histograma

Leitura de um arquivo grande de inteiros e cálculo da soma total e do histograma de frequências
usando P threads em paralelo.

### Funcionalidades
- **Particionamento**: Arquivo dividido em blocos para cada thread
- **Map local**: Cada thread calcula soma e histograma do seu bloco
- **Reduce**: Thread principal combina resultados com mínima exclusão mútua
- **Speedup**: Mede o tempo de execução com diferentes valores de P


### Exercício 7: Filósofos Jantando com Threads

Simula o clássico problema dos filósofos jantando utilizando threads, locks e semáforos.

## Funcionalidades principais:

- Threads como filósofos: Cada filósofo é uma thread que alterna entre pensar e comer.
- Garfos protegidos por locks: Cada garfo é um threading.Lock(), garantindo exclusão mútua.
- Fila de espera: Uma deque protege a ordem de quem pode pegar os garfos, evitando fome.
- Semáforo opcional: Limita o número de filósofos tentando comer simultaneamente, prevenindo deadlocks.
- Medição de desempenho: Calcula tempo de espera total, médio e máximo de cada filósofo.
- Empates determinísticos: Se dois filósofos tentam pegar os garfos ao mesmo tempo, a ordem alfabética ou numérica é usada.

O código principal (experimento) inicializa os filósofos, threads e garfos, executa as refeições e exibe estatísticas.


## Exercício 8: Buffer com Rajadas e Backpressure

Extensão do Exercício 2 para simular rajadas de produção (bursts) e períodos de ociosidade.
Implementa backpressure usando queue.Queue (thread-safe), que faz produtores aguardarem quando 
o buffer está cheio. Registra a ocupação do buffer ao longo do tempo para análise de estabilidade.

### Funcionalidades
- **Rajadas**: Produtores inserem itens em bursts e depois ficam ociosos
- **Backpressure**: Produtores bloqueiam automaticamente se o buffer enche
- **Consumidores**: Retiram itens em ritmo mais lento e variável
- **Medições**: Ocupação média e máxima do buffer registradas
- **Finalização limpa**: Uso de None como poison-pill


### Exercício 9: Corrida de Revezamento

Simula uma corrida de revezamento onde cada atleta é uma thread. Todas as threads de uma equipe devem atingir uma barreira para liberar a próxima rodada.

## Funcionalidades principais:

- Barreira sincronizada: threading.Barrier(k) garante que todos os atletas da equipe chegam à "largada" antes da próxima perna.
- Threads como atletas: Cada atleta corre (sleep aleatório) e espera na barreira.
- Contagem de rodadas: O atleta líder (índice 0 na barreira) incrementa o número de rodadas concluídas.
- Medição de desempenho: Conta quantas rodadas completas a equipe consegue realizar em um tempo fixo (DURACAO_EXPERIMENTO).

O código permite testar diferentes tamanhos de equipe e medir como o número de atletas afeta a performance.


### Exercício 10: Deadlock e Watchdog

Simula threads competindo por recursos e monitora risco de deadlock usando um watchdog.

## Funcionalidades principais:

- Threads com risco de deadlock: Algumas threads tentam adquirir locks em ordens diferentes, podendo travar.
- Threads sem risco de deadlock: Seguem ordem fixa de locks, prevenindo bloqueio circular.
- Watchdog: Monitora se houve progresso dentro de um intervalo de tempo (T) e registra alertas.
- Exclusão mútua para monitoramento: atividade_lock protege o acesso à última atividade global.
- Comparação de cenários: Ao final, exibe o número de alertas de cada cenário, permitindo análise do risco de deadlock.

O experimento mostra na prática como mudanças na ordem de aquisição de locks podem afetar a segurança e o progresso das threads.