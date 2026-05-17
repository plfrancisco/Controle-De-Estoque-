# =================================================================
# SCRIPT DE CARGA: popular_dados_reais.py
# Responsabilidade: Popular o banco com um catálogo inicial diversificado
# =================================================================

import sys
import os

# Ajusta o sys.path para permitir importações dos módulos do projeto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Controllers.ProdutoController import cadastrar_produto, listar_categorias
from Models.Produto import Produto

def popular():
    """
    Insere uma lista pré-definida de produtos para facilitar
    a visualização do sistema em funcionamento (Protótipo/MVP).
    """
    print("Sistema: Iniciando carga de dados reais...")
    
    # Matriz de Dados: (código, descrição, quantidade inicial, alerta mín, preço venda, categoria, preço custo)
    produtos_reais = [
        # Setor de Eletrônicos
        (101, "Smartphone Samsung Galaxy A54", 15, 5, 2100.00, 1, 1500.00),
        (102, "Mouse Sem Fio Logitech M280", 45, 10, 89.90, 1, 45.00),
        (103, "Teclado Mecânico HyperX Alloy", 12, 3, 450.00, 1, 280.00),
        (104, "Monitor Dell 24 Polegadas", 8, 2, 950.00, 1, 650.00),
        
        # Setor de Ferramentas
        (201, "Parafusadeira DeWalt 20V", 6, 2, 850.00, 2, 580.00),
        (202, "Jogo de Chaves combinadas 12pçs", 25, 5, 120.00, 2, 75.00),
        (203, "Martelo de Unha Tramontina", 40, 8, 35.00, 2, 18.00),
        
        # Setor de Limpeza
        (301, "Detergente Neutro 500ml", 120, 20, 2.50, 3, 1.20),
        (302, "Desinfetante Pinho Sol 1L", 60, 15, 12.00, 3, 6.50),
        (303, "Papel Toalha (Fardo 12 rolos)", 30, 10, 22.00, 3, 14.00),
        
        # Setor de Escritório
        (401, "Cadeira de Escritório Ergonômica", 5, 2, 1200.00, 4, 850.00),
        (402, "Resma de Papel A4 500fls", 200, 50, 28.00, 4, 19.50),
        (403, "Caneta Bic Azul (Caixa 50un)", 50, 10, 45.00, 4, 25.00),
        
        # Setor Gourmet/Copa
        (501, "Café Gourmet 500g", 35, 10, 24.90, 5, 15.00),
        (502, "Açúcar Refinado 1kg", 80, 20, 4.50, 5, 2.80)
    ]

    sucessos = 0
    erros = 0

    # Itera sobre a lista criando objetos da classe Produto e salvando via Controller
    for p_info in produtos_reais:
        novo_p = Produto(
            codigo=p_info[0],
            descricao=p_info[1],
            quantidade=p_info[2],
            quantidade_minima=p_info[3],
            valor_unitario=p_info[4],
            categoria=p_info[5],
            localizacao="Alocação Automática",
            preco_custo=p_info[6]
        )
        
        if cadastrar_produto(novo_p):
            print(f"[OK] Cadastrado: {p_info[1]}")
            sucessos += 1
        else:
            print(f"[ERRO] Falha ao cadastrar: {p_info[1]}")
            erros += 1

    print(f"\nResumo: {sucessos} sucessos, {erros} falhas.")

if __name__ == "__main__":
    popular()
