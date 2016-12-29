#!/usr/bin/python3
# -*- coding: utf-8 -*-

try:
    # Importação para uso direto do módulo
    from funcoes_uteis import input_tipo, validar_intervalo, pausar, limpar_tela
except ImportError:
    # Importação para uso pelo pacote sources
    from sources.funcoes_uteis import input_tipo, validar_intervalo, pausar, limpar_tela

__author__ = "Paulo C. Silva Jr."


class Fibonacci:
    """ Classe que implementa a sequência de Fibonacci. """
    def __init__(self, p=None):
        """ Construtor alimentando o atributo conjunto com sequência. """
        self._conjunto = self.listar(1, 10)[1]
        self._posicao = p

    def gerar_recursivo(self, n):
        """ Gerador baseado em recursão de acordo com posição(n) informada. [1] """
        if n < 2:
            return n
        else:
            return self.gerar_recursivo(n - 1) + self.gerar_recursivo(n - 2)

    def gerar_iterativo(self, n):
        """ Gerador baseado em iteração de acordo com posição(n) informada. [1] """
        i, j = 0, 1
        for x in range(n):
            i, j = j, (i + j)

        return i

    def gerar_generator(self, n):
        """ Gerador baseado em generator de acordo com posição(n) informada. [1] """
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

    def listar(self, inicio, fim, metodo=None):
        """ Listagem de sequência de fibonacci de acordo com inicio e fim informado.
        metodo: 1 - recursivo; 2 - iterativo; None - generator. """
        if inicio > fim:
            inicio, fim = fim, inicio
        lista = []
        listagem = ""

        for i in range(inicio, (fim + 1)):
            if metodo == 1:
                temp = self.gerar_recursivo(i)
            elif metodo == 2:
                temp = self.gerar_iterativo(i)
                # lista.append(self.gerar_iterativo(i))
            else:
                temp = self.gerar_generator(i)

            lista.append(temp)
            # lista.append(self.gerar_iterativo(i))
            listagem += str(temp) + ("" if i == fim else ", ")

        return lista, listagem

    def __repr__(self):
        """ Impressão do objeto Fibonacci. """
        if self._posicao is None:
            return "{" + self._conjunto + ", ...}"
        else:
            return str(self.gerar_generator(self._posicao))


if __name__ == "__main__":
    # Teste em interface de texto.
    f = Fibonacci()

    while True:
        limpar_tela()

        print("Sequência de Fibonacci\n")
        opc = validar_intervalo(input_tipo("1 - Gerar posição específica\n"
                        "2 - Listar\n"
                        "3 - Gerador infinito\n"
                        "4 - Conjunto\n"
                        "0 - Sair\n"
                        "\t: "), 0, 4)

        if opc == 1:
            # Geração de posição informada pelo usuário.
            posicao = input_tipo("\nPosição: ")
            # Abaixo exemplo usando método específico e método construtor.
            # print(f.gerar_generator(posicao))
            fibo = Fibonacci(posicao)
            print(fibo)
        elif opc == 2:
            # Listagem usando iteração, recursividade, generetor.
            opc2 = validar_intervalo(input_tipo("\n1 - Iteração"
                             "\n2 - Recursão"
                             "\n3 - Gerador(generator)"
                             "\n0 - Voltar"
                             "\n\t: "), 0, 3)
            if opc2:
                intervalo = input("\nIntervalo de posições(i,f): ")
                intervalo = intervalo.split(',')
                intervalo[0], intervalo[1] = int(intervalo[0]), int(intervalo[1])

                if intervalo[0] > intervalo[1]:
                    intervalo[0], intervalo[1] = intervalo[1], intervalo[0]
            if opc2 == 1:
                print(f.listar(intervalo[0], intervalo[1], 2)[0])
            elif opc2 == 2:
                print(f.listar(intervalo[0], intervalo[1], 1)[0])
            elif opc2 == 3:
                print(f.listar(intervalo[0], intervalo[1])[0])
            elif opc2 == 0:
                opc = 0
        elif opc == 3:
            # Gerador infinito usando generator.
            if input_tipo("\nCTRL + C, para PARAR.\nContinuar(S/n): ", tipo='bool'):
                cont = 0
                while True:
                    print(cont, ": ", f.gerar_generator(cont), sep="")
                    cont += 1
        elif opc == 4:
            # Impressão de conjunto exemplo.
            print("\n", f, sep="")
        else:
            break

        # Uma variável inteira zerada(==0) é equivalente a False,
        # qualquer outro valor é True.
        if opc:
            pausar()

        print("\n")

# Referência
# [1] http://victorpoluceno.blogspot.com.br/2008/08/implementaes-da-sequncia-de-fibonacci.html
