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
