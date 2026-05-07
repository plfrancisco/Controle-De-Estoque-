import sqlite3
import qrcode
import os
from Services.database import conectaBD
from Models.Produto import Produto

def gerar_qrcode_produto(codigo):
    # Cria o diretório se não existir
    pasta_qrcodes = os.path.join(os.path.dirname(__file__), '..', 'qrcodes')
    if not os.path.exists(pasta_qrcodes):
        os.makedirs(pasta_qrcodes)
    
    # Gera o QR Code contendo apenas o código do produto
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(str(codigo))
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    caminho_arquivo = os.path.join(pasta_qrcodes, f"produto_{codigo}.png")
    img.save(caminho_arquivo)
    return caminho_arquivo

def encontrar_proxima_caixa_disponivel():
    conexao = conectaBD()
    cursor = conexao.cursor()
    # Busca a primeira caixa que não esteja cheia (ocupação < 10)
    cursor.execute("SELECT id, prateleira, caixa, ocupacao FROM estrutura_armazenamento WHERE ocupacao < 10 ORDER BY id LIMIT 1")
    res = cursor.fetchone()
    conexao.close()
    return res # Retorna (id, prateleira, caixa, ocupacao)

def ocupar_espaco_caixa(id_espaco, qtd_adicionar, produto_codigo):
    conexao = conectaBD()
    cursor = conexao.cursor()
    cursor.execute("UPDATE estrutura_armazenamento SET ocupacao = ocupacao + ?, produto_codigo = ? WHERE id = ?", 
                   (qtd_adicionar, produto_codigo, id_espaco))
    conexao.commit()
    conexao.close()

def cadastrar_produto(produto):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        qtd_total = produto.get_quantidade()
        codigo = produto.get_codigo()
        
        # 1. Inserir o produto na tabela produto
        cursor.execute("""
            INSERT INTO produto (codigo, descricao, quantidade, quantidade_minima, valor_unitario, id_categoria, localizacao, preco_custo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (codigo, produto.get_descricao(), qtd_total,
              produto.get_quantidade_minima(), produto.get_valor_unitario(),
              produto.get_categoria(), "Alocação Automática", produto.get_preco_custo()))
        
        # 2. Lógica de Alocação em Caixas (10 por caixa)
        qtd_restante = qtd_total
        while qtd_restante > 0:
            # Encontra a próxima caixa com espaço
            cursor.execute("SELECT id, ocupacao FROM estrutura_armazenamento WHERE ocupacao < 10 ORDER BY id LIMIT 1")
            caixa = cursor.fetchone()
            
            if not caixa:
                break # Acabaram as caixas (30 prateleiras x 15 caixas = 4500 itens max)
            
            id_caixa, ocupacao_atual = caixa
            espaco_livre = 10 - ocupacao_atual
            qtd_a_inserir = min(qtd_restante, espaco_livre)
            
            cursor.execute("UPDATE estrutura_armazenamento SET ocupacao = ocupacao + ?, produto_codigo = ? WHERE id = ?", 
                           (qtd_a_inserir, codigo, id_caixa))
            
            qtd_restante -= qtd_a_inserir
        
        conexao.commit()
        return True
    except sqlite3.Error as e:
        print(f"\n[!] Erro ao cadastrar produto: {e}")
        return False
    finally:
        conexao.close()


def listar_categorias():
    conexao = conectaBD()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome FROM categoria")
    res = cursor.fetchall() # Retorna [(1, 'Eletrônicos'), ...]
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
