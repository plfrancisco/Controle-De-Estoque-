# =================================================================
# VIEW: PagePerfil
# Responsabilidade: Gestão de Credenciais e Configurações Pessoais
# =================================================================

import streamlit as st

def exibir_pagina():
    st.markdown("<h1 style='color: #FFFFFF; font-weight: 700; font-size: 2.5rem; letter-spacing: -1.5px; margin-bottom: 0px;'>Perfil.</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748B; font-size: 1.1rem; font-weight: 500;'>Configurações de Auditoria e Segurança</p>", unsafe_allow_html=True)
    
    # -------------------------------------------------------------
    # 1. FORMULÁRIO DE SEGURANÇA
    # -------------------------------------------------------------
    st.markdown("<div class='styled-card'>", unsafe_allow_html=True)
    st.subheader("Alterar Senha de Acesso")
    
    with st.form("form_change_password"):
        col1, col2 = st.columns(2)
        with col1:
            nova_senha = st.text_input("Nova Senha", type="password")
        with col2:
            confirmar_senha = st.text_input("Confirmar Nova Senha", type="password")
            
        if st.form_submit_button("Atualizar Credenciais", type="primary"):
            if nova_senha and nova_senha == confirmar_senha:
                # Simulação de atualização (Backend deve ser chamado aqui)
                st.success("Senha atualizada com sucesso!")
                st.toast("Credenciais sincronizadas.", icon="🔐")
            else:
                st.error("As senhas não coincidem ou estão vazias.")
    st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # 2. SEÇÃO DE DESCONEXÃO (LOGOUT)
    # -------------------------------------------------------------
    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #F8FAFC; margin-bottom: 20px;'>Encerrar Sessão</h3>", unsafe_allow_html=True)
    st.write("Deseja sair do sistema com segurança?")
    if st.button("Sair do Inventory.", type="secondary", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()
