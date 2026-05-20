# =================================================================
# VIEW: PageRelatorios
# Responsabilidade: Interface de Análise de Dados e Exportação
# =================================================================

import streamlit as st
import pandas as pd
from Controllers.ProdutoController import listar_produtos
from Controllers.MovimentacaoController import listar_movimentacoes
import plotly.express as px
from io import BytesIO

# -----------------------------------------------------------------
# 1. FUNÇÃO AUXILIAR: EXPORTAÇÃO EXCEL
# -----------------------------------------------------------------
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Relatorio')
    writer.close()
    return output.getvalue()

# -----------------------------------------------------------------
# 2. RENDERIZAÇÃO DA PÁGINA
# -----------------------------------------------------------------
def exibir_pagina():
    st.markdown("<h1 style='color: #FFFFFF; font-weight: 700; font-size: 2.5rem; letter-spacing: -1.5px; margin-bottom: 0px;'>Relatórios.</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748B; font-size: 1.1rem; font-weight: 500;'>Auditoria e Exportação de Inteligência Operacional</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    dados_p = listar_produtos()
    historico = listar_movimentacoes()
    
    # -------------------------------------------------------------
    # 3. SEÇÃO DE EXPORTAÇÃO (Central de Dados)
    # -------------------------------------------------------------
    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #F8FAFC; margin-bottom: 25px;'>Central de Exportação de Dados</h3>", unsafe_allow_html=True)
    c_exp1, c_exp2, c_exp3 = st.columns(3)
    
    if dados_p:
        df_p = pd.DataFrame(dados_p, columns=[
            "Código", "Descrição", "Qtd Atual", "Qtd Mínima", 
            "Valor Venda", "ID Categoria", "ID Fornecedor", "Localização", "Preço Custo"
        ])
        
        with c_exp1:
            st.download_button(
                label="Extrair Inventário (Excel)",
                data=to_excel(df_p),
                file_name='relatorio_inventario.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width=True
            )
        
        with c_exp2:
            criticos = df_p[df_p["Qtd Atual"] <= df_p["Qtd Mínima"]]
            st.download_button(
                label=f"Extrair Itens Críticos ({len(criticos)})",
                data=to_excel(criticos),
                file_name='relatorio_estoque_critico.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width=True
            )
    else:
        with c_exp1: st.info("Sem dados de inventário")
    
    if historico:
        df_h = pd.DataFrame(historico, columns=["ID", "Tipo", "Cód. Produto", "Descrição", "Qtd", "User", "Data/Hora"])
        with c_exp3:
            st.download_button(
                label="Extrair Log de Fluxo (Excel)",
                data=to_excel(df_h),
                file_name='historico_operacional.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width=True
            )
    else:
        with c_exp3: st.info("Sem histórico registrado")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # -------------------------------------------------------------
    # 4. ANÁLISE VISUAL (Performance Corporativa)
    # -------------------------------------------------------------
    st.markdown("### Análise Visual de Performance")
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        if dados_p:
            df_p["Valor Total"] = df_p["Qtd Atual"] * df_p["Preço Custo"]
            fig_pie = px.pie(df_p, values='Valor Total', names='ID Categoria', 
                            title='Alocação de Capital por Categoria',
                            color_discrete_sequence=px.colors.sequential.Blues_r,
                            template="plotly_dark")
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("Aguardando sincronização de dados...")

    with col_g2:
        if historico:
            fluxo = df_h.groupby('Tipo')['Qtd'].sum().reset_index()
            fig_bar = px.bar(fluxo, x='Tipo', y='Qtd', color='Tipo',
                            color_discrete_map={"ENTRADA": "#3B82F6", "SAIDA": "#94A3B8"},
                            title="Volume de Operações (Entradas vs Saídas)",
                            template="plotly_dark")
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Aguardando histórico operacional...")

    # -------------------------------------------------------------
    # 5. AUDITORIA DE REGISTROS
    # -------------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Histórico Consolidado de Auditoria")
    if historico:
        st.dataframe(df_h, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma movimentação identificada na base.")
