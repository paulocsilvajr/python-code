#!/usr/bin/python3
# coding: utf-8

try:
    # Importação para uso direto do módulo
    from funcoes_uteis import Fila, Tabela
except ImportError:
    # Importação para uso pelo pacote sources
    from sources.funcoes_uteis import Fila, Tabela

# sudo apt-get install python3-mysql.connector # ou # pip3 install mysql-connector-python
import mysql.connector
# sudo apt-get install python3-psycopg2
import psycopg2
# import psycopg2.extras  # para usar dicionários no _cursor

# builtin
import sqlite3
# pip3 freeze # listagem pacotes instalados

__author__ = "Paulo C. Silva Jr."


class Conexao:
    def __init__(self, dbms, dbname, user, host, password, historico=True, tamanho_historico=100):
        self._dbms = dbms
        self._gerar_historico = historico
        self._tamanho_hist = tamanho_historico
        self._hist = Fila()
        try:
            if dbms == 'mysql':
                self._conexao = mysql.connector.connect(user=user, password=password, host=host, database=dbname)
            elif dbms == 'postgresql':
                self._conexao = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'"
                                                 % (dbname, user, host, password))
            # A implementar
            elif dbms == 'sqlite':
                self._conexao = sqlite3.connect('%s.db' % dbname)

            if self._gerar_historico:
                self._hist.incluir("Conexão estabelecida com %s" % dbms)

            # Para o cursor na forma de dicionário no postgreSQL usar:
            # self._cursor = self._conexao._cursor(cursor_factory = psycopg2.extras.RealDictCursor)
            self._cursor = self._conexao.cursor()
        except:
            raise Exception("Conexão NÃO estabelecida com %s" % dbms)

    def consultar(self, tabela="", campos="", filtro="", ordenacao=""):
        self._historico_crud("Consultado", tabela, ("filtro: %s,ordenação: %s" % (filtro, ordenacao)))

        return self.executar("SELECT %s FROM %s%s%s" % (campos, tabela,
                             (" WHERE " + filtro if filtro else ""),
                             (" ORDER BY " + ordenacao if ordenacao else "")))

    def inserir(self, tabela="", campos="", valores=""):
        self.executar("INSERT INTO %s(%s) VALUES(%s)" % (tabela, campos, valores))
        self._conexao.commit()

        self._historico_crud("Inserido", tabela, "%s = %s" % (campos, valores))

    def excluir(self, tabela="", filtro=""):
        self.executar("DELETE FROM %s WHERE %s" % (tabela, filtro))
        self._conexao.commit()

        self._historico_crud("Excluído", tabela, filtro)

    def atualizar(self, tabela="", campos="", valores="", filtro=""):
        campos = campos.split(", " if ", " in campos else ",")
        valores = valores.split(", " if ", " in campos else ",")
        elementos = ""

        if len(campos) == len(valores):
            for i in range(len(campos)):
                elementos += "%s=%s%s" % (campos[i], valores[i], (", " if i < len(campos) - 1 else ""))

            self.executar("UPDATE %s SET %s%s" % (tabela, elementos, (" WHERE " + filtro if filtro else "")))
            self._conexao.commit()

            self._historico_crud("Atualizado", tabela, filtro)

    def executar(self, dml=""):
        self._cursor.execute(dml)
        return self._cursor

    # Criar procedure/function no PostgreSQL para testar
    def executar_procedure(self, dml="", parametros=""):
        if self._dbms == 'postgresql':
            self._cursor.callproc(dml, parametros)
            return self._cursor
        return ""

    def mensagem_status(self):
        if self._dbms == 'postgresql':
            return self._cursor.statusmessage
        return ""

    def exibir_dados(self):
        return self._cursor.fetchall()

    def descricao(self):
        return self._cursor.description

    def descricao_campos(self):
        campos = []
        for i in self._cursor.description:
            campos.append(i[0])

        return campos

    def quantidade_registros(self):
        return self._cursor.rowcount

    def exibir_historico(self, ultimo_reg=False):
        if ultimo_reg:
            print(self._hist.exibir()[-1:][0])
        else:
            for i, e in enumerate(self._hist.exibir()):
                print("%d: %s" % (i+1, e))

    def _historico_crud(self, acao="", tabela="", filtro=""):
        if self._gerar_historico:
            if len(self._hist.exibir()) == self._tamanho_hist:
                self._hist.remover()
            self._hist.incluir("%s tupla(%s) da tabela %s" % (acao, filtro, tabela))

    def __del__(self):
        self._conexao.close()
        if self._gerar_historico:
            print("Fechado a conexão com %s" % self._dbms)


if __name__ == '__main__':
    # Recuperando o usuário e a senha em arquivo
    with open('/home/paulo/pc/usuarioSenhaTeste') as f:
        usuario = f.readline()[:-1]  # recortando o \n=caracter de nova linha
        senha = f.readline()[:-1]
    # print(usuario, senha, sep="\n")

    # CONNECTION
    # postgreSQL
    c = Conexao('postgresql', 'teste', usuario, '127.0.0.1', senha)
    # MySQL/MariaDB
    # c = Conexao('mysql', 'teste', usuario, '127.0.0.1', senha)

    # INSERT
    # for i in range(100):
    #     c.inserir("teste", "texto, numero, valor, valor_decimal, data_teste",
    #               "'teste" + str(i) + "', " + str(42+i) + ", " + str(5.25+i) +
    #               ", " + str(6.35+i) + ",'" + str(2016+i) + "/03/01'")

    # DELETE
    # c.excluir("teste", "id>5")

    # UPDATE
    # c.atualizar("teste", "texto, numero", "'Paulo', 8", "id>40")

    # SELECT
    c.consultar("teste", "*", ordenacao="id")
    # for i in c.exibir_dados():
    #     print(i)

    # OU
    # for tupla in c.consultar("teste", "*", ordenacao="id"):
    #     print(tupla)

    # Descrições da tabela
    # print(c.descricao())
    # print(c.descricao_campos())

    # Mensagens
    # print(c.quantidade_registros(), "registros")
    # print(c.mensagem_status())

    # Histórico do objeto Conexao
    # c.exibir_historico()

    # Impressão dados pela class Tabela
    t = Tabela(c.exibir_dados(), c.descricao_campos(), titulo_tabela="Tabela Teste")
    print(t)

    # CLOSE CONNECTION
    del c
