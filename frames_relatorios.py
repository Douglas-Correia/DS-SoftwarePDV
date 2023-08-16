import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gráficos de Receitas e Despesas")

        # Crie um botão para gerar os gráficos
        btn_show_graphs = tk.Button(root, text="Gerar Gráficos", command=self.plot_graphs)
        btn_show_graphs.pack()

    def plot_graphs(self):
        # Dados de exemplo para as datas e valores de receitas e despesas
        datas = ["01-08-2023", "02-08-2023", "03-08-2023", "04-08-2023", "05-08-2023"]
        receitas = [200, 300, 250, 400, 350]
        despesas = [50, 70, 60, 80, 90]

        # Crie uma figura para o gráfico de Receitas
        fig_receitas = plt.figure(figsize=(6, 4))
        plt.bar(datas, receitas, color='green')
        plt.xlabel('Datas')
        plt.ylabel('Receitas')
        plt.title('Gráfico de Receitas')
        plt.xticks(rotation=45)
        canvas_receitas = FigureCanvasTkAgg(fig_receitas, master=self.root)
        canvas_receitas.get_tk_widget().pack()

        # Crie uma figura para o gráfico de Despesas
        fig_despesas = plt.figure(figsize=(6, 4))
        plt.bar(datas, despesas, color='red')
        plt.xlabel('Datas')
        plt.ylabel('Despesas')
        plt.title('Gráfico de Despesas')
        plt.xticks(rotation=45)
        canvas_despesas = FigureCanvasTkAgg(fig_despesas, master=self.root)
        canvas_despesas.get_tk_widget().pack()

root = tk.Tk()
app = GraphApp(root)
root.mainloop()
