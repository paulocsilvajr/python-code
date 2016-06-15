#!/usr/bin/python3
# coding: utf-8

try:
    # Importação para uso direto do módulo
    from funcoes_uteis import input_tipo, validar_intervalo, pausar, limpar_tela
except ImportError:
    # Importação para uso pelo pacote sources
    from sources.funcoes_uteis import input_tipo, validar_intervalo, pausar, limpar_tela

from math import log10

__author__ = "Paulo C. Silva Jr."


class Juros:
    """ Classe Base para o calculo de juros simples e compostos.
    PV: Valor presente, Capital(C)
    FV: Valor Futuro, Montante(M)
    PMT: Valor de parcelamento em x intervalo
    i: Taxa de juros
    n: Tempo/intervalo
    intervalo: Descrição do intervalo, default="mês"
    moeda: Representação da moeda local, default="R$" """

    def __init__(self, PV=None, FV=None, i=None, n=None, PMT=None, intervalo="mês", moeda="R$"):
        self.resultado = dict()
        self.resultado['PV'] = PV
        self.resultado['FV'] = FV
        self.resultado['i'] = i / 100 if isinstance(i, int) or isinstance(i, float) else i
        self.resultado['n'] = n
        self.resultado['PMT'] = PMT
        self.moeda = moeda
        self.intervalo = intervalo

    def __str__(self):
        msg = "PV:  %s %.2f\n" \
              "FV:  %s %.2f\n" \
              "PMT: %s %.2f\n" \
              "i:   %.2f%% ao %s\n" \
              "n:   %.2f %s" % (self.moeda, self.resultado['PV'],
                                self.moeda, self.resultado['FV'],
                                self.moeda, self.resultado['PMT'],
                                self.resultado['i'] * 100, self.intervalo,
                                self.resultado['n'], self.intervalo)

        if self.resultado['n'] > 1:
            if self.intervalo == "mês":
                msg = msg[:-3]  # retira "mês" do final de msg e substitui por meses
                msg += "meses"
            else:
                msg += "s"

        return msg


class Simples(Juros):
    """ Juros de cada período são sempre calculados em função
        do capital inicial(PV) aplicado. """

    def __init__(self, PV=None, FV=None, i=None, n=None, intervalo="mês", moeda="R$"):
        super().__init__(PV=PV, FV=FV, i=i, n=n, intervalo=intervalo, moeda=moeda)
        self.resultado['PMT'] = 0.0  # zerando PMT, pois não é usado nesse calculo.
        self._calcular()

    def _calcular(self):
        """ Calculo de juros simples.
        :return: None, atribui os valores ao dicionário resultado. """

        PV = self.resultado['PV']
        FV = self.resultado['FV']
        i = self.resultado['i']
        n = self.resultado['n']

        if PV is None:
            self.resultado['PV'] = FV / (1 + i * n)
        elif FV is None:
            self.resultado['FV'] = PV * (1 + i * n)
        elif i is None:
            self.resultado['i'] = (FV / PV - 1) * (1 / n)
        elif n is None:
            self.resultado['n'] = (FV - PV) / (PV * i)


class Compostos(Juros):
    """ Juros de cada período são somados ao capital,
    visando cálculos de novos juros nos períodos seguintes. """

    def __init__(self, PV=None, FV=None, i=None, n=None, PMT=None, intervalo="mês", moeda="R$"):
        super().__init__(PV=PV, FV=FV, i=i, n=n, PMT=PMT, intervalo=intervalo, moeda=moeda)
        self._calcular()

    def _calcular(self):
        """ Calculo de juros compostos.
        :return: None, atribui os valores ao dicionário resultado. """

        PV = self.resultado['PV']
        FV = self.resultado['FV']
        i = self.resultado['i']
        n = self.resultado['n']
        # PMT = self.resultado['PMT']

        if PV is None:
            self.resultado['PV'] = FV / ((1 + i) ** n)
            self.resultado['PMT'] = FV / n
        elif FV is None:
            self.resultado['FV'] = PV * ((1 + i) ** n)
            self.resultado['PMT'] = PV * (i / (1 - (1 + i) ** -n))
        elif i is None:
            self.resultado['i'] = ((FV / PV) ** (1 / n)) - 1
            self.resultado['PMT'] = FV / n
        elif n is None:
            self.resultado['n'] = (log10(FV / PV) / log10(1 + i))
            self.resultado['PMT'] = FV / self.resultado['n']


if __name__ == "__main__":
    # Teste em interface de texto.

    def capturaDados(tipo):
        valores = []
        print("Informe os valores para o calculo:\n"
              "Para o valor que deseja encontrar informar x")
        if tipo == 'compostos':
            print("Para calcular o PMT informar x para FV e PMT")
        valores.append(input("PV(Capital $):       "))
        valores.append(input("FV(Montante $):      "))
        valores.append(input("i(% taxa):           "))
        valores.append(input("n(tempo):            "))
        if tipo == 'compostos':
            valores.append(input("PMT(Parcelamento $): "))
        valores.append(input("intervalo(mês):      "))
        valores.append(input("Moeda(R$):           "))

        for i, valor in enumerate(valores):
            if i >= (len(valores) - 2):
                valores[i] = valor
            elif valor == 'x':
                valores[i] = None
            else:
                valores[i] = float(valor)

        if tipo == 'simples':
            j = Simples(*valores)
        else:
            j = Compostos(*valores)

        print(j.resultado, j, sep='\n')


    while True:
        limpar_tela()

        print("Calculo de juros:\n")
        opc = validar_intervalo(input_tipo("1 - SIMPLES\n"
                                           "2 - COMPOSTOS\n"
                                           "0 - Sair\n"
                                           "\t: "), 0, 2)

        if opc == 1:
            # Juros SIMPLES
            capturaDados('simples')
        elif opc == 2:
            # Juros Compostos
            capturaDados('compostos')
        else:
            break

        if opc != 0:
            pausar()

        print("\n")
