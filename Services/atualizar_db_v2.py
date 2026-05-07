from Services.database import conectaBD

def atualizar_esquema():
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    # Adicionando colunas de Localização e Preço de Custo se não existirem
    try:
        cursor.execute("ALTER TABLE produto ADD COLUMN localizacao TEXT")
    except: pass
    
    try:
        cursor.execute("ALTER TABLE produto ADD COLUMN preco_custo REAL")
    except: pass

    # Criando tabela de categorias se não existir (para o menu dinâmico)
    cursor.execute("CREATE TABLE IF NOT EXISTS categorias_log (nome TEXT UNIQUE)")
    categorias = ['Eletrônicos', 'Ferramentas', 'Limpeza', 'Escritório', 'Outros']
    for cat in categorias:
        try:
            cursor.execute("INSERT INTO categorias_log (nome) VALUES (?)", (cat,))
        except: pass

    conexao.commit()
    conexao.close()
    print("Esquema do banco de dados atualizado para o novo layout!")

if __name__ == "__main__":
    atualizar_esquema()
