import threading, random, argparse, time

class Conta:
    def __init__(self, saldo=1000):
        self.saldo = saldo
        self.trava = threading.Lock()

def fazer_transferencia(origem, destino, valor, usar_trava, debug):
    if usar_trava:
        x, y = (origem, destino) if id(origem) < id(destino) else (destino, origem)
        with x.trava, y.trava:
            origem.saldo -= valor
            destino.saldo += valor
    else:
        origem.saldo -= valor
        destino.saldo += valor
    if debug:
        print(f"Transferência: {valor} de {id(origem)%100} -> {id(destino)%100}")

def rotina_trabalhador(contas, qtd_ops, semente, usar_trava, debug, tid):
    rnd = random.Random(semente)
    for i in range(qtd_ops):
        a, b = rnd.sample(contas, 2)
        valor = rnd.randint(1, 9)
        fazer_transferencia(a, b, valor, usar_trava, debug)
        if debug and i % (qtd_ops//5) == 0:
            print(f"[Thread {tid}] progresso {i}/{qtd_ops}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", type=int, default=4)
    parser.add_argument("-n", type=int, default=10)
    parser.add_argument("-s", type=int, default=None)
    parser.add_argument("-d", type=int, default=0)
    args = parser.parse_args()

    semente = args.s or int(time.time())
    usar_trava = False if args.d == 2 else True

    contas = [Conta(1000) for _ in range(args.n)]
    saldo_inicial = sum(c.saldo for c in contas)

    print(f"Saldo inicial total = {saldo_inicial}")

    threads = []
    for i in range(args.t):
        th = threading.Thread(target=rotina_trabalhador, args=(contas, 20000, semente+i, usar_trava, args.d, i))
        th.start()
        threads.append(th)
    for th in threads: th.join()

    saldo_final = sum(c.saldo for c in contas)
    print("\n--- RESULTADO FINAL ---")
    for i, c in enumerate(contas):
        print(f"Conta {i}: saldo = {c.saldo}")
    print(f"Soma total: {saldo_final}")

    if usar_trava:
        assert saldo_final == saldo_inicial
        print("SOMA PRESERVADA")
    else:
        if saldo_final != saldo_inicial:
            print("CONDIÇÃO DE CORRIDA DETECTADA")
        else:
            print("Coincidiu, mas não é seguro")

if __name__ == "__main__":
    main()
