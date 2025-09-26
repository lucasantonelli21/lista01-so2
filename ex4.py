import threading, queue, argparse, time, random

def capturar(fila1, qtd, semente, trabalhadores):
    rnd = random.Random(semente)
    for i in range(qtd):
        dado = rnd.randint(0, 999)
        print(f"[CAP] gerado {dado}")
        fila1.put(dado)
        time.sleep(0.01)
    for _ in range(trabalhadores):
        fila1.put(-1)
    print("[CAP] terminou e mandou poison")

def processar(fila1, fila2, wid):
    while True:
        dado = fila1.get()
        if dado == -1:
            fila2.put(-1)
            print(f"[PROC {wid}] recebeu poison, saindo")
            break
        resultado = dado * dado
        print(f"[PROC {wid}] processou {dado} -> {resultado}")
        fila2.put(resultado)
        time.sleep(0.02)

def gravar(fila2, trabalhadores):
    finalizados = 0
    while finalizados < trabalhadores:
        dado = fila2.get()
        if dado == -1:
            finalizados += 1
            continue
        print(f"[GRAV] salvando resultado {dado}")
        time.sleep(0.01)
    print("[GRAV] terminou tudo!")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", type=int, default=2)
    parser.add_argument("-n", type=int, default=20)
    parser.add_argument("-s", type=int, default=None)
    parser.add_argument("-d", type=int, default=0)
    args = parser.parse_args()

    semente = args.s or int(time.time())
    fila1, fila2 = queue.Queue(8), queue.Queue(8)

    th_cap = threading.Thread(target=capturar, args=(fila1,args.n,semente,args.t))
    th_cap.start()

    trabalhadores = []
    for i in range(args.t):
        th = threading.Thread(target=processar, args=(fila1,fila2,i))
        th.start()
        trabalhadores.append(th)

    th_grav = threading.Thread(target=gravar, args=(fila2,args.t))
    th_grav.start()

    th_cap.join()
    for th in trabalhadores: th.join()
    th_grav.join()

if __name__ == "__main__":
    main()
