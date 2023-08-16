import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, Frame, messagebox, ttk, PhotoImage, StringVar, Scrollbar
import customtkinter as ctk
from datetime import datetime
from tkinter import simpledialog
import os
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.platypus import Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import sqlite3


# teclas_de_atalho.py
class TeclasDeAtalho:
    def __init__(self, janela, tela_usuario):
        self.janela = janela
        self.tela_usuario = tela_usuario
        # Associa as teclas de função às funções correspondentes
        self.janela.bind("<F1>", self.acao_f1)
        self.janela.bind("<F2>", self.acao_f2)
        self.janela.bind("<F5>", self.acao_f5)
        self.janela.bind("<F6>", self.acao_f6)
        self.janela.bind("<Delete>", self.acao_del)
        self.treeview_relatorio = None
        self.frame_filtros = None
        self.frame_treeview = None
        self.title_text = ""

    def acao_f1(self, event):
        # Implemente aqui a ação desejada para a tecla F1
        self.abrir_janela_pesquisa()

    def acao_f2(self, event):
        # Implemente aqui a ação desejada para a tecla F3
        self.realizar_pagamento()

    def acao_f5(self, event):
        # Implemente aqui a ação desejada para a tecla F5
        self.abrir_janela_cadastro_produtos()

    def acao_f6(self, event):
        self.relatorio_venda()

    def acao_del(self, event):
        # Implemente aqui a ação desejada para a tecla F2
        self.remover_produto_selecionado()

    def abrir_janela_pesquisa(self):
        self.executar_funcao_pesquisar()

    # CONSULTAR PRODUTOS CADASTRADOS, SELECIONAR O PRODUTO PARA VENDA. AÇÃO DO F1
    @classmethod
    def consultar_produtos(cls):
        conn = sqlite3.connect("SistemaPDV.db")
        cursor = conn.cursor()
        # Fazer a consulta para obter todos os produtos
        cursor.execute("SELECT codigo_interno, descricao, estoque, preco_venda FROM produtos")
        produtos = cursor.fetchall()
        conn.close()
        return produtos

    def executar_funcao_pesquisar(self):
        # Criar o TopLevel usando a instância da janela principal
        self.top_pesquisar = Toplevel(self.janela)
        self.top_pesquisar.title("Produtos")

        # Adicionar um frame ao TopLevel para conter os campos desejados
        frame_pesquisar = Frame(self.top_pesquisar, bg="white")
        frame_pesquisar.pack(padx=10, pady=10)

        # Adicionar os campos, botões e Treeview ao frame_quantidade
        label_pesquisar = Label(frame_pesquisar, text="Pesquisar produto", font="Roboto 14", anchor="center",
                                background="white")
        label_pesquisar.grid(row=0, column=0, sticky="nsew", padx=20)

        # Criar um botão para adicionar o código do produto no entry da TelaUsuario
        btn_adicionar = Button(frame_pesquisar, text="Adicionar", font="Roboto 12", height=2, fg="white",
                               background="blue", command=self.adicionar_codigo_produto)
        btn_adicionar.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # Criar uma Treeview para exibir os produtos do banco de dados
        # Criar uma Treeview para exibir os produtos do banco de dados
        self.treeview_produtos = ttk.Treeview(frame_pesquisar, height=10,
                                              columns=("cod_produto", "descricao", "quantidade", "vlr_unitario"),
                                              show="headings")
        self.treeview_produtos.heading("cod_produto", text="Cód. Produto")
        self.treeview_produtos.heading("descricao", text="Descrição")
        self.treeview_produtos.heading("quantidade", text="Qtdade.")
        self.treeview_produtos.heading("vlr_unitario", text="Vlr. Unitário")

        self.treeview_produtos.column("cod_produto", width=100, anchor="center", stretch=False)
        self.treeview_produtos.column("descricao", width=230, anchor="w", stretch=False)
        self.treeview_produtos.column("quantidade", width=100, anchor="center", stretch=False)
        self.treeview_produtos.column("vlr_unitario", width=100, anchor="center", stretch=False)
        self.treeview_produtos.grid(row=2, column=0, padx=20, pady=10)

        # Preencher a Treeview com os produtos do banco de dados
        produtos = TeclasDeAtalho.consultar_produtos()
        for produto in produtos:
            self.treeview_produtos.insert("", "end", values=(produto))

        # Adicionar eventos de seleção na Treeview para capturar o código do produto
        self.treeview_produtos.bind("<Double-1>", self.selecionar_produto)

        # Centralizar a janela no centro da tela
        self.centralizar_janela(self.top_pesquisar)

    def centralizar_janela(self, window):
        # Atualiza o layout da janela para garantir dimensões corretas
        window.update_idletasks()

        # Obtém a largura e a altura da janela
        window_width = window.winfo_width()
        window_height = window.winfo_height()

        # Obtém a largura e a altura da tela
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Calcula as coordenadas x e y para centralizar a janela
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Define a posição da janela no centro da tela
        window.geometry("+{}+{}".format(x, y))

    def selecionar_produto(self, event):
        # Obter o item selecionado na Treeview
        item_selecionado = self.treeview_produtos.selection()

        if item_selecionado:
            # Obter os valores das colunas do item selecionado
            cod_produto = self.treeview_produtos.item(item_selecionado, "values")[0]

            # Atualizar o código do produto no entry da TelaUsuario
            self.tela_usuario.selecionar_produto(cod_produto)

    def adicionar_codigo_produto(self):
        # Obter o código do produto selecionado na Treeview
        item_selecionado = self.treeview_produtos.focus()
        if item_selecionado:
            cod_produto = self.treeview_produtos.item(item_selecionado, "values")[0]
            # Atualizar o código do produto no entry da TelaUsuario
            self.tela_usuario.atualizar_codigo_produto(cod_produto)
            # Fechar o TopLevel após adicionar o código do produto
            self.top_pesquisar.destroy()

    # FUNÇÃO PARA CANCELAR UM PRODUTO SELECIONADO PARA VENDA. AÇÃO DO F2
    def executar_funcao_cancelar_produto(self):
        self.remover_produto_selecionado()

    def remover_produto_selecionado(self):
        # Obter o item selecionado na Treeview
        item_selecionado = self.tela_usuario.treeview_produtos.selection()
        if item_selecionado:
            # Obter a descrição do item selecionado antes da remoção
            descricao_removida = self.tela_usuario.treeview_produtos.item(item_selecionado, "values")[1]

            # Remover o produto da Treeview
            self.tela_usuario.treeview_produtos.delete(item_selecionado)

            # Atualizar a descrição do produto na label
            items = self.tela_usuario.treeview_produtos.get_children()
            if items:
                ultimo_item = items[-1]
                descricao_ultimo_item = self.tela_usuario.treeview_produtos.item(ultimo_item, "values")[1]
                self.tela_usuario.label_descricao_produto["text"] = f"{descricao_ultimo_item}"
            else:
                # Caso não tenha mais itens na Treeview, limpar a label
                self.tela_usuario.label_descricao_produto["text"] = ""

            # Limpar a imagem do produto no frame_imagem
            self.limpar_imagem()  # PRECISAMOS RESOLVER O PROBLEMA DE REMOVER A IMAGEM SOMENTE DO ITEM EXCLUIDO.

            # Recalcular e atualizar os valores
            self.tela_usuario.calcular_valores()

    def limpar_imagem(self):
        # Remove a imagem do label_imagem
        if self.tela_usuario.label_imagem_prod is not None:
            self.tela_usuario.label_imagem_prod.pack_forget()
            self.tela_usuario.label_imagem_prod = None

    # FUNÇÃO PARA PAGAMENTO, FINALIZAR O PAGAMENTO E LANÇAR NO RELATÓRIO.
    def realizar_pagamento(self):
        # Obter os produtos selecionados da instância da classe TelaUsuario
        total_compra, produtos_selecionados = self.tela_usuario.obter_produtos_selecionados()

        # Mostrar os produtos selecionados na janela de pagamento
        if produtos_selecionados:
            self.total_compra = total_compra
            self.produtos_quantidades = produtos_selecionados
            self.troco = StringVar(value="TROCO\n00,00")

            # Calcular o valor total somado de todos os itens da tabela
            valor_total_somado = sum(produto[4] for produto in produtos_selecionados)

        # data_hora_atual = datetime.now()

        # Criar o TopLevel usando a instância da janela principal
        self.top_pagamento = Toplevel(self.janela)
        self.top_pagamento.title("Pagamentos")
        self.top_pagamento.iconbitmap("img/icons/Logo-caixa.ico")
        self.top_pagamento.config(background="#fff")

        # Adicionar um frame ao TopLevel para conter os campos desejados
        frame_pagamento = Frame(self.top_pagamento, bg="white")
        frame_pagamento.grid(row=0, column=0)

        frame_btn = Frame(self.top_pagamento, bg="white")
        frame_btn.grid(row=1, column=0, sticky="nw")

        frame_footer = Frame(self.top_pagamento, bg="white")
        frame_footer.grid(row=2, column=0, sticky="nsew")

        frame_rigth = Frame(self.top_pagamento, bg="white")
        frame_rigth.grid(row=0, column=1, columnspan=2, rowspan=7, stick="nsew")

        frame_btn_finalizar = Frame(self.top_pagamento, bg="white")
        frame_btn_finalizar.grid(row=2, column=1, columnspan=2, sticky="nsew")

        self.lb_pagamento = Label(frame_pagamento, text=f"PAGAMENTO\nR$ {self.total_compra:.2f}", width=25,
                                  background="#86C335", fg="#fff", font="Helvetica 13")
        self.lb_pagamento.grid(row=0, column=0, padx=10, pady=10)

        self.lb_troco = Label(frame_pagamento, textvariable=self.troco, width=25, background="#4D4D4D", fg="#fff",
                              font="Helvetica 13")
        self.lb_troco.grid(row=0, column=1, padx=2, pady=10)

        self.lb_forma_pagamento = Label(frame_pagamento, text="FORMA DE PAGAMENTO", background="#fff", fg="black",
                                        font="Helvetica 18", anchor="w")
        self.lb_forma_pagamento.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="nw")

        self.btn_dinheiro = Button(frame_btn, text="DINHEIRO", width=10, height=4, background="#8C8C8C", fg="#fff",
                                   anchor="center", font="Helvetica 15", command=self.selecionar_pagamento_dinheiro)
        self.btn_dinheiro.grid(row=0, column=0, padx=(10, 0), pady=1, sticky="nw")

        self.btn_cartao_credito = Button(frame_btn, text="CARTÃO DE\nCRÉDITO", width=10, height=4, background="#8C8C8C",
                                         fg="#fff", anchor="center", font="Helvetica 15",
                                         command=self.selecionar_pagamento_cartao_credito)
        self.btn_cartao_credito.grid(row=1, column=0, padx=(10, 0), pady=1, sticky="nw")

        self.btn_cartao_debito = Button(frame_btn, text="CARTÃO DE \nDÉBITO", width=10, height=4, background="#8C8C8C",
                                        fg="#fff", anchor="center", font="Helvetica 15",
                                        command=self.selecionar_pagamento_cartao_debito)
        self.btn_cartao_debito.grid(row=2, column=0, padx=(10, 0), pady=1, sticky="nw")

        self.btn_pix = Button(frame_btn, text="PIX", width=10, height=4, background="#8C8C8C", fg="#fff",
                              anchor="center", font="Helvetica 15", command=self.selecionar_pagamento_pix)
        self.btn_pix.grid(row=3, column=0, padx=(10, 0), pady=1, sticky="nw")

        self.btn_vazio1 = Button(frame_btn, text="", width=10, height=4, background="#86C335", fg="#fff",
                                 font="Helvetica 15", state="disabled")
        self.btn_vazio1.grid(row=0, column=1, padx=1, pady=1, sticky="nw")

        self.btn_vazio2 = Button(frame_btn, text="", width=10, height=4, background="#86C335", fg="#fff",
                                 font="Helvetica 15", state="disabled")
        self.btn_vazio2.grid(row=1, column=1, padx=1, pady=1, sticky="nw")

        self.btn_vazio3 = Button(frame_btn, text="", width=10, height=4, background="#86C335", fg="#fff",
                                 font="Helvetica 15", state="disabled")
        self.btn_vazio3.grid(row=2, column=1, padx=1, pady=1, sticky="nw")

        self.btn_vazio4 = Button(frame_btn, text="", width=10, height=4, background="#86C335", fg="#fff",
                                 font="Helvetica 15", state="disabled")
        self.btn_vazio4.grid(row=3, column=1, padx=1, pady=1, sticky="nw")

        self.btn_vazio5 = Button(frame_btn, text="", width=10, height=4, background="#86C335", fg="#fff",
                                 font="Helvetica 15", state="disabled")
        self.btn_vazio5.grid(row=0, column=2, padx=1, pady=1, sticky="nw")

        self.btn_vazio6 = Button(frame_btn, text="", width=10, height=4, background="#86C335", fg="#fff",
                                 font="Helvetica 15", state="disabled")
        self.btn_vazio6.grid(row=1, column=2, padx=1, pady=1, sticky="nw")

        self.btn_vazio7 = Button(frame_btn, text="", width=10, height=4, background="#86C335", fg="#fff",
                                 font="Helvetica 15", state="disabled")
        self.btn_vazio7.grid(row=2, column=2, padx=1, pady=1, sticky="nw")

        self.btn_vazio8 = Button(frame_btn, text="", width=10, height=4, background="#86C335", fg="#fff",
                                 font="Helvetica 15", state="disabled")
        self.btn_vazio8.grid(row=3, column=2, padx=1, pady=1, sticky="nw")

        self.btn_vazio9 = Button(frame_btn, text="", width=10, height=4, background="#86C335", fg="#fff",
                                 font="Helvetica 15", state="disabled")
        self.btn_vazio9.grid(row=0, column=3, padx=1, pady=1, sticky="nw")

        self.btn_vazio10 = Button(frame_btn, text="", width=10, height=4, background="#86C335", fg="#fff",
                                  font="Helvetica 15", state="disabled")
        self.btn_vazio10.grid(row=1, column=3, padx=1, pady=1, sticky="nw")

        self.btn_vazio11 = Button(frame_btn, text="", width=10, height=4, background="#86C335", fg="#fff",
                                  font="Helvetica 15", state="disabled")
        self.btn_vazio11.grid(row=2, column=3, padx=1, pady=1, sticky="nw")

        self.btn_vazio12 = Button(frame_btn, text="", width=10, height=4, background="#86C335", fg="#fff",
                                  font="Helvetica 15", state="disabled")
        self.btn_vazio12.grid(row=3, column=3, padx=1, pady=1, sticky="nw")

        self.lb_valor_pago = Label(frame_footer, text="VALOR PAGO", background="#fff", fg="black", font="Helvetica 18",
                                   anchor="w")
        self.lb_valor_pago.grid(row=0, column=0, columnspan=4, sticky="nw", padx=(10, 0), pady=(10, 0))

        self.enty_valor_pago = ctk.CTkEntry(frame_footer, placeholder_text="R$ 00.00", height=60,
                                            font=ctk.CTkFont(family="Helvetica", size=15))
        self.enty_valor_pago.grid(row=1, column=0, columnspan=3, sticky="ew", padx=(10, 0), pady=(10, 10))

        self.image_confirmar = PhotoImage(file="img\icons\confirm-50x50.png")
        self.btn_confirmar = Button(frame_footer, image=self.image_confirmar, compound="left", text="CONFIRMAR", bg="white", cursor="hand2", command=self.get_valor_pago_somar_troco)
        self.btn_confirmar.grid(row=1, column=3, padx=(10, 10), pady=(10, 10))

        # Configurar expansão horizontal da coluna que contém o CTkEntry
        frame_footer.grid_columnconfigure(0, weight=2)

        # FRAME PARA DEMOSNTRAÇÃO DOS PRODUTOS SELECIONADOS E FINALIZAR VENDA
        # Exibir os produtos selecionados
        for idx, produto in enumerate(produtos_selecionados, start=1):
            codigo, self.descricao, self.quantidade, valor_unitario, self.valor_total = produto

            lb_codigo = Label(frame_rigth, text=f"{self.quantidade} x {codigo}\t\tR$ {valor_unitario:.2f}",
                              font="Helvetica 12", background="#fff")
            lb_codigo.grid(row=idx, column=0, padx=(10, 2), pady=5, sticky="nw")

            lb_valores = Label(frame_rigth, text=f"{self.descricao}\tR$ {self.valor_total:.2f}", font="Helvetica 13",
                               background="#fff")
            lb_valores.grid(row=idx, column=1, columnspan=2, padx=(0, 10), pady=5, sticky="nw")

            # Separador
            # separator = ttk.Separator(self.frame_rigth, orient="horizontal")
            # separator.grid(row=idx + 2, column=0, columnspan=4, sticky="ew", padx=10, pady=5)

        # Adicionar a linha de separação below the last product entry
        linha_separacao = Frame(frame_rigth, bg="black", height=2)
        linha_separacao.grid(row=len(produtos_selecionados) + 1, column=0, columnspan=4, sticky="new", pady=5)

        # Adicionar o campo de pagamento efetuado com o valor total somado
        lb_pagamento_efetuado = Label(frame_rigth, text=f"PAGAMENTO EFETUADO", background="#fff", fg="black",
                                      anchor="w", font="Helvetica 18")
        lb_pagamento_efetuado.grid(row=len(produtos_selecionados) + 2, column=0, columnspan=2, padx=10, pady=5,
                                   sticky="nw")

        self.lb_tipo_pagamento = StringVar()
        lb_tipo = Label(frame_rigth, textvariable=self.lb_tipo_pagamento, background="#fff", fg="black", anchor="w",
                        font="Helvetica 18")
        lb_tipo.grid(row=len(produtos_selecionados) + 3, column=0, columnspan=2, padx=10, pady=5, sticky="nw")

        lb_avista = Label(frame_rigth, text=f"À VISTA", background="#fff", fg="black", anchor="w", font="Helvetica 18")
        lb_avista.grid(row=len(produtos_selecionados) + 2, column=1, columnspan=2, padx=10, pady=5, sticky="ne")

        lb_total_somado = Label(frame_rigth, text=f"R$ {valor_total_somado:.2f}", background="#fff", fg="black",
                                anchor="w", font="Helvetica 18")
        lb_total_somado.grid(row=len(produtos_selecionados) + 3, column=1, columnspan=2, padx=10, pady=5, sticky="ne")

        # Criar o botão "Finalizar venda" ALTERADO NO BOURBON
        self.img_finalizar = PhotoImage(file="img\icons\seta-direita-50x50.png")
        self.botao_finalizar = Button(frame_btn_finalizar, image=self.img_finalizar, compound="left", text="FINALIZAR VENDA", height=50, background="#1a6278", fg="#fff" ,font="Helvetica 15", cursor="hand2", command=self.finalizar_venda_armazenar_relatorio)
        self.botao_finalizar.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="sew")

        # Configurar o frame_btn_finalizar para expandir na horizontal e vertical
        frame_btn_finalizar.columnconfigure(0, weight=1)
        frame_btn_finalizar.rowconfigure(0, weight=1)

        # Configurar um Scrollbar caso a lista de produtos seja longa
        # scrollbar = Scrollbar(self.top_pagamento, orient="vertical", command=frame_rigth)
        # scrollbar.grid(row=0, column=4, sticky="ns")
        # frame_rigth.configure(yscrollcommand=scrollbar.set)

        # Centralizar a janela no centro da tela
        self.centralizar_janela(self.top_pagamento)

    def selecionar_pagamento_dinheiro(self):
        self.lb_tipo_pagamento.set("DINHEIRO")

    def selecionar_pagamento_cartao_credito(self):
        self.lb_tipo_pagamento.set("CARTÃO DE CRÉDITO")

    def selecionar_pagamento_cartao_debito(self):
        self.lb_tipo_pagamento.set("CARTÃO DE DÉBITO")

    def selecionar_pagamento_pix(self):
        self.lb_tipo_pagamento.set("PIX")

    def get_valor_pago_somar_troco(self):
        try:
            self.valor_pago = float(self.enty_valor_pago.get())
            self.troco_lb = self.valor_pago - self.total_compra
            self.troco.set(f"TROCO\n{self.troco_lb:.2f}")
            self.enty_valor_pago.delete(0, "end")
        except ValueError:
            # Caso o valor digitado no Entry não seja um número válido
            self.troco.set("Valor inválido")

    def finalizar_venda_armazenar_relatorio(self):
        # Obter os dados da venda
        data_hora_atual = datetime.now()
        # Formatar a hora no formato brasileiro (hh:mm:ss)
        self.hora_formatada = data_hora_atual.strftime("%d/%m/%Y %H:%M:%S")
        forma_pagamento = self.lb_tipo_pagamento.get().title()

        # Verificar se a forma de pagamento é em dinheiro
        if forma_pagamento.lower() == "dinheiro":
            try:
                valor_pago_formatado = float(self.valor_pago)  # Converter a string em float
            except ValueError:
                messagebox.showerror("Erro", "Valor pago inválido. Certifique-se de digitar um número válido.")
                return

            # Calcular o troco apenas se a forma de pagamento for dinheiro
            total_compra = self.total_compra
            troco = valor_pago_formatado - total_compra
            troco_formatado = f"{troco:.2f}"
        else:
            # Caso contrário, a forma de pagamento não é dinheiro, então o troco é zero
            troco_formatado = "0.00"
            valor_pago = self.total_compra
            valor_pago_formatado = f"{valor_pago:.2f}"

        # Conectar ao banco de dados
        with sqlite3.connect('SistemaPDV.db') as conexao:
            cursor = conexao.cursor()

            # Inserir os dados da venda na tabela relatorio_vendas
            for produto in self.produtos_quantidades:
                codigo, descricao, quantidade_vendida, valor_unitario, valor_total = produto
                cursor.execute('''
                    INSERT INTO relatorios_vendas (data, nome_produto, total_compra, quantidade_vendida, forma_pagamento, valor_pago, troco)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''', (
                self.hora_formatada, descricao, valor_total, quantidade_vendida, forma_pagamento, valor_pago_formatado,
                troco_formatado))

                # Atualizar o estoque para cada produto vendido
                cursor.execute("SELECT estoque FROM produtos WHERE descricao = ?", (descricao,))
                resultado = cursor.fetchone()

                if resultado is not None:
                    quantidade_atual = int(resultado[0])
                    quantidades_vendida = float(quantidade_vendida)
                    nova_quantidade = quantidade_atual - quantidades_vendida

                    # Atualizar o estoque no banco de dados
                    cursor.execute("UPDATE produtos SET estoque = ? WHERE descricao = ?", (nova_quantidade, descricao))

        # Salvar as alterações e fechar a conexão
        conexao.commit()
        conexao.close()

        # Exibir mensagem de venda finalizada
        messagebox.showinfo("Venda Finalizada", "A venda foi finalizada com sucesso!")
        self.limpar_tela_apos_pagamento()
        # Fechar a janela de pagamento
        self.top_pagamento.destroy()

    def limpar_tela_apos_pagamento(self):
        # Implementar a lógica para limpar a tela após o pagamento
        self.tela_usuario.treeview_produtos.delete(*self.tela_usuario.treeview_produtos.get_children())
        self.tela_usuario.label_total_itens.config(text="TOTAL ITENS: 0")
        self.tela_usuario.label_total_compra.config(text="TOT. COMPRA: R$ 0.00")
        self.tela_usuario.label_descricao_produto.config(text="")
        self.limpar_imagem()
        self.tela_usuario.calcular_valores()

    # CRIAR UMA JANELA PARA CADASTRO DE PRODUTOS, CÓDIGO INSERIDO NA TelaUsuario E CHAMADA DA FUNÇÃO AQUI.
    def abrir_janela_cadastro_produtos(self):
        # Chamar o método criar_frame_cadastro da instância de TelaUsuario
        self.tela_usuario.criar_frame_cadastro()

    # CRIAR UMA JANELA PARA RELATÓRIO DE VENDAS
    def relatorio_venda(self):
        self.janela_relatorio = tk.Toplevel()
        self.janela_relatorio.title("Relatório de Vendas")
        self.frame_despesas = ""
        self.frame_receitas = ""

        # Defina o tamanho da janela para preencher toda a tela
        largura_tela = self.janela_relatorio.winfo_screenwidth()
        altura_tela = self.janela_relatorio.winfo_screenheight()
        self.janela_relatorio.geometry(f"{largura_tela}x{altura_tela}")

        # Defina a proporção de expansão das linhas
        self.janela_relatorio.grid_rowconfigure(0, weight=1)  # Frame_left ocupa 100% da altura
        # Defina a proporção de expansão das colunas
        self.janela_relatorio.grid_columnconfigure(1, weight=1)  # Frame_right ocupa 100% da largura

        # Crie um frame na parte esquerda da janela que preencha toda a altura
        frame_left = tk.Frame(self.janela_relatorio, bg="#202123")
        frame_left.grid(row=0, column=0, sticky="ns")

        # Crie o frame da direita que irá conter o frame de filtros e a treeview
        self.frame_right = tk.Frame(self.janela_relatorio, bg="white")
        self.frame_right.grid(row=0, column=1, columnspan=4, sticky="nsew")

        # Defina a proporção de expansão das colunas
        self.frame_right.grid_columnconfigure(1, weight=1)  # Frame_right ocupa 100% da largura

        # Crie o frame da treeview
        self.frame_treeview = tk.Frame(self.frame_right)
        self.frame_treeview.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Adicione os botões de filtro dentro do frame_left
        self.imagem_dia = PhotoImage(file="img/icons/icone-do-calendario-de-1-dia.png").subsample(1, 1)
        btn_filtro_dia = ctk.CTkButton(frame_left, text="Vendas do Dia", image=self.imagem_dia, compound="left", height=45,
                                       hover_color="blue",
                                       font=ctk.CTkFont(family="Roboto", size=20), text_color="white",
                                       fg_color="#267cb5", corner_radius=None, command=self.filtrar_vendas_dia)

        self.imagem_semana = PhotoImage(file="img/icons/icone-do-calendario-do-7-dia.png").subsample(1,1)
        btn_filtro_semana = ctk.CTkButton(frame_left, text="Venda Semana", image=self.imagem_semana, compound="left", height=45, hover_color="blue",
                                          font=ctk.CTkFont(family="Roboto", size=20), text_color="white",
                                          fg_color="#267cb5", corner_radius=None, command=self.filtrar_vendas_semana)

        self.imagem_mes = PhotoImage(file="img/icons/icone-do-calendario-de-30-dias.png").subsample(1,1)
        btn_filtro_mes = ctk.CTkButton(frame_left, text="Venda do Mês", image=self.imagem_mes, compound="left" ,height=45, hover_color="blue",
                                       font=ctk.CTkFont(family="Roboto", size=20), text_color="white",
                                       fg_color="#267cb5", corner_radius=None, command=self.filtrar_vendas_mes)

        self.imagem_todos = PhotoImage(file="img/icons/icone-do-calendario-de-todospng.png").subsample(1,1)
        btn_mostrar_todos = ctk.CTkButton(frame_left, text="Todas Vendas", image=self.imagem_todos, compound="left" ,height=45, hover_color="blue",
                                          font=ctk.CTkFont(family="Roboto", size=20), text_color="white",
                                          fg_color="#267cb5", corner_radius=None, command=self.filtrar_todos_os_dados)
        self.imagem_sair = PhotoImage(file="img/icons/icone-sair-50x50.png").subsample(1,1)
        btn_sair_relatorio = ctk.CTkButton(frame_left, text="Sair", image=self.imagem_sair, compound="left" ,height=45, hover_color="blue",
                                           font=ctk.CTkFont(family="Roboto", size=20), text_color="white",
                                           fg_color="#267cb5", corner_radius=None, command=self.sair_tela_relatorio)

        btn_filtro_dia.grid(row=0, padx=1, pady=5, sticky="ew")
        btn_filtro_semana.grid(row=1, padx=1, pady=5, sticky="ew")
        btn_filtro_mes.grid(row=2, padx=1, pady=5, sticky="ew")
        btn_mostrar_todos.grid(row=3, padx=1, pady=5, sticky="ew")
        btn_sair_relatorio.grid(row=4, padx=1, pady=5, sticky="ew")
        # Adicione um Label vazio para preencher toda a altura do frame
        empty_label = tk.Label(frame_left, bg="#202123")
        empty_label.grid(row=5, column=0, sticky="ns")

    def criar_frame_filtros(self):
        # Show the frame again
        self.frame_right.grid()
        if self.frame_despesas and self.frame_receitas:
            self.frame_despesas.grid_remove()
            self.frame_receitas.grid_remove()
        else:
            pass

        # Limpa o frame de filtros, se já existir
        if self.frame_filtros is not None:
            self.frame_filtros.destroy()

        # Crie o frame de filtros
        self.frame_filtros = tk.Frame(self.frame_right, background="white")
        self.frame_filtros.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

    def criar_treeview(self):
        # Show the frame again
        self.frame_right.grid()
        if self.frame_despesas and self.frame_receitas:
            self.frame_despesas.grid_remove()
            self.frame_receitas.grid_remove()
        else:
            pass
        # Cria uma única instância da treeview apenas se ela ainda não foi criada
        if self.treeview_relatorio is None:
            self.treeview_relatorio = ttk.Treeview(self.frame_treeview, height=20, columns=(
                "data", "nome_produto", "total_compra", "quantidade_vendida", "forma_pagamento", "valor_pago", "troco"))
            self.treeview_relatorio.heading("data", text="Data")
            self.treeview_relatorio.heading("nome_produto", text="Descrição")
            self.treeview_relatorio.heading("total_compra", text="Total da Compra")
            self.treeview_relatorio.heading("quantidade_vendida", text="Quantidade vendida")
            self.treeview_relatorio.heading("forma_pagamento", text="Forma de Pagamento")
            self.treeview_relatorio.heading("valor_pago", text="Valor Pago")
            self.treeview_relatorio.heading("troco", text="Troco")

            # Defina um tamanho mínimo para as colunas e remova o espaço vazio no início
            self.treeview_relatorio.column("#0", width=0, stretch=tk.NO)
            self.treeview_relatorio.column("data", width=100, anchor="center", minwidth=100)
            self.treeview_relatorio.column("nome_produto", width=150, anchor="center", minwidth=100)
            self.treeview_relatorio.column("total_compra", width=150, anchor="center", minwidth=100)
            self.treeview_relatorio.column("quantidade_vendida", width=100, anchor="center", minwidth=100)
            self.treeview_relatorio.column("forma_pagamento", width=200, anchor="center", minwidth=100)
            self.treeview_relatorio.column("valor_pago", width=150, anchor="center", minwidth=100)
            self.treeview_relatorio.column("troco", width=150, anchor="center", minwidth=100)

            self.treeview_relatorio.pack(fill="both", expand=True)
        else:
            # Se a treeview já existe, apenas limpe os itens existentes
            self.treeview_relatorio.delete(*self.treeview_relatorio.get_children())

    def filtrar_vendas_dia(self):
        # Lógica para filtrar as vendas do dia no banco de dados
        self.criar_frame_filtros()
        self.criar_treeview()

        # Crie os elementos de filtro (label, entry e botão) dentro do frame_filtros
        self.lb_dia = ctk.CTkLabel(self.frame_filtros, text="DIA INICIO:", font=ctk.CTkFont(family="Roboto", size=25))
        self.lb_dia.grid(row=0, column=0, padx=15, pady=15, sticky="e")

        self.enty_dia = ctk.CTkEntry(self.frame_filtros, placeholder_text="EX 01-01-2023", width=300, height=45,
                                     font=ctk.CTkFont(family="Roboto", size=18), text_color="black", bg_color="#252525",
                                     corner_radius=None)
        self.enty_dia.grid(row=0, column=1, padx=5, pady=15, sticky="w")

        self.btn_pesquisar = ctk.CTkButton(self.frame_filtros, text="Pesquisar", width=150, height=45,
                                           hover_color="blue", font=ctk.CTkFont(family="Roboto", size=20),
                                           text_color="white", bg_color="#252525", corner_radius=1,
                                           command=self.pesquisar_rela_dia)
        self.btn_pesquisar.grid(row=0, column=2, padx=5, pady=15, sticky="e")

        btn_imprimir = ctk.CTkButton(self.frame_filtros, text="Imprimir", width=120, height=45, hover_color="blue",
                                     font=ctk.CTkFont(family="Roboto", size=20), text_color="white", bg_color="#252525",
                                     corner_radius=None, command=self.imprimir_rela_dia)
        btn_imprimir.grid(row=0, column=3, padx=5, pady=15, sticky="w")

    def filtrar_vendas_semana(self):
        # Lógica para filtrar as vendas da semana no banco de dados
        self.criar_frame_filtros()
        self.criar_treeview()

        # Adicione no frame os elementos de filtro (label, entry e botão)
        self.lb_dia_ini_sem = ctk.CTkLabel(self.frame_filtros, text="DIA INICIO: ",
                                           font=ctk.CTkFont(family="Roboto", size=25))
        self.lb_dia_ini_sem.grid(row=0, column=0, padx=15, pady=15)

        self.enty_dia_ini_sem = ctk.CTkEntry(self.frame_filtros, placeholder_text="EX 01-01-2023", width=200, height=45,
                                             font=ctk.CTkFont(family="Roboto", size=18), text_color="black",
                                             bg_color="#252525", corner_radius=1)
        self.enty_dia_ini_sem.grid(row=0, column=1, padx=15, pady=15)

        self.lb_dia_fim_sem = ctk.CTkLabel(self.frame_filtros, text="DIA FINAL: ",
                                           font=ctk.CTkFont(family="Roboto", size=25))
        self.lb_dia_fim_sem.grid(row=0, column=2, padx=15, pady=15)

        self.enty_dia_fim_sem = ctk.CTkEntry(self.frame_filtros, placeholder_text="EX 07-01-2023", width=200, height=45,
                                             font=ctk.CTkFont(family="Roboto", size=18), text_color="black",
                                             bg_color="#252525", corner_radius=1)
        self.enty_dia_fim_sem.grid(row=0, column=3, padx=15, pady=15)

        self.btn_pesquisar_sem = ctk.CTkButton(self.frame_filtros, text="Pesquisar", width=150, height=45,
                                               hover_color="blue", font=ctk.CTkFont(family="Roboto", size=20),
                                               text_color="white", bg_color="#252525", corner_radius=None,
                                               command=self.pesquisar_rela_semana)
        self.btn_pesquisar_sem.grid(row=0, column=4, padx=10, pady=15)

        btn_imprimir = ctk.CTkButton(self.frame_filtros, text="Imprimir", width=120, height=45, hover_color="blue",
                                     font=ctk.CTkFont(family="Roboto", size=20), text_color="white", bg_color="#252525",
                                     corner_radius=None, command=self.imprimir_rela_sem)
        btn_imprimir.grid(row=0, column=5, padx=10, pady=15)

    def filtrar_vendas_mes(self):
        # Lógica para filtrar as vendas da semana no banco de dados
        self.criar_frame_filtros()
        self.criar_treeview()

        # Adicione no frame os elementos de filtro (label, entry e botão)
        self.lb_dia_ini_mes = ctk.CTkLabel(self.frame_filtros, text="DIA INICIO: ",
                                           font=ctk.CTkFont(family="Roboto", size=25))
        self.lb_dia_ini_mes.grid(row=0, column=0, padx=15, pady=15)

        self.enty_dia_ini_mes = ctk.CTkEntry(self.frame_filtros, placeholder_text="EX 01-01-2023", width=200, height=45,
                                             font=ctk.CTkFont(family="Roboto", size=18), text_color="black",
                                             bg_color="#252525", corner_radius=1)
        self.enty_dia_ini_mes.grid(row=0, column=1, padx=15, pady=15)

        self.lb_dia_fim_mes = ctk.CTkLabel(self.frame_filtros, text="DIA FINAL: ",
                                           font=ctk.CTkFont(family="Roboto", size=25))
        self.lb_dia_fim_mes.grid(row=0, column=2, padx=15, pady=15)

        self.enty_dia_fim_mes = ctk.CTkEntry(self.frame_filtros, placeholder_text="EX 01-02-2023", width=200, height=45,
                                             font=ctk.CTkFont(family="Roboto", size=18), text_color="black",
                                             bg_color="#252525", corner_radius=None)
        self.enty_dia_fim_mes.grid(row=0, column=3, padx=15, pady=15)

        self.btn_pesquisar_mes = ctk.CTkButton(self.frame_filtros, text="Pesquisar", width=150, height=45,
                                               hover_color="blue", font=ctk.CTkFont(family="Roboto", size=20),
                                               text_color="white", bg_color="#252525", corner_radius=None,
                                               command=self.pesquisar_rela_mes)
        self.btn_pesquisar_mes.grid(row=0, column=4, padx=10, pady=15)

        btn_imprimir = ctk.CTkButton(self.frame_filtros, text="Imprimir", width=120, height=45, hover_color="blue",
                                     font=ctk.CTkFont(family="Roboto", size=20), text_color="white", bg_color="#252525",
                                     corner_radius=None, command=self.imprimir_rela_mes)
        btn_imprimir.grid(row=0, column=5, padx=10, pady=15)

    def filtrar_todos_os_dados(self):
        # Lógica para mostrar todos os dados do relatório no banco de dados
        self.criar_frame_filtros()
        self.criar_treeview()

        # Crie os elementos de filtro (label, entry e botão) dentro do frame_filtros
        lb_title = ctk.CTkLabel(self.frame_filtros, text="RELATÓRIO DE TODAS AS VENDAS",
                                font=ctk.CTkFont(family="Roboto", size=25), anchor="center", bg_color="white")
        lb_title.grid(row=0, column=0, columnspan=3, padx=50, pady=15)

        btn_imprimir = ctk.CTkButton(self.frame_filtros, text="Imprimir", width=120, height=45, hover_color="blue",
                                     font=ctk.CTkFont(family="Roboto", size=20), text_color="white", bg_color="#252525",
                                     corner_radius=1, command=self.imprimir_rela_todos)
        btn_imprimir.grid(row=0, column=3, padx=10, pady=15)

        # Conectar ao banco de dados
        conn = sqlite3.connect("SistemaPDV.db")
        cursor = conn.cursor()

        # Lógica para filtrar todas as vendas do banco de dados
        cursor.execute(
            "SELECT data, nome_produto ,total_compra, quantidade_vendida ,forma_pagamento, valor_pago, troco FROM relatorios_vendas")
        dados_relatorio = cursor.fetchall()

        if dados_relatorio:  # Verifica se a lista de dados não está vazia
            # Preencher a Treeview com os dados do relatório de vendas
            for dado in dados_relatorio:
                self.treeview_relatorio.insert("", "end", values=dado)
            # Fechar a conexão com o banco de dados
            conn.close()
        else:
            messagebox.showerror("Error", "Não existe dados no banco de dados!")

    def sair_tela_relatorio(self):
        self.janela_relatorio.destroy()

    def pesquisar_rela_dia(self):
        # Conectar ao banco de dados
        conn = sqlite3.connect("SistemaPDV.db")
        cursor = conn.cursor()

        receber_enty_dia = self.enty_dia.get()
        # Usando slicing para obter dia, mês e ano
        dia = receber_enty_dia[0:2]
        mes = receber_enty_dia[3:5]
        ano = receber_enty_dia[6:11]
        palavra_invertida = f"{ano}-{mes}-{dia}"

        # Lógica para filtrar as vendas do dia no banco de dados
        cursor.execute(
            "SELECT data, nome_produto ,total_compra, quantidade_vendida ,forma_pagamento, valor_pago, troco FROM relatorios_vendas WHERE data LIKE ?",
            (f"{palavra_invertida}%",))
        dados_relatorio = cursor.fetchall()

        # Verificar se a data invertida está presente nos resultados da consulta
        if dados_relatorio:  # Verifica se a lista de dados não está vazia
            # Preencher a Treeview com os dados do relatório de vendas
            for dado in dados_relatorio:
                self.treeview_relatorio.insert("", "end", values=dado)
            # Fechar a conexão com o banco de dados
            conn.close()
            self.enty_dia.delete(0, "end")
        else:
            messagebox.showerror("Error", "Data selecionada não existente no banco de dados!")

    def pesquisar_rela_semana(self):
        # Conectar ao banco de dados
        conn = sqlite3.connect("SistemaPDV.db")
        cursor = conn.cursor()

        receber_enty_dia_ini = self.enty_dia_ini_sem.get()
        receber_enty_dia_fim = self.enty_dia_fim_sem.get()
        # Usando slicing para obter dia, mês e ano Inicio
        dia_ini = receber_enty_dia_ini[0:2]
        mes_ini = receber_enty_dia_ini[3:5]
        ano_ini = receber_enty_dia_ini[6:11]
        palavra_invertida_ini = f"{ano_ini}-{mes_ini}-{dia_ini}"
        # Usando slicing para obter dia, mês e ano Fim
        dia_fim = receber_enty_dia_fim[0:2]
        mes_fim = receber_enty_dia_fim[3:5]
        ano_fim = receber_enty_dia_fim[6:11]
        palavra_invertida_fim = f"{ano_fim}-{mes_fim}-{dia_fim}"

        # Limpa os itens existentes na treeview principal
        for item in self.treeview_relatorio.get_children():
            self.treeview_relatorio.delete(item)

        # Realizar a consulta ao banco de dados para obter os dados do relatório de vendas da semana
        cursor.execute(
            "SELECT data, nome_produto, total_compra, quantidade_vendida, forma_pagamento, valor_pago, troco FROM relatorios_vendas WHERE data BETWEEN ? AND ?",
            (palavra_invertida_ini, palavra_invertida_fim))
        dados_relatorio_semana = cursor.fetchall()

        if dados_relatorio_semana:
            # Limpar a Treeview antes de preencher com os novos dados
            self.treeview_relatorio.delete(*self.treeview_relatorio.get_children())

            # Preencher a Treeview com os dados do relatório de vendas da semana
            for dado in dados_relatorio_semana:
                self.treeview_relatorio.insert("", "end", values=dado)

        else:
            messagebox.showerror("Error", "Nenhum registro encontrado para a semana selecionada!")

        # Fechar a conexão com o banco de dados
        conn.close()

    def pesquisar_rela_mes(self):
        # Conectar ao banco de dados
        conn = sqlite3.connect("SistemaPDV.db")
        cursor = conn.cursor()

        receber_enty_dia_ini = self.enty_dia_ini_mes.get()
        receber_enty_dia_fim = self.enty_dia_fim_mes.get()
        # Usando slicing para obter dia, mês e ano Inicio
        dia_ini = receber_enty_dia_ini[0:2]
        mes_ini = receber_enty_dia_ini[3:5]
        ano_ini = receber_enty_dia_ini[6:11]
        palavra_invertida_ini = f"{ano_ini}-{mes_ini}-{dia_ini}"
        # Usando slicing para obter dia, mês e ano Fim
        dia_fim = receber_enty_dia_fim[0:2]
        mes_fim = receber_enty_dia_fim[3:5]
        ano_fim = receber_enty_dia_fim[6:11]
        palavra_invertida_fim = f"{ano_fim}-{mes_fim}-{dia_fim}"

        # Limpa os itens existentes na treeview principal
        for item in self.treeview_relatorio.get_children():
            self.treeview_relatorio.delete(item)

        # Realizar a consulta ao banco de dados para obter os dados do relatório de vendas da semana
        cursor.execute(
            "SELECT data, nome_produto, total_compra, quantidade_vendida, forma_pagamento, valor_pago, troco FROM relatorios_vendas WHERE data BETWEEN ? AND ?",
            (palavra_invertida_ini, palavra_invertida_fim))
        dados_relatorio_ini = cursor.fetchall()

        # Verificar se a data invertida está presente nos resultados da consulta e inserir na treeview principal
        if dados_relatorio_ini:
            # Limpar a Treeview antes de preencher com os novos dados
            self.treeview_relatorio.delete(*self.treeview_relatorio.get_children())

            # Preencher a Treeview com os dados do relatório de vendas da semana
            for dado in dados_relatorio_ini:
                self.treeview_relatorio.insert("", "end", values=dado)
        else:
            messagebox.showerror("Error", "Nenhum registro encontrado para o mês selecionado!")

            # Fechar a conexão com o banco de dados
            conn.close()

    def gerar_pdf(self, treeview):
        # Obtenha os dados da treeview
        data = [treeview.heading(column)["text"] for column in treeview["columns"]]
        data_rows = []
        total_vendas = 0.0  # Variável para armazenar a soma dos valores da coluna 2 (total da tabela)

        for item in treeview.get_children():
            row = [treeview.item(item, "values")[column] for column in range(len(data))]
            total_vendas += float(row[2])  # Adiciona o valor da coluna 2 (total da tabela) à soma
            data_rows.append(row)

        # Criação do documento PDF, Defina o tamanho e a orientação do PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Obtemos o timestamp atual
        nome_arquivo = f"relatorio_{timestamp}.pdf"  # Nome do arquivo com timestamp
        doc = SimpleDocTemplate(os.path.join("Relatórios", nome_arquivo), pagesize=landscape(letter))

        # Crie a lista de elementos
        elements = []

        # Adicionar o total de vendas abaixo da tabela
        style_title = ParagraphStyle(
            name='TotalStyle',
            fontName='Helvetica-Bold',
            fontSize=20,
            textColor=colors.black,  # Altere a cor para preto
            alignment=1,  # 1 = Center
        )

        p_title = Paragraph(self.title_text, style_title)
        elements.append(p_title)

        # Adicionar um espaço em branco entre o titulo e a tabela
        elements.append(Spacer(1, 20))

        # Defina o estilo da tabela
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        table = Table([data] + data_rows, repeatRows=1, hAlign="CENTER")
        table.setStyle(style)

        # Adicione a tabela à lista de elementos
        elements.append(table)

        # Adicionar um espaço em branco entre a tabela e o total de vendas
        elements.append(Spacer(1, 20))

        # Adicionar o total de vendas abaixo da tabela
        style_total = ParagraphStyle(
            name='TotalStyle',
            fontName='Helvetica-Bold',
            fontSize=14,
            textColor=colors.red,  # Altere a cor para vermelho
            alignment=1,  # 1 = Center
        )
        total_vendas_text = f"Total de vendas: R$ {total_vendas:.2f}"
        p_total = Paragraph(total_vendas_text, style_total)
        elements.append(p_total)

        # Construir o documento PDF
        doc.build(elements)

        # Exiba uma mensagem informando que o PDF foi gerado
        messagebox.showinfo("PDF", f"PDF gerado com sucesso: {nome_arquivo}")

    def imprimir_rela_dia(self):
        self.title_text = "Relatório de vendas do Dia"
        self.gerar_pdf(self.treeview_relatorio)
        self.enty_dia.delete(0, "end")
        self.criar_treeview()

    def imprimir_rela_sem(self):
        self.title_text = "Relatório de vendas da semana"
        self.gerar_pdf(self.treeview_relatorio)
        self.enty_dia_ini_sem.delete(0, "end")
        self.enty_dia_fim_sem.delete(0, "end")
        self.criar_treeview()

    def imprimir_rela_mes(self):
        self.title_text = "Relatório de vendas do Mês"
        self.gerar_pdf(self.treeview_relatorio)
        self.enty_dia_ini_mes.delete(0, "end")
        self.enty_dia_fim_mes.delete(0, "end")
        self.criar_treeview()

    def imprimir_rela_todos(self):
        self.title_text = "Relatório de todas as vendas"
        self.gerar_pdf(self.treeview_relatorio)
        self.criar_treeview()