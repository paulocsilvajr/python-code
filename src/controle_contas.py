#!/usr/bin/python3
# coding: utf-8
# Desenvolvido em Python 3.5 e PostgreSQL 9.5.
# Usando o módulo conexaoDB(presente no pacote sources) para acesso ao banco.
# DER(model MySQL-Workbench) e SQL dos elementos do banco de dados em anexo na pasta arquivos contas.

try:
    from conexaoDB import Conexao, Tabela
    from funcoes_uteis import report_event, converter_formato_data, Cpf, data_atual
except ImportError:
    from src.conexao_db import Conexao, Tabela
    from src.funcoes_uteis import report_event, converter_formato_data, Cpf, data_atual

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showwarning, askyesno
import string
from collections import OrderedDict
from datetime import datetime

__author__ = "Paulo C. Silva Jr."

# Recuperando usuario e senha de arquivo.
with open('/home/paulo/pc/usuarioSenhaTeste') as f:
    usuario = f.readline()[:-1]
    senha = f.readline()[:-1]
# print(usuario, senha)

# Criando a conexão ao banco de dados.
bd_contas = Conexao('postgresql', 'bd_contas', usuario, senha)


# Declaração das classes específicas para cada tabela.
class Contas(Tabela):
    def __init__(self):
        """ Construtor da tabela conta com identificação de campos protegidos. """
        super(Contas, self).__init__(bd_contas, 'contas')
        # Tabela.__init__(self, bd_contas, 'contas')
        self.campos_protegidos = ['id', 'data_inclusao']


class Lancamentos(Tabela):
    def __init__(self):
        super(Lancamentos, self).__init__(bd_contas, 'lancamentos')


class VwLancamentosContas(Tabela):
    def __init__(self):
        super(VwLancamentosContas, self).__init__(bd_contas, 'vw_lancamento_contas')


class Pessoas(Tabela):
    def __init__(self):
        super(Pessoas, self).__init__(bd_contas, 'pessoas')


class FrmPrincipal(tk.Tk):
    def __init__(self):
        """ Construtor da formulário principal. """
        # Construtor do tk.Tk
        super(FrmPrincipal, self).__init__()

        self.title('Controle de Contas')
        self.minsize(width=120, height=145)
        self.maxsize(width=200, height=180)
        # Se o max e min forem iguais, é broqueado o redimensionamento da janela.
        # self.root.resizable(width=False, height=False)  # Broquear redimensionamento de janela.

        ttk.Style().theme_use('clam')  # temas do ttk: 'clam', 'classic', 'default', 'alt'

        # Declaração dos elementos do formulário.
        self.lbl_mensagem = ttk.Label(self, text="Clique em um cadastro.")
        self.lbl_mensagem.place(x=10, y=10, height=20)

        self.btn_contas = ttk.Button(self, text='Contas')
        self.btn_contas.bind('<Button-1>', self.contas)
        self.btn_contas.place(x=10, y=35, width=100, height=30)

        self.btn_lancamentos = ttk.Button(self, text='Lançamentos')
        self.btn_lancamentos.bind('<Button-1>', self.lancamentos)
        self.btn_lancamentos.place(x=10, y=70, width=100, height=30)

        self.btn_pessoas = ttk.Button(self, text='Pessoas')
        self.btn_pessoas.bind('<Button-1>', self.pessoas)
        self.btn_pessoas.place(x=10, y=105, width=100, height=30)

        # Especificação das dimensões e posição.
        # Alinhamento na tela: Centralizado na margem superior
        comprimento = 200
        altura = 150
        self.geometry('%dx%d-%d-%d' % (comprimento,
                                       altura,
                                       (self.winfo_screenwidth()/2) - (comprimento/2),
                                       self.winfo_screenheight()))

        # Eventos bind ref. formulário devem ser as últimas declarações do construtor.
        self.bind('<Escape>', self.fechar)

        self.mainloop()  # Quando mainloop é declarado no construtor, deve ser a ultima linha.

    def fechar(self, event):
        self.destroy()

    def contas(self, event):
        # Para usar este método no .bind deve-se declarar o parametro event e na invocação somente declarar seu nome.
        contas = Contas()
        FrmContas(self, contas)

    def lancamentos(self, event):
        lancamentos = Lancamentos()
        contas = Contas()
        pessoas = Pessoas()
        vw_lancamento_contas = VwLancamentosContas()
        FrmLancamentos(self, lancamentos, contas, pessoas, vw_lancamento_contas)

    def pessoas(self, event):
        pessoas = Pessoas()
        FrmPessoas(self, pessoas)


class FrmContas(tk.Toplevel):
    def __init__(self, root, contas: Contas):
        # Construtor do tk.TopLevel
        super(FrmContas, self).__init__(root)
        self.contas = contas
        # Atributo obrigatório para atribuição de registro selecionado no formulário consultas.
        self.dados_consulta = []

        self.title("Cadastro de Contas")
        self.geometry('450x200')

        # ttk.Style().theme_use('clam') # Somente deve-se declarar o tema no formulário pai.

        # Definição da área do frame
        # No FrmPrincipal não foi criado um Frame.
        frame = ttk.Frame(self)
        frame.place(x=0, y=0, width=450, height=200)

        # Declaração dos elementos do formulário.
        self.lbl_id = ttk.Label(frame, text="Código")
        self.lbl_id.place(x=10, y=10, width=100, height=20)

        self.default_id = '0'
        self.lbl_numero_id = ttk.Label(frame)
        self.lbl_numero_id.place(x=120, y=10, width=100, height=20)

        self.lbl_descricao = ttk.Label(frame, text="Descrição")
        self.lbl_descricao.place(x=10, y=40, width=150, height=20)

        self.edt_descricao = ttk.Entry(frame)
        self.edt_descricao.focus_force()
        self.edt_descricao.place(x=120, y=40, width=250, height=20)

        self.lbl_conta_pai = ttk.Label(frame, text="Conta Pai")
        self.lbl_conta_pai.place(x=10, y=70, width=100, height=20)

        self.default_conta_pai = ""
        self.cbx_conta_pai = ttk.Combobox(frame, state='readonly')
        self.cbx_conta_pai.place(x=120, y=70, width=150, height=20)

        self.default_tipo = ""
        self.lbl_tipo = ttk.Label(frame, text="Tipo")
        self.lbl_tipo.place(x=10, y=100, width=100, height=20)

        self.cbx_tipo = ttk.Combobox(frame, state='readonly')
        self.cbx_tipo.place(x=120, y=100, width=80, height=20)

        self.lbl_inclusao = ttk.Label(frame, text="Data inclusão")
        self.lbl_inclusao.place(x=10, y=130, width=100, height=20)

        self.lbl_data_inclusao = ttk.Label(frame)
        self.lbl_data_inclusao.place(x=120, y=130, width=150, height=20)

        # Limpeza e atribuição de valores default.
        self.limpar_campos()

        # Botões
        self.btn_salvar = ttk.Button(frame, text="Salvar")
        self.btn_salvar.place(x=10, y=160, width=100, height=30)

        self.btn_limpar = ttk.Button(frame, text="Limpar")
        self.btn_limpar.place(x=120, y=160, width=100, height=30)

        self.btn_excluir = ttk.Button(frame, text="Excluir")
        self.btn_excluir.place(x=230, y=160, width=100, height=30)

        self.btn_consultar = ttk.Button(frame, text="Consultar")
        self.btn_consultar.place(x=340, y=160, width=100, height=30)

        self.btn_salvar.bind('<Button-1>', self.salvar)
        self.btn_salvar.bind('<space>', self.salvar)
        self.btn_limpar.bind('<Button-1>', self.limpar)
        self.btn_limpar.bind('<space>', self.limpar)
        self.btn_excluir.bind('<Button-1>', self.excluir)
        self.btn_excluir.bind('<space>', self.excluir)
        self.btn_consultar.bind('<Button-1>', self.consultar)
        self.btn_consultar.bind('<space>', self.consultar)

        # Definição do posicionamento ref. ao form. origem e definição de form. em foco.
        self.transient(root)
        self.focus_force()
        # toplevel.grab_set()
        # self.mainloop()  # Não é necessário ter nos formulários filhos.

        # Eventos do formulário.
        self.bind('<Escape>', self.fechar)
        self.bind('<Alt-s>', self.salvar)
        self.bind('<Alt-e>', self.excluir)
        self.bind('<Alt-l>', self.limpar)
        self.bind('<Alt-c>', self.consultar)

    def fechar(self, event):
        """ Evento para fechar. """
        self.destroy()

    def salvar(self, event):
        """ Evento para salvar e modificar registros. """
        id = self.lbl_numero_id['text']
        descricao = self.edt_descricao.get()
        conta_pai = self.cbx_conta_pai.get().split(':')[0]
        conta_pai = 0 if conta_pai == self.default_conta_pai else conta_pai
        lancamento_padrao = self.cbx_tipo.get()
        lancamento_padrao = "c" if lancamento_padrao == self.default_tipo else lancamento_padrao

        if not descricao:
            showwarning("Atenção", "Descrição vazia")
        else:
            if conta_pai == 0:
                parametros = {'descricao': descricao,
                              'lancamento_padrao': lancamento_padrao}
            else:
                parametros = {'descricao': descricao,
                              'conta_pai': conta_pai,
                              'lancamento_padrao': lancamento_padrao}

            if id == self.default_id:
                self.contas.inserir(**parametros)

                showinfo("Informação", "Cadastro realizado com sucesso")

                self.limpar_campos()
            else:
                self.contas.atualizar(**parametros, filtro='id = %d' % id)

                showinfo("Informação", "Atualização realizada com sucesso")

                self.limpar_campos()

    def excluir(self, event):
        """ Evento de exclusão de registro. """
        if self.lbl_numero_id['text'] == '0':
            showinfo("Atenção", "Consulte um registro para excluir")
        elif askyesno("Atenção", "Deseja realmente excluir %s" % self.edt_descricao.get()):
            if self.contas.excluir('id = %s' % self.lbl_numero_id['text']) is None:
                showinfo("Atenção", "Exclusão não realizada:\n"
                                    "Existem lançamentos referenciando esta conta.")

            self.limpar_campos()

    def consultar(self, event):
        """ Evento de consulta usando formulário genérico de consultas. """
        FrmConsultas(self, self.contas, 'id', 'descricao', 'conta_pai', 'lancamento_padrao', 'data_inclusao',
                     id='= %s', descricao="ILIKE '%%%s%%'", lancamento_padrao="= '%s'")

    def limpar(self, event):
        """ Evento de limpeza. """
        self.limpar_campos()

    def limpar_campos(self):
        """ Método de limpeza e reatribuição de valores default. """
        self.lbl_numero_id['text'] = self.default_id

        self.edt_descricao.delete(0, 'end')

        self.contas.consultar('id', 'descricao', 'conta_pai', filtro='id <> %s' %
                                        self.lbl_numero_id['text'])
        valores = self.contas.exibir()
        self.default_conta_pai = 'Escolha'  # valores[0]  # Para atribuir o 1° valor como padrão.
        self.cbx_conta_pai['values'] = [':'.join((str(x[0]), x[1], str("" if x[2] is None else x[2])))
                                        for x in valores]
        self.cbx_conta_pai.set(self.default_conta_pai)

        self.default_tipo = 'Escolha'
        self.cbx_tipo['values'] = ('c', 'd')
        self.cbx_tipo.set(self.default_tipo)

        self.lbl_data_inclusao['text'] = "  /  /  "

    def carregar_dados(self):
        """ Método obrigatório para atribuição de registro selecionado no formulário consultas. """
        self.limpar_campos()

        self.lbl_numero_id['text'] = self.dados_consulta[0]

        self.edt_descricao.insert(0, self.dados_consulta[1])

        valores = self.contas.consultar('id', 'descricao', 'conta_pai', filtro='id <> %s' %
                                        self.lbl_numero_id['text']).fetchall()
        temp = []
        for i in valores:
            if i[0] == self.dados_consulta[2]:
                temp = i
        self.cbx_conta_pai['values'] = [':'.join((str(x[0]), x[1], str("" if x[2] is None else x[2])))
                                        for x in valores]
        self.cbx_conta_pai.set(self.default_conta_pai if self.dados_consulta[2] == 'None'
                               else ':'.join((str(temp[0]), temp[1], str("" if temp[2] is None else temp[2]))))

        self.cbx_tipo.set(self.dados_consulta[3])

        self.lbl_data_inclusao['text'] = converter_formato_data(self.dados_consulta[4])


class FrmLancamentos(tk.Toplevel):
    def __init__(self, root, lancamentos: Lancamentos, contas: Contas,
                 pessoas: Pessoas, vw_lancamento_contas: VwLancamentosContas):
        super(FrmLancamentos, self).__init__(root)
        self.lancamentos = lancamentos
        self.contas = contas
        self.pessoas = pessoas
        self.vw_lancamento_contas = vw_lancamento_contas

        self.dados_consulta = []

        self.title("Lançamento de contas")
        largura, altura = 1064, 440
        self.geometry("%dx%d" % (largura, altura))
        self.resizable(width=False, height=False)

        frame = ttk.Frame(self)
        frame.place(x=0, y=0, width=largura, height=altura)

        # Consulta base para inicializar treeview.
        self.quant_reg_consultados = 0

        self.campos_treeview = ('descricao_conta', 'nome', 'data_pagamento', 'numero', 'descricao',
                                'descricao_transferencia', 'debito', 'credito')

        self.vw_lancamento_contas.consultar(*self.campos_treeview)
        self.dados = self.vw_lancamento_contas.exibir()

        # Treeview -> "grid"
        self.dataCols = self.campos_treeview + ('saldo',)
        self.tree = ttk.Treeview(frame, columns=self.dataCols, show='headings')
        self.tree.place(x=10, y=10, width=1029, height=320)

        # Definindo largura das colunas
        for col in self.dataCols:
            self.tree.column(col, width=10)

        # Barras de rolagem
        ysb = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        xsb = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree['yscroll'] = ysb.set
        self.tree['xscroll'] = xsb.set
        ysb.place(x=1034, y=10, width=20, height=315)
        xsb.place(x=10, y=325, width=1024, height=20)

        # Define o textos do cabeçalho (nome em maiúsculas)
        # o parametro chave text modifica o nome visual da coluna.
        for c in self.dataCols:
            self.tree.heading(c, text=c.title())

        # Não é necessário alimentar a treeview nessa etapa porque é invocado
        # o método limpar após a criação dos componentes do formulário,
        # que além de "zerar" todos os compomentes, atualiza a treeview.
        # Insere cada item dos dados
        # self.alimentar_treeview()

        # Componentes para manipulação de dados
        self.id_lanc = 0
        self.id_conta = 0
        self.lanc_padrao_conta = ''
        self.cpf_pessoa = ""
        self.id_transf = 0

        self.desc_conta = "Conta origem"
        self.edt_conta = ttk.Entry(frame)
        self.edt_conta.place(x=10, y=350, width=150, height=30)
        self.edt_conta.focus_force()

        self.desc_pessoa = "Nome pessoa"
        self.edt_pessoa = ttk.Entry(frame)
        self.edt_pessoa.place(x=162, y=350, width=150, height=30)

        self.desc_dvenc = "Data vencimento"
        self.edt_data_venc = ttk.Entry(frame)
        self.edt_data_venc.place(x=314, y=350, width=90, height=30)

        self.desc_dpgto = "Data pagamento"
        self.edt_data_pgto = ttk.Entry(frame)
        self.edt_data_pgto.place(x=406, y=350, width=90, height=30)

        self.desc_numero = "Número conta"
        self.edt_numero = ttk.Entry(frame)
        self.edt_numero.place(x=498, y=350, width=100, height=30)

        self.desc_descricao = "Descrição"
        self.edt_descricao = ttk.Entry(frame)
        self.edt_descricao.place(x=600, y=350, width=150, height=30)

        self.desc_transf = "Conta destino"
        self.edt_transferencia = ttk.Entry(frame)
        self.edt_transferencia.place(x=752, y=350, width=150, height=30)

        self.desc_lanc = "Valor conta"
        self.edt_lancamento = ttk.Entry(frame)
        self.edt_lancamento.place(x=904, y=350, width=150, height=30)

        self.limpar_campos()

        # Botões
        self.btn_salvar = ttk.Button(frame, text="Salvar")
        self.btn_salvar.place(x=10, y=390, width=100, height=30)

        self.btn_limpar = ttk.Button(frame, text="Limpar")
        self.btn_limpar.place(x=120, y=390, width=100, height=30)

        self.btn_excluir = ttk.Button(frame, text="Excluir")
        self.btn_excluir.place(x=230, y=390, width=100, height=30)

        self.btn_consultar = ttk.Button(frame, text="Consultar")
        self.btn_consultar.place(x=340, y=390, width=100, height=30)

        # Eventos dos componentes
        self.edt_conta.bind('<FocusIn>', self.limpar_sob_foco_in_edt_conta)
        self.edt_conta.bind('<FocusOut>', self.preencher_descricao_foco_out_edt_conta)

        self.edt_pessoa.bind('<FocusIn>', self.limpar_sob_foco_in_edt_pessoa)
        self.edt_pessoa.bind('<FocusOut>', self.preencher_descricao_foco_out_edt_pessoa)
        self.edt_pessoa.bind('<KeyPress>', self.formatar_cpf)

        self.edt_data_venc.bind('<FocusIn>', self.limpar_sob_foco_in_edt_data_venc)
        self.edt_data_venc.bind('<FocusOut>', self.preencher_descricao_foco_out_edt_data_venc)
        self.edt_data_venc.bind('<KeyPress>', self.formatar_data_venc)

        self.edt_data_pgto.bind('<FocusIn>', self.limpar_sob_foco_in_edt_data_pgto)
        self.edt_data_pgto.bind('<FocusOut>', self.preencher_descricao_foco_out_edt_data_pgto)
        self.edt_data_pgto.bind('<KeyPress>', self.formatar_data_pgto)

        self.edt_numero.bind('<FocusIn>', self.limpar_sob_foco_in_edt_numero)
        self.edt_numero.bind('<FocusOut>', self.preencher_descricao_foco_out_edt_numero)

        self.edt_descricao.bind('<FocusIn>', self.limpar_sob_foco_in_edt_descricao)
        self.edt_descricao.bind('<FocusOut>', self.preencher_descricao_foco_out_edt_descricao)

        self.edt_transferencia.bind('<FocusIn>', self.limpar_sob_foco_in_edt_transferencia)
        self.edt_transferencia.bind('<FocusOut>', self.preencher_descricao_foco_out_edt_transferencia)

        self.edt_lancamento.bind('<FocusIn>', self.limpar_sob_foco_in_edt_lancamento)
        self.edt_lancamento.bind('<FocusOut>', self.preencher_descricao_foco_out_edt_lancamento)
        self.edt_lancamento.bind('<KeyRelease>', self.formatar_valor)

        self.btn_salvar.bind('<Button-1>', self.salvar)
        self.btn_salvar.bind('<space>', self.salvar)
        self.btn_limpar.bind('<Button-1>', self.limpar)
        self.btn_limpar.bind('<space>', self.limpar)
        self.btn_excluir.bind('<Button-1>', self.excluir)
        self.btn_excluir.bind('<space>', self.excluir)
        self.btn_consultar.bind('<Button-1>', self.consultar)
        self.btn_consultar.bind('<space>', self.consultar)

        self.transient(root)
        self.focus_force()



        # Eventos do formulário.
        self.bind('<Escape>', self.fechar)
        self.bind('<Alt-s>', self.salvar)
        self.bind('<Alt-e>', self.excluir)
        self.bind('<Alt-l>', self.limpar)
        self.bind('<Alt-c>', self.consultar)

    def alimentar_treeview(self):
        cont = 0
        saldo = 0
        for i, item in enumerate(self.dados, start=1):
            # indice[6]=débito/ativo/bens e direitos, indice[7]=crédito/passivo/obrigações:
            saldo += item[6] - item[7]
            item += (saldo,)

            cont = i
            self.tree.insert('', 'end', str(i), values=item)

        self.quant_reg_consultados = cont

    def fechar(self, event):
        self.destroy()

    def salvar(self, event):
        if self.edt_data_venc.get() == self.desc_dvenc:
            data_venc = converter_formato_data(data_atual()[1], masc_data="{2}-{1}-{0}", sep_data="/")
        else:
            data_venc = converter_formato_data(self.edt_data_venc.get(),
                                               masc_data="{2}-{1}-{0}", sep_data="/")
        if self.edt_data_pgto.get() == self.desc_dpgto:
            data_pgto = converter_formato_data(data_atual()[1], masc_data="{2}-{1}-{0}", sep_data="/")
        else:
            data_pgto = converter_formato_data(self.edt_data_pgto.get(),
                                               masc_data="{2}-{1}-{0}", sep_data="/")
        n_conta = "" if self.edt_numero.get() == self.desc_numero else self.edt_numero.get()
        descricao = format(self.edt_descricao.get())
        valor = 0 if self.edt_lancamento.get() == self.desc_lanc else float(self.edt_lancamento.get())

        if not self.cpf_pessoa:
            showwarning("Atenção", "Nome pessoa vazio")
        elif not self.id_conta:
            showwarning("Atenção", "Conta origem vazia")
        elif not self.id_transf:
            showwarning("Atenção", "Conta destino vazia")
        elif descricao == self.desc_descricao:
            showwarning("Atenção", "Descrição vazia")
        elif valor == 0:
            showwarning("Atenção", "Valor vazio")
        else:
            parametros = OrderedDict()
            parametros['id_conta'] = self.id_conta
            parametros['cpf'] = self.cpf_pessoa
            parametros['data_vencimento'] = data_venc
            parametros['data_pagamento'] = data_pgto
            parametros['numero'] = n_conta
            parametros['descricao'] = descricao
            parametros['transferencia'] = self.id_transf
            parametros['lancamento'] = valor
            parametros['padrao'] = 'TRUE'

            self.lancamentos.consultar(filtro="id = %s" % self.id_lanc)
            lanc_cadastrado = self.pessoas.exibir()

            if not lanc_cadastrado:
                bd_contas.executar("SELECT inserir_lancamento({},'{}','{}','{}','{}','{}',{},{},{})".format(
                    *parametros.values()))

                showinfo("Informação", "Cadastro realizado com sucesso")

                self.limpar_campos()
            else:
                parametros.pop('padrao')
                self.lancamentos.atualizar(**parametros, filtro="id = %s" % self.id_lanc)

                showinfo("Informação", "Atualização realizada com sucesso")

                self.limpar_campos()

    def consultar(self, event):
        consultas = FrmConsultas(self, self.vw_lancamento_contas,
                                 'id', 'id_conta', 'descricao_conta', 'cpf', 'nome', 'data_vencimento',
                                 'data_pagamento', 'numero', 'descricao', 'transferencia',
                                 'descricao_transferencia', 'debito', 'credito', 'data_inclusao',
                                 cpf="= '%s'", nome="ILIKE '%%%s%%'", descricao_conta="ILIKE '%%%s%%'",
                                 descricao="ILIKE '%%%s%%'")
        if not self.wait_window(consultas):
            self.atualizar_treeview()


    def excluir(self, event):
        if self.id_lanc == 0:
            showinfo("Atenção", "Consulte um registro para excluir")
        elif askyesno("Atenção", "Deseja realmente excluir %s" % self.edt_descricao.get()):
            self.lancamentos.excluir("id = %s" % self.id_lanc)

            self.limpar_campos()

    def limpar(self, event):
        self.limpar_campos()

    def limpar_campos(self, default=True):
        self.id_lanc = 0
        self.id_conta = 0
        self.cpf_pessoa = ""
        self.id_transf = 0

        self.edt_conta.delete(0, 'end')
        if default:
            self.edt_conta.insert(0, self.desc_conta)

        self.edt_pessoa.delete(0, 'end')
        if default:
            self.edt_pessoa.insert(0, self.desc_pessoa)

        self.edt_data_venc.delete(0, 'end')
        if default:
            self.edt_data_venc.insert(0, self.desc_dvenc)

        self.edt_data_pgto.delete(0, 'end')
        if default:
            self.edt_data_pgto.insert(0, self.desc_dpgto)

        self.edt_numero.delete(0, 'end')
        if default:
            self.edt_numero.insert(0, self.desc_numero)

        self.edt_descricao.delete(0, 'end')
        if default:
            self.edt_descricao.insert(0, self.desc_descricao)

        self.edt_transferencia.delete(0, 'end')
        if default:
            self.edt_transferencia.insert(0, self.desc_transf)

        self.edt_lancamento.delete(0, 'end')
        if default:
            self.edt_lancamento.insert(0, self.desc_lanc)

        self.atualizar_treeview()

    def carregar_dados(self):
        self.limpar_campos(default=False)

        self.id_lanc = self.dados_consulta[0]
        self.id_conta = self.dados_consulta[1]
        self.edt_conta.insert(0, self.dados_consulta[2])
        self.cpf_pessoa = self.dados_consulta[3]
        self.edt_pessoa.insert(0, self.dados_consulta[4])
        self.edt_data_venc.insert(0, self.desc_dvenc if self.dados_consulta[5] == 'None'
        else converter_formato_data(self.dados_consulta[5]))
        self.edt_data_pgto.insert(0, self.desc_dpgto if self.dados_consulta[6] == 'None'
        else converter_formato_data(self.dados_consulta[6]))
        self.edt_numero.insert(0,  self.desc_numero if self.dados_consulta[7] == 'None' else self.dados_consulta[7])
        self.edt_descricao.insert(0, self.dados_consulta[8])
        self.id_transf = self.dados_consulta[9]
        self.edt_transferencia.insert(0, self.dados_consulta[10])
        self.edt_lancamento.insert(0, float(self.dados_consulta[11]) - float(self.dados_consulta[12]))

    def limpar_sob_foco_in_edt_conta(self, event):
        if self.edt_conta.get() == self.desc_conta:
            self.edt_conta.delete(0, 'end')

    def preencher_descricao_foco_out_edt_conta(self, event):
        if self.edt_conta.get() == "":
            self.edt_conta.insert(0, self.desc_conta)
            self.id_conta = 0
        else:
            self.pesquisar_atribuir_conta_origem()

        self.atualizar_treeview()

    def limpar_sob_foco_in_edt_pessoa(self, event):
        if self.edt_pessoa.get() == self.desc_pessoa:
            self.edt_pessoa.delete(0, 'end')

    def preencher_descricao_foco_out_edt_pessoa(self, event):
        if self.edt_pessoa.get() == "":
            self.edt_pessoa.insert(0, self.desc_pessoa)
            self.cpf_pessoa = ""
        else:
            self.pesquisar_atribuir_pessoa()

        self.atualizar_treeview()

    def limpar_sob_foco_in_edt_data_venc(self, event):
        if self.edt_data_venc.get() == self.desc_dvenc:
            self.edt_data_venc.delete(0, 'end')

    def preencher_descricao_foco_out_edt_data_venc(self, event):
        if self.edt_data_venc.get() == "":
            self.edt_data_venc.insert(0, self.desc_dvenc)
        elif self.edt_data_venc.get().lower() == "hoje":
            self.edt_data_venc.delete(0, 'end')
            self.edt_data_venc.insert(0, data_atual(False)[1])

    def limpar_sob_foco_in_edt_data_pgto(self, event):
        if self.edt_data_pgto.get() == self.desc_dpgto:
            self.edt_data_pgto.delete(0, 'end')

    def preencher_descricao_foco_out_edt_data_pgto(self, event):
        if self.edt_data_pgto.get() == "":
            self.edt_data_pgto.insert(0, self.desc_dpgto)
        elif self.edt_data_pgto.get().lower() == "hoje":
            self.edt_data_pgto.delete(0, 'end')
            self.edt_data_pgto.insert(0, data_atual()[1])

    def limpar_sob_foco_in_edt_numero(self, event):
        if self.edt_numero.get() == self.desc_numero:
            self.edt_numero.delete(0, 'end')

    def preencher_descricao_foco_out_edt_numero(self, event):
        if self.edt_numero.get() == "":
            self.edt_numero.insert(0, self.desc_numero)

    def limpar_sob_foco_in_edt_descricao(self, event):
        if self.edt_descricao.get() == self.desc_descricao:
            self.edt_descricao.delete(0, 'end')

    def preencher_descricao_foco_out_edt_descricao(self, event):
        if self.edt_descricao.get() == "":
            self.edt_descricao.insert(0, self.desc_descricao)

    def limpar_sob_foco_in_edt_transferencia(self, event):
        if self.edt_transferencia.get() == self.desc_transf:
            self.edt_transferencia.delete(0, 'end')

    def preencher_descricao_foco_out_edt_transferencia(self, event):
        if self.edt_transferencia.get() == "":
            self.edt_transferencia.insert(0, self.desc_transf)
            self.id_transf = 0
        else:
            self.pesquisar_atribuir_conta_destino()

    def limpar_sob_foco_in_edt_lancamento(self, event):
        if self.edt_lancamento.get() == self.desc_lanc:
            self.edt_lancamento.delete(0, 'end')

    def preencher_descricao_foco_out_edt_lancamento(self, event):
        if self.edt_lancamento.get() == "":
            self.edt_lancamento.insert(0, self.desc_lanc)

    def pesquisar_atribuir_conta_origem(self):
        if self.edt_conta.get() != self.desc_conta:
            dado = self.pesquisar(self.contas, 'id', 'descricao', 'lancamento_padrao',
                                  filtro="descricao ILIKE '%%%s%%'" % self.edt_conta.get(),
                                  quantidade=(1,))
            if dado:
                self.id_conta = int(dado[0][0])
                self.edt_conta.delete(0, 'end')
                self.edt_conta.insert(0, dado[0][1])
                self.lanc_padrao_conta = dado[0][2]
            else:
                self.id_conta = 0
                self.lanc_padrao_conta = ''

                if askyesno("Atenção", "Deseja cadastrar a conta %s" % self.edt_conta.get()):
                    contas = FrmContas(self, self.contas)
                    contas.edt_descricao.insert(0, self.edt_conta.get())

                    # Se não fechar o form. FrmContas
                    if not self.wait_window(contas):
                        self.pesquisar_atribuir_conta_origem()
                else:
                    self.edt_conta.delete(0, 'end')
                    self.edt_conta.insert(0, self.desc_conta)

    def atualizar_treeview(self):
        for i in range(1, self.quant_reg_consultados + 1):
            self.tree.delete(str(i))

        if self.id_conta != 0 and self.cpf_pessoa != "":
            self.vw_lancamento_contas.consultar(*self.campos_treeview,
                                                filtro="id_conta = %s AND cpf = '%s'" % (self.id_conta, self.cpf_pessoa))
        else:
            self.vw_lancamento_contas.consultar(*self.campos_treeview)

        self.dados = self.vw_lancamento_contas.exibir()

        self.alimentar_treeview()

    def formatar_cpf(self, event):
        if event.char in string.digits:
            FrmPessoas.escrever_mascara_entry(event.char, self.edt_pessoa, '   .   .   -  ')

    def formatar_data_pgto(self, event):
        if event.char in string.digits:
            FrmPessoas.escrever_mascara_entry(event.char, self.edt_data_pgto, '  /  /    ')

    def formatar_data_venc(self, event):
        if event.char in string.digits:
            FrmPessoas.escrever_mascara_entry(event.char, self.edt_data_venc, '  /  /    ')

    def formatar_valor(self, event):
        FrmPessoas.apagar_caracter_invalido(event.char, self.edt_lancamento,
                                            (string.ascii_letters +
                                             string.punctuation.replace('.', '').replace(',', '').replace('-', '') +
                                             ' '))
        if event.char == ',':
            self.edt_lancamento.delete(len(self.edt_lancamento.get()) - 1, 'end')
            self.edt_lancamento.insert('end', '.')

    def pesquisar_atribuir_pessoa(self):
        if self.edt_pessoa.get() != self.desc_pessoa:
            dado = self.pesquisar(self.pessoas, 'cpf', 'nome',
                                  filtro="cpf ILIKE '%%%s%%' OR nome ILIKE '%%%s%%'" %
                                         (self.edt_pessoa.get(), self.edt_pessoa.get()),
                                  quantidade=(1,))
            if dado:
                self.cpf_pessoa = dado[0][0]
                self.edt_pessoa.delete(0, 'end')
                self.edt_pessoa.insert(0, dado[0][1])
            else:
                self.cpf_pessoa = ""

                if askyesno("Atenção", "Deseja cadastrar a pessoa %s" % self.edt_pessoa.get()):
                    pessoas = FrmPessoas(self, self.pessoas)
                    if self.edt_pessoa.get()[0] in string.digits:
                        pessoas.edt_cpf.delete(0, 'end')
                        pessoas.edt_cpf.insert(0, self.edt_pessoa.get())
                    else:
                        pessoas.edt_nome.insert(0, self.edt_pessoa.get())

                    # Se não fechar o form. FrmContas
                    if not self.wait_window(pessoas):
                        self.pesquisar_atribuir_pessoa()
                else:
                    self.edt_pessoa.delete(0, 'end')
                    self.edt_pessoa.insert(0, self.desc_pessoa)

    def pesquisar_atribuir_conta_destino(self):
        if self.edt_transferencia.get() != self.desc_transf:
            dado = self.pesquisar(self.contas, 'id', 'descricao',
                                  filtro="descricao ILIKE '%%%s%%' and id <> '%s'" %
                                         (self.edt_transferencia.get(), self.id_conta),
                                  quantidade=(1,))
            # print(bd_contas.dml)
            if dado:
                if self.id_conta == int(dado[0][0]):
                    showinfo("Atenção", "Conta %s já está sendo usada como conta origem" % self.edt_conta.get())
                    self.edt_transferencia.delete(0, 'end')
                    self.edt_transferencia.insert(0, self.desc_transf)
                else:
                    self.id_transf = int(dado[0][0])
                    self.edt_transferencia.delete(0, 'end')
                    self.edt_transferencia.insert(0, dado[0][1])
            else:
                self.id_transf = 0

                if askyesno("Atenção", "Deseja cadastrar a conta %s" % self.edt_transferencia.get()):
                    contas = FrmContas(self, self.contas)
                    contas.edt_descricao.insert(0, self.edt_conta.get())

                    # Se não fechar o form. FrmContas
                    if not self.wait_window(contas):
                        self.pesquisar_atribuir_conta_destino()
                else:
                    self.edt_transferencia.delete(0, 'end')
                    self.edt_transferencia.insert(0, self.desc_transf)

    def pesquisar(self, tabela: Tabela, *campos, **kfiltro) -> str:
        tabela.consultar(*campos, **kfiltro)
        return tabela.exibir()


class FrmPessoas(tk.Toplevel):
    def __init__(self, root, pessoas: Pessoas):
        super(FrmPessoas, self).__init__(root)
        self.pessoas = pessoas

        self.dados_consulta = []

        self.title("Cadastro de Pessoas")
        largura, altura = 450, 170
        self.geometry("%dx%d" % (largura, altura))
        self.resizable(width=False, height=False)

        frame = ttk.Frame(self)
        frame.place(x=0, y=0, width=largura, height=altura)

        # Componentes do formulário.
        self.lbl_cpf = ttk.Label(frame, text="CPF")
        self.lbl_cpf.place(x=10, y=10, width=100, height=20)

        self.default_cpf = "   .   .   -  "
        self.edt_cpf = ttk.Entry(frame)
        self.edt_cpf.focus_force()
        self.edt_cpf.place(x=120, y=10, width=150, height=20)
        self.edt_cpf.bind('<KeyPress>', self.escrever_cpf)
        self.edt_cpf.bind('<KeyRelease>', self.escrever_cpf_release)

        self.lbl_rg = ttk.Label(frame, text="RG")
        self.lbl_rg.place(x=10, y=40, width=100, height=20)

        self.default_rg = "  .   .   - "
        self.edt_rg = ttk.Entry(frame)
        self.edt_rg.place(x=120, y=40, width=150, height=20)
        self.edt_rg.bind('<KeyPress>', self.escrever_rg)
        self.edt_rg.bind('<KeyRelease>', self.escrever_rg_release)

        self.lbl_nome = ttk.Label(frame, text="Nome")
        self.lbl_nome.place(x=10, y=70, width=100, height=20)

        self.edt_nome = ttk.Entry(frame)
        self.edt_nome.place(x=120, y=70, width=250, height=20)

        self.lbl_inclusao = ttk.Label(frame, text="Data inclusão")
        self.lbl_inclusao.place(x=10, y=100, width=100, height=20)

        self.default_data = "  /  /    "
        self.lbl_data_inclusao = ttk.Label(frame)
        self.lbl_data_inclusao.place(x=120, y=100, width=150, height=20)

        # Limpar e atribuição de valores default.
        self.limpar_campos()

        # Botões
        self.btn_salvar = ttk.Button(frame, text="Salvar")
        self.btn_salvar.place(x=10, y=130, width=100, height=30)

        self.btn_limpar = ttk.Button(frame, text="Limpar")
        self.btn_limpar.place(x=120, y=130, width=100, height=30)

        self.btn_excluir = ttk.Button(frame, text="Excluir")
        self.btn_excluir.place(x=230, y=130, width=100, height=30)

        self.btn_consultar = ttk.Button(frame, text="Consultar")
        self.btn_consultar.place(x=340, y=130, width=100, height=30)

        self.btn_salvar.bind('<Button-1>', self.salvar)
        self.btn_salvar.bind('<space>', self.salvar)
        self.btn_limpar.bind('<Button-1>', self.limpar)
        self.btn_limpar.bind('<space>', self.limpar)
        self.btn_excluir.bind('<Button-1>', self.excluir)
        self.btn_excluir.bind('<space>', self.excluir)
        self.btn_consultar.bind('<Button-1>', self.consultar)
        self.btn_consultar.bind('<space>', self.consultar)

        self.transient(root)
        self.focus_force()

        # Eventos do formulário.
        self.bind('<Escape>', self.fechar)
        self.bind('<Alt-s>', self.salvar)
        self.bind('<Alt-e>', self.excluir)
        self.bind('<Alt-l>', self.limpar)
        self.bind('<Alt-c>', self.consultar)

    def escrever_cpf(self, event):
        # report_event(event)
        self.escrever_mascara_entry(event.char, self.edt_cpf, self.default_cpf)

    @staticmethod
    def escrever_mascara_entry(evento_char, ref_entry: ttk.Entry, mascara: str, especial: str = ''):
        """ Método estático para formatar a entrada de um Entry de acordo com mascara.
        Pode ser usado sem instanciação.
        :param evento_char: event.char do evento.
        :param ref_entry: Referência do componente Entry.
        :param mascara: Mascara base para a formatação. Deve apresentar espacos onde quer ser inseridos os números.
        :return: none. """
        # Apaga o Entry caso o conteúdo seja o default.
        if ref_entry.get() == mascara:
            ref_entry.delete(0, 'end')

        # O event.char captura de tecla literalmente, mas não captura teclas de controle(Backspace, ...).
        # O event.keysym usa uma nomenclatura diferente, e captura todas as teclas.
        # Tkinter 8.5 reference gui for Python. 161-162.
        if evento_char in string.digits or evento_char in especial:
            pos = len(ref_entry.get())
            try:
                if mascara[pos] != ' ':
                    ref_entry.insert('end', mascara[pos])
            except IndexError:
                ref_entry.delete(0, 'end')

    def escrever_cpf_release(self, event):
        # report_event(event)
        self.apagar_caracter_invalido(event.char, self.edt_cpf, string.ascii_letters)

    @staticmethod
    def apagar_caracter_invalido(evento_char, ref_entry: ttk.Entry, caracteres_inválidos: str):
        """ Método estático para apagar os caracteres inseridos em um Entry no momento da digitação(evento Release).
        Pode ser usado sem instanciação.
        :param evento_char: event.char do evento.
        :param ref_entry: Referência do componente Entry.
        :param caracteres_inválidos: string de caracteres que deseja-se que sejam apagados.
        :return: none. """
        if evento_char in caracteres_inválidos:
            ref_entry.delete(len(ref_entry.get()) - 1, 'end')

    def escrever_rg(self, event):
        self.escrever_mascara_entry(event.char, self.edt_rg, self.default_rg, especial='xX')

    def escrever_rg_release(self, event):
        letras = string.ascii_letters.replace('X', '').replace('x', '')
        self.apagar_caracter_invalido(event.char, self.edt_rg, letras)

    def carregar_dados(self):
        self.limpar_campos(default=False)

        self.edt_cpf.insert(0, self.dados_consulta[0])
        self.edt_rg.insert(0, self.default_rg if self.dados_consulta[1] == 'None' else self.dados_consulta[1])
        self.edt_nome.insert(0, self.dados_consulta[2])
        self.lbl_data_inclusao['text'] = converter_formato_data(self.dados_consulta[3])

    def fechar(self, event):
        self.destroy()

    def salvar(self, event):
        """ Evento para salvar e modificar registros. """
        cpf = "" if self.edt_cpf.get() == self.default_cpf else self.edt_cpf.get()
        if self.edt_rg.get() == self.default_rg or self.edt_rg.get() == "":
            rg = "NULL"
        else:
            rg = self.edt_rg.get()
        nome = self.edt_nome.get()

        if not nome:
            showwarning("Atenção", "Nome vazio")
        elif not cpf:
            showwarning("Atenção", "CPF vazio")
        elif not Cpf(cpf):
            showwarning("Atenção", "CPF inválido")
        else:
            parametros = {'cpf': cpf,
                          'rg': rg,
                          'nome': nome}

            self.pessoas.consultar(filtro="cpf = '%s'" % cpf)
            cpf_cadastrado = self.pessoas.exibir()

            if not cpf_cadastrado:
                self.pessoas.inserir(**parametros)

                showinfo("Informação", "Cadastro realizado com sucesso")

                self.limpar_campos()
            else:
                self.pessoas.atualizar(**parametros, filtro="cpf = '%s'" % cpf)

                showinfo("Informação", "Atualização realizada com sucesso")

                self.limpar_campos()

    def limpar(self, event):
        self.limpar_campos()

    def limpar_campos(self, default=True):
        self.edt_cpf.delete(0, 'end')
        if default:
            self.edt_cpf.insert(0, self.default_cpf)

        self.edt_rg.delete(0, 'end')
        if default:
            self.edt_rg.insert(0, self.default_rg)

        self.edt_nome.delete(0, 'end')
        self.edt_nome.insert(0, "")

        self.lbl_data_inclusao['text'] = self.default_data

    def excluir(self, event):
        cpf = self.edt_cpf.get()
        if cpf == '' or cpf == self.default_cpf:
            showinfo("Atenção", "Consulte um registro para excluir")
        elif askyesno("Atenção", "Deseja realmente excluir %s" % self.edt_nome.get()):
            if self.pessoas.excluir("cpf = '%s'" % cpf) is None:
                showinfo("Atenção", "Exclusão não realizada:\n"
                                    "Existem lançamentos referenciando esta pessoa")
            self.limpar_campos()

    def consultar(self, event):
        FrmConsultas(self, self.pessoas, 'cpf', 'rg', 'nome', 'data_inclusao',
                     cpf="= '%s'", nome="ILIKE '%%%s%%'", rg="= '%s'")


class FrmConsultas(tk.Toplevel):
    """ Formulário genérico para consultas. """
    def __init__(self, root, origem: Tabela, *campos, **kfiltro):
        # FrmConsultas(self, self.contas, 'id', 'descricao', 'conta_pai', 'lancamento_padrao', 'data_inclusao',
        #             id='= %s', descricao="ILIKE '%%%s%%'", lancamento_padrao="= '%s'")
        """ Construtor.
        Elaboração da TreeView baseado em <http://pt.stackoverflow.com/questions/23053/ajuda-tables-python27>
        :param root: Formulário pai.
        :param origem: Tabela que se deseja consultar.
        :param campos: Campos em forma de valores de parametros que serão exibidos na TreeView.
        :param kfiltro: Filtros que serão empregados na consulta.
        Obs: Deve-se declarar no formulário pai: um atributo self.dados_consulta = [] e
        um método self.carregar_dados(self): ..., que tem que atribuir os componentes do formulario pai
        os mesmos valores informados no parametro campos do contrutor de FrmConsultas(). """
        # Construtor do TopLevel
        super(FrmConsultas, self).__init__(root)
        self.frm_original = root
        self.campos = campos
        self.kfiltro = kfiltro
        self.quant_reg_consultados = 0

        self.title("Consulta")
        self.geometry('640x370')
        self.resizable(width=False, height=False)

        frame = ttk.Frame(self)
        frame.place(x=0, y=0, width=640, height=370)

        # Consulta base para inicializar.
        self.consulta = origem
        self.consulta.consultar(*self.campos) if campos else self.consulta.consultar()
        self.dados = self.consulta.exibir()

        # Elementos do formulário.
        self.edt_pesquisa = ttk.Entry(frame)
        self.edt_pesquisa.place(x=10, y=10, width=400, height=30)

        self.cbx_filtro = ttk.Combobox(frame, state='readonly')
        self.cbx_filtro.place(x=420, y=10, width=100, height=30)
        self.cbx_filtro['values'] = [x for x in self.kfiltro.keys()]  # self.consulta.campos
        self.default_filtro = 'Escolha'
        self.cbx_filtro.set(self.default_filtro)

        self.btn_pesquisar = ttk.Button(frame, text='Pesquisar')
        self.btn_pesquisar.place(x=530, y=10, width=100, height=30)

        # treeview -> "grid"
        self.dataCols = self.consulta.campos
        self.tree = ttk.Treeview(frame, columns=self.dataCols, show='headings')
        self.tree.place(x=10, y=50, width=600, height=300)

        # Barras de rolagem
        ysb = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        xsb = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree['yscroll'] = ysb.set
        self.tree['xscroll'] = xsb.set
        ysb.place(x=610, y=50, width=20, height=290)
        xsb.place(x=10, y=340, width=600, height=20)

        # Define o textos do cabeçalho (nome em maiúsculas)
        for c in self.dataCols:
            self.tree.heading(c, text=c.title())

        # Insere cada item dos dados
        self.alimentar_treeview()

        self.edt_pesquisa.bind('<Return>', self.pesquisar)
        self.tree.bind('<Double-1>', self.carregar_dados)
        self.btn_pesquisar.bind('<Button-1>', self.pesquisar)
        self.btn_pesquisar.bind('<space>', self.pesquisar)

        self.transient(root)
        self.focus_force()

        # Eventos do formulário.
        self.bind('<Escape>', self.fechar)

    def fechar(self, event):
        self.destroy()

    def carregar_dados(self, event):
        """ Função para carregar os dados qualificados para o formulário original.
        O formulário original deve conter um atributo self.dados_consulta, para armazenar o registro selecionado e
        um método self.carregar_dados(), para carregar os elementos os dados contidos no atributo self.dados_consulta.
        :param event: Parametro de captura de evento.
        :return: None. """
        item = self.tree.selection()[0]
        self.frm_original.dados_consulta = self.tree.item(item)['values']
        self.frm_original.carregar_dados()
        self.destroy()

    def alimentar_treeview(self):
        cont = 0
        for i, item in enumerate(self.dados, start=1):
            cont = i
            self.tree.insert('', 'end', str(i), values=item)
        self.quant_reg_consultados = cont

    def pesquisar(self, event):
        if self.cbx_filtro.get() != self.default_filtro:
            filtro = self.kfiltro[self.cbx_filtro.get()]
            self.consulta.consultar(*self.campos,
                                    filtro="%s %s" % (self.cbx_filtro.get(),
                                                      filtro % (self.edt_pesquisa.get().lower())))
            self.dados = self.consulta.exibir()

            # Limpeza do TreeView.
            for i in range(1, self.quant_reg_consultados + 1):
                self.tree.delete(str(i))

            self.alimentar_treeview()

        print(report_event(event), bd_contas.dml, sep="\n")


def principal():
    FrmPrincipal()

if __name__ == '__main__':
    principal()
