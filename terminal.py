#!/usr/bin/python3
# coding: utf-8
from time import sleep
from threading import Thread
from src.funcoes_uteis import limpar_tela

__author__ = "Paulo C. Silva Jr"


class Timer(Thread):
    def __init__(self):
        self.relogio = 0, 0.0
        self.min = 108  # 108 default
        self.entrada = ""
        self._rodando = True
        self.numeros = ''
        Thread.__init__(self)

    # Override
    def run(self):
        for i in range((self.min * 60), -1, -1):
            if not self._rodando:
                if not self.entrada:
                    print("Reiniciando relógio...")
                    sleep(1.5)
                break

            # if i < 60:
            #     print(i)

            print('\r:: {} ::  {}'.format(self.relogio[1], self.numeros), flush=True, end="")
            sleep(1)
            self.relogio = i, round(i / 60, 1)


            if self.relogio[1] == 0.0:
                while True:
                    print("Fim do mundo")

    def finalizar(self, entr):
        self.entrada = entr
        self._rodando = False


entrada = ""

while True:
    if not entrada:
        tempo = Timer()
        tempo.start()

        for i in range(6):
            limpar_tela()
            entrada += input("{}".format(entrada)) + (" " if i < 5 else "")
            tempo.numeros = entrada
        # print(entrada)

        if entrada == "4 8 15 16 23 42":
            print(":: ", tempo.relogio[1], " ::")
            entrada = ""

        tempo.finalizar(entrada)
        tempo.join()
        del tempo
    else:
        print("Fim do mundo")
