import threading, argparse, time
from collections import Counter

def processar_bloco(bloco, soma_local, hist_local, tid):
    soma = sum(bloco)
    hist = Counter(bloco)
    soma_local[tid] = soma
    hist_local[tid] = hist
    print(f"[THREAD {tid}] processou {len(bloco)} números")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", type=str, required=True, help="Arquivo de inteiros")
    parser.add_argument("-p", type=int, default=4, help="Número de threads")
    args = parser.parse_args()

    with open(args.f) as arq:
        numeros = [int(l.strip()) for l in arq if l.strip()]

    n = len(numeros)
    bloco_tam = (n + args.p - 1) // args.p

    soma_local = [0]*args.p
    hist_local = [None]*args.p
    threads = []

    inicio = time.time()
    for i in range(args.p):
        inicio_b = i*bloco_tam
        fim_b = min((i+1)*bloco_tam, n)
        bloco = numeros[inicio_b:fim_b]
        t = threading.Thread(target=processar_bloco, args=(bloco, soma_local, hist_local, i))
        t.start()
        threads.append(t)

    for t in threads: t.join()

    soma_total = sum(soma_local)
    hist_total = Counter()
    for h in hist_local: hist_total.update(h)

    fim = time.time()

    print("\n--- RESULTADO FINAL ---")
    print(f"Soma total = {soma_total}")
    print("Histograma (primeiros 10 valores):")
    for v, c in list(hist_total.items())[:10]:
        print(f"{v}: {c}")
    print(f"Tempo total: {fim - inicio:.4f}s")

if __name__ == "__main__":
    main()
