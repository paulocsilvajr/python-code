#!/usr/bin/python3
# -*- coding: utf-8 -*-

from random import shuffle
from os import system, name
from time import sleep

__author__ = "Paulo C. Silva Jr"

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

    def ordenar(self, reverso=False):
        """ Ordenação de itens homogêneos.
        Parametro reverso para ordenar lista decrescentemente.
        Default False(crescente).
        Retorna False caso for heterogênea ou vazia. """
        if self._elementos:
            try:
                if reverso:
                    self._elementos.sort(reverse=True)
                else:
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
    # Override
    def remover(self, metodo=None):
        """ Método para exclusão de itens.
        Remoção do primeiro item incluido.
        Retorna o item removido ou False caso vazia. """
        return super().remover('FIFO')


class Tabela:
    """ Classe para impressão de tabela em modo texto.
    Métodos:
        Construtor:
            Tabela(dados_tabela, titulos_colunas, largura, titulo_tabela)
            Parametros
                Obrigatórios: dados_tabela
                Opcionais: titulo_colunas, largura, titulo """

    def __init__(self, dados_tabela, titulos_colunas=None, largura=0, titulo_tabela=""):
        assert isinstance(dados_tabela, list) or isinstance(dados_tabela, tuple), "Formato do parâmetro dados_tabela inválido"
        # Descobrindo a maior largura para cada coluna do parametro dados_tabela, se não for modificado o valor default.
        if largura == 0:
            largura = len(dados_tabela[0]) * [0]
            for linha in dados_tabela:
                for i, celula in enumerate(linha):
                    n = len(celula) + 2 if isinstance(celula, str) \
                        else len(str(celula)) + 2
                    if largura[i] < n:
                        largura[i] = n
        # Caso o usuário informar um valor de largura, este será usado para todas as colunas da tabela
        else:
            largura = len(dados_tabela[0]) * [largura + 2]

        self.__titulo = ""
        if titulo_tabela:
            self.__titulo += "| "
            self.__titulo += str(titulo_tabela).center(sum(largura))[:sum(largura)] + " |"

        self.__linha = "+"
        for e in largura:
            self.__linha += (e * "-") + "+"

        # Se o usuário não informar o cabelhado para as colunas será usado a nomenclatura coluna 1, coluna 2...
        if titulos_colunas is None:
            self.__cabecalho = "| "
            for i, e in enumerate(largura):
                self.__cabecalho += (("Coluna " + str(i + 1)).center(largura[i] - 2)[:largura[i] - 2]) + " | "
        else:
            self.__cabecalho = "| "
            for i, e in enumerate(largura):
                self.__cabecalho += (str(titulos_colunas[i]).center(largura[i] - 2)[:largura[i] - 2]) + " | "

        self.__corpo = ""
        for linha in dados_tabela:
            self.__corpo += "| "
            for i, celula in enumerate(linha):
                self.__corpo += str(celula).center(largura[i] - 2)[:largura[i] - 2] + " | "
            self.__corpo += "\n"

    def __repr__(self):
        if self.__titulo:
            return "%s\n%s\n%s\n%s\n%s\n%s%s" % (self.__linha, self.__titulo, self.__linha, self.__cabecalho,
                                                 self.__linha, self.__corpo, self.__linha)
        else:
            return "%s\n%s\n%s\n%s%s" % (self.__linha, self.__cabecalho, self.__linha, self.__corpo, self.__linha)


def pausar(mensagem='\nENTER para continuar '):
    while True:
        entrada = input(mensagem)
        
        if not entrada:
            break


def input_tipo(texto='\t: ', mensagem_erro='\tValor incorreto', tipo='int'):
    """ Captura entrada do teclado com validação, retorno de acordo com tipo especificado:
    tipo='int': Validação de inteiro, default, retorno int;
    tipo='float': Validação de ponto flutuante, returno float;
    tipo='list': Validação de lista, retorno list;
    tipo='bool': Validação de booleano, retorno bool;
    Uso principalmente em menus e em interface de texto. """
    n = 0
    while True:
        n = input('%s' % texto)
        try:
            # Inteiro
            if tipo == 'int':
                n = int(n)
            # Ponto flutuante
            elif tipo == 'float':
                n = float(n)
            # Lista
            elif tipo == 'list':
                separador = ', ' if ', ' in n else ','

                n = n.split(separador)
                for i, x in enumerate(n):
                    try:
                        n[i] = int(x)
                    except ValueError:
                        try:
                            n[i] = float(x)
                        except ValueError:
                            n[i] = x
            # Booleano
            elif tipo == 'bool':
                dic = {True: ('yes', 'sim', 'y', 's'),
                       False: ('not', 'no', 'não', 'n')}
                if n.lower() in dic[True]:
                    n = True
                elif n.lower() in dic[False]:
                    n = False
                else:
                    raise ValueError
            break
        except ValueError:
            if mensagem_erro:
                print(mensagem_erro)
    return n


def validar_intervalo(valor, inicio, fim, mensagem_erro='\tValor incorreto', tipo='int'):
    """ Retorna um valor validado dentro do intervalo homogêneo e de acordo com tipo informado.
    Default: tipo='int'.
    Caso informado intervalo inválido, recaptura-se o valor.
    Uso principalmente em menus e em interface de texto. """
    if inicio > fim:
        inicio, fim = fim, inicio

    while True:
        if inicio <= valor <= fim:
            break
        else:
            print('%s\n' % mensagem_erro)
            valor = input_tipo('Informe um novo valor: ', tipo=tipo)
    return valor


def lista_randomica(inicio, fim):
    """ Gera uma lista randomica de acordo com intervalo(inicio-fim). """
    if inicio > fim:
        inicio, fim = fim, inicio

    lista = [x for x in range(inicio, fim + 1)]  # list(range(inicio, fim + 1))

    # Embaralhando a lista gerada acima de acordo com intervalo.
    shuffle(lista)

    return lista


def limpar_tela():
    """ Limpa tela de acordo com o sistema operacional. """
    sist_linux = ('posix',)
    sist_windowns = ('nt', 'ce',)

    if name in sist_linux:
        system('clear')
    elif name in sist_windowns:
        system('cls')


if __name__ == '__main__':
    # Teste em interface de texto.
    while True:
        limpar_tela()

        print("Funções e classes úteis\n")
        opc = validar_intervalo(input_tipo("1 - Pilha\n"
                                           "2 - Fila\n"
                                           "3 - Lista aleatória\n"
                                           "0 - Sair\n"
                                           "\t: "), 0, 3)

        if opc == 1 or opc == 2:
            if opc == 1:
                l = Pilha()
                # Pilha/Fila pode ser inicializada com n elementos.
                # l = Pilha(2, 5, 8)
                # l = Fila(1, 1, 2, 3)
                # Na inclusão pode-se inserir n elementos também.
                # l.incluir(6, 9, 12)
            else:
                l = Fila()

            while True:
                limpar_tela()

                opc2 = validar_intervalo(input_tipo("\n1 - Incluir\n"
                                                    "2 - Remover\n"
                                                    "3 - Ordenar\n"
                                                    "4 - Exibir\n"
                                                    "0 - Voltar\n"
                                                    "\t: "), 0, 4)

                if opc2 == 1:
                    n = input_tipo("\nDigite: ")
                    l.incluir(n)
                elif opc2 == 2:
                    t = l.remover()
                    print(("\nRemovido valor: %s" % t) if t else "\nVazia")
                    sleep(1.5)
                elif opc2 == 3:
                    print("" if l.ordenar() else "\nElementos heterogêneos/vazio")
                elif opc2 == 4:
                    print("\nPilha: " + str(l) if opc == 1 else "\nFila: " + str(l))
                    pausar()
                else:
                    break
        elif opc == 3:
            print("\n\nLista aleatória")
            print(">>>", lista_randomica(input_tipo("Inicial: "),
                                         input_tipo("Final: ")))
        else:
            break

        if opc != 0 or opc2 == 0:
            pausar()
