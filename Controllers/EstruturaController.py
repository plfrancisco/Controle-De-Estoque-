# =================================================================
# CONTROLLER: EstruturaController
# Responsabilidade: Gestão física do almoxarifado (Prateleiras e Caixas)
# =================================================================

from Services.database import conectaBD
import sqlite3

def listar_prateleiras():
    """Retorna um resumo das prateleiras e sua ocupação."""
    conexao = conectaBD()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT prateleira, COUNT(id) as total_caixas, SUM(ocupacao) as ocupacao_total
        FROM estrutura_armazenamento
        GROUP BY prateleira
    """)
    res = cursor.fetchall()
    conexao.close()
    return res

def cadastrar_prateleira(nome, qtd_caixas=15):
    """Cria uma nova prateleira com um número definido de caixas."""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        # Verifica se o nome já existe
        cursor.execute("SELECT id FROM estrutura_armazenamento WHERE prateleira = ? LIMIT 1", (nome,))
        if cursor.fetchone():
            return False, "Esta prateleira já existe no sistema."
        
        for i in range(1, qtd_caixas + 1):
            cursor.execute("""
                INSERT INTO estrutura_armazenamento (prateleira, caixa, ocupacao, capacidade_max)
                VALUES (?, ?, 0, 10)
            """, (nome, i))
        
        conexao.commit()
        return True, f"Prateleira {nome} criada com {qtd_caixas} caixas."
    except sqlite3.Error as e:
        return False, f"Erro ao criar estrutura: {e}"
    finally:
        conexao.close()

def excluir_prateleira(nome):
    """Remove uma prateleira completa se ela estiver vazia."""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        # Verifica ocupação
        cursor.execute("SELECT SUM(ocupacao) FROM estrutura_armazenamento WHERE prateleira = ?", (nome,))
        total = cursor.fetchone()[0]
        
        if total is None:
            return False, "Prateleira não encontrada."
        
        if total > 0:
            return False, "Não é possível excluir uma prateleira ocupada. Remova os produtos primeiro."
        
        cursor.execute("DELETE FROM estrutura_armazenamento WHERE prateleira = ?", (nome,))
        conexao.commit()
        return True, f"Prateleira {nome} removida do almoxarifado."
    except sqlite3.Error as e:
        return False, f"Erro ao excluir: {e}"
    finally:
        conexao.close()
