# =================================================================
# SERVIÇO: Conexão com Banco de Dados (database.py)
# Responsabilidade: Prover a ponte entre a aplicação e o SQLite
# =================================================================

import sqlite3
import os

def conectaBD():
    """
    Centraliza a lógica de conexão com o banco de dados.
    Configurações críticas como check_same_thread=False são necessárias
    para que o Streamlit (que usa threads) possa operar o SQLite com segurança.
    """
    # Determina o caminho absoluto do arquivo .db independente de onde o script é chamado
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    caminho_db = os.path.abspath(os.path.join(current_file_path, '..', 'Estoque.db'))
    
    # Estabelece a conexão com timeout estendido para evitar erros de 'Database Locked'
    conexao = sqlite3.connect(caminho_db, check_same_thread=False, timeout=10)
    return conexao
