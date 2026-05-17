# =================================================================
# VIEW: PageLogin
# Responsabilidade: Interface de Autenticação e Controle de Acesso
# =================================================================

import streamlit as st

def exibir_pagina():
    # -------------------------------------------------------------
    # 1. LAYOUT CENTRALIZADO
    # -------------------------------------------------------------
    st.markdown("<div style='text-align: center; padding-top: 100px;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color: #FF6B6B; font-weight: 800;'>Inventory Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #A1A1AA;'>Acesse sua conta para gerenciar o inventário.</p>", unsafe_allow_html=True)
    
    with st.container():
        # Cria colunas para centralizar o formulário no meio da tela
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<div class='styled-card'>", unsafe_allow_html=True)
            with st.form("login_form"):
                user = st.text_input("Usuário", placeholder="admin")
                pwd = st.text_input("Senha", type="password", placeholder="••••••")
                
                # -------------------------------------------------------------
                # 2. LÓGICA DE VALIDAÇÃO
                # -------------------------------------------------------------
                if st.form_submit_button("Entrar no Sistema", type="primary", use_container_width=True):
                    # Login de Laboratório: admin / admin123
                    if user == "admin" and pwd == "admin123":
                        # Ativa o estado de autenticado no Session State global
                        st.session_state.autenticado = True
                        st.session_state.usuario_nome = "Administrador"
                        st.rerun() # Recarrega para o main.py rotear para o Dashboard
                    else:
                        st.error("Credenciais inválidas.")
            st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
