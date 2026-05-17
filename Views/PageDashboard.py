# =================================================================
# VIEW: PageDashboard
# Responsabilidade: Painel de Indicadores Estratégicos e Performance
# =================================================================

import streamlit as st
from streamlit_lottie import st_lottie
import requests
from Controllers.ProdutoController import listar_produtos
import pandas as pd
import plotly.express as px

def load_lottieurl(url):
    """Auxiliar: Carrega animações JSON de URLs externas."""
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

def exibir_pagina():
    # -------------------------------------------------------------
    # 1. CABEÇALHO COM ANIMAÇÃO
    # -------------------------------------------------------------
    lottie_url = "https://assets5.lottiefiles.com/packages/lf20_qpwb7qhc.json"
    lottie_json = load_lottieurl(lottie_url)

    col_title, col_anim = st.columns([3, 1])
    with col_title:
        st.markdown("<h1 style='color: #FF6B6B;'>Performance Geral</h1>", unsafe_allow_html=True)
        st.markdown("Bem-vindo ao seu centro estratégico de inventário.")
    with col_anim:
        if lottie_json:
            st_lottie(lottie_json, height=100, key="welcome")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # -------------------------------------------------------------
    # 2. COLETA E LIMPEZA DE DADOS
    # -------------------------------------------------------------
    dados = listar_produtos()
    
    if dados:
        df = pd.DataFrame(dados, columns=[
            "Código", "Descrição", "Qtd Atual", "Qtd Mínima", 
            "Valor Venda", "ID Categoria", "ID Fornecedor", "Localização", "Preço Custo"
        ])
        
        # Conversão de tipos para garantir cálculos matemáticos precisos
        for col in ["Qtd Atual", "Preço Custo", "Valor Venda"]:
            df[col] = pd.to_numeric(df[col]).fillna(0)
        
        # -------------------------------------------------------------
        # 3. KPIS (Métricas de Topo)
        # -------------------------------------------------------------
        total_skus = len(df)
        valor_estoque = (df["Qtd Atual"] * df["Preço Custo"]).sum()
        lucro_potencial = (df["Qtd Atual"] * (df["Valor Venda"] - df["Preço Custo"])).sum()
        itens_criticos = len(df[df["Qtd Atual"] <= df["Qtd Mínima"]])
        
        # Estilização CSS para os cartões de métricas
        st.markdown("""
            <style>
            div[data-testid="metric-container"] {
                background: linear-gradient(135deg, rgba(255, 107, 107, 0.1) 0%, rgba(255, 179, 71, 0.1) 100%);
                border: 1px solid rgba(255, 107, 107, 0.2);
                padding: 20px;
                border-radius: 16px;
                text-align: center;
            }
            [data-testid="stMetricLabel"] { color: #FFB347 !important; font-weight: 600 !important; }
            [data-testid="stMetricValue"] { color: #FAFAFA !important; }
            </style>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("SKUs Ativos", total_skus)
        c2.metric("Valor Patrimonial", f"R$ {valor_estoque:,.2f}")
        c3.metric("Lucro Estimado", f"R$ {lucro_potencial:,.2f}")
        c4.metric("Atenção Crítica", itens_criticos)

        # -------------------------------------------------------------
        # 4. ANÁLISE DE CURVA ABC
        # Classifica produtos por relevância financeira acumulada.
        # -------------------------------------------------------------
        st.markdown("<br>### Estratégia de Valor (Curva ABC)", unsafe_allow_html=True)
        df["Valor Total"] = df["Qtd Atual"] * df["Preço Custo"]
        df = df.sort_values(by="Valor Total", ascending=False)
        df["Soma Acumulada"] = df["Valor Total"].cumsum()
        total_geral = df["Valor Total"].sum()
        df["Percentual Acumulado"] = (df["Soma Acumulada"] / total_geral) * 100 if total_geral > 0 else 0
        
        def classificar_abc(row):
            if row["Percentual Acumulado"] <= 80: return "Classe A (Prioritário)"
            elif row["Percentual Acumulado"] <= 95: return "Classe B (Intermediário)"
            else: return "Classe C (Baixo Valor)"
            
        df["Classe"] = df.apply(classificar_abc, axis=1)
        
        fig_abc = px.bar(df, x="Descrição", y="Valor Total", color="Classe",
                        color_discrete_map={
                            "Classe A (Prioritário)": "#FF6B6B", 
                            "Classe B (Intermediário)": "#FFB347", 
                            "Classe C (Baixo Valor)": "#FFE066"
                        },
                        template="plotly_dark")
        fig_abc.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_abc, use_container_width=True)

        # -------------------------------------------------------------
        # 5. VISÃO DE QUANTIDADES
        # -------------------------------------------------------------
        st.markdown("### Panorama de Quantidades")
        st.bar_chart(df.set_index("Descrição")["Qtd Atual"], color="#FF6B6B")
            
    else:
        st.warning("Aguardando dados para gerar o panorama estratégico.")
