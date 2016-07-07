#!/usr/bin/python3
# coding: utf-8
# Desenvolvido em Python 3.5 e PostgreSQL 9.5.
# Usando o módulo conexaoDB(presente no pacote sources) para acesso ao banco.
# DER(model MySQL-Workbench) e SQL dos elementos do banco de dados em anexo na pasta arquivos contas.

try:
    from conexaoDB import Conexao, Tabela
    from funcoes_uteis import report_event, converter_formato_data
except ImportError:
    from sources.conexaoDB import Conexao, Tabela
    from sources.funcoes_uteis import report_event, converter_formato_data

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showwarning, askyesno

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
        report_event(event)
        showinfo("teste", "criar cadastro lancamentos")

    def pessoas(self, event):
        showinfo("teste", "criar cadastro pessoas")


class FrmContas(tk.Toplevel):
    def __init__(self, root, contas: Contas):
        # Construtor do tk.TopLevel
        super(FrmContas, self).__init__(root)
        self.contas = contas
        # Atributo obrigatório para atribuição de registro selecionado no formulário consultas.
        self.dados_consulta = []

        self.title("Cadastro de contas")
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
        self.edt_descricao.place(x=120, y=40, width=150, height=20)

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
        self.btn_salvar.bind('<Button-1>', self.salvar)
        self.btn_salvar.place(x=10, y=160, width=100, height=30)

        self.btn_limpar = ttk.Button(frame, text="Limpar")
        self.btn_limpar.place(x=120, y=160, width=100, height=30)
        self.btn_limpar.bind('<Button-1>', self.limpar)

        self.btn_excluir = ttk.Button(frame, text="Excluir")
        self.btn_excluir.bind('<Button-1>', self.excluir)
        self.btn_excluir.place(x=230, y=160, width=100, height=30)

        self.btn_consultar = ttk.Button(frame, text="Consultar")
        self.btn_consultar.bind('<Button-1>', self.consultar)
        self.btn_consultar.place(x=340, y=160, width=100, height=30)

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
            self.contas.excluir('id = %s' % self.lbl_numero_id['text'])

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

        valores = self.contas.consultar('id', 'descricao', 'conta_pai', filtro='id <> %s' %
                                        self.lbl_numero_id['text']).fetchall()
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


class FrmLancamentos:
    # A implementar.
    pass


class FrmPessoas:
    # A implementar.
    pass


class FrmConsultas(tk.Toplevel):
    """ Formulário genérico para consultas. """
    def __init__(self, root, origem: Tabela, *campos, **kfiltro):
        """ Construtor.
        Elaboração da TreeView baseado em <http://pt.stackoverflow.com/questions/23053/ajuda-tables-python27>
        :param root: Formulário pai.
        :param origem: Tabela que se deseja consultar.
        :param campos: Campos em forma de valores de parametros que serão exibidos na TreeView."""
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
        self.edt_pesquisa.bind('<Return>', self.pesquisar)

        self.cbx_filtro = ttk.Combobox(frame, state='readonly')
        self.cbx_filtro.place(x=420, y=10, width=100, height=30)
        self.cbx_filtro['values'] = [x for x in self.kfiltro.keys()]  # self.consulta.campos
        self.default_filtro = 'Escolha'
        self.cbx_filtro.set(self.default_filtro)

        self.btn_pesquisar = ttk.Button(frame, text='Pesquisar')
        self.btn_pesquisar.place(x=530, y=10, width=100, height=30)
        self.btn_pesquisar.bind('<Button-1>', self.pesquisar)

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

        self.transient(root)
        self.focus_force()

        # Eventos do formulário.
        self.bind('<Double-1>', self.carregar_dados)
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
