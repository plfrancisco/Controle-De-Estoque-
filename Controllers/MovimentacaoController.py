# =================================================================
# CONTROLLER: MovimentacaoController
# Responsabilidade: Gestão de Fluxo de Estoque e Almoxarifado Físico
# =================================================================

import sqlite3
from Services.database import conectaBD

def registrar_movimentacao(codigo_produto, quantidade, tipo, id_usuario):
    """
    Executa uma transação completa de entrada ou saída.
    Além de registrar o log, atualiza o saldo do produto e a ocupação
    física nas caixas do almoxarifado.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    try:
        # Bloco 1: Registro do Evento (Log para auditoria)
        cursor.execute("""
            INSERT INTO movimentacao (tipo, codigo_produto, quantidade, id_usuario)
            VALUES (?, ?, ?, ?)
        """, (tipo, codigo_produto, quantidade, id_usuario))
        
        # Bloco 2: Atualização do Saldo Mestre
        # 'ENTRADA' soma (+1), 'SAIDA' subtrai (-1)
        fator = 1 if tipo == 'ENTRADA' else -1
        cursor.execute("""
            UPDATE produto 
            SET quantidade = quantidade + ? 
            WHERE codigo = ?
        """, (fator * quantidade, codigo_produto))
        
        # Bloco 3: Atualização do Almoxarifado (Lógica de Prateleiras)
        qtd_restante = quantidade
        
        if tipo == 'ENTRADA':
            # Algoritmo de Preenchimento: Tenta ocupar caixas que já possuem o item primeiro
            while qtd_restante > 0:
                cursor.execute("""
                    SELECT id, ocupacao FROM estrutura_armazenamento 
                    WHERE (produto_codigo = ? OR produto_codigo IS NULL OR ocupacao = 0)
                    AND ocupacao < 10 
                    ORDER BY (CASE WHEN produto_codigo = ? THEN 0 ELSE 1 END), id 
                    LIMIT 1
                """, (codigo_produto, codigo_produto))
                caixa = cursor.fetchone()
                
                if not caixa: break # Armazém lotado
                
                id_caixa, ocupacao_atual = caixa
                espaco_livre = 10 - ocupacao_atual
                qtd_a_inserir = min(qtd_restante, espaco_livre)
                
                cursor.execute("""
                    UPDATE estrutura_armazenamento 
                    SET ocupacao = ocupacao + ?, produto_codigo = ? 
                    WHERE id = ?
                """, (qtd_a_inserir, codigo_produto, id_caixa))
                
                qtd_restante -= qtd_a_inserir
                
        elif tipo == 'SAIDA':
            # Algoritmo de Retirada (LIFO reverso): Remove das caixas do fim para o início
            while qtd_restante > 0:
                cursor.execute("""
                    SELECT id, ocupacao FROM estrutura_armazenamento 
                    WHERE produto_codigo = ? AND ocupacao > 0
                    ORDER BY id DESC LIMIT 1
                """, (codigo_produto,))
                caixa = cursor.fetchone()
                
                if not caixa: break # Produto não encontrado
                
                id_caixa, ocupacao_atual = caixa
                qtd_a_remover = min(qtd_restante, ocupacao_atual)
                
                nova_ocupacao = ocupacao_atual - qtd_a_remover
                # Se a caixa esvaziar, removemos o vínculo com o produto
                novo_produto_codigo = codigo_produto if nova_ocupacao > 0 else None
                
                cursor.execute("""
                    UPDATE estrutura_armazenamento 
                    SET ocupacao = ?, produto_codigo = ? 
                    WHERE id = ?
                """, (nova_ocupacao, novo_produto_codigo, id_caixa))
                
                qtd_restante -= qtd_a_remover
        
        conexao.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro Transacional: {e}")
        conexao.rollback() # Cancela tudo se houver erro
        return False
    finally:
        conexao.close()

def listar_movimentacoes():
    """
    Retorna o histórico formatado para exibição nos relatórios.
    Faz um JOIN entre Movimentação e Produto para mostrar a descrição legível.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT m.id, m.tipo, m.codigo_produto, p.descricao, m.quantidade, m.id_usuario, m.data_hora
            FROM movimentacao m
            JOIN produto p ON m.codigo_produto = p.codigo
            ORDER BY m.data_hora DESC
        """)
        return cursor.fetchall()
    finally:
        conexao.close()

# -----------------------------------------------------------------
# GESTÃO DE ESTRUTURA (Prateleiras e Caixas)
# -----------------------------------------------------------------

def listar_prateleiras():
    """Retorna a lista de nomes únicos de prateleiras cadastradas."""
    conexao = conectaBD()
    cursor = conexao.cursor()
    cursor.execute("SELECT DISTINCT prateleira FROM estrutura_armazenamento ORDER BY prateleira")
    res = [str(r[0]) for r in cursor.fetchall() if r[0] is not None]
    conexao.close()
    return res

def listar_detalhes_almoxarifado():
    """Agrega dados por prateleira para visualização no dashboard de gestão."""
    conexao = conectaBD()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT 
            prateleira, 
            COUNT(id) as total_caixas,
            SUM(ocupacao) as total_ocupado,
            GROUP_CONCAT(DISTINCT produto_codigo) as produtos
        FROM estrutura_armazenamento
        GROUP BY prateleira
        ORDER BY prateleira
    """)
    res = cursor.fetchall()
    conexao.close()
    return res

def criar_prateleira(nome_prateleira):
    """Cria uma nova prateleira com 15 caixas vazias por padrão."""
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        nome_p = str(nome_prateleira)
        for i in range(1, 16):
            cursor.execute("""
                INSERT INTO estrutura_armazenamento (prateleira, caixa, ocupacao)
                VALUES (?, ?, 0)
            """, (nome_p, i))
        conexao.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        conexao.close()

def excluir_prateleira(numero_prateleira):
    """
    Só permite excluir uma prateleira se ela estiver vazia.
    Regra de Segurança: Impede perda acidental de estoque.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT SUM(ocupacao) FROM estrutura_armazenamento WHERE prateleira = ?", (numero_prateleira,))
        total_ocupado = cursor.fetchone()[0] or 0
        
        if total_ocupado > 0:
            return False, "A prateleira não está vazia. Transfira os itens antes."
        
        cursor.execute("DELETE FROM estrutura_armazenamento WHERE prateleira = ?", (numero_prateleira,))
        conexao.commit()
        return True, "Prateleira removida."
    except sqlite3.Error as e:
        return False, str(e)
    finally:
        conexao.close()
