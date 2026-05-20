# =================================================================
# VIEW: PageDashboard
# Responsabilidade: Executive Intelligence Panel (Sofia Edition)
# =================================================================

import streamlit as st
from Controllers.ProdutoController import listar_produtos
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def exibir_pagina():
    # -------------------------------------------------------------
    # 1. CSS LOCAL: THE GLASS METRICS & LAYOUT
    # -------------------------------------------------------------
    st.markdown("""
        <style>
        /* Fade-in Animation */
        @keyframes page-fade {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .main-container {
            animation: page-fade 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        /* Glass Cards para KPIs (Organic Flow Edition) */
        div[data-testid="metric-container"] {
            background: rgba(30, 41, 59, 0.45) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            padding: 28px !important;
            border-radius: 35px !important; /* Aumento drástico para suavidade */
            box-shadow: 
                0 20px 25px -5px rgba(0, 0, 0, 0.2),
                0 8px 10px -6px rgba(0, 0, 0, 0.2) !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        div[data-testid="metric-container"]:hover {
            transform: translateY(-4px) !important;
            background: rgba(30, 41, 59, 0.6) !important;
            border-color: rgba(59, 130, 246, 0.3) !important;
        }

        /* Tipografia de Luxo para Métricas */
        [data-testid="stMetricLabel"] { 
            color: #94A3B8 !important; 
            font-size: 0.8rem !important; 
            font-weight: 600 !important;
            letter-spacing: 1px !important;
            text-transform: uppercase !important;
        }
        [data-testid="stMetricValue"] { 
            color: #FFFFFF !important; 
            font-family: 'Inter', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -1px !important;
        }

        /* Seções e Cabeçalhos */
        .section-header {
            color: #F8FAFC;
            font-size: 1.5rem;
            font-weight: 700;
            margin-top: 40px;
            margin-bottom: 20px;
            letter-spacing: -0.5px;
        }
        </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # 2. CABEÇALHO EXECUTIVO
    # -------------------------------------------------------------
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    col_h1, col_h2 = st.columns([2, 1])
    with col_h1:
        st.markdown("<h1 style='color: #FFFFFF; font-weight: 700; font-size: 2.5rem; letter-spacing: -1.5px; margin-bottom: 0px;'>Performance.</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748B; font-size: 1.1rem; font-weight: 500;'>Inteligência de Ativos e Fluxo Operacional</p>", unsafe_allow_html=True)
    
    with col_h2:
        st.markdown("<div style='text-align: right; margin-top: 20px;'>", unsafe_allow_html=True)
        st.button("↻ Sincronizar Dados", type="secondary", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
    
    # -------------------------------------------------------------
    # 3. DATA ENGINE
    # -------------------------------------------------------------
    dados = listar_produtos()
    
    if dados:
        df = pd.DataFrame(dados, columns=[
            "C", "D", "Q", "M", "V", "Cat", "F", "L", "P"
        ])
        
        # Tipagem técnica
        df["Q"] = pd.to_numeric(df["Q"]).fillna(0)
        df["P"] = pd.to_numeric(df["P"]).fillna(0)
        df["V"] = pd.to_numeric(df["V"]).fillna(0)
        
        # Cálculos BI
        total_skus = len(df)
        patrimonio = (df["Q"] * df["P"]).sum()
        yield_potencial = (df["Q"] * (df["V"] - df["P"])).sum()
        rupturas = len(df[df["Q"] <= df["M"]])
        
        # -------------------------------------------------------------
        # 4. GLASS METRICS (KPIs)
        # -------------------------------------------------------------
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("SKUs em Operação", f"{total_skus:02d}")
        c2.metric("Patrimônio Ativo", f"R$ {patrimonio:,.2f}")
        c3.metric("Yield Estimado", f"R$ {yield_potencial:,.2f}")
        c4.metric("Rupturas Críticas", rupturas)

        # -------------------------------------------------------------
        # 5. ESTRATÉGIA DE VALOR (ABC Luxury Chart)
        # -------------------------------------------------------------
        st.markdown("<div class='section-header'>Análise de Relevância (Curva ABC)</div>", unsafe_allow_html=True)
        
        df["Valor_T"] = df["Q"] * df["P"]
        df = df.sort_values(by="Valor_T", ascending=False)
        df["Soma_A"] = df["Valor_T"].cumsum()
        total_g = df["Valor_T"].sum()
        df["Perc_A"] = (df["Soma_A"] / total_g) * 100 if total_g > 0 else 0
        
        def classificar(row):
            if row["Perc_A"] <= 80: return "Classe A (Prioritário)"
            elif row["Perc_A"] <= 95: return "Classe B (Estratégico)"
            else: return "Classe C (Operacional)"
            
        df["Classe"] = df.apply(classificar, axis=1)
        
        # Plotly Luxury Customization
        fig_abc = px.bar(df, x="D", y="Valor_T", color="Classe",
                        color_discrete_map={
                            "Classe A (Prioritário)": "#3B82F6", 
                            "Classe B (Estratégico)": "#60A5FA", 
                            "Classe C (Operacional)": "#1E293B"
                        },
                        hover_data={"D": True, "Valor_T": ":.2f", "Classe": True})
        
        fig_abc.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", color="#94A3B8"),
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=False, title=None),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title="Valor (R$)"),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_abc, use_container_width=True)

        # -------------------------------------------------------------
        # 6. VOLUME E CAPACIDADE (Luxury Horizontal Bar)
        # -------------------------------------------------------------
        st.markdown("<div class='section-header'>Fluxo de Volume por SKU</div>", unsafe_allow_html=True)
        
        fig_vol = go.Figure(go.Bar(
            x=df["Q"],
            y=df["D"],
            orientation='h',
            marker=dict(
                color='#3B82F6',
                line=dict(color='rgba(59, 130, 246, 0.5)', width=1)
            )
        ))
        
        fig_vol.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", color="#94A3B8"),
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title="Unidades"),
            yaxis=dict(showgrid=False, title=None, autorange="reversed"),
            height=400
        )
        st.plotly_chart(fig_vol, use_container_width=True)
            
    else:
        st.info("Aguardando sincronização de dados para gerar o panorama estratégico.")
    
    st.markdown("</div>", unsafe_allow_html=True) # main-container
