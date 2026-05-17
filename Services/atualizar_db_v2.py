# =================================================================
# SCRIPT DE MANUTENÇÃO: atualizar_db_v2.py
# Responsabilidade: Migração e evolução do esquema do banco de dados
# =================================================================

from Services.database import conectaBD

def atualizar_esquema():
    """
    Adiciona novas colunas e tabelas necessárias para as versões mais
    recentes do sistema sem apagar os dados existentes.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    # Bloco 1: Evolução da Tabela Produto
    # Tenta adicionar as colunas. O 'try/except' evita erro se a coluna já existir.
    try:
        cursor.execute("ALTER TABLE produto ADD COLUMN localizacao TEXT")
    except: pass
    
    try:
        cursor.execute("ALTER TABLE produto ADD COLUMN preco_custo REAL")
    except: pass

    # Bloco 2: Criação de Tabelas Auxiliares
    cursor.execute("CREATE TABLE IF NOT EXISTS categorias_log (nome TEXT UNIQUE)")
    
    # Seed de Categorias Iniciais
    categorias = ['Eletrônicos', 'Ferramentas', 'Limpeza', 'Escritório', 'Outros']
    for cat in categorias:
        try:
            cursor.execute("INSERT INTO categorias_log (nome) VALUES (?)", (cat,))
        except: pass

    conexao.commit()
    conexao.close()
    print("Sistema: Esquema de banco de dados atualizado!")

if __name__ == "__main__":
    atualizar_esquema()
