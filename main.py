# =================================================================
# ARQUIVO PRINCIPAL: Orquestrador do Sistema (main.py)
# Responsabilidade: Gerenciar Navegação, Autenticação e Estilo Global
# =================================================================

import streamlit as st
import sys
import os
import pandas as pd

# -----------------------------------------------------------------
# 1. CONFIGURAÇÃO DE AMBIENTE E PATHS
# Garante que o Python encontre os módulos nas subpastas (Controllers, Models, etc)
# -----------------------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
os.chdir(current_dir)

from streamlit_option_menu import option_menu
from Controllers.ProdutoController import listar_produtos
import Views.PageDashboard as PageDashboard
import Views.PageInventario as PageInventario
import Views.PageMovimentacao as PageMovimentacao
import Views.PageRelatorios as PageRelatorios
import Views.PageLogin as PageLogin
import Views.PagePerfil as PagePerfil

# -----------------------------------------------------------------
# 2. GERENCIAMENTO DE ESTADO (Session State)
# O Streamlit é 'stateless' por padrão. Usamos st.session_state para
# manter dados entre interações (como se o usuário está logado).
# -----------------------------------------------------------------
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'pagina_ativa' not in st.session_state:
    st.session_state.pagina_ativa = "Dashboard"

# -----------------------------------------------------------------
# 3. CONFIGURAÇÃO DA PÁGINA (Layout e Título)
# -----------------------------------------------------------------
st.set_page_config(
    page_title="Inventory Control System v8.1",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------
# 4. CAMADA DE ESTILO (CSS Customizado - Shadow Palette)
# -----------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Configurações Globais */
    html, body, [class*="css"] { 
        font-family: 'Inter', sans-serif; 
        color: #E0E6ED;
    }

    /* Fundo Imersivo Global (Executivo) */
    .stApp {
        background: radial-gradient(circle at top right, #1E293B 0%, #0F172A 100%) !important;
    }
    
    /* Customização da Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(14, 17, 23, 0.95) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Botão de Logout no Rodapé */
    div.stButton > button[key="btn_logout"] {
        position: fixed;
        bottom: 20px;
        left: 20px;
        width: 260px !important;
        background-color: transparent !important;
        color: #94A3B8 !important;
        border: 1px solid #2D3748 !important;
        font-weight: 500 !important;
        z-index: 1000;
    }
    div.stButton > button[key="btn_logout"]:hover {
        border-color: #EF4444 !important;
        color: #EF4444 !important;
    }
    
    /* Cards de Alerta Customizados (Organic Edition) */
    .alert-card {
        background: rgba(26, 28, 36, 0.6);
        backdrop-filter: blur(8px);
        border-left: 4px solid #EF4444;
        padding: 16px;
        margin-bottom: 15px;
        border-radius: 18px; /* Mais arredondado */
        box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.3);
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }
    .alert-title {
        color: #F1F5F9;
        font-size: 0.88rem;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .alert-desc {
        color: #94A3B8;
        font-size: 0.78rem;
    }

    /* Inputs e Botões Globais (Organic Flow Edition) */
    .stTextInput input, .stNumberInput input, .stSelectbox [data-baseweb="select"] {
        border-radius: 20px !important;
        background-color: rgba(15, 23, 42, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        padding: 12px 20px !important;
        transition: all 0.4s ease !important;
    }
    .stTextInput input:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 1px #3B82F6 !important;
    }

    div.stButton > button {
        border-radius: 20px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: none !important;
    }
    
    /* Botão Primário com Gradiente Suave */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%) !important;
        box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.4) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 15px 30px -8px rgba(37, 99, 235, 0.6) !important;
    }

    /* Espaçadores Customizados */
    .sidebar-spacer {
        margin-top: 25px;
        margin-bottom: 10px;
    }

    /* Executive Data Grid (Corporate Edition) */
    /* Remove bordas globais de tabelas nativas do Streamlit e aplica Glass Hover */
    [data-testid="stTable"], [data-testid="stDataFrame"] {
        border: none !important;
        background: transparent !important;
    }
    
    /* Estilização via Injeção de Classes para Tabelas Customizadas */
    .executive-grid {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        background: rgba(30, 41, 59, 0.2);
        border-radius: 24px;
        overflow: hidden;
    }
    .executive-grid th {
        background: rgba(15, 23, 42, 0.8) !important;
        color: #64748B !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        font-weight: 600 !important;
        padding: 20px 25px !important;
        text-align: left !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    .executive-grid td {
        padding: 18px 25px !important;
        color: #E2E8F0 !important;
        font-size: 0.9rem !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.03) !important;
        transition: all 0.3s ease !important;
    }
    .executive-grid tr:hover td {
        background: rgba(59, 130, 246, 0.08) !important;
        color: #FFFFFF !important;
    }
    .executive-grid .mono-data {
        font-family: 'JetBrains Mono', 'Courier New', monospace !important;
        font-size: 0.85rem !important;
        color: #3B82F6 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------
# 5. LÓGICA DE ROTEAMENTO E INTERFACE
# -----------------------------------------------------------------
if not st.session_state.autenticado:
    PageLogin.exibir_pagina()
else:
    # --- BARRA LATERAL (SIDEBAR) ---
    with st.sidebar:
        st.markdown("<h2 style='color: #FFFFFF; font-weight: 700; font-size: 2.2rem; letter-spacing: -1.5px; margin-bottom: 0px;'>Inventory.</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #3B82F6; font-size: 0.75rem; font-weight: 600; letter-spacing: 1.2px; opacity: 0.8;'>EXECUTIVE CONSOLE</p>", unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

        # Mapeamento de Termos Executivos
        menu_options = ["Dashboard", "Gestão de Ativos", "Fluxo de Operações", "Relatórios"]
        icons = ["bar-chart-line", "package", "arrow-left-right", "file-text"]
        
        page_map = {
            "Dashboard": "Dashboard",
            "Gestão de Ativos": "Inventário",
            "Fluxo de Operações": "Movimentação",
            "Relatórios": "Relatórios"
        }
        
        # Inverte o mapa para encontrar o índice correto
        inv_map = {v: k for k, v in page_map.items()}
        current_idx = menu_options.index(inv_map[st.session_state.pagina_ativa]) if st.session_state.pagina_ativa in inv_map else 0
        
        escolha_exibicao = option_menu(
            menu_title=None,
            options=menu_options,
            icons=icons,
            default_index=current_idx,
            styles={
                "container": {"padding": "0px", "background-color": "transparent"},
                "nav-link": {
                    "font-size": "0.9rem", 
                    "text-align": "left", 
                    "margin": "6px 0px", 
                    "color": "#94A3B8", 
                    "font-family": "Inter",
                    "padding": "10px 15px"
                },
                "nav-link-selected": {"background-color": "#3B82F6", "color": "#FFFFFF", "font-weight": "500"}
            }
        )

        # Atualiza a página ativa
        st.session_state.pagina_ativa = page_map[escolha_exibicao]

        st.markdown("<div class='sidebar-spacer'></div>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748B; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px;'>Monitoramento Ativo</p>", unsafe_allow_html=True)

        # Bloco de Alertas de Performance (Cards Customizados)
        dados_alerta = listar_produtos()
        if dados_alerta:
            df_a = pd.DataFrame(dados_alerta, columns=["C", "D", "Q", "M", "V", "Cat", "F", "L", "P"])
            criticos = df_a[df_a["Q"] <= df_a["M"]]
            if not criticos.empty:
                for _, row in criticos.head(5).iterrows(): # Mostra os 5 principais
                    st.markdown(f"""
                        <div class="alert-card">
                            <div class="alert-title">{row['D']}</div>
                            <div class="alert-desc">Saldo: {row['Q']} | Mínimo: {row['M']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                if len(criticos) > 5:
                    st.info(f"Mais {len(criticos)-5} alertas ocultos.")
        
        # Botão de Logout (Posicionado via CSS no rodapé)
        if st.button("SAIR DO SISTEMA", key="btn_logout"):
            st.session_state.autenticado = False
            st.rerun()

    # -----------------------------------------------------------------
    # 6. RENDERIZAÇÃO DA PÁGINA SELECIONADA
    # Switch-case para decidir qual VIEW (Página) renderizar na área principal.
    # -----------------------------------------------------------------
    if st.session_state.pagina_ativa == "Perfil":
        PagePerfil.exibir_pagina()
    elif st.session_state.pagina_ativa == "Dashboard":
        PageDashboard.exibir_pagina()
    elif st.session_state.pagina_ativa == "Inventário":
        PageInventario.exibir_pagina()
    elif st.session_state.pagina_ativa == "Movimentação":
        PageMovimentacao.exibir_pagina()
    elif st.session_state.pagina_ativa == "Relatórios":
        PageRelatorios.exibir_pagina()
