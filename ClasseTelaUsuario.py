from tkinter import Tk, PhotoImage, messagebox
from tkinter import Toplevel, Label ,LabelFrame ,Button, Frame, Canvas, ttk
import customtkinter as ctk
from Teclas_de_atalho import TeclasDeAtalho
from datetime import datetime
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter import filedialog
import os
import re
import sqlite3

class TelaUsuario:
    def __init__(self, janela_principal):
        self.janela_pdv = Toplevel(janela_principal)
        self.janela_pdv.geometry("{}x{}+0+0".format(self.janela_pdv.winfo_screenwidth(), self.janela_pdv.winfo_screenheight()))
        self.janela_pdv.title("Sistema de caixa")
        self.janela_pdv.iconbitmap("img/icons/caixa-icone.ico")
        self.janela_pdv.resizable(False, False)
        self.Criar_Interface()
        self.Treeview()
        self.Label_frame_esquerdo()
        self.Atalhos()
        self.atualizar_hora()  # Iniciar a atualização da hora
        # Crie uma instância da classe TeclasDeAtalho, passando a janela e a própria instância de TelaUsuario como argumentos
        self.teclas_atalho = TeclasDeAtalho(self.janela_pdv, self)
        self.janela_pdv.after(100, self.Entry_codigo_produto)  # Agendar a chamada da função
        self.foto = None
        self.label_imagem = None
        self.valor_abertura_caixa = None  # Variável para armazenar o valor de abertura do caixa
        # Vincular o evento 'Escape' para encerrar o programa
        self.janela_pdv.bind("<Escape>", self.encerrar_programa)

# Função para criar interface e widgets
    def Criar_Interface(self):
        # Configurar layout de grid
        self.janela_pdv.config(background="white")
        self.janela_pdv.grid_columnconfigure(0, weight=1)
        self.janela_pdv.grid_columnconfigure(1, weight=2)
        self.janela_pdv.grid_rowconfigure(0, weight=0)  # Linha 0 com peso 0 (não expansível)
        self.janela_pdv.grid_rowconfigure(1, weight=0)  # Linha 1 com peso 1 (expansível)
        self.caminho_imagem = ""
        self.quantidade_total = 0
        self.valor_Total = 0
        self.descricao_produto = ""
        self.cam_imagem = None  
        self.label_imagem_prod = None 

        # Frame principal
        self.frame_principal = Frame(self.janela_pdv)
        self.frame_principal.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

        # Label para exibir informações do produto
        self.label_descricao_produto = Label(self.frame_principal, text="", font=("Arial", 22), bg="blue", fg="white", width=90, height=3)
        self.label_descricao_produto.grid(row=0, column=0, columnspan=2, padx=5, pady=(10), sticky="nsew")

        # Frame da esquerda
        self.frame_esquerda_produto = Frame(self.frame_principal, bg="white", height=610)
        self.frame_esquerda_produto.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        self.frame_esquerda_produto.grid_columnconfigure(0, weight=1)  # Expandir o frame na coluna 0
        self.frame_esquerda_produto.grid_rowconfigure(0, weight=1)  # Expandir o frame na linha 0

        # Frame da imagem do produto
        self.frame_imagem_produto = Frame(master=self.frame_esquerda_produto, bg="white", height=300)
        self.frame_imagem_produto.grid(row=2, column=0, columnspan=2 ,padx=5, pady=5, sticky="new")

        # Frame da direita
        self.frame_direita_treeview = Frame(self.frame_principal, bg="white", height=610)
        self.frame_direita_treeview.grid(row=1, column=1, padx=(10, 20), pady=10, sticky="nsew")

        # Frame da direita
        self.frame_footer = Frame(self.frame_principal, bg="blue", height=70)
        self.frame_footer.grid(row=2, column=0, columnspan=2, padx=(10, 20), pady=5, sticky="nsew")

    def Treeview(self):
        # Criação da Treeview
        self.treeview_produtos = ttk.Treeview(self.frame_direita_treeview, height=30, columns=("cod_produto", "descricao", "quantidade", "vlr_unitario", "vlr_total"), show="headings")
        self.treeview_produtos.heading("cod_produto", text="Cód. Produto")
        self.treeview_produtos.heading("descricao", text="Descrição")
        self.treeview_produtos.heading("quantidade", text="Qtdade.")
        self.treeview_produtos.heading("vlr_unitario", text="Vlr. Unitário")
        self.treeview_produtos.heading("vlr_total", text="Vlr. Total")

        self.treeview_produtos.column("cod_produto", width=100, anchor="center", stretch=False)
        self.treeview_produtos.column("descricao", width=230, anchor="w", stretch=False)
        self.treeview_produtos.column("quantidade", width=100, anchor="center", stretch=False)
        self.treeview_produtos.column("vlr_unitario", width=100, anchor="center", stretch=False)
        self.treeview_produtos.column("vlr_total", width=160, anchor="center", stretch=False)
        
        self.treeview_produtos.pack(fill="both", padx=2, pady=1, expand=True)

    def Label_frame_esquerdo(self):
        self.label_total_itens = Label(master=self.frame_esquerda_produto, text="TOTAL ITENS: ", font=("Arial", 20), bg="blue", fg="white", height=2)
        self.label_total_itens.grid(row=0, column=0, columnspan=2 ,padx=5, pady=5, sticky="new")

        self.label_total_compra = Label(master=self.frame_esquerda_produto, text="TOT. COMPRA: ", font=("Arial", 20), bg="blue", fg="white", height=2)
        self.label_total_compra.grid(row=1, column=0, columnspan=2 ,padx=5, pady=5, sticky="new")

    def Atalhos(self):
        # Criar um LabelFrame com título
        label_frame = LabelFrame(self.frame_esquerda_produto, text="Teclas de Atalho" ,padx=10, pady=10, fg="blue", height=150)
        label_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=0, sticky="nsew")

        # Adicionar widgets dentro do LabelFrame
        label_pesquisar = Label(label_frame, text="[ F1 ] Pesquisar produto", font="Roboto 14", anchor="w")
        label_pesquisar.grid(row=0, column=0, sticky="w", padx=20)

        label_dinheiro = Label(label_frame, text="[ F2 ] Dinheiro", font="Roboto 14", anchor="w")
        label_dinheiro.grid(row=1, column=0, sticky="w", padx=20)

        label_cartao = Label(label_frame, text="[ F3 ] Cartão", font="Roboto 14", anchor="w")
        label_cartao.grid(row=2, column=0, sticky="w", padx=20)

        label_pix = Label(label_frame, text="[ F4 ] PIX", font="Roboto 14", anchor="w")
        label_pix.grid(row=3, column=0, sticky="w", padx=20)

        label_cancelar_produto = Label(label_frame, text="[ DEL ] Cancelar produto", font="Roboto 14", anchor="w")
        label_cancelar_produto.grid(row=0, column=1, sticky="w", padx=20)

        label_cadastrar_produto = Label(label_frame, text="[ F5 ] Cadastrar produto", font="Roboto 14", anchor="w")
        label_cadastrar_produto.grid(row=1, column=1, sticky="w", padx=20)

        label_confirmar_produto = Label(label_frame, text="[ F6 ] Relatório de vendas", font="Roboto 14", anchor="w")
        label_confirmar_produto.grid(row=2, column=1, sticky="w", padx=20)

        label_esc_sair = Label(label_frame, text="[ ESC ] Fechar sistema", font="Roboto 14", anchor="w")
        label_esc_sair.grid(row=3, column=1, sticky="w", padx=20)
        #label_frame.grid_columnconfigure(1, weight=1)    

    def atualizar_hora(self):
        # Obter a data e hora atual
        data_hora_atual = datetime.now()

        # Formatar a data no formato brasileiro (dd/mm/aaaa)
        self.data_formatada = data_hora_atual.strftime("%d/%m/%Y")

        # Formatar a hora no formato brasileiro (hh:mm:ss)
        self.hora_formatada = data_hora_atual.strftime("%H:%M:%S")

        # Agendar a próxima atualização da hora após 1 segundo (1000 milissegundos)
        self.janela_pdv.after(1000, self.atualizar_hora)

        self.data = Label(self.frame_footer, text=self.data_formatada, height=2, width=20, anchor="w", justify="left", font="Roboto 12")
        self.data.grid(row=0, column=1, padx=2, pady=5)

        self.hora = Label(self.frame_footer, text=self.hora_formatada, height=2, width=20, anchor="w", justify="left", font="Roboto 12")
        self.hora.grid(row=0, column=3, padx=2, pady=5)

        # Puxar o nome do cliente e colocar na tela
        self.conn = sqlite3.connect("SistemaPDV.db")
        self.cursor = self.conn.cursor()
        select_query = "SELECT nameClient FROM UsersName"
        self.cursor.execute(select_query)
        result = self.cursor.fetchone()
        nome_cliente = result[0] if result else ""  # Obter o primeiro elemento da tupla ou uma string vazia se não houver resultado
        self.nome_cliente = Label(self.frame_footer, text=f"PDV: {nome_cliente}", height=2, width=20, anchor="w", justify="left", font="Roboto 12")
        self.nome_cliente.grid(row=0, column=4, padx=2, pady=5)
        self.cursor.close()


        # Atualizar os rótulos de data e hora
        self.data.config(text=self.data_formatada)
        self.hora.config(text=self.hora_formatada)

    def Entry_codigo_produto(self):
        self.entry_codigo = ctk.CTkEntry(self.frame_footer, placeholder_text="CÓDIGO E QUANTIDADE DO PRODUTO: EX: 2x0001", height=43 ,width=720, font=ctk.CTkFont(family="Roboto", size=16), text_color="black" ,bg_color="#252525", corner_radius=None)
        self.entry_codigo.grid(row=0, column=0 ,padx=5, pady=5)
        # Adiciona os eventos de binding ao campo "Código do Produto"
        self.entry_codigo.bind('<Return>', self.on_enter)

    def atualizar_treeview(self,codigo_produto):
        # Verifica se o código do produto está no formato correto
        if re.match(r'^\d+x\d+$', codigo_produto):
            # Separa a quantidade e o código do produto
            quantidade, codigo = codigo_produto.split('x')
            
            # Acessando o banco de dados para obter as informações do produto
            self.conn = sqlite3.connect("SistemaPDV.db")
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT descricao, preco_venda, caminho_imagem FROM produtos WHERE codigo_interno = ?", (codigo,))
            result = self.cursor.fetchone()
            
            if result:
                self.descricao = result[0]
                valor_unitario = result[1]
                self.cam_imagem = result[2]
                
                # Calcula o valor total
                self.quantidade = int(quantidade)
                self.valor_total = self.quantidade * valor_unitario

                # Adiciona os valores às quantidades e valores totais acumulados
                self.quantidade_total += self.quantidade
                self.valor_Total += self.valor_total
                self.label_descricao_produto["text"] = ""
                self.descricao_produto = self.descricao
                
                # Atualiza a Treeview com as informações do produto
                self.treeview_produtos.insert("", "end", values=(codigo, self.descricao, self.quantidade, valor_unitario, self.valor_total))

                # Atualiza a imagem
                self.atualizar_imagem()
                
                # Limpa o campo "Código do Produto"
                self.entry_codigo.delete(0, "end")

                # Atualiza as labels com os resultados acumulados
                self.atualizar_labels()
        
        else:
            pass
    
    def atualizar_labels(self):
        self.label_total_itens["text"] = f"TOTAL ITENS: {self.quantidade_total}"
        self.label_total_compra["text"] = f"TOT. COMPRA: R${self.valor_Total:.2f}"
        self.label_descricao_produto["text"] = f"{self.descricao_produto}"

    def atualizar_imagem(self):
        # Verificar se a imagem está disponível
        if self.cam_imagem and os.path.exists(self.cam_imagem):
            # Carregar a imagem selecionada
            imagem = Image.open(self.cam_imagem)

            # Definir o tamanho fixo para o frame de imagem
            largura_frame = 350  # Defina a largura desejada
            altura_frame = 300  # Defina a altura desejada
            self.frame_imagem_produto.config(width=largura_frame, height=altura_frame)

            # Redimensionar a imagem para caber no frame
            imagem_redimensionada = imagem.resize((largura_frame, altura_frame))

            # Criar um objeto PhotoImage com a imagem redimensionada
            self.foto = ImageTk.PhotoImage(imagem_redimensionada)

            # Criar um Label para exibir a imagem
            if self.label_imagem_prod is not None:
                # Atualizar a imagem existente
                self.label_imagem_prod.configure(image=self.foto)
                self.label_imagem_prod.image = self.foto  # Atualizar a referência da imagem
            else:
                # Criar uma nova imagem
                self.label_imagem_prod = Label(self.frame_imagem_produto, image=self.foto)
                self.label_imagem_prod.pack(fill="both", expand=True)
        else:
            # Se a imagem não estiver disponível, limpar a imagem existente
            if self.label_imagem_prod is not None:
                self.label_imagem_prod.configure(image=None)
                self.label_imagem_prod.pack_forget()
                self.label_imagem_prod = None  # Defina self.label_imagem_prod como None

    def on_enter(self, event=None):  # "event=None" como argumento padrão
        codigo_produto = self.entry_codigo.get()
        self.atualizar_treeview(codigo_produto)
        # Atualiza as labels com os resultados
        self.atualizar_labels()

# Função para criar frame de cadastro e cadastrar produtos
    def criar_frame_cadastro(self):
        # Destruir os frames existentes
        self.label_descricao_produto.destroy()
        self.frame_esquerda_produto.destroy()
        self.frame_direita_treeview.destroy()
        self.frame_footer.destroy()

        # Criar um novo frame para o cadastro
        self.frame_principal.config(background="#0063A6")
        self.janela_pdv.config(background="#0063A6")
        self.frame_cadastro = Frame(self.frame_principal, bg="white")
        self.frame_cadastro.grid(row=0, column=0, padx=400, pady=90, sticky="nsew")

        # Adicionar o "título" como um frame vazio
        self.frame_titulo = Frame(self.frame_cadastro, bg="blue", height=45)
        self.frame_titulo.grid(row=0, column=0, columnspan=8,sticky="ew")

        # Adicionar os botões ao Frame de botões
        self.frame_btn = Frame(self.frame_cadastro, bg="white", height=60)
        self.frame_btn.grid(row=1, column=0, columnspan=8, sticky="ew")

        self.frame_imagem = Frame(self.frame_cadastro, background="white")
        self.frame_imagem.grid(row=5, column=5, columnspan=3, rowspan=4, sticky="nsew")

        self.titulo_cadastro = Label(self.frame_titulo, text="Cadastro de Produtos", font=("Arial", 10), background="blue", fg="white")
        self.titulo_cadastro.grid(row=0, column=0, columnspan=8 , sticky="ew", padx=10)

        # Adicionar widgets e lógica específica do cadastro aqui

        # Adicionar botões para funcionalidades
        # Carregar a imagem e atribuir a um atributo da classe
        self.imagem_novo = PhotoImage(file="img/icons/icone-novo-50x50.png").subsample(1, 1)
        btn_novo = Button(self.frame_btn, text="Novo", image=self.imagem_novo, compound="top", width=70, command=self.Limpar_campos_entrys)
        btn_novo.grid(row=0, column=0, pady=5)

        # Carregar a imagem e atribuir a um atributo da classe
        self.imagem_pesquisar = PhotoImage(file="img/icons/icone-pesquisar-50x50.png").subsample(1, 1)
        btn_pesquisar = Button(self.frame_btn, text="Pesquisar", image=self.imagem_pesquisar, compound="top", width=70, command=self.pesquisar_produto)
        btn_pesquisar.grid(row=0, column=1, padx=5, pady=5)

        # Carregar a imagem e atribuir a um atributo da classe
        self.imagem_limpar = PhotoImage(file="img/icons/icone-limpar-50x50.png").subsample(1, 1)
        btn_limpar = Button(self.frame_btn, text="Limpar", image=self.imagem_limpar, compound="top", width=70, command=self.Limpar_campos_entrys)
        btn_limpar.grid(row=0, column=2, padx=5, pady=5)

        # Carregar a imagem e atribuir a um atributo da classe
        self.imagem_excluir = PhotoImage(file="img/icons/icone-excluir-50x50.png").subsample(1, 1)
        btn_excluir = Button(self.frame_btn, text="Excluir", image=self.imagem_excluir, compound="top", width=70, command=self.excluir_produto)
        btn_excluir.grid(row=0, column=3, padx=5, pady=5)

        # Carregar a imagem e atribuir a um atributo da classe
        self.imagem_gravar = PhotoImage(file="img/icons/icone-salvar-50x50.png").subsample(1, 1)
        btn_gravar = Button(self.frame_btn, text="Gravar", image=self.imagem_gravar, compound="top", width=70, command=self.armazenar_dados_produtos)
        btn_gravar.grid(row=0, column=4, padx=5, pady=5)

        # Carregar a imagem e atribuir a um atributo da classe
        self.imagem_alterar = PhotoImage(file="img/icons/icone-alterar-50x50.png").subsample(1, 1)
        btn_alterar = Button(self.frame_btn, text="At. Produto", image=self.imagem_alterar, compound="top", width=70, command=self.alterar_preco_produto)
        btn_alterar.grid(row=0, column=5, padx=5, pady=5)

        # Botão para retornar à tela principal
        # Carregar a imagem e atribuir a um atributo da classe
        self.imagem_voltar = PhotoImage(file="img/icons/icon-voltar-50x50.png").subsample(1, 1)
        btn_voltar = Button(self.frame_btn, text="Sair", image=self.imagem_voltar, compound="top", width=70, command=self.voltar_para_tela_principal)
        btn_voltar.grid(row=0, column=6, padx=5, pady=5)

        # Labels e Entrys para o código
        self.lb_cod_interno = ctk.CTkLabel(self.frame_cadastro, text="Cód. Interno :", anchor="e", font=ctk.CTkFont(family="Roboto", size=13), text_color="blue" ,bg_color="white")
        self.lb_cod_interno.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        self.enty_cod_interno = ctk.CTkEntry(self.frame_cadastro)
        self.enty_cod_interno.grid(row=2, column=1, columnspan=3, sticky="ew", padx=0, pady=5)

        # Labels e Entrys para a data atualização
        self.lb_data_atualizacao = ctk.CTkLabel(self.frame_cadastro, text="Data. Atualização :", anchor="e", font=ctk.CTkFont(family="Roboto", size=13), text_color="blue" ,bg_color="white")
        self.lb_data_atualizacao.grid(row=2, column=4, columnspan=2, sticky="w", padx=15, pady=5)
        self.enty_data_atualizacao = ctk.CTkEntry(self.frame_cadastro)
        self.enty_data_atualizacao.grid(row=2, column=5, columnspan=2, sticky="ew", padx=0, pady=5)

        # Labels e Entrys para a descrição
        self.lb_descricao = ctk.CTkLabel(self.frame_cadastro, text="Descrição :", anchor="e", font=ctk.CTkFont(family="Roboto", size=13), text_color="blue" ,bg_color="white")
        self.lb_descricao.grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.enty_descricao = ctk.CTkEntry(self.frame_cadastro)
        self.enty_descricao.grid(row=3, column=1, columnspan=9, sticky="ew", padx=2, pady=5)

        # Labels e Entrys para preço custo
        self.lb_preco_custo = ctk.CTkLabel(self.frame_cadastro, text="Preço custo :", anchor="e", font=ctk.CTkFont(family="Roboto", size=13), text_color="blue" ,bg_color="white")
        self.lb_preco_custo.grid(row=4, column=0, sticky="e", padx=10, pady=5)
        self.enty_preco_custo = ctk.CTkEntry(self.frame_cadastro)
        self.enty_preco_custo.grid(row=4, column=1, columnspan=2, sticky="ew", padx=2, pady=5)

        # Labels e Entrys para preço ipi
        self.lb_IPI = ctk.CTkLabel(self.frame_cadastro, text="% I.P.I :", anchor="e", font=ctk.CTkFont(family="Roboto", size=13), text_color="blue" ,bg_color="white")
        self.lb_IPI.grid(row=4, column=3, sticky="e", padx=10, pady=5)
        self.enty_IPI = ctk.CTkEntry(self.frame_cadastro)
        self.enty_IPI.grid(row=4, column=4, sticky="ew", padx=2, pady=5)

        # Labels e Entrys para preço lucro
        self.lb_preco_lucro = ctk.CTkLabel(self.frame_cadastro, text="% Lucro :", anchor="e", font=ctk.CTkFont(family="Roboto", size=13), text_color="blue" ,bg_color="white")
        self.lb_preco_lucro.grid(row=4, column=5, sticky="e", padx=10, pady=5)
        self.enty_preco_lucro = ctk.CTkEntry(self.frame_cadastro)
        self.enty_preco_lucro.grid(row=4, column=6, sticky="ew", padx=2, pady=5)

        #Label e Entrys para preço de venda
        self.lb_preco_venda = ctk.CTkLabel(self.frame_cadastro, text="Preço venda :", anchor="e", font=ctk.CTkFont(family="Roboto", size=13), text_color="blue" ,bg_color="white")
        self.lb_preco_venda.grid(row=5, column=0, sticky="e", padx=10, pady=5)
        self.enty_preco_venda = ctk.CTkEntry(self.frame_cadastro)
        self.enty_preco_venda.grid(row=5, column=1, columnspan=2, sticky="ew", padx=2, pady=5)

        # Labels e Entrys para preço quantidade minima
        self.lb_qtde_minima = ctk.CTkLabel(self.frame_cadastro, text="Qtde Minima :", anchor="e", font=ctk.CTkFont(family="Roboto", size=13), text_color="blue" ,bg_color="white")
        self.lb_qtde_minima.grid(row=5, column=3, sticky="e", padx=10, pady=5)
        self.enty_qtde_minima = ctk.CTkEntry(self.frame_cadastro)
        self.enty_qtde_minima.grid(row=5, column=4, sticky="ew", padx=2, pady=5)

        # Botão "Add Imagem"
        self.btn_add_imagem = Button(self.frame_imagem, text="Add Imagem", command=self.adicionar_imagem, bg="white", fg="blue")
        self.btn_add_imagem.pack(side="top", anchor="w" ,pady=2, padx=2)

        # Labels e Entrys para Marca do produto
        self.lb_marca = ctk.CTkLabel(self.frame_cadastro, text="Marca :", anchor="e", font=ctk.CTkFont(family="Roboto", size=13), text_color="blue" ,bg_color="white")
        self.lb_marca.grid(row=6, column=0, sticky="e", padx=10, pady=5)
        self.enty_marca = ctk.CTkEntry(self.frame_cadastro)
        self.enty_marca.grid(row=6, column=1, columnspan=4 ,sticky="ew", padx=2, pady=5)

        # Labels e Entrys para Fornecedor do produto
        self.lb_fornecedor = ctk.CTkLabel(self.frame_cadastro, text="Fornecedor :", anchor="e", font=ctk.CTkFont(family="Roboto", size=13), text_color="blue" ,bg_color="white")
        self.lb_fornecedor.grid(row=7, column=0, sticky="e", padx=10, pady=5)
        self.enty_fornecedor = ctk.CTkEntry(self.frame_cadastro)
        self.enty_fornecedor.grid(row=7, column=1, columnspan=4 ,sticky="ew", padx=2, pady=5)

        # Labels e Entrys para Estoque
        self.lb_estoque = ctk.CTkLabel(self.frame_cadastro, text="Estoque :", anchor="e", font=ctk.CTkFont(family="Roboto", size=13), text_color="blue" ,bg_color="white")
        self.lb_estoque.grid(row=8, column=0, sticky="e", padx=10, pady=5)
        self.enty_estoque = ctk.CTkEntry(self.frame_cadastro)
        self.enty_estoque.grid(row=8, column=1, columnspan=4 ,sticky="ew", padx=2, pady=5)

        # Criar um LabelFrame com título e ajuda
        self.label_frame_ajuda = LabelFrame(self.frame_cadastro, text="Ajuda" ,padx=10, pady=10, fg="red", height=200)
        self.label_frame_ajuda.grid(row=9, column=0, columnspan=8, padx=2, pady=0, sticky="nsew")

        # Ajuda imagem
        lb_ajuda_imagem = Label(self.label_frame_ajuda, text="A imagem do produto é opcional.", anchor="w", padx=2, pady=2)
        lb_ajuda_imagem.grid(row=0, column=0)

        # Ajuda código do produto
        lb_ajuda_imagem = Label(self.label_frame_ajuda, text="O código do produto é obrigatório.", anchor="w", padx=2, pady=2)
        lb_ajuda_imagem.grid(row=1, column=0)

        # Ajuda Nome do produto
        lb_ajuda_imagem = Label(self.label_frame_ajuda, text="O Nome do produto é obrigatório.", anchor="w", padx=2, pady=2)
        lb_ajuda_imagem.grid(row=2, column=0)
    
    def Receber_variaveis_produtos(self):
        self.cod_produto = self.enty_cod_interno.get()
        self.data_atualizacao = self.enty_data_atualizacao.get()
        self.descricao = self.enty_descricao.get()
        self.preco_custo = self.enty_preco_custo.get()
        self.IPI = self.enty_IPI.get()
        self.preco_lucro = self.enty_preco_lucro.get()
        self.preco_venda = self.enty_preco_venda.get()
        self.qtde_minima = self.enty_qtde_minima.get()
        self.marca = self.enty_marca.get()
        self.fornecedor = self.enty_fornecedor.get()
        self.estoque = self.enty_estoque.get()

    def Limpar_campos_entrys(self):
        # Limpar os campos
        self.enty_cod_interno.delete(0, 'end')
        self.enty_data_atualizacao.delete(0, 'end')
        self.enty_descricao.delete(0, 'end')
        self.enty_preco_custo.delete(0, 'end')
        self.enty_IPI.delete(0, 'end')
        self.enty_preco_lucro.delete(0, 'end')
        self.enty_preco_venda.delete(0, 'end')
        self.enty_qtde_minima.delete(0, 'end')
        self.enty_marca.delete(0, 'end')
        self.enty_fornecedor.delete(0, 'end')
        self.enty_estoque.delete(0, 'end')
        # Verificar se um arquivo foi selecionado
        self.limpar_imagem()

    def limpar_imagem(self):
        # Limpa a imagem anterior, se houver
        if self.label_imagem:
            self.label_imagem.pack_forget()
            self.label_imagem = None  # Definir a variável como None para indicar que não há imagem no momento

    def adicionar_imagem(self):
        # Abrir o diálogo de seleção de arquivo
        filetypes = (("Arquivos de Imagem", "*.jpg;*.jpeg;*.png"), ("Todos os arquivos", "*.*"))
        self.filename = filedialog.askopenfilename(filetypes=filetypes)

        # Verificar se um arquivo foi selecionado
        if self.filename:
            # Obter o caminho absoluto do arquivo
            abs_path = os.path.abspath(self.filename)

            # Carregar a imagem selecionada
            imagem = Image.open(abs_path)

            # Atualizar as dimensões do frame
            self.frame_imagem.update()
            largura_frame = self.frame_imagem.winfo_width()
            altura_frame = self.frame_imagem.winfo_height()

            # Redimensionar a imagem para caber no frame
            imagem_redimensionada = imagem.resize((largura_frame, altura_frame))

            # Criar um objeto PhotoImage com a imagem redimensionada
            foto = ImageTk.PhotoImage(imagem_redimensionada)

            # Criar um Label para exibir a imagem
            self.label_imagem = Label(self.frame_imagem, image=foto)
            self.label_imagem.image = foto  # Salvar uma referência para evitar a coleta de lixo
            self.label_imagem.pack(fill="both", expand=True)

            # Armazenar o caminho absoluto do arquivo para uso posterior
            self.caminho_imagem = abs_path
            #print(self.caminho_imagem)

    def armazenar_dados_produtos(self):
        # Obter os valores das Entries
        self.Receber_variaveis_produtos()

        # Verificar se o código já existe no banco de dados
        conn = sqlite3.connect("SistemaPDV.db")
        cursor = conn.cursor()

        select_query = "SELECT codigo_interno FROM produtos WHERE codigo_interno = ?"
        cursor.execute(select_query, (self.cod_produto,))
        resultado = cursor.fetchone()

        if resultado is not None:
            messagebox.showinfo("Error", "Esse código já está sendo utilizado. Por favor, escolha outro.")
            conn.close()
            return

        # Inserir os dados na tabela produtos
        insert_query = "INSERT INTO produtos (codigo_interno, data_atualizacao, descricao, preco_custo, ipi, lucro, preco_venda, qtde_minima, caminho_imagem, marca, fornecedor, estoque) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        messagebox.showinfo("Sucesso", "Produtos cadastrados com sucesso!")  # 267cb5
        self.caminho_imagem_vazio = "None"

        if self.caminho_imagem:
            # Se o caminho da imagem existir, usar o valor normalmente
            cursor.execute(insert_query, (
                self.cod_produto, self.data_atualizacao, self.descricao, self.preco_custo, self.IPI, self.preco_lucro,
                self.preco_venda, self.qtde_minima, self.caminho_imagem, self.marca, self.fornecedor, self.estoque))
        else:
            # Se o caminho da imagem for vazio, passar None ou uma string vazia
            cursor.execute(insert_query, (
                self.cod_produto, self.data_atualizacao, self.descricao, self.preco_custo, self.IPI, self.preco_lucro,
                self.preco_venda, self.qtde_minima, self.caminho_imagem_vazio, self.marca, self.fornecedor,
                self.estoque))

        # Commit para salvar as alterações no banco de dados
        conn.commit()

        # Fechar a conexão com o banco de dados
        conn.close()
        self.Limpar_campos_entrys()

# Função para pesquisar, excluir, alterar produtos
    def pesquisar_produto(self):
        # Obter o código interno digitado pelo usuário
        codigo_produto = self.enty_cod_interno.get()

        # Verificar se o código está no formato correto
        if re.match(r'^\d+$', codigo_produto):
            # Acessar o banco de dados para obter as informações do produto
            self.conn = sqlite3.connect("SistemaPDV.db")
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT data_atualizacao, descricao, preco_custo, ipi ,lucro, preco_venda, qtde_minima, caminho_imagem, marca, fornecedor, estoque FROM produtos WHERE codigo_interno = ?", (codigo_produto,))
            result = self.cursor.fetchone()

            if result:
                # Atualizar os campos com as informações do produto
                data_atualizacao, descricao, preco_custo, ipi, lucro, preco_venda, qtde_minima, caminho_imagem, marca, fornecedor, estoque = result

                # Atualizar os campos com as informações do produto encontrado
                self.enty_data_atualizacao.delete(0, "end")
                self.enty_data_atualizacao.insert(0, data_atualizacao)

                self.enty_descricao.delete(0, "end")
                self.enty_descricao.insert(0, descricao)

                self.enty_preco_custo.delete(0, "end")
                self.enty_preco_custo.insert(0, preco_custo)

                self.enty_IPI.delete(0, "end")
                self.enty_IPI.insert(0, ipi)

                self.enty_preco_lucro.delete(0, "end")
                self.enty_preco_lucro.insert(0, lucro)

                self.enty_preco_venda.delete(0, "end")
                self.enty_preco_venda.insert(0, preco_venda)

                self.enty_qtde_minima.delete(0, "end")
                self.enty_qtde_minima.insert(0, qtde_minima)

                self.enty_marca.delete(0, "end")
                self.enty_marca.insert(0, marca)

                self.enty_fornecedor.delete(0, "end")
                self.enty_fornecedor.insert(0, fornecedor)

                self.enty_estoque.delete(0, "end")
                self.enty_estoque.insert(0, estoque)

                # Atualizar a imagem na interface
                imagem = Image.open(caminho_imagem)

                # Atualizar as dimensões do frame
                self.frame_imagem.update()
                # Definir o tamanho fixo para o frame de imagem
                largura_frame = 200  # Defina a largura desejada
                altura_frame = 150  # Defina a altura desejada
                self.frame_imagem.config(width=largura_frame, height=altura_frame)

                # Redimensionar a imagem para caber no frame
                imagem_redimensionada = imagem.resize((largura_frame, altura_frame))

                # Criar um objeto PhotoImage com a imagem redimensionada
                self.foto = ImageTk.PhotoImage(imagem_redimensionada)

                # Criar ou atualizar o Label para exibir a imagem
                if self.label_imagem is None:
                    self.label_imagem = Label(self.frame_imagem, image=self.foto)
                    self.label_imagem.pack(fill="both", expand=True)
                else:
                    self.label_imagem.configure(image=self.foto)
                    self.label_imagem.image = self.foto  # Salvar uma referência para evitar a coleta de lixo
                    self.limpar_imagem()
            else:
                # Produto não encontrado, exibir mensagem de erro
                messagebox.showerror("Erro", "Produto não encontrado no banco de dados.")
        else:
            # Código inválido, exibir mensagem de erro
            messagebox.showerror("Erro", "Código inválido. Certifique-se de digitar apenas números.")

    def excluir_produto(self):
        # Obter o código interno digitado pelo usuário
        codigo_produto = self.enty_cod_interno.get()

        # Verificar se o código está no formato correto
        if re.match(r'^\d+$', codigo_produto):
            # Conectar ao banco de dados
            conn = sqlite3.connect("SistemaPDV.db")
            cursor = conn.cursor()

            # Verificar se o produto com o código interno informado existe no banco de dados
            cursor.execute("SELECT * FROM produtos WHERE codigo_interno = ?", (codigo_produto,))
            result = cursor.fetchone()

            if result:
                # Confirmar a exclusão com o usuário antes de prosseguir
                confirmar = messagebox.askyesno("Confirmar exclusão", "Tem certeza que deseja excluir o produto?")
                if confirmar:
                    # Excluir o produto do banco de dados
                    cursor.execute("DELETE FROM produtos WHERE codigo_interno = ?", (codigo_produto,))
                    conn.commit()
                    conn.close()

                    # Limpar os campos após a exclusão
                    self.Limpar_campos_entrys()

                    # Exibir mensagem de sucesso
                    messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
            else:
                # Produto não encontrado, exibir mensagem de erro
                messagebox.showerror("Erro", "Produto não encontrado no banco de dados.")
        else:
            # Código inválido, exibir mensagem de erro
            messagebox.showerror("Erro", "Código inválido. Certifique-se de digitar apenas números.")

    def alterar_preco_produto(self):
        # Obter o código interno digitado pelo usuário
        codigo_produto = self.enty_cod_interno.get()

        # Verificar se o código está no formato correto
        if re.match(r'^\d+$', codigo_produto):
            # Acessar o banco de dados para obter as informações do produto
            self.conn = sqlite3.connect("SistemaPDV.db")
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT * FROM produtos WHERE codigo_interno = ?", (codigo_produto,))
            result = self.cursor.fetchone()

            if result:
                campos_banco = [
                    "codigo_interno",
                    "data_atualizacao",
                    "descricao",
                    "preco_custo",
                    "ipi",
                    "lucro",
                    "preco_venda",
                    "qtde_minima",
                    "caminho_imagem",
                    "marca",
                    "fornecedor",
                    "estoque"
                ]

                campos_atual = [
                    self.enty_cod_interno.get(),
                    self.enty_data_atualizacao.get(),
                    self.enty_descricao.get(),
                    float(self.enty_preco_custo.get()),
                    float(self.enty_IPI.get()),
                    float(self.enty_preco_lucro.get()),
                    float(self.enty_preco_venda.get()),
                    int(self.enty_qtde_minima.get()),
                    self.filename if hasattr(self, 'filename') else None,
                    self.enty_marca.get(),
                    self.enty_fornecedor.get(),
                    int(self.enty_estoque.get())
                ]

                # Verificar quais campos foram alterados
                campos_diferentes = [i for i in range(len(campos_banco)) if campos_banco[i] != campos_atual[i]]

                if campos_diferentes:
                    # Montar a mensagem de confirmação com as informações que serão alteradas
                    mensagem_confirmacao = "Deseja alterar os seguintes campos?\n"
                    for indice in campos_diferentes:
                        mensagem_confirmacao += f"{campos_banco[indice]}: {campos_atual[indice]}\n"

                    # Exibir mensagem de confirmação ao usuário
                    resposta = messagebox.askyesno("Confirmar Alteração", mensagem_confirmacao)
                    if resposta == True:
                        # Atualizar as informações do produto no banco de dados
                        for indice in campos_diferentes:
                            self.cursor.execute(f"UPDATE produtos SET {campos_banco[indice]} = ? WHERE codigo_interno = ?", (campos_atual[indice], codigo_produto))
                        self.conn.commit()
                        messagebox.showinfo("Sucesso", "Produto alterado com sucesso!")
                        # Atualizar a imagem na interface
                        self.atualizar_imagem()
                    else:
                        messagebox.showinfo("Alteração Cancelada", "A alteração foi cancelada pelo usuário.")
                else:
                    messagebox.showinfo("Nenhuma Alteração", "Não há alterações nos campos do produto.")
            else:
                # Produto não encontrado, exibir mensagem de erro
                messagebox.showerror("Erro", "Produto não encontrado no banco de dados.")
        else:
            # Código inválido, exibir mensagem de erro
            messagebox.showerror("Erro", "Código inválido. Certifique-se de digitar apenas números.")

    def atualizar_codigo_produto(self, codigo_produto):
        # Atualizar o valor do entry_codigo
        self.entry_codigo.delete(0, "end")
        self.entry_codigo.insert(0, f"1x{codigo_produto}")

    def calcular_valores(self):
        total_quantidade = 0
        total_valor = 0

        # Percorre os itens da Treeview e calcula os valores
        for item in self.treeview_produtos.get_children():
            quantidade = int(self.treeview_produtos.item(item, "values")[2])
            valor_total = float(self.treeview_produtos.item(item, "values")[4])
            total_quantidade += quantidade
            total_valor += valor_total

        # Atualiza as Labels com os novos valores
        self.label_total_itens.config(text=f"TOTAL ITENS: {total_quantidade}")
        self.label_total_compra.config(text=f"TOT. COMPRA: R$ {total_valor:.2f}")
        self.quantidade_total = 0
        self.valor_Total = 0

    def calcular_total_compra(self):
        total_compra = 0.0
        produtos_quantidades = []  # Lista para armazenar os nomes dos produtos e suas quantidades

        for item in self.treeview_produtos.get_children():
            preco_unitario = float(self.treeview_produtos.item(item, "values")[3])
            quantidade = int(self.treeview_produtos.item(item, "values")[2])
            total_item = preco_unitario * quantidade
            total_compra += total_item

            # Obtém o nome do produto e sua quantidade e adiciona à lista
            produto = self.treeview_produtos.item(item, "values")[1]
            produtos_quantidades.append((produto, quantidade))

        return total_compra, produtos_quantidades

    def criar_interface_tela_principal(self):
        self.Criar_Interface()
        self.Treeview()
        self.Label_frame_esquerdo()
        self.Atalhos()
        self.atualizar_hora()  # Iniciar a atualização da hora
        self.Entry_codigo_produto()
        self.on_enter()
        self.teclas_atalho = TeclasDeAtalho(self.janela_pdv, self)

    def voltar_para_tela_principal(self):
        # Destruir o frame de cadastro
        self.frame_cadastro.destroy()

        # Destruir o frame principal atual
        self.frame_principal.destroy()

        # Recriar a interface da tela principal
        self.criar_interface_tela_principal()

    # NOVO CAMPO ALTERADO PARA NOVA FORMA DE PAGAMENTO
    def obter_produtos_selecionados(self):
        # Implemente aqui a lógica para obter a lista de produtos selecionados
        produtos_selecionados = []
        total_compra = 0  # Variável para armazenar o total da compra

        for item in self.treeview_produtos.get_children():
            codigo = self.treeview_produtos.item(item, "values")[0]
            descricao = self.treeview_produtos.item(item, "values")[1]
            quantidade = self.treeview_produtos.item(item, "values")[2]
            valor_unitario = float(self.treeview_produtos.item(item, "values")[3])
            valor_total = float(self.treeview_produtos.item(item, "values")[4])
            total_compra += float(valor_total)  # Somar ao total da compra

            produtos_selecionados.append((codigo, descricao, quantidade, valor_unitario, valor_total))

        # Retornar o total da compra e a lista de produtos selecionados
        return total_compra, produtos_selecionados

    def Fechar_Tela(self):
        self.janela_pdv.destroy()

    def encerrar_programa(self, event=None):
        # Encerrar o programa
        confirm = messagebox.askyesno("Encerrar programa", "Deseja encerrar o programa?")
        if confirm:
            self.janela_pdv.destroy()
        else:
            pass