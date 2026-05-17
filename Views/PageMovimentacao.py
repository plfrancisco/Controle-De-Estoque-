# =================================================================
# VIEW: PageMovimentacao
# Responsabilidade: Gestão de Entradas/Saídas e Estrutura Física (Almoxarifado)
# =================================================================

import streamlit as st
from Controllers.ProdutoController import listar_produtos, buscar_produto_por_codigo
from Controllers.MovimentacaoController import (
    registrar_movimentacao, 
    listar_movimentacoes, 
    listar_prateleiras, 
    criar_prateleira, 
    excluir_prateleira,
    listar_detalhes_almoxarifado
)
import pandas as pd

def exibir_pagina():
    st.title("Movimentação de Estoque")
    st.markdown("---")
    
    # Divisão entre Operações Diárias e Gestão de Estrutura
    tab_mov, tab_estrutura = st.tabs(["Movimentações", "Gestão de Almoxarifado"])
    
    # --- ABA 1: REGISTRO DE FLUXO ---
    with tab_mov:
        dados = listar_produtos()
        if not dados:
            st.warning("Cadastre produtos antes de realizar movimentações.")
        else:
            df_p = pd.DataFrame(dados, columns=["Código", "Descrição", "Qtd", "Min", "V", "C", "F", "L", "P"])
            
            st.markdown("### Registrar Nova Operação")
            with st.form("form_movimentacao", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    opcao_selecionada = st.selectbox(
                        "Selecione o Produto",
                        options=df_p["Código"].tolist(),
                        format_func=lambda x: f"{x} - {df_p[df_p['Código']==x]['Descrição'].values[0]}"
                    )
                    tipo = st.radio("Tipo de Movimentação", ["ENTRADA", "SAIDA"], horizontal=True)
                with col2:
                    qtd = st.number_input("Quantidade", min_value=1, step=1)
                    motivo = st.text_input("Observação/Motivo (Opcional)")
                
                if st.form_submit_button("Confirmar Movimentação"):
                    produto_db = buscar_produto_por_codigo(opcao_selecionada)
                    qtd_atual = produto_db[2]
                    
                    # Validação de Negócio: Impede saída maior que o saldo
                    if tipo == "SAIDA" and qtd > qtd_atual:
                        st.error(f"Operação negada: Saldo insuficiente. Estoque atual: {qtd_atual}")
                    else:
                        if registrar_movimentacao(opcao_selecionada, qtd, tipo, 1):
                            st.toast(f"{tipo} concluída!", icon="🚀")
                            st.rerun()
                        else:
                            st.error("Erro ao salvar no banco.")

            st.markdown("### Histórico Recente")
            historico = listar_movimentacoes()
            if historico:
                df_h = pd.DataFrame(historico, columns=["ID", "Tipo", "Cód. Produto", "Descrição", "Qtd", "User", "Data/Hora"])
                st.dataframe(df_h, use_container_width=True)

    # --- ABA 2: GESTÃO FÍSICA (ALMOXARIFADO) ---
    with tab_estrutura:
        st.markdown("### Status do Almoxarifado")
        detalhes_a = listar_detalhes_almoxarifado()
        if detalhes_a:
            df_a = pd.DataFrame(detalhes_a, columns=["Prateleira", "Total Caixas", "Itens Totais", "Produtos (SKUs)"])
            # Visualização Progressiva da Ocupação Física
            st.dataframe(
                df_a, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "Itens Totais": st.column_config.ProgressColumn(
                        "Ocupação Física", min_value=0, max_value=150, format="%d itens"
                    )
                }
            )

        st.divider()
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.markdown("#### Adicionar Prateleira")
            nova_p = st.text_input("Identificação (Ex: P31, Setor A)")
            if st.button("Criar Estrutura"):
                if nova_p:
                    if criar_prateleira(nova_p):
                        st.toast(f"Estrutura {nova_p} adicionada!", icon="🏗️")
                        st.rerun()
        
        with col_c2:
            st.markdown("#### Remover Prateleira")
            prateleiras_atuais = listar_prateleiras()
            if prateleiras_atuais:
                p_excluir = st.selectbox("Selecione para Excluir", options=prateleiras_atuais)
                with st.popover("Confirmar Remoção", use_container_width=True):
                    if st.button("Sim, Excluir", type="primary", use_container_width=True):
                        sucesso, msg = excluir_prateleira(p_excluir)
                        if sucesso: st.rerun()
                        else: st.error(msg)
