

import tkinter as tk
from tkinter import ttk
import crud as crud


class PrincipalBD:
    def __init__(self, win):
        self.objBD = crud.AppBD()
        # componentes
        self.lbCodigo = tk.Label(win, text='Código do Produto:')
        self.lblNome = tk.Label(win, text='Nome do Produto')
        self.lblPreco = tk.Label(win, text='Preço')
        self.lblPrecoVenda = tk.Label(win, text='Preço de Venda')

        self.txtCodigo = tk.Entry(bd=3)
        self.txtNome = tk.Entry()
        self.txtPreco = tk.Entry()
        self.txtPrecoVenda = tk.Entry()
        self.btnCadastrar = tk.Button(win, text='Cadastrar', command=self.fCadastrarProduto)
        self.btnAtualizar = tk.Button(win, text='Atualizar', command=self.fAtualizarProduto)
        self.btnExcluir = tk.Button(win, text='Excluir', command=self.fExcluirProduto)
        self.btnLimpar = tk.Button(win, text='Limpar', command=self.fLimparTela)

        # sistema de vendas
        # componente treeview
        self.dadosColunas = ("Código", "Nome", "Preço", "Preço de Venda")

        self.treeProdutos = ttk.Treeview(win,
                                         columns=self.dadosColunas,
                                         selectmode='browse')

        self.verscrlbar = ttk.Scrollbar(win,
                                        orient="vertical",
                                        command=self.treeProdutos.yview)
        self.verscrlbar.pack(side='left', fill='x')

        self.treeProdutos.configure(yscrollcommand=self.verscrlbar.set)

        self.treeProdutos.heading("Código", text="Código")
        self.treeProdutos.heading("Nome", text="Nome")
        self.treeProdutos.heading("Preço", text="Preço")
        self.treeProdutos.heading("Preço de Venda", text="Preço de Venda")

        self.treeProdutos.column("Código", minwidth=0, width=100)
        self.treeProdutos.column("Nome", minwidth=0, width=100)
        self.treeProdutos.column("Preço", minwidth=0, width=100)
        self.treeProdutos.column("Preço de Venda", minwidth=0, width=100)

        self.treeProdutos.pack(padx=10, pady=10)

        self.treeProdutos.bind("<<TreeviewSelect>>",
                               self.apresentarRegistrosSelecionados)

        # layout dos elementos da tela

        self.lbCodigo.place(x=100, y=50)
        self.txtCodigo.place(x=250, y=50)

        self.lblNome.place(x=100, y=100)
        self.txtNome.place(x=250, y=100)

        self.lblPreco.place(x=100, y=150)
        self.txtPreco.place(x=250, y=150)

        self.btnCadastrar.place(x=100, y=200)
        self.btnAtualizar.place(x=200, y=200)
        self.btnExcluir.place(x=300, y=200)
        self.btnLimpar.place(x=400, y=200)

        self.treeProdutos.place(x=100, y=300)
        self.verscrlbar.place(x=700, y=300, height=225)
        self.carregarDadosIniciais()


    def apresentarRegistrosSelecionados(self, event):
        self.fLimparTela()
        for selection in self.treeProdutos.selection():
            item = self.treeProdutos.item(selection)
            codigo, nome, preco = item["values"][0:3]
            self.txtCodigo.insert(0, codigo)
            self.txtNome.insert(0, nome)
            self.txtPreco.insert(0, preco)
            self.txtPrecoVenda.insert(0, preco)

    def carregarDadosIniciais(self):
        try:
            self.id = 0
            self.iid = 0
            registros = self.objBD.selecionarDados
            print("dados dsponíveis")
            for item in registros:
                codigo = item[0]
                nome = item[1]
                preco = item[2]
                precovenda = item[3]
                print("Códig0 = ", codigo)
                print("Nome = ", nome)
                print("Preço  = ", preco)
                print("Preço de Venda  = ", precovenda, "\n")

                self.treeProdutos.insert('', 'end',
                                         iid=self.iid,
                                         values=(codigo,
                                                 nome,
                                                 preco,
                                                 precovenda))

                self.iid = self.iid + 1
                self.id = self.id + 1
            print('Dados da base')
        except:
            print('Ainda não existem dados para carregar')

    #ler dados de saída
    def fLerCampos(self):
        try:
            print("dados disponíveis")
            codigo = int(self.txtCodigo.get())
            print('codigo', codigo)
            nome = self.txtNome.get()
            print('nome', nome)
            preco = float(self.txtPreco.get())
            print('preco', preco)
            # precovenda = float(self.txtPrecoVenda.get())
            # print('preco', precovenda)
            calcprecovenda = preco+preco*0.1
            print('A leitura dos foi realizada')
        except:
            print('Não foi possível ler os dados.')
        return codigo, nome, preco, calcprecovenda

    # cadastro do prod
    def fCadastrarProduto(self):
        try:
            print("dados disponíveis")
            codigo, nome, preco, precovenda = self.fLerCampos()
            self.objBD.inserirDados(codigo, nome, preco, precovenda)
            self.treeProdutos.insert('', 'end',
                                     iid=self.iid,
                                     values=(codigo,
                                             nome,
                                             preco,
                                             precovenda))
            self.iid = self.iid + 1
            self.id = self.id + 1
            self.fLimparTela()
            print('Produto cadastrado com sucesso.')
        except:
            print('Não foi possível realizar o cadastro.')

    # atualizar prod
    def fAtualizarProduto(self):
        try:
            print("dados disponíveis")
            codigo, nome, preco, precovenda = self.fLerCampos()
            self.objBD.atualizarDados(codigo, nome, preco, precovenda)
            self.treeProdutos.delete(*self.treeProdutos.get_children())
            self.carregarDadosIniciais()
            self.fLimparTela()
            print('Produto atualizado com sucesso.')
        except:
            print('Não foi possível realizar a atualização.')

    # excluir prod
    def fExcluirProduto(self):
        try:
            print("dados disponíveis")
            codigo, nome, preco, precovenda = self.fLerCampos()
            self.objBD.excluirDados(codigo)
            self.treeProdutos.delete(*self.treeProdutos.get_children())
            self.carregarDadosIniciais()
            self.fLimparTela()
            print('Produto excluído com sucesso.')
        except:
            print('Não foi possível realizar a exclusão do produto.')

    # limpar
    def fLimparTela(self):
        try:
            print("dados disponíveis")
            self.txtCodigo.delete(0, tk.END)
            self.txtNome.delete(0, tk.END)
            self.txtPreco.delete(0, tk.END)
            print('Os campos foram limpos!')
        except:
            print('Não foi possível limpar os campos.')

# main program
janela = tk.Tk()
principal = PrincipalBD(janela)
janela.title('Suffered Baby')
janela.geometry("820x600+10+10")
janela.mainloop()
