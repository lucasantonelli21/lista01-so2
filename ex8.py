
import threading, queue, argparse, time, random

def produtor(fila, idp, qtd, debug, ocupacao):
    for i in range(qtd):
        item = random.randint(1,100)
        fila.put(item)
        ocupacao.append(fila.qsize())
        if debug: print(f"[PROD {idp}] produziu {item} (ocupação {fila.qsize()})")
        if i % 10 == 0:
            time.sleep(random.uniform(0.3,0.6))  
    fila.put(None)

def consumidor(fila, idc, debug, ocupacao):
    while True:
        item = fila.get()
        if item is None:
            fila.put(None)
            break
        if debug: print(f"[CONS {idc}] consumiu {item} (ocupação {fila.qsize()})")
        ocupacao.append(fila.qsize())
        time.sleep(random.uniform(0.05,0.15))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, default=2, help="Produtores")
    parser.add_argument("-c", type=int, default=2, help="Consumidores")
    parser.add_argument("-n", type=int, default=20, help="Tamanho do buffer")
    parser.add_argument("-d", type=int, default=0, help="Debug")
    args = parser.parse_args()

    fila = queue.Queue(args.n)
    ocupacao = []
    threads = []

    for i in range(args.p):
        t = threading.Thread(target=produtor, args=(fila,i,30,args.d,ocupacao))
        t.start()
        threads.append(t)

    for i in range(args.c):
        t = threading.Thread(target=consumidor, args=(fila,i,args.d,ocupacao))
        t.start()
        threads.append(t)

    for t in threads: t.join()

    print("\n--- RESULTADO ---")
    print(f"Ocupação média do buffer: {sum(ocupacao)/len(ocupacao):.2f}")
    print(f"Ocupação máxima observada: {max(ocupacao)}")

if __name__ == "__main__":
    main()
