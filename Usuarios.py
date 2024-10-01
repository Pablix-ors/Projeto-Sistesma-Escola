import tkinter as tk
from tkinter import messagebox
from Banco import Banco  # Banco.py é responsável pela conexão ao banco de dados
import os  # Usando os para abrir principal.py

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Tela de Login")
        self.banco = Banco()
        self.create_login_widgets()

    def create_login_widgets(self):
        """Cria os widgets para a tela de login"""
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Usuário:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.login_frame, text="Senha:").grid(row=1, column=0, padx=10, pady=5)

        self.usuario_entry = tk.Entry(self.login_frame)
        self.senha_entry = tk.Entry(self.login_frame, show="*")

        self.usuario_entry.grid(row=0, column=1, padx=10, pady=5)
        self.senha_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(self.login_frame, text="Login", command=self.authenticate).grid(row=2, column=0, columnspan=2, pady=10)

        # Botão para ir à tela de cadastro
        self.cadastrar_button = tk.Button(self.root, text="Não tem login? Cadastre-se!", command=self.show_registration)
        self.cadastrar_button.pack(pady=10)

    def authenticate(self):
        """Autentica o usuário"""
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()

        if not (usuario and senha):
            messagebox.showwarning("Aviso", "Usuário e senha devem ser preenchidos")
            return

        if self.banco.check_user(usuario, senha):  # Função que verifica no banco de dados
            messagebox.showinfo("Sucesso", "Login realizado com sucesso")
            self.root.withdraw()  # Oculta a janela de login
            self.open_principal()  # Redireciona para o arquivo principal.py
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos")  # Exibe mensagem de erro

    def show_registration(self):
        """Mostra a tela de cadastro"""
        self.login_frame.pack_forget()
        self.cadastrar_button.pack_forget()
        self.create_registration_widgets()

    def create_registration_widgets(self):
        """Cria os widgets para a tela de cadastro"""
        self.registration_frame = tk.Frame(self.root)
        self.registration_frame.pack(pady=20)

        tk.Label(self.registration_frame, text="Nome:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.registration_frame, text="Usuário:").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.registration_frame, text="Senha:").grid(row=2, column=0, padx=10, pady=5)

        self.nome_entry = tk.Entry(self.registration_frame)
        self.usuario_entry_reg = tk.Entry(self.registration_frame)
        self.senha_entry_reg = tk.Entry(self.registration_frame, show="*")

        self.nome_entry.grid(row=0, column=1, padx=10, pady=5)
        self.usuario_entry_reg.grid(row=1, column=1, padx=10, pady=5)
        self.senha_entry_reg.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self.registration_frame, text="Cadastrar", command=self.register).grid(row=3, column=0, columnspan=2, pady=10)

    def register(self):
        """Registra o usuário e salva nas tabelas tbl_cadastro e tbl_usuarios"""
        nome = self.nome_entry.get()
        usuario = self.usuario_entry_reg.get()
        senha = self.senha_entry_reg.get()

        if not (nome and usuario and senha):
            messagebox.showwarning("Aviso", "Todos os campos devem ser preenchidos")
            return

        self.banco.add_user(nome, usuario, senha)  # Adiciona nas duas tabelas
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso")

        # Voltar para a tela de login
        self.registration_frame.pack_forget()
        self.create_login_widgets()

    def open_principal(self):
        """Redireciona para o arquivo principal.py"""
        try:
            # Importar principal.py para ser executado dentro do mesmo processo
            import principal
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir principal.py: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.state('zoomed')
    app = App(root)
    root.mainloop()
