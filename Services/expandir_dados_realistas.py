# =================================================================
# SCRIPT DE EXPANSÃO: expandir_dados_realistas.py
# Responsabilidade: Estressar o sistema com volume de dados e movimentações
# =================================================================

import sys
import os
import random
from datetime import datetime, timedelta

# Configura o path para encontrar os módulos mestre do projeto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Controllers.ProdutoController import cadastrar_produto, listar_produtos
from Controllers.MovimentacaoController import registrar_movimentacao
from Models.Produto import Produto

def expandir_dados():
    """
    Adiciona novos produtos e gera movimentações aleatórias para testar
    a robustez dos gráficos e do almoxarifado físico.
    """
    print("🚀 Iniciando expansão de massa de dados...")
    
    # 1. Cadastro de novos itens para diversificar o catálogo
    novos_produtos = [
        (601, "Cabo HDMI 2.0 2 metros", 50, 10, 45.00, 1, 15.00),
        (602, "Headset Gamer Redragon", 20, 5, 299.00, 1, 145.00),
        (204, "Alicate Universal Gedore", 30, 8, 75.00, 2, 42.00),
        (205, "Nível de Mão Alumínio 30cm", 15, 3, 55.00, 2, 28.00),
        (304, "Álcool em Gel 70% 5L", 40, 10, 48.00, 3, 22.00),
        (305, "Vassoura Multiuso Reforçada", 25, 5, 18.50, 3, 8.00),
        (404, "Grampeador de Mesa Metal", 12, 4, 32.00, 4, 14.50),
        (405, "Calculadora Científica Casio", 18, 5, 115.00, 4, 65.00),
        (503, "Copo Térmico Inox 473ml", 60, 10, 85.00, 5, 35.00),
        (504, "Garrafa de Água Esportiva 1L", 100, 20, 25.00, 5, 9.00)
    ]

    for p_info in novos_produtos:
        p = Produto(p_info[0], p_info[1], p_info[2], p_info[3], p_info[4], p_info[5], "Alocação Automática", p_info[6], fornecedores=[1, 2])
        if cadastrar_produto(p):
            print(f"[OK] Adicionado: {p_info[1]}")

    # 2. Geração de Movimentações Aleatórias (Simulação de Uso Diário)
    produtos_atuais = listar_produtos()
    tipos = ["ENTRADA", "SAIDA"]
    
    mov_sucesso = 0
    for _ in range(30): # Gera 30 registros aleatórios no histórico
        prod = random.choice(produtos_atuais)
        codigo = prod[0]
        qtd_atual = prod[2]
        tipo = random.choice(tipos)
        
        # Lógica de segurança para não tentar retirar mais do que existe no mock
        if tipo == "SAIDA":
            qtd_mov = random.randint(1, min(qtd_atual, 5) if qtd_atual > 0 else 1)
        else:
            qtd_mov = random.randint(1, 10)
            
        if registrar_movimentacao(codigo, qtd_mov, tipo, 1):
            mov_sucesso += 1

    print(f"\n✅ Concluído: {mov_sucesso} movimentações simuladas.")

if __name__ == "__main__":
    expandir_dados()
