import threading
import time
import random

DURACAO_EXPERIMENTO = 60


class CorridaRevezamento:
    def __init__(self, tamanho_equipe):
        self.k = tamanho_equipe
        self.barreira = threading.Barrier(self.k)
        self.rodadas = 0
        self.lock = threading.Lock()
        self.inicio = None

    def atleta(self, id_atleta):
        while True:
            if time.time() - self.inicio >= DURACAO_EXPERIMENTO:
                break

            time.sleep(random.uniform(0.01, 0.05))

            indice = self.barreira.wait()

            if indice == 0:
                with self.lock:
                    self.rodadas += 1

    def executar(self):
        self.inicio = time.time()
        threads = []

        for i in range(self.k):
            t = threading.Thread(target=self.atleta, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        return self.rodadas


def main():
    tamanhos_equipes = [2, 4, 8, 16]

    for k in tamanhos_equipes:
        corrida = CorridaRevezamento(k)
        rodadas = corrida.executar()
        print(f"Equipe com {k} atletas concluiu {rodadas} rodadas em {DURACAO_EXPERIMENTO} segundos.")


if __name__ == "__main__":
    main()
