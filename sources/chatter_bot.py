#!/usr/bin/python3
# coding: utf-8

import sqlite3
import re


class ChatterBot:
    """ ChatterBot simples usando SQLite para armazenar conhecimento e
    Regex(Expressões regulares) para identificar entrada para calculos. """
    def __init__(self):
        """ Construtor. """
        self.bd_mensagens = sqlite3.connect('bd_mensagens.db')

        try:
            self.bd_mensagens.execute('CREATE TABLE mensagem('
                                      'chave VARCHAR(50) PRIMARY KEY NOT NULL, '
                                      'valor VARCHAR(50) NOT NULL)')
            self.bd_mensagens.commit()
        except sqlite3.OperationalError:
            pass

        self.interagir()

    def interagir(self) -> None:
        """ Função de interação.
        :return: None. """
        while 1:
            try:
                # Captura da interação do usuário.
                msg = input(": ").lower()
                # print("<'%s'" % msg)

                # re procurando 1 ou mais numeros não seguidos por uma ou mais letras e espaços.
                padrao = r'[0-9]+[^a-zA-Z ]+'
                if re.search(padrao, msg):
                    print(eval(msg))
                else:
                    # Recuperação de interações cadastradas no BD.
                    lista_mensagens = self.bd_mensagens.execute("SELECT chave, valor FROM mensagem").fetchall()

                    if msg == 'ls':
                        for linha in lista_mensagens:
                            print(linha[0])
                    elif msg in ('help', 'ajuda'):
                        print('Digite ls para listar os comandos disponíveis e informe um deles\n'
                              'ou informe um calculo(ex: 1+1)')
                    else:
                        # Procurando se a interação do usuário encaixa com alguma cadastrada.
                        resposta = ""
                        for item in lista_mensagens:
                            if item[0] in msg:
                                resposta = item[1]
                                break

                        # Se tiver resposta,
                        if resposta:
                            if resposta == "quit":
                                break
                            else:
                                print("> %s" % resposta)
                        # Senão, solicita ao usuário o cadastro da resposta para a interação, caso usuário aceite.
                        else:
                            print("Não sei como interagir\nDeseja cadastrar a interação[S/n]: ", end="")
                            confirmacao = input("").lower()

                            if confirmacao == "s":
                                try:
                                    # Gravação da nova interação no BD.
                                    self.bd_mensagens.execute("INSERT INTO mensagem(chave, valor)"
                                                              "VALUES('%s', '%s')" % (msg,
                                                                                      input("Resposta para '%s': " % msg)))
                                    self.bd_mensagens.commit()
                                except sqlite3.OperationalError:
                                    pass
            # Foi tratado a excessão de interrupção pelo teclado(CTRL+C), por isso deve-se usar 'sair' para fechar.
            except KeyboardInterrupt:
                pass


def main():
    # Declaração de classe anônima.
    ChatterBot()

if __name__ == "__main__":
    main()
