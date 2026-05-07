import sqlite3
from Services.database import conectaBD
from Models.Usuario import Usuario

def autenticar_usuario(login, senha):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM usuario WHERE login = ? AND senha = ?", (login, senha))
        row = cursor.fetchone()
        if row:
            # Retorna um objeto Usuario
            return Usuario(row[0], row[1], row[2], row[3])
        return None
    except sqlite3.Error as e:
        print(f"Erro ao autenticar usuário: {e}")
        return None
    finally:
        conexao.close()

def atualizar_senha_admin():
    # Garante que o admin tenha a senha 'admin' conforme solicitado
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("UPDATE usuario SET senha = ? WHERE login = ?", ('admin', 'admin'))
        conexao.commit()
    finally:
        conexao.close()
