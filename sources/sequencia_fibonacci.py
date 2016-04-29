#!usr/bin/python3
# -*- coding: utf-8 -*-


class Fibonacci:
    """ Classe que implementa a sequência de Fibonacci. """
    def __init__(self):
        """ Construtor alimentando o atributo conjunto com sequência. """
        self._conjunto = self.listar(1, 10)

    def gerar_recursivo(self, n):
        """ Gerador baseado em recursão de acordo com posição(n) informada. """
        if n < 2:
            return n
        else:
            return self.gerar_recursivo(n - 1) + self.gerar_recursivo(n - 2)

    def gerar_iterativo(self, n):
        """ Gerador baseado em iteração de acordo com posição(n) informada. """
        i, j = 0, 1
        for x in range(n):
            i, j = j, (i + j)

        return i

    def gerar_generator(self, n):
        """ Gerador baseado em generator de acordo com posição(n) informada. """
        g = self._gerador()

        for i in range(n):
            next(g)

        return next(g)

    def _gerador(self):
        """ Gerador sequencial, iniciando na posição 0, usando generator. """
        i, j = 0, 1
        while True:
            yield i
            i, j = j, (i + j)

    def listar(self, inicio, fim):
        """ Listagem de sequência de fibonacci de acordo com inicio e fim informado. """
        if inicio > fim:
            inicio, fim = fim, inicio
        lista = []

        for i in range(inicio, (fim + 1)):
            lista.append(self.gerar_iterativo(i))

        return lista

    def __repr__(self):
        """ Impressão do objeto Fibonacci. """
        conj = str(self._conjunto)[1:-1]
        return "{" + conj + ", ...}"


if __name__ == "__main__":
    # Teste em interface de texto.
    f = Fibonacci()

    while True:
        print("Sequência de Fibonacci\n")
        opc = int(input("1 - Gerar posição específica\n"
                        "2 - Listar\n"
                        "3 - Gerador infinito\n"
                        "4 - Conjunto\n"
                        "0 - Sair\n"
                        "\t: "))

        if opc == 1:
            # Geração de posição informada pelo usuário.
            posicao = int(input("\nPosição: "))
            print(f.gerar_generator(posicao))
        elif opc == 2:
            # Listagem usando iteração, recursividade, generetor.
            opc2 = int(input("\n1 - Iteração"
                             "\n2 - Recursão"
                             "\n3 - Gerador(generator)"
                             "\n0 - Voltar"
                             "\n\t: "))
            if opc2 != 0:
                intervalo = input("\nIntervalo de posições(i,f): ")
                intervalo = intervalo.split(',')

                if int(intervalo[0]) > int(intervalo[1]):
                    intervalo[0], intervalo[1] = intervalo[1], intervalo[0]

            if opc2 == 1:
                for x in range(int(intervalo[0]), int(intervalo[1]) + 1):
                    print(x, ": ", f.gerar_iterativo(x), end=("" if x == int(intervalo[1]) else ", "), sep="")
            elif opc2 == 2:
                for x in range(int(intervalo[0]), int(intervalo[1]) + 1):
                    print(x, ": ", f.gerar_recursivo(x), end=("" if x == int(intervalo[1]) else ", "), sep="")
            elif opc2 == 3:
                for x in range(int(intervalo[0]), int(intervalo[1]) + 1):
                    print(x, ": ", f.gerar_generator(x), end=("" if x == int(intervalo[1]) else ", "), sep="")
            elif opc2 == 0:
                opc = 0
        elif opc == 3:
            # Gerador infinito usando generator.
            if (input("\nCTRL + C, para PARAR.\nContinuar(S/n): ")).upper() == 'S':
                cont = 0
                while True:
                    print(cont, ": ", f.gerar_generator(cont), sep="")
                    cont += 1
        elif opc == 4:
            # Impressão de conjunto exemplo.
            print(f)
        else:
            break

        # Uma variável inteira zerada(==0) é equivalente a False,
        # qualquer outro valor é True.
        if opc:
            input("\n\nEnter para continuar ")

        print("\n")
