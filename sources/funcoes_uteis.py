#!/usr/bin/python3
# -*- coding: utf-8 -*-

from random import shuffle
from os import system, name
from time import sleep
from threading import Thread
from datetime import datetime, timedelta
import re

__author__ = "Paulo C. Silva Jr"

""" Módulo com funções e classes úteis para qualquer programa.
    Desenvolvido em Python 3.x """


class Pilha:
    """ FILO - First In Last Out. """
    # Atributo estático quantificador de instâncias.
    quantidade = 0
    def __init__(self, *itens):
        """ Construtor da classe.
        Possibilita a inclusão de itens na criação do objeto. """
        self._elementos = []
        if itens:
            self._adicionar_elementos(itens)

        # Incremento ao atribuito estático, contando a quantidade de instâncias do classe Pilha.
        Pilha.quantidade += 1

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

    def limpar(self):
        self._elementos.clear()
        return self._elementos

    def __getitem__(self, item):
        """ Exibição de _elementos[item]. """
        return self._elementos[item]

    def __setitem__(self, key, value):
        """ Atibuição de value em _elementos[key]. """
        self._elementos[key] = value

    def __bool__(self):
        """ Caso exista itens em _elementos, retorna True. """
        return bool(self._elementos)

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
    """ Classe para impressão de tabela em modo texto. """

    def __init__(self, dados_tabela, titulos_colunas=None, largura=0, titulo_tabela=""):
        """ Método construtor e gerador da tabela.
        :param dados_tabela: tupla ou lista contendo os dados(registros)
        :param titulos_colunas: tupla ou lista com os títulos das colunas, caso omitido,
        assume-se nomenclatura padrão: coluna1, col...
        :param largura: largura, em inteiro, para as colunas. Caso omitido, é assumido o maior registro de cada coluna.
        :param titulo_tabela: Titulo da tabela, caso omitido, não é exibido. """
        assert isinstance(dados_tabela, list) or isinstance(dados_tabela, tuple), \
            "Formato do parâmetro dados_tabela inválido"
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
        """ Impressão do objeto coluna.
        :return: String da tabela elaborado pelo construtor. """
        if self.__titulo:
            return "%s\n%s\n%s\n%s\n%s\n%s%s" % (self.__linha, self.__titulo, self.__linha, self.__cabecalho,
                                                 self.__linha, self.__corpo, self.__linha)
        else:
            return "%s\n%s\n%s\n%s%s" % (self.__linha, self.__cabecalho, self.__linha, self.__corpo, self.__linha)


class Temporizador(Thread):
    def __init__(self, horario: str, funcao: object, *args, **kwargs):
        """ Temporizador de função em horários definidos. Cada execução da função é feita por uma thread própria.
        :param horario: string contendo os horários gatilho.
        Formatos: hh:mm:ss ou dd/mm/yyyy hh:mm:ss ou +1h ou +1m ou +1s
        :param funcao: nome da função que será executado nos horários definidos.
        :param args: parametros da função, separados por virgula.
        :param kwargs: parametros(em formato chave=valor) da função. Deve ser informado nomeparametro=valor, n...
        :param formato: Opcional. Formato do horário informado: 'AM', 'PM', '24hs(default). '
        :param completo: Opcional. Se True, o horário deve ser no formato dd/mm/yyyy hh:mm:ss. """
        assert isinstance(funcao, object), "Formato do parâmetro funcao inválido"
        assert isinstance(horario, str), "Formato do parâmetro horario inválido"

        self._lista_horario = Fila()
        self.funcao = funcao
        self.parametro = args
        self.kparametro = kwargs

        if horario:
            param = {}
            if 'formato' in self.kparametro.keys():
                param['formato'] = self.kparametro['formato']
                self.kparametro.pop('formato')
            if 'completo' in self.kparametro.keys():
                param['completo'] = self.kparametro['completo']
                self.kparametro.pop('completo')

            if not self._adicionar_horario(horario, **param):
                raise Exception("Formato de horário inválido. ")
        Thread.__init__(self)

        # Inicialização da thread.
        self.start()
        self.join()

    def _adicionar_horario(self, horario: str, formato="24hs", completo=False) -> None:
        """ Inclusão do(s) horário(s) gatilho do temporizador.
        :param horario: Horario(s). Separador por ',' caso seja informado em plural.
        :param formato: Definição do formato do horário: AM, PM ou 24hs(default).
        :param completo: Formato da horário. Caso True o formato deve ser 'dd/mm/yyyy hh:mm:ss', se não, 'hh:mm:ss'.
        Pode-se omitir os segundos.
        :return: None. """
        try:
            if "+" in horario:
                # Validação para execução por acrescimo de tempo(h, m, s)
                agora = datetime.now()
                if "h" in horario:
                    n = int(horario.replace("+", "").replace("h", ""))
                    horario = agora + timedelta((1/24)*n)
                elif "m" in horario:
                    n = int(horario.replace("+", "").replace("m", ""))
                    horario = agora + timedelta(((1/24)/60)*n)
                elif "s" in horario:
                    n = int(horario.replace("+", "").replace("s", ""))
                    horario = agora + timedelta((((1/24)/60)/60)*n)

                self._lista_horario.incluir(horario)
            else:
                for i in converter_string_data(horario, formato, completo):
                    self._lista_horario.incluir(i)

            return True
        except ValueError or IndexError:
            return False

    # Override
    def run(self):
        """ Processo principal da thread.
        :return: None. """
        while self._lista_horario:
            sleep(1)
            agora = datetime.now()

            # Teste de resposta da thread
            # print("Esperando...", self._lista_horario[0], "- agora:", agora)

            if agora.year == self._lista_horario[0].year and \
                    agora.month == self._lista_horario[0].month and \
                    agora.day == self._lista_horario[0].day and \
                    agora.hour == self._lista_horario[0].hour and \
                    agora.minute == self._lista_horario[0].minute and \
                    agora.second == self._lista_horario[0].second:
                self._lista_horario.remover()

                if self.kparametro is not None or self.parametro is not None:
                    th = Thread(target=self.funcao, args=self.parametro, kwargs=self.kparametro)
                else:
                    th = Thread(target=self.funcao)
                th.start()
            elif self._lista_horario[0] < agora:
                break

            if not self._lista_horario:
                break


def converter_string_data(horario: str, formato="24hs", completo=False, ordenar=True) -> list:
    """ Conversão de string em datetime. Usado na classe Temporizador.
    :param horario: Horario(s). Separador por ',' caso seja informado em grupo.
    :param formato: Definição do formato do horário: AM, PM ou 24hs(default).
    :param completo: Formato da horário. Caso True o formato deve ser 'dd/mm/yyyy hh:mm:ss', senão, 'hh:mm:ss'.
    Pode-se omitir os segundos.
    :param ordenar: Classificação em ordem crescente dos horários.
    :return: lista de horários(datetime). """
    assert isinstance(horario, str), "Formato do parâmetro horário inválido"

    separador = ', ' if ', ' in horario else ','

    lista_horario = horario.split(separador)

    ano, mes, dia = datetime.now().year, datetime.now().month, datetime.now().day
    segundo = 0

    for i, h in enumerate(lista_horario):
        if completo:
            h = h.replace('/', ':')
            h = h.replace(' ', ':')
            lista_horario[i] = h.split(':')

            ano, mes, dia = int(lista_horario[i][2]), int(lista_horario[i][1]), int(lista_horario[i][0])
            hora, minuto = int(lista_horario[i][3]), int(lista_horario[i][4])

            if formato.lower() == 'pm':
                hora += 12

            if len(lista_horario[i]) > 5:
                segundo = int(lista_horario[i][5])
        else:
            lista_horario[i] = h.split(':')
            hora, minuto = int(lista_horario[i][0]), int(lista_horario[i][1])

            if formato.lower() == 'pm':
                hora += 12

            if len(lista_horario[i]) > 2:
                segundo = int(lista_horario[i][2])

        lista_horario[i] = datetime(ano, mes, dia, hora, minuto, segundo)

    if len(lista_horario) > 1 and ordenar:
        lista_horario.sort()
    return lista_horario


class Cpf:
    """ Classe validadora CPF. Baseado em <http://www.python.org.br/wiki/VerificadorDeCPF>. Adaptado para Python3. """
    def __init__(self, cpf):
        """O argumento cpf pode ser uma string nas formas:
            12345678910
            123.456.789-10
        ou uma lista ou tuple:
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 0]
            (1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 0) """
        if isinstance(cpf, str):
            if not cpf.isdigit():
                cpf = self.translate(cpf)

        self.cpf = [int(x) for x in cpf]

    @staticmethod
    def translate(cpf):
        """ Traduz CPF com os separadores para somente números. """
        return ''.join(re.findall("\d", cpf))

    def _exceptions(self, cpf):
        """ Exceções para invalidação de CPF. """
        if len(cpf) != 11:
            return True
        else:
            s = ''.join(str(x) for x in cpf)
            if s == '00000000000' or s == '11111111111' or s == '22222222222' or s == '33333333333' or \
               s == '44444444444' or s == '55555555555' or s == '66666666666' or \
               s == '77777777777' or s == '88888888888' or s == '99999999999':
                return True
        return False

    def _gen(self, cpf):
        """ Gera o próximo dígito do número de CPF. """
        res = []
        for i, a in enumerate(cpf):
            b = len(cpf) + 1 - i
            res.append(b * a)

        res = sum(res) % 11

        if res > 1:
            return 11 - res
        else:
            return 0

    def __getitem__(self, index):
        """ Retorna o dígito em index como string. """
        return self.cpf[index]

    def __repr__(self):
        """ Retorna uma representação 'real', ou seja, eval(repr(cpf)) == cpf. """
        return "CPF('%s')" % ''.join(str(x) for x in self.cpf)

    def __eq__(self, other):
        """ Provê teste de igualdade para números de CPF. """
        return isinstance(other, Cpf) and self.cpf == other.cpf

    def __str__(self):
        """ Retorna uma representação do CPF na forma: 123.456.789-10. """
        d = iter("..-")
        s = list(map(str, self.cpf))
        for i in range(3, 12, 4):
            s.insert(i, d.next())
        r = ''.join(s)
        return r

    def is_valid(self):
        """ Valida o número de cpf. """
        if self._exceptions(self.cpf):
            return False

        s = self.cpf[:9]
        s.append(self._gen(s))
        s.append(self._gen(s))
        return s == self.cpf[:]

    def __bool__(self):
        return self.is_valid()


def pausar(mensagem='\nENTER para continuar '):
    while True:
        entrada = input(mensagem)

        if not entrada:
            break


def calcular_string(texto, operacoes=('+', '-', '*', '/', '**', '//', '%')):
    for op in operacoes:
        if op in texto:
            print(texto, '=', eval(texto))
            break
    return eval(texto)


def input_tipo(texto='\t: ', mensagem_erro='\tValor incorreto', tipo='int',
               operacoes=('+', '-', '*', '/', '**', '//', '%')):
    """ Captura entrada do teclado com validação, retorno de acordo com tipo especificado.
    Nos tipos int e float pode-se fazer calculos(1+2)
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
                n = calcular_string(n, operacoes)
                n = int(n)
            # Ponto flutuante
            elif tipo == 'float':
                n = calcular_string(n, operacoes)
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


def report_event(event):
    """Imprime a descrição de um evento, baseado em seus atributos.
    ref. FERD, Steven. PENSANDO EM TKINTER. Disponível em
    <http://www.dcc.ufrj.br/~fabiom/mab225/PensandoTkinter.pdf>.
    Eventos: Tkinter 8.5 reference gui for Python. 158-162."""
    event_name = {"2": "KeyPress", "3": "KeyRelease", "4": "ButtonPress"}
    print("Time:", str(event.time))

    print("EventType=" + str(event.type) + "=" +
          event_name[str(event.type)] if str(event.type) in event_name.keys() else "",
          "EventWidgetId=" + str(event.widget),
          "EventKeySymbol=" + str(event.keysym), "KeyChar(KeyPress/KeyRelease)=" + event.char, sep="\n")


def converter_formato_data(strdata: str, masc_data="{2}/{1}/{0}", sep_data="-") -> str:
    """ Conversão de data no formato da mascara informada.
    0: ano, 1: mês, 2: ano.
    hora no formato H:M:S"""
    if len(strdata) > 10:
        completo = True
    else:
        completo = False

    data = strdata.split(' ')
    if completo:
        data, hora = data[0], data[1]
    else:
        data = data[0]

    hora = "" if not completo else hora.split('.')[0]
    data = masc_data.format(*data.split(sep_data))
    return data + ((" " + hora) if completo else "")


def data_atual(completo=True):
    """ Retorna a data atual em uma tupla contendo uma data no formato datetime e uma string da data. """
    agora = datetime.now()
    return agora, agora.strftime('%d/%m/%Y %H:%M:%S') if completo else agora.strftime('%d/%m/%Y')


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
        opc2 = None

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
