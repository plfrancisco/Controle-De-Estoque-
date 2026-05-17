# =================================================================
# CONTROLLER: FornecedorController
# Responsabilidade: Gestão de Contatos e Vínculos com Fornecedores
# =================================================================

from Services.database import conectaBD

def listar_fornecedores():
    """Retorna lista de todos os fornecedores cadastrados."""
    conexao = conectaBD()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome FROM fornecedor")
    res = cursor.fetchall()
    conexao.close()
    return res

def vincular_fornecedores(produto_codigo, lista_fornecedores_ids):
    """Cria os vínculos na tabela associativa (Muitos para Muitos)."""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        for f_id in lista_fornecedores_ids:
            cursor.execute("INSERT INTO produto_fornecedor (produto_codigo, fornecedor_id) VALUES (?, ?)", 
                           (produto_codigo, f_id))
        conexao.commit()
        return True
    except:
        return False
    finally:
        conexao.close()

def listar_fornecedores_por_produto(produto_codigo):
    """Retorna os nomes dos fornecedores que atendem um determinado SKU."""
    conexao = conectaBD()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT f.nome FROM fornecedor f
        JOIN produto_fornecedor pf ON f.id = pf.fornecedor_id
        WHERE pf.produto_codigo = ?
    """, (produto_codigo,))
    res = [r[0] for r in cursor.fetchall()]
    conexao.close()
    return res

def cadastrar_fornecedor(nome, cnpj, email, telefone):
    """Insere um novo fornecedor com dados de contato completos."""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        # Preenche campos novos e o legado (contato) para compatibilidade
        cursor.execute("""
            INSERT INTO fornecedor (nome, cnpj, email, telefone, contato) 
            VALUES (?, ?, ?, ?, ?)
        """, (nome, cnpj, email, telefone, email))
        conexao.commit()
        return True
    except Exception as e:
        print(f"Erro no cadastro: {e}")
        return False
    finally:
        conexao.close()
