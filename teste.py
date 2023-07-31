from tkinter import Tk, Button, PhotoImage

class MinhaApp:
    def __init__(self):
        self.janela = Tk()
        self.janela.title("Exemplo de Botão com Imagem")
        
        # Carregar a imagem e atribuir a um atributo da classe
        self.imagem_novo = PhotoImage(file="img/icons/icone-novo.png").subsample(7, 10)

        btn_novo = Button(self.janela, text="Novo", image=self.imagem_novo, compound="top", command=self.Limpar_campos_entrys)
        btn_novo.grid(row=0, column=0, pady=5)

    def Limpar_campos_entrys(self):
        # Implemente a função de limpar campos aqui
        pass

    def run(self):
        self.janela.mainloop()

app = MinhaApp()
app.run()
