#!/usr/bin/python3
# coding: utf-8
from time import sleep
from threading import Thread
from os import system, name
from sources.funcoes_uteis import limpar_tela

__author__ = "Paulo C. Silva Jr"


class Timer(Thread):
    def __init__(self):
        self.relogio = 0, 0.0
        self.min = 108  # 108 default
        self.entrada = ""
        self._rodando = True
        Thread.__init__(self)

    # Override
    def run(self):
        for i in range((self.min * 60), -1, -1):
            if not self._rodando:
                if not entrada:
                    print("Reiniciando relógio...")
                    sleep(1.5)
                break

            if i < 60:
                print(i)
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
            # system('clear') if name in ('posix',) else system('cls') if name in ('nt', 'ce') else None
            limpar_tela()
            entrada += input("%s" % entrada) + (" " if i < 5 else "")
        # print(entrada)

        if entrada == "4 8 15 16 23 42":
            print(":: ", tempo.relogio[1], " ::")
            entrada = ""

        tempo.finalizar(entrada)
        tempo.join()
        del tempo
    else:
        print("Fim do mundo")
