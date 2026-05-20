# =================================================================
# VIEW: PageMovimentacao
# Responsabilidade: Gestão de Fluxo de Materiais (Entradas e Saídas)
# =================================================================

import streamlit as st
import pandas as pd
import time
from Controllers.ProdutoController import listar_produtos, buscar_produto_por_codigo
from Controllers.MovimentacaoController import registrar_movimentacao

def exibir_pagina():
    st.markdown("<h1 style='color: #FFFFFF; font-weight: 700; font-size: 2.5rem; letter-spacing: -1.5px; margin-bottom: 0px;'>Fluxo.</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748B; font-size: 1.1rem; font-weight: 500;'>Registro e Monitoramento de Entradas e Saídas de Ativos</p>", unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)

    # 1. FORMULÁRIO DE MOVIMENTAÇÃO (Organic Style)
    with st.container():
        with st.form("form_movimentacao_v8", clear_on_submit=True):
            st.markdown("<h3 style='color: #F8FAFC; margin-bottom: 20px;'>Nova Transação de Estoque</h3>", unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns([2, 1, 1])
            
            produtos = listar_produtos()
            with c1:
                prod_selecionado = st.selectbox(
                    "Identificar SKU para Operação",
                    options=[p[0] for p in produtos],
                    format_func=lambda x: next(f"ID {p[0]}: {p[1]}" for p in produtos if p[0] == x)
                )
            
            with c2:
                tipo = st.selectbox("Natureza da Operação", ["ENTRADA (Suprimento)", "SAÍDA (Consumo/Venda)"])
            
            with c3:
                quantidade = st.number_input("Quantidade", min_value=1, step=1)
            
            motivo = st.text_area("Justificativa / Observação Técnica", placeholder="Ex: Reposição de estoque semanal ou Venda direta para cliente X")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.form_submit_button("Sincronizar Operação", type="primary", use_container_width=True):
                tipo_db = "Entrada" if "ENTRADA" in tipo else "Saída"
                
                # Validação de Saldo para Saída
                if tipo_db == "Saída":
                    dados_p = buscar_produto_por_codigo(prod_selecionado)
                    qtd_atual = dados_p[2]
                    if quantidade > qtd_atual:
                        st.error(f"❌ Operação Negada: Saldo insuficiente em estoque (Saldo Disponível: {qtd_atual}).")
                        time.sleep(3.0)
                        st.rerun()
                        return

                # Processamento
                if registrar_movimentacao(prod_selecionado, quantidade, tipo_db, motivo):
                    st.success(f"✅ Protocolo de {tipo_db} concluído e registrado no log operacional.")
                    time.sleep(2.5)
                    st.rerun()
                else:
                    st.error("❌ Erro técnico: Falha ao persistir transação no banco de dados.")
                    time.sleep(3.0)

    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    
    # 2. TABELA DE INFRAESTRUTURA (Refined Grid)
    from Controllers.EstruturaController import listar_prateleiras
    st.markdown("<h3 style='color: #F8FAFC; margin-bottom: 20px;'>Mapa de Ocupação da Infraestrutura</h3>", unsafe_allow_html=True)
    
    prats = listar_prateleiras()
    if prats:
        rows_est = "".join([f"<tr><td style='font-weight: 600; color: #3B82F6;'>{p[0]}</td><td class='mono-data'>{p[1]}</td><td class='mono-data'>{p[2]}</td><td style='color: #64748B;'>{((p[2]/p[1])*100):.1f}% Ocupado</td></tr>" for p in prats])
        html_est = f"<table class='executive-grid'><thead><tr><th>Prateleira</th><th>Capacidade (Caixas)</th><th>Ocupação Atual</th><th>Eficiência</th></tr></thead><tbody>{rows_est}</tbody></table>"
        st.markdown(html_est, unsafe_allow_html=True)
    else:
        st.info("Aguardando definição de infraestrutura física para mapeamento.")
