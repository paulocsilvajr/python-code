#!/usr/bin/python3
# coding: utf-8

import sqlite3
import re
import random


class ChatterBot:
    """ ChatterBot simples usando SQLite para armazenar conhecimento e
    Regex(Expressões regulares) para identificar entrada para calculos. """
    def __init__(self):
        """ Construtor. """
        self.bd_mensagens = sqlite3.connect('bd_mensagens.db')

        self.prompt_user = ": "
        self.prompt_bot = "> "

        self.interagir()

    def interagir(self) -> None:
        """ Função de interação.
        :return: None. """
        while 1:
            try:
                # Captura da interação do usuário.
                msg = input(self.prompt_user).lower()
                # print("<'%s'" % msg)

                # re procurando 1 ou mais numeros não seguidos por uma ou mais letras e espaços.
                # padrao = r'[0-9]+[^a-zA-Z ]+'
                padrao = r'^[0-9]+\.?[0-9]*([\+\-\/%]|[\*]{1,2})[0-9]+\.?[0-9]*$'

                if re.search(padrao, msg):
                    print(self.prompt_bot + str(eval(msg)))
                else:
                    # Recuperação de interações cadastradas no BD.
                    lista_mensagens = self.bd_mensagens.\
                        execute("SELECT chave, valor FROM mensagens ORDER BY chave").fetchall()

                    if msg == 'ls':
                        temp = ""
                        print(self.prompt_bot + "Listagem de comandos disponíveis:")
                        for linha in lista_mensagens:
                            if linha[0] != temp:
                                print(self.prompt_bot + linha[0])
                            temp = linha[0]

                    elif msg in ('help', 'ajuda'):
                        print(self.prompt_bot +
                              'Digite ls para listar os comandos disponíveis e informe um deles ou\n'
                              '> Informe um calculo(ex: 1+1) ou\n'
                              '> Informe =pergunta para cadastrar nova pergunta(use REGEX para melhor'
                              ' performance, ex: ol[aá])')
                    else:
                        resposta = []
                        # filtro para cadastro de nova resposta para uma pergunta.
                        if re.search(r'=.+', msg):
                            msg = msg[1:]

                            for item in lista_mensagens:
                                if re.search(item[0], msg):
                                    msg = item[0]
                                    break
                        else:
                            # Procurando se a interação do usuário encaixa com alguma cadastrada.
                            for item in lista_mensagens:
                                # if item[0] in msg: # Substituido por busca por REGEX.
                                if re.search(item[0], msg):
                                    resposta.append(item[1])

                        # Se tiver resposta,
                        if resposta:
                            if resposta[0] == "quit":
                                break
                            else:
                                random.shuffle(resposta)
                                print("%s%s" % (self.prompt_bot, resposta[0]))
                        # Senão, solicita ao usuário o cadastro da resposta para a interação, caso usuário aceite.
                        else:
                            print("{0}Não sei como interagir\n{1}Deseja cadastrar a interação[S/n]: ".format(
                                self.prompt_bot, self.prompt_bot), end="")
                            confirmacao = input("").lower()

                            if confirmacao == "s":
                                try:
                                    # Gravação da nova interação no BD.
                                    self.bd_mensagens.execute("INSERT INTO mensagens(chave, valor)"
                                                              "VALUES('%s', '%s')" %
                                                              (msg, input("Resposta para '%s': " % msg)))
                                    self.bd_mensagens.commit()
                                except sqlite3.OperationalError:
                                    print(self.prompt_bot + "Ocorreu um problema na gravação da nova integração.")
                                except sqlite3.IntegrityError:
                                    print(self.prompt_bot + "Você informou uma integração já cadastrada.")

            # Foi tratado a excessão de interrupção pelo teclado(CTRL+C), por isso deve-se usar 'sair' para fechar.
            except KeyboardInterrupt:
                pass


def main():
    # Declaração de classe anônima.
    ChatterBot()


if __name__ == "__main__":
    main()
