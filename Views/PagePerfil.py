# =================================================================
# VIEW: PagePerfil
# Responsabilidade: Gestão de Credenciais e Configurações Pessoais
# =================================================================

import streamlit as st

def exibir_pagina():
    st.markdown("<h1 style='color: #FF6B6B;'>Minha Conta</h1>", unsafe_allow_html=True)
    st.markdown("Gerencie suas credenciais e preferências de acesso.")
    
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
    st.markdown("<div class='styled-card' style='border-left: 5px solid #FFB347;'>", unsafe_allow_html=True)
    st.subheader("Encerrar Sessão")
    st.write("Deseja sair do sistema com segurança?")
    if st.button("🚪 Sair do Inventory Pro", type="secondary", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
