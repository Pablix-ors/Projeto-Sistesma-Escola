import tkinter as tk
import subprocess
import sys
import os

# Ajustar o caminho para o módulo Banco
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def open_professores():
    subprocess.Popen([sys.executable, 'professores.py'])

def open_alunos():
    subprocess.Popen([sys.executable, 'alunos.py'])

def open_cidades():
    subprocess.Popen([sys.executable, 'cidades.py'])

def exit_app():
    root.quit()

root = tk.Tk()
root.title("Sistema Agenda")

# Maximizar a janela
root.state('zoomed')

# Criar o menu
menu = tk.Menu(root)
root.config(menu=menu)

# Adicionar itens ao menu
file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Arquivo", menu=file_menu)
file_menu.add_command(label="Professores", command=open_professores)
file_menu.add_command(label="Alunos", command=open_alunos)
file_menu.add_command(label="Cidades", command=open_cidades)
file_menu.add_separator()
file_menu.add_command(label="Sair", command=exit_app)

root.mainloop()
