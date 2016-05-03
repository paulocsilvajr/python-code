#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
from sys import platform
from os import system


__author__ = "Paulo C. Silva Junior"

""" Módulo com funções e classes úteis para qualquer programa.
   Desenvolvido em Python 3.x """


class Pilha:
    """ FILO - First In Last Out. """
    def __init__(self, *itens):
        """ Construtor da classe.
        Possibilita a inclusão de itens na criação do objeto. """
        self._elementos = []
        if itens:
            self._adicionar_elementos(itens)

    def _adicionar_elementos(self, elementos):
        for x in elementos:
            self._elementos.append(x)

    def incluir(self, *n):
        """ Método para inclusão de itens.
        Pode-se fazer inclusão de vários itens simultaneamente. """
        if isinstance(n, tuple):
            self._adicionar_elementos(n)
        else:
            self._elementos.append(n)

    def remover(self, metodo=None):
        """ Método para exclusão de item.
        Remoção do último item incluido.
        Retorna o item removido ou False caso vazia. """
        if self._elementos:
            if metodo == 'FIFO':
                return self._elementos.pop(0)
            return self._elementos.pop()
        return False

    def ordenar(self):
        """ Ordenação de itens homogêneos.
        Retorna False caso for heterogênea ou vazia. """
        if self._elementos:
            try:
                self._elementos.sort()
                return True
            except TypeError:
                pass
        return False

    def exibir(self):
        """ Retorna os item em uma list. """
        return self._elementos

    def __repr__(self):
        """ Impressão do objeto em str. """
        return str(self._elementos)


class Fila(Pilha):
    """ FIFO - First In First Out. """
    def remover(self):
        """ Método para exclusão de itens.
        Remoção do primeiro item incluido.
        Retorna o item removido ou False caso vazia. """
        return super().remover('FIFO')


def pausar(mensagem='\nENTER para continuar '):
    while True:
        entrada = input(mensagem)
        
        if not entrada:
            break


def input_tipo(texto='\t: ', mensagem='\tValor incorreto', tipo=None):
    """ Captura entrada do teclado com validação para números inteiros.
    Uso principalmente em menus. """
    n = 0
    while True:
        n = input('%s' % texto)
        try:
            if tipo == 'int':
                n = int(n)
            elif tipo == 'float':
                n = float(n)
            break
        except ValueError:
            if mensagem:
                print(mensagem)
    return n


def validar_intervalo(valor, inicio, fim, mensagem='\tValor incorreto', tipo='int'):
    """ Retorna um valor validado dentro do intervalo heterogêneo informado.
    Caso informado intervalo inválido, recaptura-se o valor.
    Uso em menus. """
    if inicio > fim:
        inicio, fim = fim, inicio

    while True:
        if inicio <= valor <= fim:
            break
        else:
            print('%s\n' % mensagem)
            valor = input_tipo('Informe um novo valor: ', tipo=tipo)
    return valor


def lista_randomica(inicio, fim):
    """ Gera uma lista randomica de acordo com intervalo(inicio-fim). """
    if inicio > fim:
        inicio, fim = fim, inicio

    lista = [x for x in range(inicio, fim + 1)]  # list(range(inicio, fim + 1))

    random.shuffle(lista)

    return lista


def limpar_tela():
    """ Limpa tela de acordo com o sistema operacional. """
    sist_linux = ('linux',)
    sist_windowns = ('win32',)

    if platform in sist_linux:
        system('clear')
    elif platform in sist_windowns:
        system('cls')


if __name__ == '__main__':
    limpar_tela()

    p = Pilha(2, 5, 8)
    p.incluir(3, 8)
    print("Pilha:", p)
    print("Removido 2 itens", p.remover(), p.remover(), p, sep='\n')

    f = Fila(1, 1, 2)
    f.incluir(3)
    print("\nFila:", f)
    print("Removido 1 item", f.remover(), f, sep='\n')

    numero = validar_intervalo(input_tipo(texto='\n\nInforme um número: ', tipo='int'),
                               input_tipo(texto='Inicial: ', tipo='int'),
                               input_tipo(texto='final: ', tipo='int'))
    print('Número validado no intervalo:', numero)

    print("\n\nLista aleatória")
    print(">>>", lista_randomica(input_tipo("Inicial: ", tipo='int'),
                                 input_tipo("Final: ", tipo='int')))
