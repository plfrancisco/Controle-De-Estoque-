# =================================================================
# VIEW: PageLogin
# Responsabilidade: Interface de Autenticação (Corporate Edition - Fix)
# =================================================================

import streamlit as st

def exibir_pagina():
    # 1. INJEÇÃO DE CSS REFINADO (Seletores Diretos para evitar Div Clipping)
    st.markdown("""
        <style>
        /* Ocultar elementos padrão do Streamlit no Login */
        [data-testid="stHeader"], [data-testid="stFooter"] {
            display: none !important;
        }

        /* Fundo Imersivo aplicado ao AppView principal */
        .stApp {
            background: radial-gradient(circle at top right, #1E293B 0%, #0F172A 100%) !important;
        }

        /* Container do Formulário (Transformado em Card Glassmorphism) */
        [data-testid="stForm"] {
            background: rgba(30, 41, 59, 0.6) !important;
            backdrop-filter: blur(25px) !important;
            -webkit-backdrop-filter: blur(25px) !important;
            border-radius: 40px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            padding: 60px !important;
            box-shadow: 
                0 20px 40px -10px rgba(0, 0, 0, 0.5),
                0 10px 15px -5px rgba(0, 0, 0, 0.4) !important;
            max-width: 480px !important;
            margin: 80px auto !important;
            animation: card-entrance 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        @keyframes card-entrance {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Cabeçalho do Card (Injetado via Markdown dentro do form) */
        .login-title {
            color: #FFFFFF;
            font-weight: 700;
            font-size: 2.2rem;
            letter-spacing: -1.5px;
            margin-bottom: 5px;
            text-align: center;
        }
        .login-subtitle {
            color: #64748B;
            font-size: 0.95rem;
            font-weight: 500;
            margin-bottom: 40px;
            text-align: center;
        }

        /* Inputs Customizados */
        div[data-testid="stForm"] .stTextInput input {
            border-radius: 18px !important;
            background-color: rgba(15, 23, 42, 0.5) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            padding: 16px 20px !important;
            color: #F1F5F9 !important;
            transition: all 0.3s ease !important;
        }
        div[data-testid="stForm"] .stTextInput input:focus {
            border-color: #3B82F6 !important;
            background-color: rgba(15, 23, 42, 0.8) !important;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
        }

        /* Botão de Entrada (Luxury Blue) */
        div[data-testid="stForm"] .stButton button {
            border-radius: 18px !important;
            padding: 16px 24px !important;
            font-weight: 600 !important;
            background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%) !important;
            border: none !important;
            box-shadow: 0 8px 16px -4px rgba(37, 99, 235, 0.4) !important;
            margin-top: 20px !important;
            transition: all 0.3s ease !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 0.8rem;
        }
        div[data-testid="stForm"] .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 12px 24px -6px rgba(37, 99, 235, 0.6) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. ESTRUTURA DE CONTEÚDO
    # Usamos o formulário nativo como o próprio card (estilizado via CSS acima)
    with st.form("login_portal"):
        st.markdown("<div class='login-title'>Inventory.</div>", unsafe_allow_html=True)
        st.markdown("<div class='login-subtitle'>Terminal de Acesso Premium</div>", unsafe_allow_html=True)
        
        st.markdown("<p style='color: #94A3B8; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;'>Identidade</p>", unsafe_allow_html=True)
        user = st.text_input("Usuário", placeholder="ID do Auditor", label_visibility="collapsed")
        
        st.write("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        
        st.markdown("<p style='color: #94A3B8; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;'>Segurança</p>", unsafe_allow_html=True)
        pwd = st.text_input("Senha", type="password", placeholder="••••••••", label_visibility="collapsed")
        
        st.write("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        
        if st.form_submit_button("Autenticar Operação", use_container_width=True):
            if user == "admin" and pwd == "admin123":
                st.session_state.autenticado = True
                st.session_state.usuario_nome = "Administrador"
                st.rerun()
            else:
                st.error("Credenciais inválidas.")

    # Footer fora do card para manter o minimalismo
    st.markdown("""
        <div style='text-align: center; margin-top: 30px; opacity: 0.5;'>
            <p style='color: #475569; font-size: 0.7rem; font-weight: 500; letter-spacing: 1px;'>
                SECURE GATEWAY &middot; V8.3.0 CORPORATE
            </p>
        </div>
    """, unsafe_allow_html=True)
