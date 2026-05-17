# =================================================================
# SERVIÇO: Inicialização de Banco de Dados (inicializar_db.py)
# Responsabilidade: Criar a estrutura de tabelas (Schema) do sistema
# =================================================================

from Services.database import conectaBD

def criar_tabelas():
    """
    Executa comandos DDL (Data Definition Language) para criar as tabelas
    se elas ainda não existirem no arquivo .db.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    # Bloco 1: Gestão de Acesso
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        nivel_acesso TEXT NOT NULL
    )
    """)

    # Bloco 2: Apoio e Classificação
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fornecedor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        contato TEXT
    )
    """)

    # Bloco 3: Core do Negócio (Produtos e Estoque)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produto (
        codigo INTEGER PRIMARY KEY,
        descricao TEXT NOT NULL,
        quantidade INTEGER DEFAULT 0,
        quantidade_minima INTEGER DEFAULT 5,
        valor_unitario REAL,
        id_categoria INTEGER,
        id_fornecedor INTEGER,
        FOREIGN KEY (id_categoria) REFERENCES categoria(id),
        FOREIGN KEY (id_fornecedor) REFERENCES fornecedor(id)
    )
    """)

    # Bloco 4: Histórico Operacional
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimentacao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        codigo_produto INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        id_usuario INTEGER,
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (codigo_produto) REFERENCES produto(codigo),
        FOREIGN KEY (id_usuario) REFERENCES usuario(id)
    )
    """)

    # Bloco 5: Configuração Inicial (Seed Data)
    try:
        cursor.execute("INSERT INTO usuario (login, senha, nivel_acesso) VALUES (?, ?, ?)", 
                       ('admin', 'admin123', 'ADMIN'))
    except:
        pass # Ignora se o admin já estiver cadastrado

    conexao.commit()
    conexao.close()
    print("Sistema: Tabelas configuradas com sucesso!")

# Permite rodar este script diretamente via terminal para resetar/configurar o banco
if __name__ == "__main__":
    criar_tabelas()
