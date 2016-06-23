#!/usr/bin/python3
# coding: utf-8

try:
    from funcoes_uteis import Fila, Tabela  # Importação para uso direto do módulo
except ImportError:
    from sources.funcoes_uteis import Fila, Tabela  # Importação para uso pelo pacote sources

import mysql.connector  # sudo apt-get install python3-mysql.connector # ou # pip3 install mysql-connector-python
import psycopg2  # sudo apt-get install python3-psycopg2
# import psycopg2.extras  # para usar dicionários no self._cursor
import sqlite3  # builtin
from sys import exc_info
# pip3 freeze # listagem pacotes instalados

__author__ = "Paulo C. Silva Jr."


class Conexao:
    def __init__(self, dbms='', dbname='', user='', host='', password='', historico=True, tamanho_historico=100):
        """ Construtor da classe Conexao.
        :param dbms: nome do Sistema Gerenciador de BD(SGBD). DBMS=Data Base Management System.
        :param dbname: nome do BD. SQLite criará um banco local caso não exista.
        :param user: usuário usado na conexão. Usuários Admin: PostgreSQL=postgres, MySQL=root. SQLite não tem usuário.
        :param host: host da conexão. Geralmente localhost para teste local. SQLite não tem host.
        :param password: senha do usuário informado. SQLite não tem senha.
        :param historico: Habilita o armazenamento de histórico de ações do objeto Conexao.
        :param tamanho_historico: quantidade de registros do histórico. """
        self._dbms = dbms
        self._gerar_historico = historico
        self._tamanho_hist = tamanho_historico
        self._hist = Fila()
        self._excecao = None

        try:
            if dbms == 'mysql':
                self._conexao = mysql.connector.connect(user=user, password=password, host=host, database=dbname)
                self._excecao = mysql.connector.errors.DatabaseError
            elif dbms == 'postgresql':
                self._conexao = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'"
                                                 % (dbname, user, host, password))
                self._excecao = psycopg2.DatabaseError
            elif dbms == 'sqlite':
                self._conexao = sqlite3.connect('%s.db' % dbname)
                self._excecao = sqlite3.DatabaseError
            else:
                # Caso for informado um SGBD não cadastrado, gera uma exceção.
                raise Exception("SGBD %s não cadastrado" % dbms)

            if self._gerar_historico:
                self._hist.incluir("Conexão estabelecida com %s" % dbms)

            # Para o cursor na forma de dicionário no postgreSQL usar:
            # self._cursor = self._conexao._cursor(cursor_factory = psycopg2.extras.RealDictCursor)
            self._cursor = self._conexao.cursor()
        except:
            raise Exception("Conexão NÃO estabelecida com %s" % dbms)

    def consultar(self, tabela: str, campos="", filtro="", ordenacao=""):
        """ Função de consultas ao BD.
        :param tabela: nome da tabela.
        :param campos: nome dos campos que serão exibidos.
        :param filtro: classificação das tuplas.
        :param ordenacao: ordenação das tuplas.
        :return: Lista contendo tuplas dos registro da tabela pesquisada. """
        assert isinstance(tabela, str), "Formato do parâmetro tabela inválido"

        if campos == "":
            campos = "*"

        self._historico_crud("Consultado", tabela, ("filtro: %s,ordenação: %s" % (filtro, ordenacao)))

        return self.executar("SELECT %s FROM %s%s%s" % (campos, tabela,
                             (" WHERE " + filtro if filtro else ""),
                             (" ORDER BY " + ordenacao if ordenacao else "")))

    def inserir(self, tabela: str, campos: str, valores: str):
        """ Função para inserir registros ao BD.
        :param tabela: nome da tabela.
        :param campos: nome dos campos.
        :param valores: valores referentes ao campos inseridos.
        :return: None. """
        assert isinstance(tabela, str), "Formato do parâmetro tabela inválido"
        assert isinstance(campos, str), "Formato do parâmetro campos inválido"
        assert isinstance(valores, str), "Formato do parâmetro valores inválido"

        self.executar("INSERT INTO %s(%s) VALUES(%s)" % (tabela, campos, valores))
        self._conexao.commit()

        self._historico_crud("Inserido", tabela, "%s = %s" % (campos, valores))

    def excluir(self, tabela: str, filtro: str):
        """ Função para apagar registros de tabela do BD.
        :param tabela: nome tabela.
        :param filtro: classificação dos registro a apagar.
        :return: None. """
        assert isinstance(tabela, str), "Formato do parâmetro tabela inválido"
        assert isinstance(filtro, str), "Formato do parâmetro filtro inválido"

        self.executar("DELETE FROM %s WHERE %s" % (tabela, filtro))
        self._conexao.commit()

        self._historico_crud("Excluído", tabela, filtro)

    def atualizar(self, tabela: str, campos: str, valores: str, filtro=""):
        """ Função para modificar registro de tabela do BD.
        :param tabela: nome da tabela.
        :param campos: campos que serão modificados.
        :param valores: valores referentes aos campos inseridos.
        :param filtro: classificação da modificação.
        :return: None. """
        assert isinstance(tabela, str), "Formato do parâmetro tabela inválido"
        assert isinstance(campos, str), "Formato do parâmetro campos inválido"
        assert isinstance(valores, str), "Formato do parâmetro valores inválido"

        campos = campos.split(", " if ", " in campos else ",")
        valores = valores.split(", " if ", " in campos else ",")
        elementos = ""

        if len(campos) == len(valores):
            for i in range(len(campos)):
                elementos += "%s=%s%s" % (campos[i], valores[i], (", " if i < len(campos) - 1 else ""))

            self.executar("UPDATE %s SET %s%s" % (tabela, elementos, (" WHERE " + filtro if filtro else "")))
            self._conexao.commit()

            self._historico_crud("Atualizado", tabela, filtro)

    def criar_tabela(self, nome: str, campos: str):
        """ Função para criação de tabelas do BD conectado.
        :param nome: string: nome da tabela.
        :param campos: string: nome dos campos. Ex: nome tipo chave primaria não nulo, nome tipo ...
        :return: None. """
        assert isinstance(nome, str), "Formato do parâmetro tabela inválido"
        assert isinstance(campos, str), "Formato do parâmetro campos inválido"

        self.executar("CREATE TABLE %s(%s)" % (nome, campos))
        self._conexao.commit()

    def executar(self, dml: str):
        """ Função base para execução de SQL no BD.
        :param dml: string: intrução SQL.
        :return: retorna self._conexao.cursor(), caso a instrução SQL for válida,
        ou exc_info: informações da execução, caso contrário. """
        try:
            assert isinstance(dml, str), "Formato do parâmetro dml inválido"
            self._cursor.execute(dml)
            return self._cursor
        except self._excecao:
            print(exc_info()[1])
            return exc_info()

    # Criar procedure/function no PostgreSQL para testar
    def executar_procedure(self, dml: str, parametros=""):
        assert isinstance(dml, str), "Formato do parâmetro dml inválido"

        if self._dbms == 'postgresql':
            self._cursor.callproc(dml, parametros)
            return self._cursor
        return None

    def mensagem_status(self):
        if self._dbms == 'postgresql':
            return self._cursor.statusmessage
        return None

    def exibir_dados(self):
        """ Função para exibição dos dados do cursor.
        :return: Lista com registros do cursor. """
        return self._cursor.fetchall()

    def descricao(self):
        """ Função base para a função descrição campos.
        :return: Lista contendo descrições do cursor
        """
        return self._cursor.description

    def descricao_campos(self):
        """ Função contendo nomes dos campos(colunas) do cursor.
        :return: Lista de strings dos campos. """
        campos = []
        for i in self._cursor.description:
            campos.append(i[0])

        return campos

    def quantidade_registros(self):
        """ Função quantificadora de registro do cursor.
        :return: quantidade de registro do cursor em inteiro. """
        return self._cursor.rowcount

    def exibir_historico(self, ultimo_reg=False):
        """ Função para exibir o histórico de transações no BD.
        :param ultimo_reg: exibe registro de histórico. Caso True, exibe somente o último registro.
        :return: string do histórico. """
        msg = ""
        if ultimo_reg:
            msg = self._hist.exibir()[-1:][0]
        else:
            for i, e in enumerate(self._hist.exibir()):
                msg += "%d: %s\n" % (i+1, e)
        if self._gerar_historico:
            print(msg)
        return msg

    def _historico_crud(self, acao: str, tabela: str, filtro=""):
        """ Função base para geração de histórico.
        :return: None. """
        if self._gerar_historico:
            if len(self._hist.exibir()) == self._tamanho_hist:
                self._hist.remover()
            self._hist.incluir("%s tupla(%s) da tabela %s" % (acao, filtro, tabela))

    def __del__(self):
        """ Função para fechar a conexão quando o objeto Conexao for destruido. """
        self._conexao.close()
        if self._gerar_historico:
            print("Fechado a conexão com %s" % self._dbms)


if __name__ == '__main__':
    # TESTE # TESTE # TESTE # TESTE # TESTE # TESTE # TESTE # TESTE # TESTE # TESTE #
    # Recuperando o usuário e a senha em arquivo
    with open('/home/paulo/pc/usuarioSenhaTeste') as f:
        usuario = f.readline()[:-1]  # recortando o \n=caracter de nova linha
        senha = f.readline()[:-1]
    # print(usuario, senha, sep="\n")

    # CONNECTION
    # postgreSQL
    # c = Conexao('postgresql', 'teste', usuario, '127.0.0.1', senha)
    # MySQL/MariaDB
    # c = Conexao('mysql', 'teste', usuario, '127.0.0.1', senha)
    # SQLite
    c = Conexao('sqlite', 'teste')

    # INSERT
    # for i in range(100):
    #     c.inserir("teste", "texto, numero, valor, valor_decimal, data_teste",
    #               "'teste" + str(i) + "', " + str(42+i) + ", " + str(5.25+i) +
    #               ", " + str(6.35+i) + ",'" + str(2016+i) + "/03/01'")
    # for i in range(10000):
    #     c.inserir('pessoa', 'nome, data_nascimento', "'Nome%s', '%d/12/05'" % (i, 2000+i))

    # DELETE
    # c.excluir("teste", "id>5")

    # UPDATE
    # c.atualizar("teste", "texto, numero", "'Paulo', 8", "id>40")

    # SELECT
    # c.consultar("teste", "*", ordenacao="id")
    # for i in c.exibir_dados():
    #     print(i)
    # c.consultar("pessoa", filtro="id>=75 and id<=100")
    # t = Tabela(c.exibir_dados(), c.descricao_campos(), titulo_tabela="pessoa")
    # print(t)

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
    # t = Tabela(c.exibir_dados(), c.descricao_campos(), titulo_tabela="Tabela Teste")
    # print(t)

    # CREATE TABLE
    # SQLite EXAMPLE
    # c.criar_tabela('pessoa', "id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
    #                          "nome VARCHAR(100) NOT NULL,"
    #                          "data_nascimento TIMESTAMP")
    # for i in range(100):
    #     c.inserir('pessoa', 'nome, data_nascimento', "'Pessoa%s', '2000/02/01'" % i)
    for i in c.consultar('pessoa', filtro="id<26", ordenacao='id, nome'):
        print(i)

    # CLOSE CONNECTION
    del c
