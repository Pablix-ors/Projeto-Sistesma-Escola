import tkinter as tk
from tkinter import ttk
import mysql.connector
import subprocess
import sys
import os

def open_professores():
    subprocess.Popen([sys.executable, 'professores.py'])

def open_alunos():
    subprocess.Popen([sys.executable, 'alunos.py'])

def open_principal():
    subprocess.Popen([sys.executable, 'principal.py'])

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

# Classe para gerenciar as operações da tabela de cidades
class Cidades:
    def __init__(self, cid_id=None, cid_nome=None, cid_uf=None):
        self.cid_id = cid_id
        self.cid_nome = cid_nome
        self.cid_uf = cid_uf
        self.conexao = Banco().conexao

    def insertCidade(self):
        cursor = self.conexao.cursor()
        sql = """
        INSERT INTO tbl_cidades (cid_nome, cid_uf)
        VALUES (%s, %s)
        """
        valores = (self.cid_nome, self.cid_uf)
        cursor.execute(sql, valores)
        self.conexao.commit()
        cursor.close()
        return "Cidade inserida com sucesso!"

    def updateCidade(self):
        cursor = self.conexao.cursor()
        sql = """
        UPDATE tbl_cidades 
        SET cid_nome=%s, cid_uf=%s
        WHERE cid_id=%s
        """
        valores = (self.cid_nome, self.cid_uf, self.cid_id)
        cursor.execute(sql, valores)
        self.conexao.commit()
        cursor.close()
        return "Cidade atualizada com sucesso!"

    def deleteCidade(self):
        cursor = self.conexao.cursor()
        sql = "DELETE FROM tbl_cidades WHERE cid_id=%s"
        cursor.execute(sql, (self.cid_id,))
        self.conexao.commit()
        cursor.close()
        return "Cidade excluída com sucesso!"

    def selectCidade(self, cid_id):
        cursor = self.conexao.cursor()
        sql = "SELECT * FROM tbl_cidades WHERE cid_id=%s"
        cursor.execute(sql, (cid_id,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            self.cid_id, self.cid_nome, self.cid_uf = row
            return row
        else:
            return None

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
def inserir_cidade():
    nome = cid_nome_entry.get()
    uf = cid_uf_entry.get()

    if not (nome and uf):
        mostrar_mensagem_cidade("Todos os campos devem ser preenchidos!", "red")
        return

    cidade = Cidades(cid_nome=nome, cid_uf=uf)
    cidade.insertCidade()
    limpar_campos_cidade()
    mostrar_mensagem_cidade("Cidade inserida com sucesso!")
    atualizar_treeview_cidades()

def alterar_cidade():
    cid_id = cid_id_entry.get()
    nome = cid_nome_entry.get()
    uf = cid_uf_entry.get()

    if not cid_id:
        mostrar_mensagem_cidade("ID da Cidade é obrigatório para alterar!", "red")
        return

    cidade = Cidades(cid_id=cid_id, cid_nome=nome, cid_uf=uf)
    cidade.updateCidade()
    limpar_campos_cidade()
    mostrar_mensagem_cidade("Cidade atualizada com sucesso!")
    atualizar_treeview_cidades()

def excluir_cidade():
    cid_id = cid_id_entry.get()

    if not cid_id:
        mostrar_mensagem_cidade("ID da Cidade é obrigatório para excluir!", "red")
        return

    cidade = Cidades(cid_id=cid_id)
    cidade.deleteCidade()
    limpar_campos_cidade()
    mostrar_mensagem_cidade("Cidade excluída com sucesso!")
    atualizar_treeview_cidades()

def buscar_cidade():
    cid_id = cid_id_entry.get()
    if not cid_id:
        mostrar_mensagem_cidade("ID da Cidade não pode estar vazio!", "red")
        return

    cidade = Cidades()
    resultado = cidade.selectCidade(cid_id)
    if resultado:
        cid_nome_entry.delete(0, tk.END)
        cid_nome_entry.insert(0, resultado[1])
        cid_uf_entry.delete(0, tk.END)
        cid_uf_entry.insert(0, resultado[2])
        mostrar_mensagem_cidade("Cidade encontrada!")
    else:
        limpar_campos_cidade()
        mostrar_mensagem_cidade("Cidade não encontrada", "red")

def limpar_campos_cidade():
    cid_id_entry.delete(0, tk.END)
    cid_nome_entry.delete(0, tk.END)
    cid_uf_entry.delete(0, tk.END)
    mostrar_mensagem_cidade("")

def mostrar_mensagem_cidade(mensagem, cor="green"):
    mensagem_cidade_label.config(text=mensagem, fg=cor)

def atualizar_treeview_cidades():
    data = fetch_cidades()
    populate_treeview_cidades(treeview_cidades, data)

def populate_treeview_cidades(treeview, data):
    for item in treeview.get_children():
        treeview.delete(item)
    for row in data:
        treeview.insert("", "end", values=row)

def selecionar_item_cidade(event):
    item = treeview_cidades.selection()[0]
    valores = treeview_cidades.item(item, "values")

    cid_id_entry.delete(0, tk.END)
    cid_id_entry.insert(0, valores[0])

    cid_nome_entry.delete(0, tk.END)
    cid_nome_entry.insert(0, valores[1])

    cid_uf_entry.delete(0, tk.END)
    cid_uf_entry.insert(0, valores[2])

# Interface gráfica com Tkinter
root = tk.Tk()
root.title("Gerenciamento de Cidades")

# Criar o menu
menu = tk.Menu(root)
root.config(menu=menu)

# Adicionar itens ao menu
file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Arquivo", menu=file_menu)
file_menu.add_command(label="Professores", command=open_professores)
file_menu.add_command(label="Alunos", command=open_alunos)
file_menu.add_command(label="Principal", command=open_principal)
file_menu.add_separator()
file_menu.add_command(label="Sair", command=exit_app)

frame_central = tk.Frame(root)
frame_central.grid(row=0, column=0, padx=20, pady=20)

# Widgets para os campos
cid_id_label = tk.Label(frame_central, text="ID Cidade:")
cid_id_label.grid(row=0, column=0)
cid_id_entry = tk.Entry(frame_central)
cid_id_entry.grid(row=0, column=1)

cid_nome_label = tk.Label(frame_central, text="Nome:")
cid_nome_label.grid(row=1, column=0)
cid_nome_entry = tk.Entry(frame_central)
cid_nome_entry.grid(row=1, column=1)

cid_uf_label = tk.Label(frame_central, text="UF:")
cid_uf_label.grid(row=2, column=0)
cid_uf_entry = tk.Entry(frame_central)
cid_uf_entry.grid(row=2, column=1)

# Botões
inserir_btn_cidade = tk.Button(frame_central, text="Inserir", command=inserir_cidade)
inserir_btn_cidade.grid(row=3, column=0, padx=10, pady=10)

alterar_btn_cidade = tk.Button(frame_central, text="Alterar", command=alterar_cidade)
alterar_btn_cidade.grid(row=3, column=1, padx=10, pady=10)

excluir_btn_cidade = tk.Button(frame_central, text="Excluir", command=excluir_cidade)
excluir_btn_cidade.grid(row=3, column=2, padx=10, pady=10)

buscar_btn_cidade = tk.Button(frame_central, text="Buscar", command=buscar_cidade)
buscar_btn_cidade.grid(row=0, column=2, padx=10, pady=10)

# Treeview para mostrar dados
treeview_cidades = ttk.Treeview(frame_central, columns=("cid_id", "cid_nome", "cid_uf"), show="headings")
treeview_cidades.grid(row=4, column=0, columnspan=3)
treeview_cidades.heading("cid_id", text="ID")
treeview_cidades.heading("cid_nome", text="Nome")
treeview_cidades.heading("cid_uf", text="UF")
treeview_cidades.bind("<Double-1>", selecionar_item_cidade)

# Label para mensagens
mensagem_cidade_label = tk.Label(root, text="")
mensagem_cidade_label.grid(row=1, column=0)

# Atualizar Treeview com dados
atualizar_treeview_cidades()

root.state('zoomed')
root.mainloop()
