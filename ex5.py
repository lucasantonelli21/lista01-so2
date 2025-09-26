import threading, queue, argparse, sys, time

def eh_primo(num):
    if num <= 1: return False
    if num <= 3: return True
    if num % 2 == 0: return False
    i = 3
    while i * i <= num:
        if num % i == 0: return False
        i += 2
    return True

def trabalhador(fila, wid):
    while True:
        valor = fila.get()
        if valor == -1:
            print(f"[TRAB {wid}] recebeu poison, encerrando...")
            break
        resultado = "primo" if eh_primo(valor) else "composto"
        print(f"[TRAB {wid}] começou {valor}")
        time.sleep(0.1)
        print(f"[TRAB {wid}] terminou: {valor} é {resultado}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", type=int, default=4, help="Número de threads")
    parser.add_argument("-n", type=int, default=32, help="Capacidade da fila")
    args = parser.parse_args()

    fila = queue.Queue(args.n)

    trabalhadores = []
    for i in range(args.t):
        th = threading.Thread(target=trabalhador, args=(fila, i))
        th.start()
        trabalhadores.append(th)

    print("Digite números (EOF encerra):")
    qtd_tarefas = 0
    for linha in sys.stdin:
        try:
            valor = int(linha.strip())
            fila.put(valor)
            qtd_tarefas += 1
            print(f"[MAIN] enfileirado {valor}")
        except:
            continue


    for _ in range(args.t):
        fila.put(-1)

    for th in trabalhadores:
        th.join()

    print(f"✅ Todos terminaram. {qtd_tarefas} tarefas processadas com sucesso.")

if __name__ == "__main__":
    main()
