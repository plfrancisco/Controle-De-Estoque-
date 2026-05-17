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
    page_title="Inventory Pro v6.0",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------
# 4. CAMADA DE ESTILO (CSS Customizado)
# Injeta CSS para personalizar a aparência padrão do Streamlit.
# -----------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* Customização dos botões da Sidebar */
    [data-testid="stSidebar"] div.stButton > button {
        background-color: transparent !important;
        color: #FF4B4B !important;
        border: 1px solid #FF4B4B !important;
        font-weight: 600 !important;
        height: 35px !important;
        font-size: 12px !important;
        text-transform: uppercase !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #FF4B4B !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------
# 5. LÓGICA DE ROTEAMENTO E INTERFACE
# Verifica se o usuário está logado. Se não, força a exibição da tela de login.
# -----------------------------------------------------------------
if not st.session_state.autenticado:
    PageLogin.exibir_pagina()
else:
    # --- BARRA LATERAL (SIDEBAR) ---
    with st.sidebar:
        st.markdown("<h2 style='color: #FF6B6B; font-weight: 700;'>Inventory Pro</h2>", unsafe_allow_html=True)
        
        # Bloco de Navegação (Menu Principal)
        menu_options = ["Dashboard", "Inventário", "Movimentação", "Relatórios"]
        current_idx = menu_options.index(st.session_state.pagina_ativa) if st.session_state.pagina_ativa in menu_options else 0
        
        escolha = option_menu(
            menu_title=None,
            options=menu_options,
            icons=["grid-1x2", "package", "arrow-repeat", "file-bar-graph"],
            default_index=current_idx,
            styles={
                "nav-link-selected": {"background": "linear-gradient(135deg, #FF6B6B 0%, #FFB347 100%)", "font-weight": "600"}
            }
        )

        # Atualiza a página ativa com base no clique no menu
        if escolha != st.session_state.pagina_ativa:
            st.session_state.pagina_ativa = escolha

        st.divider()

        # Bloco de Alertas Críticos (Consulta o Controller em tempo real)
        dados_alerta = listar_produtos()
        if dados_alerta:
            df_a = pd.DataFrame(dados_alerta, columns=["C", "D", "Q", "M", "V", "Cat", "F", "L", "P"])
            criticos = df_a[df_a["Q"] <= df_a["M"]]
            if not criticos.empty:
                with st.expander(f"⚠️ {len(criticos)} ALERTAS CRÍTICOS", expanded=False):
                    for _, row in criticos.iterrows():
                        st.error(f"**{row['D']}**\nSaldo: {row['Q']} (Mín: {row['M']})")
        
        st.write("<div style='height: 50px;'></div>", unsafe_allow_html=True)
        
        # Botão de Encerramento de Sessão
        if st.button("ENCERRAR SESSÃO", use_container_width=True, key="btn_logout"):
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
