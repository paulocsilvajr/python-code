#!/usr/bin/python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
from funcoes_uteis import input_tipo, validar_intervalo, pausar, limpar_tela

__author__ = "Paulo C. Silva Jr."


class NumerosRomanos:
    def __init__(self, numero=None):
        """ Construtor da classe.
            :param numero é opcional, quando informado armazena no atributo romano
            o número informado convertido. Caso seja criado uma instância sem
            parametro, deve-se usar o método converter_romano(Numero),
            que retorna um string representando um algarismo romano.
            Na configuração original, o programa aceita converter
            números de 1 à 3999, podendo-se extender sua funcionalidade
            atribuindo chaves e valores ao dicionário. """
        self._dic = OrderedDict()
        self._dic[1] = 'I'
        self._dic[5] = 'V'
        self._dic[10] = 'X'
        self._dic[50] = 'L'
        self._dic[100] = 'C'
        self._dic[500] = 'D'
        self._dic[1000] = 'M'

        self.romano = ''

        if isinstance(numero, int):
            self.romano = self.converter_romano(numero)

    def converter_romano(self, n):
        """Método para conversão de número arábico em romano. """
        if n in self._dic.keys():
            return self._dic[n]
        else:
            temp = ''
            for i in self.separador_casas_decimais(n):
                if i in self._dic.keys():
                    temp += self._dic[i]
                else:
                    # função depreciada
                    # temp += self._identificador(i)
                    temp += self._identificador2(i)
            return temp

    # função depreciada, substituida por _identificador2
    def _identificador(self, n):
        """ Depreciada.
            Método original para identificar símbolo romano a partir de equivalente arábico(np). """
        if 2 <= n <= 3:
            return n * self._dic[1]
        elif n == 4:
            return self._dic[1] + self._dic[5]
        elif 6 <= n <= 8:
            return self._dic[5] + ((n - 5) * self._dic[1])
        elif n == 9:
            return self._dic[1] + self._dic[10]
        elif 20 <= n <= 30:
            return (n // 10) * self._dic[10]
        elif n == 40:
            return self._dic[10] + self._dic[50]
        elif 60 <= n <= 80:
            return self._dic[50] + (((n - 50) // 10) * self._dic[10])
        elif n == 90:
            return self._dic[10] + self._dic[100]
        elif 200 <= n <= 300:
            return (n // 100) * self._dic[100]
        elif n == 400:
            return self._dic[100] + self._dic[500]
        elif 600 <= n <= 800:
            return self._dic[500] + (((n - 500) // 100) * self._dic[100])
        elif n == 900:
            return self._dic[100] + self._dic[1000]
        else:
            return 'Não cadastrado'

    def _identificador2(self, n):
        """ Método otimizado e generalizado para identificar simbolo romano a partir de equivalente arábico(np). """
        try:
            if '2' in str(n) or '3' in str(n):
                return (n // self._item_anterior_posterior(n)[0]) * self._dic[self._item_anterior_posterior(n)[0]]
            elif '4' in str(n):
                return self._dic[self._item_anterior_posterior(n)[0]] + \
                       self._dic[self._item_anterior_posterior(n)[1]]
            elif '6' in str(n) or '7' in str(n) or '8' in str(n):
                # O calculo de temp resulta no número inicial de uma parte específica do dicionário de simbolos romanos
                # Ex: np == 600, temp == 100, o primeiro item do intervalo entre 100 e 1000, do qual 600 pertence.
                # As próximas 4 linhas atribuindo valor em temp estão em forma didática,
                # no elif '9' está na forma resumida. """
                temp = self._item_anterior_posterior(n)[0]
                temp = str(temp)[0]
                temp = int(temp)
                temp = self._item_anterior_posterior(n)[0] // temp
                return self._dic[self._item_anterior_posterior(n)[0]] + \
                       (((n - self._item_anterior_posterior(n)[0]) // temp) * self._dic[temp])
            elif '9' in str(n):
                temp = self._item_anterior_posterior(n)[0] // (int(str(self._item_anterior_posterior(n)[0])[0]))
                return self._dic[temp] + self._dic[self._item_anterior_posterior(n)[1]]
        except KeyError:
            return 'Não cadastrado'

    def exibir_dicionario(self):
        """ Retorna o dicionário de símbolos romanos com seus respectivos equivalentes arábicos. """
        return self._dic

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

    def _item_anterior_posterior(self, n):
        """ Retorna os itens anterior e posterior ao informado(np) em uma lista de 2 posições,
            baseados no dicionário de simbolos romanos.
            _item_anterior_porterior(np)[0] == anterior
            _item_anterior_porterior(np)[0] == posterior. """
        lista = [x for x in self._dic.keys()]
        anterior, posterior = 0, 0
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
    # Teste em interface de texto.

    while True:
        limpar_tela()
        print("Conversor de numero arábico para Romano")
        opc = validar_intervalo(input_tipo("1 - Converter\n"
                        "2 - Listagem\n"
                        "0 - Sair\n"
                        "\t: "), 0, 2)

        if opc == 1:
            # conversão de inteiro para número romano
            n = input_tipo("\nDigite um número: ")

            r = NumerosRomanos(n)
            print("{}: {}".format(n, r.romano))
            # A forma acima demonstra a criação de um novo objeto
            # passando um número como parametro.
            # Abaixo está expressado a forma de uso sem a passagem de parametro.
            # r = NumerosRomanos()
            # print(r.converter_romano(np))
        elif opc == 2:
            # lista de números romanos; i, f == inicial, final
            i = input_tipo("\nNúmero inicial: ")
            f = input_tipo("Número Final: ")

            if i > f:
                i, f = f, i

            r = NumerosRomanos()
            if (i + f) > 0:
                for r in r.listar(i, f):
                    print("{}: {}; ".format(i, r), sep="", end="")
                    i += 1
        elif opc == 0:
            break

        if opc != 0:
            pausar()

        print("\n")
