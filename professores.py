import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import subprocess
import sys
import os

def open_principal():
    subprocess.Popen([sys.executable, 'pricipal.py'])

def open_alunos():
    subprocess.Popen([sys.executable, 'alunos.py'])

def open_cidades():
    subprocess.Popen([sys.executable, 'cidades.py'])

def exit_app():
    root.quit()


# Conexão com o banco de dados MySQL
class Banco:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host='localhost',
            user='root',  # Altere conforme suas credenciais
            password='',  # Altere conforme suas credenciais
            database='aula_escola'
        )

# Classe para gerenciar as operações da tabela de professores
class Professores:
    def __init__(self, pro_id=None, pro_nome=None, pro_endereco=None, pro_email=None, pro_CPF=None, pro_idade=None, cid_id=None):
        self.pro_id = pro_id
        self.pro_nome = pro_nome
        self.pro_endereco = pro_endereco
        self.pro_email = pro_email
        self.pro_CPF = pro_CPF
        self.pro_idade = pro_idade
        self.cid_id = cid_id  # ID da cidade
        self.conexao = Banco().conexao

    def insertProfessor(self):
        cursor = self.conexao.cursor()
        sql = """
        INSERT INTO tbl_professores (pro_nome, pro_endereco, pro_email, pro_CPF, pro_idade, cid_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (self.pro_nome, self.pro_endereco, self.pro_email, self.pro_CPF, self.pro_idade, self.cid_id)
        cursor.execute(sql, valores)
        self.conexao.commit()
        cursor.close()
        return "Professor inserido com sucesso!"

    def updateProfessor(self):
        cursor = self.conexao.cursor()
        sql = """
        UPDATE tbl_professores 
        SET pro_nome=%s, pro_endereco=%s, pro_email=%s, pro_CPF=%s, pro_idade=%s, cid_id=%s
        WHERE pro_id=%s
        """
        valores = (self.pro_nome, self.pro_endereco, self.pro_email, self.pro_CPF, self.pro_idade, self.cid_id, self.pro_id)
        cursor.execute(sql, valores)
        self.conexao.commit()
        cursor.close()
        return "Professor atualizado com sucesso!"

    def deleteProfessor(self):
        cursor = self.conexao.cursor()
        sql = "DELETE FROM tbl_professores WHERE pro_id=%s"
        cursor.execute(sql, (self.pro_id,))
        self.conexao.commit()
        cursor.close()
        return "Professor excluído com sucesso!"

    def selectProfessor(self, pro_id):
        cursor = self.conexao.cursor()
        sql = "SELECT * FROM tbl_professores WHERE pro_id=%s"
        cursor.execute(sql, (pro_id,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            self.pro_id, self.pro_nome, self.pro_endereco, self.pro_email, self.pro_CPF, self.pro_idade, self.cid_id = row
            return row
        else:
            return None

def fetch_data():
    try:
        conn = Banco().conexao
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbl_professores")
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except mysql.connector.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return []

def fetch_cidades():
    try:
        conn = Banco().conexao
        cursor = conn.cursor()
        cursor.execute("SELECT cid_id, cid_nome FROM tbl_cidades")
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
    CPF = CPF_entry.get()
    idade = idade_entry.get()
    cid_id = cid_combobox.get()  # ID da cidade selecionada

    if not (nome and endereco and email and CPF and idade and cid_id):
        mostrar_mensagem("Todos os campos devem ser preenchidos!", "red")
        return

    professor = Professores(pro_nome=nome, pro_endereco=endereco, pro_email=email, pro_CPF=CPF, pro_idade=idade, cid_id=cid_id)
    professor.insertProfessor()
    limpar_campos()
    mostrar_mensagem("Professor inserido com sucesso!")
    atualizar_treeview()

def alterar():
    pro_id = pro_id_entry.get()
    nome = nome_entry.get()
    endereco = endereco_entry.get()
    email = email_entry.get()
    CPF = CPF_entry.get()
    idade = idade_entry.get()
    cid_id = cid_combobox.get()  # ID da cidade selecionada

    if not pro_id:
        mostrar_mensagem("ID do Professor é obrigatório para alterar!", "red")
        return

    professor = Professores(pro_id=pro_id, pro_nome=nome, pro_endereco=endereco, pro_email=email, pro_CPF=CPF, pro_idade=idade, cid_id=cid_id)
    professor.updateProfessor()
    limpar_campos()
    mostrar_mensagem("Professor atualizado com sucesso!")
    atualizar_treeview()

def excluir():
    pro_id = pro_id_entry.get()

    if not pro_id:
        mostrar_mensagem("ID do Professor é obrigatório para excluir!", "red")
        return

    professor = Professores(pro_id=pro_id)
    professor.deleteProfessor()
    limpar_campos()
    mostrar_mensagem("Professor excluído com sucesso!")
    atualizar_treeview()

def buscar():
    pro_id = pro_id_entry.get()
    if not pro_id:
        mostrar_mensagem("ID do Professor não pode estar vazio!", "red")
        return

    professor = Professores()
    resultado = professor.selectProfessor(pro_id)
    if resultado:
        nome_entry.delete(0, tk.END)
        nome_entry.insert(0, resultado[1])
        endereco_entry.delete(0, tk.END)
        endereco_entry.insert(0, resultado[2])
        email_entry.delete(0, tk.END)
        email_entry.insert(0, resultado[3])
        CPF_entry.delete(0, tk.END)
        CPF_entry.insert(0, resultado[4])
        idade_entry.delete(0, tk.END)
        idade_entry.insert(0, resultado[5])
        cid_combobox.set(resultado[6])  # Define a cidade selecionada
        mostrar_mensagem("Professor encontrado!")
    else:
        limpar_campos()
        mostrar_mensagem("Professor não encontrado", "red")

def limpar_campos():
    pro_id_entry.delete(0, tk.END)
    nome_entry.delete(0, tk.END)
    endereco_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    CPF_entry.delete(0, tk.END)
    idade_entry.delete(0, tk.END)
    cid_combobox.set("")  # Limpa o combo box de cidades
    mostrar_mensagem("")

def mostrar_mensagem(mensagem, cor="green"):
    mensagem_label.config(text=mensagem, fg=cor)

def atualizar_treeview():
    data = fetch_data()
    populate_treeview(treeview, data)

def populate_treeview(treeview, data):
    for item in treeview.get_children():
        treeview.delete(item)
    for row in data:
        treeview.insert("", "end", values=row)

def selecionar_item(event):
    item = treeview.selection()[0]
    valores = treeview.item(item, "values")

    pro_id_entry.delete(0, tk.END)
    pro_id_entry.insert(0, valores[0])

    nome_entry.delete(0, tk.END)
    nome_entry.insert(0, valores[1])

    endereco_entry.delete(0, tk.END)
    endereco_entry.insert(0, valores[2])

    email_entry.delete(0, tk.END)
    email_entry.insert(0, valores[3])

    CPF_entry.delete(0, tk.END)
    CPF_entry.insert(0, valores[4])

    idade_entry.delete(0, tk.END)
    idade_entry.insert(0, valores[5])

    cid_combobox.set(valores[6])  # Define a cidade selecionada

# Interface gráfica com Tkinter
root = tk.Tk()
root.title("Gerenciamento de Professores")

# Criar o menu
menu = tk.Menu(root)
root.config(menu=menu)

# Adicionar itens ao menu
file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Arquivo", menu=file_menu)
file_menu.add_command(label="Principal", command=open_principal)
file_menu.add_command(label="Alunos", command=open_alunos)
file_menu.add_command(label="Cidades", command=open_cidades)
file_menu.add_separator()
file_menu.add_command(label="Sair", command=exit_app)


frame_central = tk.Frame(root)
frame_central.grid(row=0, column=0, padx=20, pady=20)

# Widgets para os campos
pro_id_label = tk.Label(frame_central, text="ID Professor:")
pro_id_label.grid(row=0, column=0)
pro_id_entry = tk.Entry(frame_central)
pro_id_entry.grid(row=0, column=1)

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

CPF_label = tk.Label(frame_central, text="CPF:")
CPF_label.grid(row=4, column=0)
CPF_entry = tk.Entry(frame_central)
CPF_entry.grid(row=4, column=1)

idade_label = tk.Label(frame_central, text="Idade:")
idade_label.grid(row=5, column=0)
idade_entry = tk.Entry(frame_central)
idade_entry.grid(row=5, column=1)

cidade_label = tk.Label(frame_central, text="Cidade:")
cidade_label.grid(row=6, column=0)
cid_combobox = ttk.Combobox(frame_central, values=[f"{cid[0]} - {cid[1]}" for cid in fetch_cidades()])
cid_combobox.grid(row=6, column=1)

# Botões de operação
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, pady=10)

insert_button = tk.Button(button_frame, text="Inserir", command=inserir)
insert_button.grid(row=0, column=0, padx=5)

update_button = tk.Button(button_frame, text="Alterar", command=alterar)
update_button.grid(row=0, column=1, padx=5)

delete_button = tk.Button(button_frame, text="Excluir", command=excluir)
delete_button.grid(row=0, column=2, padx=5)

search_button = tk.Button(button_frame, text="Buscar", command=buscar)
search_button.grid(row=0, column=3, padx=5)

clear_button = tk.Button(button_frame, text="Limpar", command=limpar_campos)
clear_button.grid(row=0, column=4, padx=5)

# Treeview para listar os professores
treeview = ttk.Treeview(root, columns=("pro_id", "pro_nome", "pro_endereco", "pro_email", "pro_CPF", "pro_idade", "cid_id"), show='headings')
treeview.grid(row=2, column=0, padx=20, pady=20)
treeview.heading("pro_id", text="ID")
treeview.heading("pro_nome", text="Nome")
treeview.heading("pro_endereco", text="Endereço")
treeview.heading("pro_email", text="Email")
treeview.heading("pro_CPF", text="CPF")
treeview.heading("pro_idade", text="Idade")
treeview.heading("cid_id", text="ID Cidade")

treeview.bind("<ButtonRelease-1>", selecionar_item)

# Label para mensagens
mensagem_label = tk.Label(root, text="", fg="green")
mensagem_label.grid(row=3, column=0, pady=5)

# Atualiza o Treeview na inicialização
atualizar_treeview()

root.state('zoomed')
root.mainloop()
