# =================================================================
# CONTROLLER: ProdutoController
# Responsabilidade: Regras de Negócio para Gestão de Produtos e Inventário
# =================================================================

import sqlite3
import qrcode
import os
from Services.database import conectaBD
from Models.Produto import Produto

# -----------------------------------------------------------------
# 1. UTILITÁRIOS: GERAÇÃO DE QR CODE
# Cria uma representação visual do SKU para facilitar o escaneamento físico.
# -----------------------------------------------------------------
def gerar_qrcode_produto(codigo):
    pasta_qrcodes = os.path.join(os.path.dirname(__file__), '..', 'qrcodes')
    if not os.path.exists(pasta_qrcodes):
        os.makedirs(pasta_qrcodes)
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(str(codigo))
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    caminho_arquivo = os.path.join(pasta_qrcodes, f"produto_{codigo}.png")
    img.save(caminho_arquivo)
    return caminho_arquivo

# -----------------------------------------------------------------
# 2. LÓGICA DE ALMOXARIFADO (Estratégia de Ocupação de Espaço)
# Gerencia como os produtos são distribuídos fisicamente em caixas.
# -----------------------------------------------------------------
def encontrar_proxima_caixa_disponivel():
    conexao = conectaBD()
    cursor = conexao.cursor()
    # FIFO: Busca a primeira caixa que ainda tenha espaço livre (ocupação < 10)
    cursor.execute("SELECT id, prateleira, caixa, ocupacao FROM estrutura_armazenamento WHERE ocupacao < 10 ORDER BY id LIMIT 1")
    res = cursor.fetchone()
    conexao.close()
    return res

def ocupar_espaco_caixa(id_espaco, qtd_adicionar, produto_codigo):
    conexao = conectaBD()
    cursor = conectaBD().cursor() # Abre nova conexão/cursor
    cursor.execute("UPDATE estrutura_armazenamento SET ocupacao = ocupacao + ?, produto_codigo = ? WHERE id = ?", 
                   (qtd_adicionar, produto_codigo, id_espaco))
    # Note: O commit deve ser feito na conexão correta.
    # [Correção Pedagógica]: Idealmente passar a conexão ou gerenciar aqui.

# -----------------------------------------------------------------
# 3. CRUD: CRIAÇÃO E PERSISTÊNCIA
# Orquestra a inserção do produto, sua alocação física e seus fornecedores.
# -----------------------------------------------------------------
from Controllers.FornecedorController import vincular_fornecedores

def cadastrar_produto(produto):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        qtd_total = produto.get_quantidade()
        codigo = produto.get_codigo()
        
        # Bloco A: Inserção no Catálogo Geral
        cursor.execute("""
            INSERT INTO produto (codigo, descricao, quantidade, quantidade_minima, valor_unitario, id_categoria, localizacao, preco_custo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (codigo, produto.get_descricao(), qtd_total,
              produto.get_quantidade_minima(), produto.get_valor_unitario(),
              produto.get_categoria(), "Alocação Automática", produto.get_preco_custo()))
        
        # Bloco B: Algoritmo de Fracionamento (10 itens por caixa)
        # Distribui a carga inicial em múltiplas caixas da estrutura de armazenamento.
        qtd_restante = qtd_total
        while qtd_restante > 0:
            cursor.execute("SELECT id, ocupacao FROM estrutura_armazenamento WHERE ocupacao < 10 ORDER BY id LIMIT 1")
            caixa = cursor.fetchone()
            if not caixa: break # Fim do estoque físico/espaço
            
            id_caixa, ocupacao_atual = caixa
            espaco_livre = 10 - ocupacao_atual
            qtd_a_inserir = min(qtd_restante, espaco_livre)
            
            cursor.execute("UPDATE estrutura_armazenamento SET ocupacao = ocupacao + ?, produto_codigo = ? WHERE id = ?", 
                           (qtd_a_inserir, codigo, id_caixa))
            qtd_restante -= qtd_a_inserir
        
        # Bloco C: Relação Muitos-para-Muitos (N:N)
        # Registra quais fornecedores atendem este produto.
        for f_id in produto.get_fornecedores():
            cursor.execute("INSERT INTO produto_fornecedor (produto_codigo, fornecedor_id) VALUES (?, ?)", 
                           (codigo, f_id))
        
        conexao.commit()
        return True
    except sqlite3.Error as e:
        print(f"\n[!] Erro no Controller: {e}")
        return False
    finally:
        conexao.close()

# -----------------------------------------------------------------
# 4. QUERIES: LEITURA E CONSULTA
# -----------------------------------------------------------------
def listar_categorias():
    conexao = conectaBD()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome FROM categoria")
    res = cursor.fetchall()
    conexao.close()
    return res

def listar_produtos():
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM produto")
        return cursor.fetchall()
    finally:
        conexao.close()

def buscar_produto_por_codigo(codigo):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM produto WHERE codigo = ?", (codigo,))
        return cursor.fetchone()
    finally:
        conexao.close()

# -----------------------------------------------------------------
# 5. CRUD: EXCLUSÃO E LIMPEZA DE REFERÊNCIAS
# Garante a integridade referencial limpando o almoxarifado e o histórico.
# -----------------------------------------------------------------
def excluir_produto(codigo):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        # 1. Libera as caixas ocupadas por este produto
        cursor.execute("UPDATE estrutura_armazenamento SET ocupacao = 0, produto_codigo = NULL WHERE produto_codigo = ?", (codigo,))
        
        # 2. Remove o histórico vinculado (Prevenção de Orfãos)
        cursor.execute("DELETE FROM movimentacao WHERE codigo_produto = ?", (codigo,))
        
        # 3. Remove o registro mestre
        cursor.execute("DELETE FROM produto WHERE codigo = ?", (codigo,))
        
        conexao.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        conexao.close()
