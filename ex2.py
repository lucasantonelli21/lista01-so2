import threading
import time
import random
from collections import deque

class BufferCircular:
    def __init__(self, tamanho):
        self.buffer = [None] * tamanho
        self.tamanho = tamanho
        self.inicio = 0
        self.fim = 0
        self.count = 0
        
        self.mutex = threading.Lock()
        self.cheio = threading.Condition(self.mutex)
        self.vazio = threading.Condition(self.mutex)
        
        # Estatísticas
        self.itens_produzidos = 0
        self.itens_consumidos = 0
        self.tempo_espera_total = 0
        self.inicio_experimento = time.time()
    
    def produzir(self, item):
        inicio_espera = time.time()
        with self.vazio:
            while self.count == self.tamanho:
                self.vazio.wait()
            
            self.buffer[self.fim] = item
            self.fim = (self.fim + 1) % self.tamanho
            self.count += 1
            self.itens_produzidos += 1
            self.tempo_espera_total += time.time() - inicio_espera
            
            self.cheio.notify()
    
    def consumir(self):
        inicio_espera = time.time()
        with self.cheio:
            while self.count == 0:
                self.cheio.wait()
            
            item = self.buffer[self.inicio]
            self.inicio = (self.inicio + 1) % self.tamanho
            self.count -= 1
            self.itens_consumidos += 1
            self.tempo_espera_total += time.time() - inicio_espera
            
            self.vazio.notify()
            return item
    
    def estatisticas(self):
        tempo_total = time.time() - self.inicio_experimento
        throughput = (self.itens_produzidos + self.itens_consumidos) / (2 * tempo_total)
        tempo_medio_espera = self.tempo_espera_total / max(1, self.itens_produzidos + self.itens_consumidos)
        return throughput, tempo_medio_espera

def produtor(buffer, id_produtor, total_itens):
    for i in range(total_itens):
        item = f"P{id_produtor}-{i}"
        buffer.produzir(item)
        time.sleep(random.uniform(0.01, 0.05))

def consumidor(buffer, id_consumidor, total_itens):
    for _ in range(total_itens):
        item = buffer.consumir()
        time.sleep(random.uniform(0.01, 0.05))

def experimento(tamanho_buffer, num_produtores=2, num_consumidores=2, itens_por_thread=20):
    buffer = BufferCircular(tamanho_buffer)
    threads = []
    
    # Criar produtores
    for i in range(num_produtores):
        t = threading.Thread(target=produtor, args=(buffer, i, itens_por_thread))
        threads.append(t)
    
    # Criar consumidores
    for i in range(num_consumidores):
        t = threading.Thread(target=consumidor, args=(buffer, i, itens_por_thread))
        threads.append(t)
    
    # Iniciar threads
    for t in threads:
        t.start()
    
    # Aguardar conclusão
    for t in threads:
        t.join()
    
    return buffer.estatisticas()

def main():
    print("BUFFER CIRCULAR - PRODUTORES/CONSUMIDORES")
    print("=" * 45)
    
    tamanhos = [1, 5, 10, 20]
    
    for tamanho in tamanhos:
        throughput, tempo_espera = experimento(tamanho)
        print(f"Buffer {tamanho:2d}: Throughput={throughput:6.2f} ops/s, Espera={tempo_espera*1000:5.1f}ms")

if __name__ == "__main__":
    main()
