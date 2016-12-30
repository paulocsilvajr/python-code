#!/usr/bin/python3
# coding: utf-8

import random


def insert_sort(original):
    tamanho = len(original)
    for i in range(1, tamanho):
        valor_corrente = original[i]
        posicao = i

        while posicao > 0 and original[posicao-1] > valor_corrente:
            original[posicao] = original[posicao-1]
            posicao -= 1

        original[posicao] = valor_corrente


def selection_sort(original):
    tamanho = len(original)
    for i in range(0, tamanho):
        posicao_menor = i
        for j in range(i, tamanho):
            if original[j] < original[posicao_menor]:
                posicao_menor = j
        original[posicao_menor], original[i] = original[i], original[posicao_menor]


def bubble_sort(original):
    tamanho = len(original) - 1
    for i in range(tamanho, 0, -1):
        for j in range(0, i):
            if original[j] > original[j+1]:
                # print(i, j, original)
                original[j], original[j+1] = original[j+1], original[j]
                # print(i, j, original)


def comb_sort(original):
    gap = len(original)
    swaps = True

    while gap > 1 or swaps:
        gap = max(1, int(gap / 1.247330950103979))
        swaps = False

        for i in range(len(original) - gap):
            j = i+gap

            if original[i] > original[j]:
                original[i], original[j] = original[j], original[i]
                swaps = True


if __name__ == "__main__":
    listagem = list(range(1000000))
    random.shuffle(listagem)
    print("Original:", listagem)

    # Métodos simples
    # selection_sort(listagem)
    # insert_sort(listagem)
    # bubble_sort(listagem)
    # comb_sort(listagem)

    # print("Ordenado:", listagem)

    # print("Ordenado:", sorted(listagem), "<built-in>")

    # teste de desempenho efetuado no ipython3 usando função %timeit:
    # lista base é formada por range(100) embaralhado com a função random.shuffle()
    # µs = microsegundo = um milionésimo de segundo
    # src.ordenacao.insert_sort(): '100000 loops, best of 3: 18.1 µs per loop',
    # src.ordenacao.bubble_sort(): '1000 loops, best of 3: 490 µs per loop',
    # src.ordenacao.comb_sort(): '10000 loops, best of 3: 137 µs per loop,
    # src.ordenacao.selection_sort(): '1000 loops, best of 3: 437 µs per loop',
    # __builtins__.sorted(): '100000 loops, best of 3: 11.4 µs per loop'

