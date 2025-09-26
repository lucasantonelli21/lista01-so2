import threading
import time
import random
from collections import deque

class Filosofo(threading.Thread):

    def __init__(self, id, garfos, fila, lock_fila, semaforo=None,
                 ordem_global=False, refeicoes=25):
        super().__init__()
        self.id = id
        self.garfos = garfos          
        self.n = len(garfos)
        self.fila = fila                
        self.lock_fila = lock_fila     
        self.semaforo = semaforo        
        self.ordem_global = ordem_global
        self.refeicoes_a_fazer = refeicoes

        self.qtd_refeicoes = 0
        self.maior_espera = 0.0
        self.total_espera = 0.0

    def pensar(self):
        time.sleep(random.uniform(0.005, 0.02))

    def comer(self):
        time.sleep(random.uniform(0.005, 0.02))

    def espera_media(self):
        if self.qtd_refeicoes == 0:
            return 0.0
        return self.total_espera / self.qtd_refeicoes

    def tentar_pegar_dois_garfos(self, primeiro, segundo, timeout=0.1):
        self.garfos[primeiro].acquire()
        conseguiu = self.garfos[segundo].acquire(timeout=timeout)
        if conseguiu:
            return True
        else:
            self.garfos[primeiro].release()
            return False

    def soltar_garfos(self, esquerdo, direito):
        try:
            self.garfos[esquerdo].release()
        except RuntimeError:
            pass
        try:
            self.garfos[direito].release()
        except RuntimeError:
            pass

    def requisitar_para_comer(self):
        inicio = time.time()

        if self.semaforo:
            self.semaforo.acquire()

        with self.lock_fila:
            self.fila.append(self.id)

        conseguiu = False
        while not conseguiu:
            with self.lock_fila:
                cabeca = self.fila[0] if len(self.fila) > 0 else None
            if cabeca != self.id:
                time.sleep(0.002)
                continue

            esquerdo = self.id
            direito = (self.id + 1) % self.n
            if self.ordem_global:
                primeiro, segundo = (min(esquerdo, direito), max(esquerdo, direito))
            else:
                primeiro, segundo = esquerdo, direito

            sucesso = self.tentar_pegar_dois_garfos(primeiro, segundo, timeout=0.05)

            if sucesso:
                with self.lock_fila:
                    if len(self.fila) > 0 and self.fila[0] == self.id:
                        self.fila.popleft()
                    else:
                        self.soltar_garfos(esquerdo, direito)
                        sucesso = False

            if sucesso:
                conseguiu = True
            else:
                time.sleep(random.uniform(0.002, 0.01))

        fim = time.time()
        return fim - inicio

    def run(self):
        for _ in range(self.refeicoes_a_fazer):
            self.pensar()

            espera = self.requisitar_para_comer()
            self.total_espera += espera
            self.maior_espera = max(self.maior_espera, espera)

            self.comer()
            self.qtd_refeicoes += 1

            esquerdo = self.id
            direito = (self.id + 1) % self.n
            self.soltar_garfos(esquerdo, direito)

            if self.semaforo:
                try:
                    self.semaforo.release()
                except ValueError:
                    pass


def experimento(qtd_filosofos=4, refeicoes=25, solucao="a", limite_semaforo=None, ordem_global=True, seed=42):

    random.seed(seed)
    n = qtd_filosofos

    garfos = [threading.Lock() for _ in range(n)]
    fila = deque()
    lock_fila = threading.Lock()
    semaforo = threading.Semaphore(limite_semaforo) if limite_semaforo else None

    filosofos = [
        Filosofo(i, garfos, fila, lock_fila,
                 semaforo=semaforo,
                 ordem_global=ordem_global,
                 refeicoes=refeicoes)
        for i in range(n)
    ]

    inicio = time.time()
    for f in filosofos:
        f.start()
    for f in filosofos:
        f.join()
    fim = time.time()

    print(f"\n=== EXPERIMENTO ({solucao}) ===")
    print(f"Filósofos: {n}, Refeições cada: {refeicoes}, Tempo total: {fim - inicio:.3f}s")

    total_refeicoes = 0
    for f in filosofos:
        total_refeicoes += f.qtd_refeicoes
        print(f"Filósofo {f.id:2d} | Refeições = {f.qtd_refeicoes:2d} | "
              f"Maior espera = {f.maior_espera*1000:8.2f} ms | "
              f"Espera média = {f.espera_media()*1000:8.2f} ms")

    esperado = n * refeicoes
    print(f"Total de refeições: {total_refeicoes} (esperado {esperado})")


def main():
    qtd_filosofos = 4
    refeicoes = 25

    experimento(qtd_filosofos=qtd_filosofos,
                refeicoes=refeicoes,
                solucao="a",
                limite_semaforo=None,
                ordem_global=True,
                seed=123)

    experimento(qtd_filosofos=qtd_filosofos,
                refeicoes=refeicoes,
                solucao="b",
                limite_semaforo=4,
                ordem_global=True,
                seed=123)


if __name__ == "__main__":
    main()
