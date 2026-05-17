import sqlite3
import os
import random

def conectaBD():
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    caminho_db = os.path.abspath(os.path.join(current_file_path, '..', 'Estoque.db'))
    return sqlite3.connect(caminho_db)

def popular_total():
    print("🏗️ Iniciando ocupação total das prateleiras...")
    conexao = conectaBD()
    cursor = conexao.cursor()

    # 1. Obter todos os produtos
    cursor.execute("SELECT codigo FROM produto")
    produtos = [r[0] for r in cursor.fetchall()]
    
    if not produtos:
        print("❌ Nenhum produto encontrado. Cadastre produtos primeiro.")
        return

    # 2. Obter todas as caixas vazias
    cursor.execute("SELECT id FROM estrutura_armazenamento WHERE ocupacao = 0")
    caixas_vazias = [r[0] for r in cursor.fetchall()]
    
    print(f"📦 Localizadas {len(caixas_vazias)} caixas vazias.")

    stats_por_produto = {p: 0 for p in produtos}

    # 3. Preencher cada caixa
    for caixa_id in caixas_vazias:
        produto_aleatorio = random.choice(produtos)
        qtd = random.randint(2, 10) # No mínimo 2 para não ficar tão vazio
        
        cursor.execute("""
            UPDATE estrutura_armazenamento 
            SET ocupacao = ?, produto_codigo = ? 
            WHERE id = ?
        """, (qtd, produto_aleatorio, caixa_id))
        
        stats_por_produto[produto_aleatorio] += qtd

    # 4. Atualizar o saldo total na tabela produto
    for produto_codigo, qtd_adicional in stats_por_produto.items():
        cursor.execute("""
            UPDATE produto 
            SET quantidade = quantidade + ? 
            WHERE codigo = ?
        """, (qtd_adicional, produto_codigo))

    conexao.commit()
    conexao.close()
    print(f"✅ Sucesso! Todas as prateleiras estão agora 100% ocupadas.")

if __name__ == "__main__":
    popular_total()
