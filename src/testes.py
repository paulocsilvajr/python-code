#!/usr/bin/python3
# coding: utf-8

try:
    # Importação para uso direto do módulo
    from funcoes_uteis import *
    from conexaoDb import *
except ImportError:
    # Importação para uso pelo pacote sources
    from src.funcoes_uteis import *
    from src.conexao_db import *

# from abc import ABCMeta, abstractmethod
#
# class TemplateAnimal(metaclass=ABCMeta):
#     @abstractmethod
#     def correr(self):
#         pass
#
#     @abstractmethod
#     def alimentar(self):
#         pass
#
#
# class Animal(TemplateAnimal):
#     def __init__(self, especie):
#         self.__especie = especie
#
#     @property
#     def especie(self):
#         return self.__especie
#
#     def correr(self):
#         return 'O %s está correndo' % self.especie
#
#     def alimentar(self):
#         return 'O %s está se alimentando' % self.especie
#
#
# class AnimalExtraterreste(Animal):
#     def __init__(self):
#         super(AnimalExtraterreste, self).__init__('Desconhecido')

if __name__ == "__main__":
    p = Pilha(1, 2, 3)
    p2 = Pilha(5, 6, 8)
    p2.incluir(8, 6)
    p3 = Pilha(8, 8, 8)
    f = Fila(2, 6, 3)
    f2 = Fila(6, 5, 8)
    p4 = Pilha(5, 6, 8)
    f2.incluir(2, 3, 6)
    f3 = Fila(*range(10))
    print('Quant. Pilhas: ', p.quantidade, '\tQuant. Filas: ', f.quantidade)
    del p2, f3, p3, p4
    print('Quant. Pilhas: ', p.quantidade, '\tQuant. Filas: ', f.quantidade)

    # componentes = vars()
    # # print(componentes)
    # for elemento in list(componentes.keys()):
    #     if isinstance(componentes[elemento], (Pilha, Fila)):
    #         print(elemento, ':', componentes[elemento])
    retornar_componentes_tipo((Pilha, Fila), escopo=globals(), imprimir=True)

    # gato = Animal('Gato')
    # print(gato.especie)
    # print(gato.correr())
    # print(gato.alimentar())
    #
    # et = AnimalExtraterreste()
    # print(et.especie)
    # print(et.correr())
    # print(et.alimentar())

    # teste do Temporizador
    # import datetime
    # def hora(repetir):
    #     for i in range(repetir):
    #         print(datetime.datetime.now())
    #         sleep(1)
    #
    # print("Início:", datetime.datetime.now())
    #
    # t = Temporizador("13:12", hora, 2)

    # Exemplo utilização função converter_string_data
    # lista_data = converter_string_data('15/12/2013 23:25:01', completo=True)
    # print(lista_data, *converter_string_data("13:12,15:23,23:58:16"), sep="\n")

    # Exemplo atributo estático.
    # p0 = Pilha()
    # p1 = Pilha(6, 5, 8)
    # p2 = Pilha('a', 'b', 'c')
    #
    # print(Pilha.quantidade, p0.quantidade, p1.quantidade, p2.quantidade)
    # print(*p1, *p2, sep=":")

    # pilha = Pilha(2, 3, 6)
    # pilha.incluir(7, 9, 10)
    # print(pilha)
    # print(pilha.limpar())
    # print(pilha, type(pilha))

    # ordenação de pilha contendo lista usando chave de posição
    # o mesmo conceito é aplicado sobre pilhas contendo dicionários(deve-se informa a chave em string)
    # p = Pilha((2, 3, 4), (5, 3, 2))
    # # p = Pilha(2, 3, 4, 5, 3, 2)
    #
    # if p.ordenar(chave=2, reverso=True):
    #     print(p)
    #
    pass
