from tkinter import Tk, PhotoImage, messagebox, Label
import customtkinter as ctk
import sqlite3
from ClasseTelaUsuario import TelaUsuario


class ApplicationLogin:
    def __init__(self):
        self.janela = Tk()
        self.Conectar_Banco()
        self.Tema()
        self.Tela()
        self.Tela_Login()
        self.Campo_Entrys()
        # Bind the <Return> event to the entry fields and button
        self.entry_username.bind("<Return>", self.enter)
        self.entry_password.bind("<Return>", self.enter)
        self.janela.mainloop()

    def Conectar_Banco(self):
        self.conn = sqlite3.connect("SistemaPDV.db")
        self.cursor = self.conn.cursor()

        # Criar a tabela "UsersName"
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS UsersName (
            Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            userName TEXT NOT NULL,
            userPassword TEXT NOT NULL,
            nameClient TEXT NOT NULL)
        """)
        # Criar a tabela "produtos"
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
            codigo_interno TEXT NOT NULL,
            data_atualizacao TEXT,
            descricao TEXT NOT NULL,
            preco_custo REAL NOT NULL,
            ipi REAL,
            lucro REAL,
            preco_venda REAL NOT NULL,
            qtde_minima REAL,
            caminho_imagem TEXT,
            marca TEXT,
            fornecedor TEXT,
            estoque REAL NOT NULL)
        """)
        # Criar a tabela "relatorios_vendas"
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS relatorios_vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                nome_produto TEXT,
                total_compra REAL,
                quantidade_vendida REAL,
                forma_pagamento TEXT,
                valor_pago REAL,
                troco REAL)
        """)

        # Verificando se o usuário admin123 já existe
        select_query = "SELECT * FROM UsersName WHERE userName = ? AND userPassword = ?"
        self.cursor.execute(select_query, ("admin123", "admin123"))
        result = self.cursor.fetchone()

        if result is None:
            # Inserindo novo registro com usuário e senha admin123
            insert_query = "INSERT INTO UsersName (userName, userPassword, nameClient) VALUES (?, ?, ?)"
            self.cursor.execute(insert_query, ("admin123", "admin123", "Adiministrador"))
            self.conn.commit()

    # DEFININDO O TEMA
    def Tema(self):
        self.janela.configure(bg="#252525")

    # CONFIGURANDO A JANELA
    def Tela(self):
        self.janela.geometry("700x400+500+200")
        self.janela.title("Area de login")
        self.janela.iconbitmap("img/icons/Logo-caixa.ico")
        self.janela.resizable(False, False)

    # CAMPO DE LOGIN
    def Tela_Login(self):
        self.img = PhotoImage(file="img/icons/Logo-login.png")
        self.label_img = Label(master=self.janela, image=self.img, background="#252525")
        self.label_img.place(x=5, y=50)

        # FRAME DA JANELA DE LOGIN
        self.frame_login = ctk.CTkFrame(master=self.janela, width=360, height=400, fg_color="#252525", corner_radius=0)
        self.frame_login.pack(side="right")

        # CAMPO DE LABELS
        self.label_ = ctk.CTkLabel(master=self.janela, text="SISTEMA DE PDV",
                                   font=ctk.CTkFont(family="Roboto", size=22), text_color="white", bg_color="#252525",
                                   corner_radius=None)
        self.label_.place(x=70, y=5)
        self.label_ = ctk.CTkLabel(master=self.frame_login, text="EFETUAR LOGIN",
                                   font=ctk.CTkFont(family="Roboto", size=19), text_color="white", bg_color="#252525",
                                   corner_radius=None)
        self.label_.place(x=100, y=7)

    def Campo_Entrys(self):
        # CAMPO DE ENTRY PARA RECEBER VARIÁVEIS DE LOGIN E SENHA
        self.entry_username = ctk.CTkEntry(master=self.frame_login, placeholder_text="Entre com Usuario", width=300,
                                           height=45, font=ctk.CTkFont(family="Roboto", size=14), text_color="black",
                                           bg_color="#252525", corner_radius=None)
        self.entry_username.place(x=30, y=60)

        self.lb_alert_obg = ctk.CTkLabel(master=self.frame_login, text="*O campo de usuario é de carater obrigatório",
                                         text_color="green", bg_color="#252525", corner_radius=None)
        self.lb_alert_obg.place(x=30, y=109)

        self.entry_password = ctk.CTkEntry(master=self.frame_login, placeholder_text="Entre com a Senha", width=300,
                                           height=45, font=ctk.CTkFont(family="Roboto", size=14), show="*",
                                           text_color="black", bg_color="#252525", corner_radius=None)
        self.entry_password.place(x=30, y=150)
        self.lb_alert_obg = ctk.CTkLabel(master=self.frame_login, text="*O campo de senha é de carater obrigatório",
                                         text_color="green", bg_color="#252525", corner_radius=None)
        self.lb_alert_obg.place(x=30, y=200)

        # CAMPO DE CHECKBOX
        self.check_box = ctk.CTkCheckBox(master=self.frame_login, text="Lembrar senha", hover_color="blue",
                                         text_color="white", bg_color="#252525", corner_radius=None)
        self.check_box.place(x=30, y=240)

        # CAMPO DE BOTÕES
        self.button = ctk.CTkButton(master=self.frame_login, text="Entrar", command=self.Verificar_Login, width=300,
                                    height=45, hover_color="blue", font=ctk.CTkFont(family="Roboto", size=20),
                                    text_color="white", bg_color="#252525", corner_radius=None)
        self.button.place(x=30, y=280)

    def Receber_Variaveis_Login(self):
        self.username = str(self.entry_username.get())
        self.userpassword = str(self.entry_password.get())

    def enter(self, event=None):
        self.Verificar_Login()

    def Verificar_Login(self):
        self.Receber_Variaveis_Login()
        veri_login = "SELECT * FROM UsersName WHERE userName like '" + self.username + "'AND userPassword like '" + self.userpassword + "'"
        self.cursor.execute(veri_login)
        validado = self.cursor.fetchall()
        if len(validado) > 0:
            messagebox.showinfo(title="Login bem-sucedido", message="Login realizado com sucesso!")
            self.janela.withdraw()  # Oculta a janela de login
            tela_usuario = TelaUsuario(self.janela)  # Abre a tela do usuário
        elif validado == "":
            messagebox.showinfo(title="Erro", message="Preencha todos os campos!!")
            self.Verificar_Login()
        else:
            messagebox.showerror(title="Erro de Login", message="Verifique usuário e senha!!")

    def Abrir_Tela_Usuario(self):
        self.janela.withdraw()  # Oculta a janela de login
        tela_usuario = TelaUsuario(self.janela)  # Abre a tela do usuário


def main():
    app = ApplicationLogin()


if __name__ == "__main__":
    main()