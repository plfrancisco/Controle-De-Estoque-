import sqlite3
from Services.database import conectaBD

def registrar_movimentacao(codigo_produto, quantidade, tipo, id_usuario):
    """
    Registra uma movimentação (ENTRADA ou SAIDA) e atualiza o estoque e a estrutura de armazenamento.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    try:
        # 1. Registrar na tabela movimentacao
        cursor.execute("""
            INSERT INTO movimentacao (tipo, codigo_produto, quantidade, id_usuario)
            VALUES (?, ?, ?, ?)
        """, (tipo, codigo_produto, quantidade, id_usuario))
        
        # 2. Atualizar a quantidade na tabela produto
        fator = 1 if tipo == 'ENTRADA' else -1
        cursor.execute("""
            UPDATE produto 
            SET quantidade = quantidade + ? 
            WHERE codigo = ?
        """, (fator * quantidade, codigo_produto))
        
        # 3. Atualizar a estrutura de armazenamento
        qtd_restante = quantidade
        
        if tipo == 'ENTRADA':
            # Preencher caixas disponíveis
            while qtd_restante > 0:
                # Busca caixa que já contenha o produto e tenha espaço, ou uma caixa vazia
                cursor.execute("""
                    SELECT id, ocupacao FROM estrutura_armazenamento 
                    WHERE (produto_codigo = ? OR produto_codigo IS NULL OR ocupacao = 0)
                    AND ocupacao < 10 
                    ORDER BY (CASE WHEN produto_codigo = ? THEN 0 ELSE 1 END), id 
                    LIMIT 1
                """, (codigo_produto, codigo_produto))
                caixa = cursor.fetchone()
                
                if not caixa:
                    break # Sem espaço no armazém
                
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
            # Remover das caixas onde o produto está (da última para a primeira para "esvaziar" o armazém do fim)
            while qtd_restante > 0:
                cursor.execute("""
                    SELECT id, ocupacao FROM estrutura_armazenamento 
                    WHERE produto_codigo = ? AND ocupacao > 0
                    ORDER BY id DESC LIMIT 1
                """, (codigo_produto,))
                caixa = cursor.fetchone()
                
                if not caixa:
                    break # Produto não encontrado em nenhuma caixa (erro de integridade?)
                
                id_caixa, ocupacao_atual = caixa
                qtd_a_remover = min(qtd_restante, ocupacao_atual)
                
                nova_ocupacao = ocupacao_atual - qtd_a_remover
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
        print(f"Erro ao registrar movimentação: {e}")
        conexao.rollback()
        return False
    finally:
        conexao.close()

def listar_movimentacoes():
    """
    Retorna o histórico completo de movimentações com detalhes de produto e usuário.
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
