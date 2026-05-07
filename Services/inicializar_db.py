from Services.database import conectaBD

def criar_tabelas():
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    # Tabela Usuario
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        nivel_acesso TEXT NOT NULL
    )
    """)

    # Tabela Categoria
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    """)

    # Tabela Fornecedor
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fornecedor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        contato TEXT
    )
    """)

    # Tabela Produto
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

    # Tabela Movimentacao
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

    # Criar usuário admin padrão (senha simples para teste: 'admin123')
    try:
        cursor.execute("INSERT INTO usuario (login, senha, nivel_acesso) VALUES (?, ?, ?)", 
                       ('admin', 'admin123', 'ADMIN'))
    except:
        pass # Usuário já existe

    conexao.commit()
    conexao.close()
    print("Banco de dados e tabelas configurados com sucesso!")

if __name__ == "__main__":
    criar_tabelas()
