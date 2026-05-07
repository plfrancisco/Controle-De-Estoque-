import sqlite3
import os

def conectaBD():
    # Caminho absoluto para garantir que o BD seja criado no local correto
    caminho_db = os.path.join(os.path.dirname(__file__), '..', 'Estoque.db')
    conexao = sqlite3.connect(caminho_db)
    return conexao
