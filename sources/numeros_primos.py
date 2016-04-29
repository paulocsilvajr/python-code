#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = "Paulo C. Silva Jr."


class NumeroPrimo:
    """ Classe para verificação e geração de números primos. """
    def __init__(self):
        self._conjunto = self.listar(1, 100)

    @staticmethod
    def eh_numero_primo(n):
        """ Verifica se o parametro informado é um número primo. """
        assert isinstance(n, int), "Param. n não é inteiro."
        assert n > 0, "Param. n <= 0"

        primo = True
        # Verificação de número primo.
        # Regra: Um número é primo somente se ele for divisível por ele mesmo e por 1.
        if n > 2:
            for x in range(2, n - 1):
                if n % x == 0:
                    primo = False
                    break

        return primo

    def listar(self, inicial, final):
        """ Retorna uma lista de números primos dentro do intervalo informado(inicial, final). """
        # Verificação para os parametros de entrada, gera excessão caso não atendidas.
        assert isinstance(inicial, int), "Param. inicial não é inteiro"
        assert isinstance(inicial, int), "Param. final não é inteiro"
        assert inicial > 0, "Param. inicial <= 0"
        # Troca, caso inicial seja maior que final.
        if final < inicial:
            inicial, final = final, inicial

        lista = []
        for x in range(inicial, final + 1):
            if self.eh_numero_primo(x):
                lista.append(x)

        return lista

    def gerador(self):
        """ Retorna um generator de números primos. """
        cont = 0
        while True:
            cont += 1
            if self.eh_numero_primo(cont):
                yield cont

    def __repr__(self):
        conj = str(self._conjunto)[1:-1]
        return "{" + conj + ",...}"


if __name__ == "__main__":
    # Teste em interface de texto.
    np = NumeroPrimo()

    while True:
        print("Números primos\n")
        opc = int(input("1 - Verificar\n"
                        "2 - Listar\n"
                        "3 - Gerador infinito\n"
                        "4 - Conjunto\n"
                        "0 - Sair\n"
                        "\t: "))

        if opc == 1:
            # Verificação de número primo, usando if como operador ternário.
            n = int(input("\nDigite um número: "))
            print(n, "é PRIMO\n" if np.eh_numero_primo(n) else "NÃO é primo\n")
        elif opc == 2:
            # Listagem de números primos, de acordo com input do usuário.
            t = input("\nDigite 2 números(x,y): ")

            t = [int(x) for x in (t.split(","))]
            if t[0] > t[1]:
                t[0], t[1] = t[1], t[0]

            print(np.listar(t[0], t[1]), end="\n")
        elif opc == 3:
            if (input("\nCTRL + C, para PARAR.\nContinuar(S/n): ")).upper() == 'S':
                g = np.gerador()
                cont = 1
                # Exemplo de aplicação do generator de números primos.
                while True:
                    v = next(g)
                    print("{}:{}".format(cont, v))
                    cont += 1
        elif opc == 4:
            print(np)
        else:
            break

        if opc != 0:
            input("\n\nEnter para continuar ")

        print("\n")
