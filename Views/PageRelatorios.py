import streamlit as st
import pandas as pd
from Controllers.ProdutoController import listar_produtos
from Controllers.MovimentacaoController import listar_movimentacoes
import plotly.express as px
from io import BytesIO

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    processed_data = output.getvalue()
    return processed_data

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
# Converte um DataFrame do Pandas em um arquivo Excel binário para download.
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
    st.title("Relatórios Consolidados")
    st.markdown("---")
    
    # Bloco A: Coleta de Dados via Controllers
    # Buscamos os dados brutos do banco para transformar em DataFrames do Pandas.
    dados_p = listar_produtos()
    historico = listar_movimentacoes()
    
    # -------------------------------------------------------------
    # 3. SEÇÃO DE EXPORTAÇÃO (Topo)
    # Organiza os botões de download em colunas para economizar espaço.
    # -------------------------------------------------------------
    st.subheader("🛠️ Central de Exportação")
    c_exp1, c_exp2, c_exp3 = st.columns(3)
    
    # Processamento e Download de Inventário
    if dados_p:
        df_p = pd.DataFrame(dados_p, columns=[
            "Código", "Descrição", "Qtd Atual", "Qtd Mínima", 
            "Valor Venda", "ID Categoria", "ID Fornecedor", "Localização", "Preço Custo"
        ])
        
        with c_exp1:
            st.download_button(
                label="📦 Baixar Inventário (Excel)",
                data=to_excel(df_p),
                file_name='inventario_completo.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width=True
            )
        
        with c_exp2:
            # Filtro rápido para identificar itens em risco
            criticos = df_p[df_p["Qtd Atual"] <= df_p["Qtd Mínima"]]
            st.download_button(
                label=f"⚠️ Baixar Críticos ({len(criticos)})",
                data=to_excel(criticos),
                file_name='estoque_critico.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width=True
            )
    else:
        with c_exp1: st.info("Sem dados de inventário")
    
    # Exportação de Movimentações
    if historico:
        df_h = pd.DataFrame(historico, columns=["ID", "Tipo", "Cód. Produto", "Descrição", "Qtd", "User", "Data/Hora"])
        with c_exp3:
            st.download_button(
                label="📜 Baixar Histórico (Excel)",
                data=to_excel(df_h),
                file_name='historico_movimentacoes.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width=True
            )
    else:
        with c_exp3: st.info("Sem histórico registrado")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # -------------------------------------------------------------
    # 4. ANÁLISE VISUAL (Gráficos Lado a Lado)
    # Utiliza Plotly Express para gerar gráficos interativos.
    # -------------------------------------------------------------
    st.subheader("📊 Análise Visual Consolidada")
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        # Gráfico de Investimento (Pizza)
        if dados_p:
            df_p["Valor Total"] = df_p["Qtd Atual"] * df_p["Preço Custo"]
            fig_pie = px.pie(df_p, values='Valor Total', names='ID Categoria', 
                            title='Investimento por Categoria',
                            color_discrete_sequence=px.colors.sequential.Purp)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("Aguardando dados de inventário...")

    with col_g2:
        # Gráfico de Fluxo Operacional (Barras)
        if historico:
            # Agrupamento para somar quantidades por tipo de operação
            fluxo = df_h.groupby('Tipo')['Qtd'].sum().reset_index()
            fig_bar = px.bar(fluxo, x='Tipo', y='Qtd', color='Tipo',
                            color_discrete_map={"ENTRADA": "#7F56D9", "SAIDA": "#FDA29B"},
                            title="Volume Operacional (Entradas vs Saídas)")
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Aguardando histórico de movimentações...")

    # -------------------------------------------------------------
    # 5. TABELA DE AUDITORIA
    # Exibe a tabela bruta para conferência detalhada pelo usuário.
    # -------------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🕵️ Histórico Detalhado de Operações")
    if historico:
        st.dataframe(df_h, use_container_width=True)
    else:
        st.info("Nenhuma movimentação para exibir.")
