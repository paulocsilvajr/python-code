#!/usr/bin/python3
# coding: utf-8

try:
    # Importação para uso direto do módulo
    from funcoes_uteis import Fila, Tabela, input_tipo, validar_intervalo, pausar, limpar_tela
except ImportError:
    # Importação para uso pelo pacote sources
    from sources.funcoes_uteis import Fila, Tabela, input_tipo, validar_intervalo, pausar, limpar_tela

import mysql.connector  # sudo apt-get install python3-mysql.connector # ou # pip3 install mysql-connector-python
import psycopg2  # sudo apt-get install python3-psycopg2
# import psycopg2.extras  # para usar dicionários no self._cursor
import sqlite3  # builtin
from sys import exc_info
# pip3 freeze # listagem pacotes instalados

__author__ = "Paulo C. Silva Jr."


class Conexao:
    def __init__(self, dbms='', dbname='', user='', password='', host='localhost',
                 historico=True, tamanho_historico=100):
        """ Construtor da classe Conexao.
        :param dbms: nome do Sistema Gerenciador de BD(SGBD). DBMS=Data Base Management System.
        :param dbname: nome do BD. SQLite criará um banco local caso não exista.
        :param user: usuário usado na conexão. Usuários Admin: PostgreSQL=postgres, MySQL=root. SQLite não tem usuário.
        :param password: senha do usuário informado. SQLite não tem senha.
        :param host: host da conexão. Geralmente localhost para teste local. SQLite não tem host.
        :param historico: Habilita o armazenamento de histórico de ações do objeto Conexao.
        :param tamanho_historico: quantidade de registros do histórico. """
        self._dbms = dbms
        self._gerar_historico = historico
        self._tamanho_hist = tamanho_historico
        self._historico_acoes = Fila()
        self._excecao = None
        self.dml = ""

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
                self._historico_acoes.incluir("Conexão estabelecida com %s" % dbms)

            # Para o cursor na forma de dicionário no postgreSQL usar:
            # self._cursor = self._conexao._cursor(cursor_factory = psycopg2.extras.RealDictCursor)
            self._cursor = self._conexao.cursor()
        except:
            raise Exception("Conexão NÃO estabelecida com %s" % dbms)

    def consultar(self, tabela: str, campos="", filtro="", ordenacao="", quantidade=(0, 0)):
        """ Função de consultas ao BD.
        :param tabela: nome da tabela.
        :param campos: nome dos campos que serão exibidos.
        :param filtro: qualificação das tuplas(WHERE).
        :param ordenacao: ordenação das tuplas(ORDER BY).
        :param quantidade: quantidade de registros exibidos(LIMIT), [0]: registro inicial, [1]: quantidade registros.
        :return: Lista contendo tuplas dos registro da tabela pesquisada. """
        assert isinstance(tabela, str), "Formato do parâmetro tabela inválido"
        assert isinstance(quantidade, tuple), "Formato do parâmetro quantidade inválido"

        if campos == "":
            campos = "*"

        quant = ""
        if quantidade != (0, 0):
            if len(quantidade) == 1:
                quantidade = (0, quantidade[0])
            if self._dbms == 'mysql':
                quant = " LIMIT %d, %d" % (quantidade[0], quantidade[1])
            elif self._dbms in ('postgresql', 'sqlite'):
                quant = " LIMIT %d OFFSET %d" % (quantidade[1], quantidade[0])

        self._historico_crud("Consultado", tabela, ("filtro: %s,ordenação: %s" % (filtro, ordenacao)))

        return self.executar("SELECT %s FROM %s%s%s%s" % (campos, tabela,
                                                          (" WHERE " + filtro if filtro else ""),
                                                          (" ORDER BY " + ordenacao if ordenacao else ""),
                                                          quant))

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
        :param filtro: qualificação dos registro a apagar.
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
        :param filtro: qualificação da modificação.
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
            self.dml = dml
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

    def exibir_historico_acoes(self, ultimo_reg=False):
        """ Função para exibir o histórico de transações no BD.
        :param ultimo_reg: exibe registro de histórico. Caso True, exibe somente o último registro.
        :return: string do histórico. """
        msg = ""
        if ultimo_reg:
            msg = self._historico_acoes.exibir()[-1:][0]
        else:
            for i, e in enumerate(self._historico_acoes.exibir()):
                msg += "%d: %s\n" % (i+1, e)
        if self._gerar_historico:
            print(msg)
        return msg

    def _historico_crud(self, acao: str, tabela: str, filtro=""):
        """ Função base para geração de histórico.
        :return: None. """
        if self._gerar_historico:
            if len(self._historico_acoes.exibir()) == self._tamanho_hist:
                self._historico_acoes.remover()
            self._historico_acoes.incluir("%s tupla(%s) da tabela %s" % (acao, filtro, tabela))

    def __del__(self):
        """ Função para fechar a conexão quando o objeto Conexao for destruido. """
        self._conexao.close()
        if self._gerar_historico:
            print("Fechado a conexão com %s" % self._dbms)

    def fechar(self):
        self.__del__()


class Tabela:
    def __init__(self, bd: Conexao, tabela: str):
        """ Construtor genérico de tabela. Informar obrigatóriamente uma base de dados e uma tabela válida. """
        assert isinstance(bd, Conexao), "Tipo do parâmetro bd inválido."
        assert isinstance(tabela, str), "Tipo do parâmetro tabela inválido"

        self.bd = bd
        self.nome_tabela = tabela
        bd.consultar(self.nome_tabela, quantidade=(1,))
        self.campos = bd.descricao_campos()
        self.campos_protegidos = []

    def consultar(self, *args, **kwargs):
        """ Consulta da tabela.
        :param args: indices do atributo self.campos ou string da coluna. Ex. campos[1].
        :param kwargs: dicionário para qualificação da consulta(filtro: str, ordenacao: str, quantidade: tuple).
        :return: cursor ref. a consulta realizada. Para exibir os dados usar .fetchall() ou o método exibir(). """
        if len(args) == 0:
            campos = "*"
        else:
            campos = ((len(args) - 1) * "{}, " + "{}").format(*args)

        return self.bd.consultar(self.nome_tabela, campos, **kwargs)

    def exibir(self):
        """ Exibição dos dados consultados da tabela.
        :return: lista de tuplas correspondente aos registros consultados. """
        return self.bd.exibir_dados()

    def _campos_autorizados(self, funcao: str, kwargs):
        """ Verificação dos campos autorizados à atualização e inserção."""
        if self.campos_protegidos:
            for campo in self.campos_protegidos:
                if campo in kwargs.keys():
                    raise Exception('{}: Campos {} devem ser preservados.'.format(funcao, self.campos_protegidos))

        return True

    def inserir(self, **kwargs):
        """ Insercão de dados na tabela.
        :param kwargs: parametros em forma de dicionário: campo='Valor Campo'.
        :return: None. """
        if self._campos_autorizados(self.nome_tabela+'.inserir', kwargs):
            campos = ((len(kwargs) - 1) * "{}, " + "{}").format(*kwargs.keys())
            valores = ""

            for i, valor in enumerate(kwargs.values(), start=1):
                separador = ', ' if i < len(kwargs) else ''

                if isinstance(valor, str):
                    valores += "'{}'{}".format(valor, separador)
                else:
                    valores += "{}{}".format(valor, separador)

            self.bd.inserir(self.nome_tabela, campos, valores)

    def atualizar(self, **kwargs):
        """ Atualização de dados da tabela.
        :param kwargs: parametros em forma de dicionário: campo='Valor Campo'.
        Para especificar quais campos devem ser modificados, deve-se usar o parametro filtro='campo=Numero'.
        :return: None. """
        if self._campos_autorizados(self.nome_tabela+'.atualizar', kwargs):
            if 'filtro' in kwargs.keys():
                filtro = kwargs.pop('filtro')
            else:
                filtro = ""

            campos = ((len(kwargs) - 1) * "{}, " + "{}").format(*kwargs.keys())
            valores = ""

            for i, valor in enumerate(kwargs.values(), start=1):
                separador = ', ' if i < len(kwargs) else ''

                if isinstance(valor, str):
                    valores += "'{}'{}".format(valor, separador)
                else:
                    valores += "{}{}".format(valor, separador)

            self.bd.atualizar(self.nome_tabela, campos, valores, filtro)

    def excluir(self, filtro: str):
        """ Exclusão de dados da tabela.
        :param filtro: Delimitação da exclusão.
        :return: None. """
        assert isinstance(filtro, str), "Formato do parâmetro filtro inválido"

        self.bd.excluir(self.nome_tabela, filtro)


if __name__ == "__main__":
    pass
