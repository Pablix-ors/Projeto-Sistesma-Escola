import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import subprocess
import sys
import os

def open_professores():
    subprocess.Popen([sys.executable, 'professores.py'])

def open_principal():
    subprocess.Popen([sys.executable, 'principal.py'])

def open_cidades():
    subprocess.Popen([sys.executable, 'cidades.py'])

def exit_app():
    root.quit()


# Conexão com o banco de dados MySQL
class Banco:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='aula_escola'
        )

# Classe para gerenciar as operações da tabela de alunos
class Alunos:
    def __init__(self, alu_id=None, alu_nome=None, alu_endereco=None, alu_email=None, alu_telefone=None, alu_idade=None, cid_id=None):
        self.alu_id = alu_id
        self.alu_nome = alu_nome
        self.alu_endereco = alu_endereco
        self.alu_email = alu_email
        self.alu_telefone = alu_telefone
        self.alu_idade = alu_idade
        self.cid_id = cid_id
        self.conexao = Banco().conexao

    def insertAluno(self):
        cursor = self.conexao.cursor()
        sql = """
        INSERT INTO tbl_alunos (alu_nome, alu_endereco, alu_email, alu_telefone, alu_idade, cid_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (self.alu_nome, self.alu_endereco, self.alu_email, self.alu_telefone, self.alu_idade, self.cid_id)
        cursor.execute(sql, valores)
        self.conexao.commit()
        cursor.close()
        return "Aluno inserido com sucesso!"

    def deleteAluno(self):
        cursor = self.conexao.cursor()
        sql = "DELETE FROM tbl_alunos WHERE alu_id=%s"
        cursor.execute(sql, (self.alu_id,))
        self.conexao.commit()
        cursor.close()
        return "Aluno excluído com sucesso!"

    def fetchAll(self):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT alu_id, alu_nome, alu_endereco, alu_email, alu_telefone, alu_idade, cid_id FROM tbl_alunos")
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def fetchById(self):
        cursor = self.conexao.cursor()
        sql = "SELECT alu_id, alu_nome, alu_endereco, alu_email, alu_telefone, alu_idade, cid_id FROM tbl_alunos WHERE alu_id=%s"
        cursor.execute(sql, (self.alu_id,))
        row = cursor.fetchone()
        cursor.close()
        return row

# Função para buscar todas as cidades cadastradas
def fetch_cidades():
    try:
        conn = Banco().conexao
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbl_cidades")
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except mysql.connector.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return []

# Funções para manipular os dados no Treeview e no banco
def inserir():
    nome = nome_entry.get()
    endereco = endereco_entry.get()
    email = email_entry.get()
    telefone = telefone_entry.get()
    idade = idade_entry.get()
    cid_id = cidade_combobox.get()

    if not (nome and endereco and email and telefone and idade and cid_id):
        mostrar_mensagem("Todos os campos devem ser preenchidos!", "red")
        return

    aluno = Alunos(alu_nome=nome, alu_endereco=endereco, alu_email=email, alu_telefone=telefone, alu_idade=idade, cid_id=cid_id)
    aluno.insertAluno()
    limpar_campos()
    mostrar_mensagem("Aluno inserido com sucesso!")
    atualizar_treeview_alunos()

def excluir():
    selected_item = tree_alunos.selection()
    if not selected_item:
        mostrar_mensagem("Selecione um aluno para excluir.", "red")
        return

    aluno_id = tree_alunos.item(selected_item, 'values')[0]
    aluno = Alunos(alu_id=aluno_id)
    aluno.deleteAluno()
    mostrar_mensagem("Aluno excluído com sucesso!")
    atualizar_treeview_alunos()

def buscar():
    aluno_id = alu_id_entry.get()
    if not aluno_id:
        mostrar_mensagem("Digite o ID do aluno para buscar.", "red")
        return

    aluno = Alunos(alu_id=aluno_id)
    dados_aluno = aluno.fetchById()
    if dados_aluno:
        limpar_campos()
        alu_id_entry.insert(0, dados_aluno[0])
        nome_entry.insert(0, dados_aluno[1])
        endereco_entry.insert(0, dados_aluno[2])
        email_entry.insert(0, dados_aluno[3])
        telefone_entry.insert(0, dados_aluno[4])
        idade_entry.insert(0, dados_aluno[5])
        cidade_combobox.set(dados_aluno[6])
    else:
        mostrar_mensagem("Aluno não encontrado.", "red")

def limpar_campos():
    alu_id_entry.delete(0, tk.END)
    nome_entry.delete(0, tk.END)
    endereco_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    telefone_entry.delete(0, tk.END)
    idade_entry.delete(0, tk.END)
    cidade_combobox.set('')

def atualizar_treeview_alunos():
    # Limpa todos os itens no Treeview
    for item in tree_alunos.get_children():
        tree_alunos.delete(item)
    # Adiciona novamente todos os itens
    alunos = Alunos().fetchAll()
    for aluno in alunos:
        tree_alunos.insert("", "end", values=aluno)

# Atualiza o combobox com as cidades
def atualizar_combobox_cidades():
    cidades = fetch_cidades()
    cidade_combobox['values'] = [cid[1] for cid in cidades]  # Usando o nome da cidade

# Mostrar mensagem na interface
def mostrar_mensagem(mensagem, cor='black'):
    mensagem_label.config(text=mensagem, fg=cor)

# Interface gráfica com Tkinter
root = tk.Tk()
root.title("Gerenciamento de Alunos e Cidades")

# Criar o menu
menu = tk.Menu(root)
root.config(menu=menu)

# Adicionar itens ao menu
file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Arquivo", menu=file_menu)
file_menu.add_command(label="Professores", command=open_professores)
file_menu.add_command(label="Principal", command=open_principal)
file_menu.add_command(label="Cidades", command=open_cidades)
file_menu.add_separator()
file_menu.add_command(label="Sair", command=exit_app)

frame_central = tk.Frame(root)
frame_central.grid(row=0, column=0, padx=20, pady=20)

# Widgets para os campos dos alunos
alu_id_label = tk.Label(frame_central, text="ID Aluno:")
alu_id_label.grid(row=0, column=0)
alu_id_entry = tk.Entry(frame_central)
alu_id_entry.grid(row=0, column=1)

nome_label = tk.Label(frame_central, text="Nome:")
nome_label.grid(row=1, column=0)
nome_entry = tk.Entry(frame_central)
nome_entry.grid(row=1, column=1)

endereco_label = tk.Label(frame_central, text="Endereço:")
endereco_label.grid(row=2, column=0)
endereco_entry = tk.Entry(frame_central)
endereco_entry.grid(row=2, column=1)

email_label = tk.Label(frame_central, text="Email:")
email_label.grid(row=3, column=0)
email_entry = tk.Entry(frame_central)
email_entry.grid(row=3, column=1)

telefone_label = tk.Label(frame_central, text="Telefone:")
telefone_label.grid(row=4, column=0)
telefone_entry = tk.Entry(frame_central)
telefone_entry.grid(row=4, column=1)

idade_label = tk.Label(frame_central, text="Idade:")
idade_label.grid(row=5, column=0)
idade_entry = tk.Entry(frame_central)
idade_entry.grid(row=5, column=1)

# Combobox para selecionar a cidade
cidade_label = tk.Label(frame_central, text="Cidade:")
cidade_label.grid(row=6, column=0)
cidade_combobox = ttk.Combobox(frame_central)
cidade_combobox.grid(row=6, column=1)
atualizar_combobox_cidades()

# Botões para operações
inserir_button = tk.Button(frame_central, text="Inserir Aluno", command=inserir)
inserir_button.grid(row=7, column=0, pady=10)

excluir_button = tk.Button(frame_central, text="Excluir Aluno", command=excluir)
excluir_button.grid(row=7, column=1, pady=10)

buscar_button = tk.Button(frame_central, text="Buscar Aluno", command=buscar)
buscar_button.grid(row=8, column=0, pady=10)

limpar_button = tk.Button(frame_central, text="Limpar Campos", command=limpar_campos)
limpar_button.grid(row=8, column=1, pady=10)

mensagem_label = tk.Label(frame_central, text="", fg="black")
mensagem_label.grid(row=9, column=0, columnspan=2)

# Treeview para exibir alunos cadastrados
tree_frame = tk.Frame(root)
tree_frame.grid(row=1, column=0, padx=20, pady=20)

tree_scroll = tk.Scrollbar(tree_frame)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

tree_alunos = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, columns=("ID", "Nome", "Endereço", "Email", "Telefone", "Idade", "Cidade"), show='headings')
tree_scroll.config(command=tree_alunos.yview)

# Definir cabeçalhos do Treeview
tree_alunos.heading("ID", text="ID")
tree_alunos.heading("Nome", text="Nome")
tree_alunos.heading("Endereço", text="Endereço")
tree_alunos.heading("Email", text="Email")
tree_alunos.heading("Telefone", text="Telefone")
tree_alunos.heading("Idade", text="Idade")
tree_alunos.heading("Cidade", text="Cidade")

tree_alunos.pack(fill=tk.BOTH, expand=True)
atualizar_treeview_alunos()

root.state('zoomed')
root.mainloop()
