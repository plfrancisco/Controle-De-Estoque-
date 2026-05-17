# =================================================================
# CONTROLLER: UsuarioController
# Responsabilidade: Autenticação e Gestão de Operadores
# =================================================================

import sqlite3
from Services.database import conectaBD
from Models.Usuario import Usuario

def autenticar_usuario(login, senha):
    """
    Verifica as credenciais e retorna o Objeto Usuario se bem-sucedido.
    Este objeto será guardado no 'session_state' do Streamlit.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM usuario WHERE login = ? AND senha = ?", (login, senha))
        row = cursor.fetchone()
        if row:
            # Instancia o modelo para uso em toda a aplicação
            return Usuario(row[0], row[1], row[2], row[3])
        return None
    except sqlite3.Error as e:
        print(f"Erro de Segurança: {e}")
        return None
    finally:
        conexao.close()

def atualizar_senha_admin():
    """Script utilitário para resetar/ajustar a senha do administrador."""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("UPDATE usuario SET senha = ? WHERE login = ?", ('admin', 'admin'))
        conexao.commit()
    finally:
        conexao.close()
