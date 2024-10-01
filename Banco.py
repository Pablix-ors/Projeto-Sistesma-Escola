import mysql.connector

class Banco:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="aula_escola"
        )
        self.cursor = self.conn.cursor()

    def check_user(self, usuario, senha):
        """Verifica se o usuário e a senha estão corretos na tabela tbl_usuarios"""
        query = "SELECT * FROM tbl_usuarios WHERE usu_username = %s AND usu_senha = %s"
        self.cursor.execute(query, (usuario, senha))
        result = self.cursor.fetchone()
        return result is not None

    def add_user(self, nome, usuario, senha):
        """Adiciona o usuário nas tabelas tbl_cadastro e tbl_usuarios"""
        query_cadastro = "INSERT INTO tbl_cadastro (cad_nome, cad_username, cad_senha) VALUES (%s, %s, %s)"
        query_usuario = "INSERT INTO tbl_usuarios (usu_nome, usu_username, usu_senha) VALUES (%s, %s, %s)"

        self.cursor.execute(query_cadastro, (nome, usuario, senha))
        self.cursor.execute(query_usuario, (nome, usuario, senha))
        self.conn.commit()

