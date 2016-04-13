#!/usr/bin/python3
# -*- coding: utf-8 -*-
from collections import OrderedDict


class NumerosRomanos:
    def __init__(self, numero=None):
        """ Construtor da classe.
            :param numero é opcional, quando informado armazena no atributo romano
            o número informado convertido.
            Na configuração original, o programa aceita converter
            números de 1 à 3999, podendo-se extender sua funcionalidade
            atribuindo valores no dicionário. """
        self.__dic = OrderedDict()
        self.__dic[1] = 'I'
        self.__dic[5] = 'V'
        self.__dic[10] = 'X'
        self.__dic[50] = 'L'
        self.__dic[100] = 'C'
        self.__dic[500] = 'D'
        self.__dic[1000] = 'M'
        self.romano = ''

        if isinstance(numero, int):
            self.romano = self.converter_romano(numero)

    def converter_romano(self, n) -> object:
        """Método para conversão de número arábico em romano. """
        if n in self.__dic.keys():
            return self.__dic[n]
        else:
            temp = ''
            for i in self.separador_casas_decimais(n):
                if i in self.__dic.keys():
                    temp += self.__dic[i]
                else:
                    # função depreciada
                    # temp += self.__identificador(i)
                    temp += self.__identificador2(i)
            return temp

    # função depreciada, substituida por __identificador2
    def __identificador(self, n):
        """ Depreciada.
            Método original para identificar símbolo romano a partir de equivalente arábico(n). """
        if 2 <= n <= 3:
            return n * self.__dic[1]
        elif n == 4:
            return self.__dic[1] + self.__dic[5]
        elif 6 <= n <= 8:
            return self.__dic[5] + ((n - 5) * self.__dic[1])
        elif n == 9:
            return self.__dic[1] + self.__dic[10]
        elif 20 <= n <= 30:
            return (n // 10) * self.__dic[10]
        elif n == 40:
            return self.__dic[10] + self.__dic[50]
        elif 60 <= n <= 80:
            return self.__dic[50] + (((n - 50) // 10) * self.__dic[10])
        elif n == 90:
            return self.__dic[10] + self.__dic[100]
        elif 200 <= n <= 300:
            return (n // 100) * self.__dic[100]
        elif n == 400:
            return self.__dic[100] + self.__dic[500]
        elif 600 <= n <= 800:
            return self.__dic[500] + (((n - 500) // 100) * self.__dic[100])
        elif n == 900:
            return self.__dic[100] + self.__dic[1000]
        else:
            return 'Não cadastrado'

    def __identificador2(self, n):
        """ Método otimizado e generalizado para identificar simbolo romano a partir de equivalente arábico(n). """
        try:
            if '2' in str(n) or '3' in str(n):
                return (n // self.__item_anterior_posterior(n)[0]) * self.__dic[self.__item_anterior_posterior(n)[0]]
            elif '4' in str(n):
                return self.__dic[self.__item_anterior_posterior(n)[0]] +\
                       self.__dic[self.__item_anterior_posterior(n)[1]]
            elif '6' in str(n) or '7' in str(n) or '8' in str(n):
                """ O calculo de temp resulta no número inicial de uma parte específica do dicionário de simbolos romanos
                    Ex: n == 600, temp == 100, o primeiro item do intervalo entre 100 e 1000, do qual 600 pertence.
                    As próximas 4 linhas atribuindo valor em temp estão em forma didática, no elif '9' está na forma resumida. """
                temp = self.__item_anterior_posterior(n)[0]
                temp = str(temp)[0]
                temp = int(temp)
                temp = self.__item_anterior_posterior(n)[0] // temp
                return self.__dic[self.__item_anterior_posterior(n)[0]] +\
                    (((n - self.__item_anterior_posterior(n)[0]) // temp) * self.__dic[temp])
            elif '9' in str(n):
                temp = self.__item_anterior_posterior(n)[0] // (int(str(self.__item_anterior_posterior(n)[0])[0]))
                return self.__dic[temp] + self.__dic[self.__item_anterior_posterior(n)[1]]
        except KeyError:
            return 'Não cadastrado'

    def exibir_dicionario(self):
        """ Retorna o dicionário de símbolos romanos com seus respectivos equivalentes arábicos. """
        return self.__dic

    def separador_casas_decimais(self, n):
        """ Converte um número em uma lista contendo as casas decimais(...centena, dezena, unidade),
            separadas em cada item da mesma. """
        numero_str = str(n)

        lista = []
        for casa, numero in enumerate(numero_str, start=1):
            numero = int(numero)
            if numero != 0:
                lista.append(numero * (10 ** (len(numero_str) - casa)))

        return lista

    def __item_anterior_posterior(self, n):
        """ Retorna os itens anterior e posterior ao informado(n) em uma lista de 2 posições,
            baseados no dicionário de simbolos romanos.
            __item_anterior_porterior(n)[0] == anterior
            __item_anterior_porterior(n)[0] == posterior. """
        lista = [x for x in self.__dic.keys()]
        for i, item in enumerate(lista):
            if n > item:
                anterior = item
                try:
                    posterior = lista[i + 1]
                except IndexError:
                    posterior = 0

        return [anterior, posterior]

    def listar(self, inicial, final):
        """ Retorna uma lista de números romanos de acordo com intervalo informado. """
        l = []
        for i in range(inicial, final + 1):
            l.append(self.converter_romano(i))

        return l


if __name__ == '__main__':
    while(True):
        print("Conversor de numero arábico para Romano")
        opc = int(input("1 - Converter\n"
                        "2 - Listagem\n"
                        "0 - Sair\n"
                        "\t: "))

        if opc == 1:
            # conversão de inteiro para número romano
            n = int(input("Digite um número: "))

            r = NumerosRomanos(n)
            print("{}: {}".format(n, r.romano))
            # r = NumerosRomanos()
            # print(r.converter_romano(n))
        elif opc == 2:
            # lista de números romanos; i, f == inicial, final
            i = int(input("Número inicial: "))
            f = int(input("Número Final: "))

            if i > f:
                i, f = f, i

            r = NumerosRomanos()
            if (i + f) > 0:
                for r in r.listar(i, f):
                    print(i, ": ", r, "; ", sep="", end="")
                    i += 1
        elif opc == 0:
            break

        input("\n\nEnter para continuar ")

        print("\n")
