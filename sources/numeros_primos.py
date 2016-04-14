#!/usr/bin/python3
# -*- coding: utf-8 -*-


class NumeroPrimo:
    def eh_numero_primo(self, n):
        assert isinstance(n, int)
        assert n > 0

        primo = True

        if n > 2:
            for x in range(2, n - 1):
                if n % x == 0:
                    primo = False
                    break

        return primo

    def lista_numeros_primos(self, inicial, final):
        assert isinstance(inicial, int)
        assert isinstance(inicial, int)
        assert inicial > 0

        if final < inicial:
            inicial, final = final, inicial

        lista = []
        for x in range(inicial, final + 1):
            if self.eh_numero_primo(x):
                lista.append(x)

        return lista

    def gerador_numero_primo(self):
        cont = 0
        while True:
            cont += 1
            if self.eh_numero_primo(cont):
                yield cont


if __name__ == "__main__":
    # Teste em interface de texto.
    while True:
        print("Números primos\n")
        opc = int(input("1 - Verificar\n"
                        "2 - Listar\n"
                        "3 - Gerador infinito\n"
                        "0 - Sair\n"
                        "\t: "))

        np = NumeroPrimo()

        if opc == 1:
            n = int(input("\nDigite um número: "))
            print(n, "é PRIMO\n" if np.eh_numero_primo(n) else "NÃO é primo\n")
        elif opc == 2:
            t = input("\nDigite 2 números(x,y): ")

            t = [int(x) for x in (t.split(","))]
            if t[0] > t[1]:
                t[0], t[1] = t[1], t[0]

            print(np.lista_numeros_primos(t[0], t[1]), end="\n")
        elif opc == 3:
            if (input("\nCTRL + C, para PARAR.\nContinuar(S/n): ")).upper() == 'S':
                g = np.gerador_numero_primo()
                cont = 1

                while True:
                    v = next(g)
                    print("{}:{}".format(cont, v))
                    cont += 1
        else:
            break

        if opc != 0:
            input("\n\nEnter para continuar ")

        print("\n")
