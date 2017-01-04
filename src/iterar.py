#!/usr/bin/python3
# -*- coding: utf-8 -*-

from time import sleep
from random import randint
from argparse import ArgumentParser

""" Exemplo de retorno de carro e passagem de argumentos. """

parser = ArgumentParser(description='Exemplo de retorno de carro e passagem de argumentos')
parser.add_argument('-s',
                    action='store',
                    type=float,
                    dest='segundos',
                    default=0.0,
                    help='Intervalo de impressão em segundos, padrão: 0.0 segundos')
parser.add_argument('-n',
                    action='store',
                    type=int,
                    dest='numero',
                    default=100,
                    help='Quantidade de iterações, padrão: 100 iterações')

args = parser.parse_args()

# os parametros são capturados por atributos do objeto args, segundo informado no parâmetro dest de
# parser.add_argument()
Q = args.numero

# system('clear')
for i in range(1, Q + 1):
    sleep(args.segundos)
    # retorno de carro para imprimir no mesmo local a contagem de números, semelhante a uma barras de progresso.
    # deve ter o carriage return no início da impressão(\r) e o parâmetro flush=True.
    # a formatação irá imprimir os números com zeros a esquerda de acordo com a quantidade de caracteres de Q.
    print('\r{:0>{}}'.format(i, len(str(Q))), end="", flush=True)

    if i == randint(1, Q):
        # sorteio aleatório
        print(' -> Número sorteado')
else:
    print('\nEND OF LINE.')
