# =================================================================
# ENGINE DE INFRAESTRUTURA: database_engine.py (v10.0 Consolidated)
# Responsabilidade: Gestão Única de Schema e Carga de Dados
# =================================================================

import sqlite3
import os
import sys
import random

# Ajusta path para importar controllers e models se necessário
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '..'))

def conectaBD():
    """Conexão centralizada com SQLite."""
    caminho_db = os.path.abspath(os.path.join(current_dir, '..', 'Estoque.db'))
    return sqlite3.connect(caminho_db, check_same_thread=False, timeout=10)

def inicializar_sistema():
    """Cria todas as tabelas (Schema Consolidado) e o admin inicial."""
    print("🛸 [Inventory. Engine] Iniciando configuração de infraestrutura...")
    conexao = conectaBD()
    cursor = conexao.cursor()

    # 1. GESTÃO DE ACESSO
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        nivel_acesso TEXT NOT NULL
    )
    """)

    # 2. ESTRUTURA E PARCEIROS
    cursor.execute("CREATE TABLE IF NOT EXISTS categoria (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL UNIQUE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS fornecedor (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, contato TEXT, cnpj TEXT, email TEXT)")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prateleira (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        identificacao TEXT UNIQUE NOT NULL,
        total_caixas INTEGER DEFAULT 15
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estrutura_armazenamento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prateleira_id INTEGER,
        posicao_caixa INTEGER,
        produto_codigo INTEGER,
        ocupacao INTEGER DEFAULT 0,
        FOREIGN KEY (prateleira_id) REFERENCES prateleira(id),
        FOREIGN KEY (produto_codigo) REFERENCES produto(codigo)
    )
    """)

    # 3. CORE: PRODUTOS E ESTOQUE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produto (
        codigo INTEGER PRIMARY KEY,
        descricao TEXT NOT NULL,
        quantidade INTEGER DEFAULT 0,
        quantidade_minima INTEGER DEFAULT 5,
        valor_unitario REAL,
        id_categoria INTEGER,
        id_fornecedor INTEGER,
        preco_custo REAL,
        localizacao TEXT,
        FOREIGN KEY (id_categoria) REFERENCES categoria(id),
        FOREIGN KEY (id_fornecedor) REFERENCES fornecedor(id)
    )
    """)

    # 4. TABELAS ASSOCIATIVAS (M:N)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produto_fornecedor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_codigo INTEGER,
        fornecedor_id INTEGER,
        FOREIGN KEY (produto_codigo) REFERENCES produto(codigo),
        FOREIGN KEY (fornecedor_id) REFERENCES fornecedor(id)
    )
    """)

    # 5. AUDITORIA E FLUXO
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimentacao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        codigo_produto INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        id_usuario INTEGER,
        motivo TEXT,
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (codigo_produto) REFERENCES produto(codigo),
        FOREIGN KEY (id_usuario) REFERENCES usuario(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS log_exclusao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_codigo INTEGER,
        descricao_resumo TEXT,
        motivo TEXT,
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 6. SEED DATA (Admin e Categorias)
    try:
        cursor.execute("INSERT INTO usuario (login, senha, nivel_acesso) VALUES (?, ?, ?)", ('admin', 'admin123', 'ADMIN'))
    except: pass

    categorias = ['Eletrônicos', 'Ferramentas', 'Limpeza', 'Escritório', 'Copa/Gourmet']
    for cat in categorias:
        try: cursor.execute("INSERT INTO categoria (nome) VALUES (?)", (cat,))
        except: pass

    conexao.commit()
    conexao.close()
    print("✅ [OK] Schema consolidado e validado.")

def popular_massa_teste():
    """Gera dados reais e movimentações aleatórias para teste de estresse."""
    from Controllers.ProdutoController import cadastrar_produto, listar_produtos
    from Controllers.MovimentacaoController import registrar_movimentacao
    from Models.Produto import Produto
    
    print("🚀 [Inventory. Engine] Iniciando carga de alta fidelidade...")
    
    # Matriz de Produtos
    massa_dados = [
        (101, "Servidor Enterprise Rack 2U", 10, 2, 15000.0, 1, 8500.0),
        (102, "Monitor Dell UltraSharp 27", 25, 5, 3200.0, 1, 1800.0),
        (201, "Kit Ferramentas Titanium Pro", 15, 3, 850.0, 2, 450.0),
        (301, "Sanitizante Hospitalar 5L", 50, 10, 120.0, 3, 45.0),
        (401, "Cadeira Ergonômica Herman Miller", 5, 2, 8500.0, 4, 5200.0)
    ]

    for d in massa_dados:
        p = Produto(d[0], d[1], d[2], d[3], d[4], d[5], "Alocação Automática", d[6], fornecedores=[])
        if cadastrar_produto(p): print(f"  + Ativo: {d[1]}")

    # Simulação de Fluxo
    print("📦 Simulando movimentações transacionais...")
    produtos = listar_produtos()
    if produtos:
        for _ in range(20):
            prod = random.choice(produtos)
            tipo = random.choice(["ENTRADA", "SAIDA"])
            qtd = random.randint(1, 5)
            registrar_movimentacao(prod[0], qtd, tipo, "Carga de Teste Automatizada")
    
    print("✅ [OK] Ecossistema pronto para operação.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Inventory. Engine - Gestão de Dados")
    parser.add_argument("--init", action="store_true", help="Inicializar schema")
    parser.add_argument("--seed", action="store_true", help="Popular massa de teste")
    args = parser.parse_args()

    if args.init: inicializar_sistema()
    if args.seed: popular_massa_teste()
    if not any(vars(args).values()):
        inicializar_sistema()
