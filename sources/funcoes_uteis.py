#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import sys
import os

__author__ = "Paulo C. Silva Junior"

""" Módulo com funções e classes úteis para qualquer programa.
   Desenvolvido em Python 3.x """


class Pilha:
    """ FILO - First In Last Out. """
    def __init__(self, *itens):
        self._elementos = []
        if itens:
            self._adicionar_elementos(itens)

    def _adicionar_elementos(self, elementos):
        for x in elementos:
            self._elementos.append(x)

    def incluir(self, *n):
        if isinstance(n, tuple):
            self._adicionar_elementos(n)
        else:
            self._elementos.append(n)

    def remover(self, metodo=None):
        if self._elementos:
            if metodo == 'FIFO':
                return self._elementos.pop(0)
            return self._elementos.pop()
        return False

    def ordenar(self):
        if self._elementos:
            try:
                self._elementos.sort()
                return True
            except TypeError:
                pass
        return False

    def exibir(self):
        return self._elementos

    def __repr__(self):
        return str(self._elementos)


class Fila(Pilha):
    """ FIFO - First In First Out. """
    def remover(self):
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
        try:
            if tipo == 'int':
                n = int(input('%s' % texto))
            elif tipo == 'float':
                n = float(input('%s' % texto))
            else:
                n = input('%s' % texto)
            break
        except:
            if mensagem:
                print(mensagem)
    return n


def validar_intervalo(valor, inicio, fim, mensagem = '\tValor incorreto'):
    """ Retorna um valor inteiro validado dentro do intervalo informado. """
    while True:
        try:
            if valor < inicio or valor > fim:
                print('%s\n' % mensagem)
                valor = input_tipo('\tInforme um novo valor: ', tipo='int')
            else:
                break
        except:
            pass
    return valor


def lista_randomica(inicio, fim):
    """ Gera uma lista randomica de acordo com intervalo(inicio-fim). """
    if inicio > fim:
        inicio, fim = fim, inicio

    lista = [x for x in range(inicio, fim + 1)]# list(range(inicio, fim + 1))

    random.shuffle(lista)

    return lista

def limparTela():
    '''Limpa tela de acordo com o sistema operacional.'''
    sistLinux = ('linux',)
    sistWindowns = ('win32',)

    if sys.platform in sistLinux:
        os.system('clear')
    elif sys.platform in sistWindowns:
        os.system('cls')


if __name__ == '__main__':
    pass
