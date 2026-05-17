# =================================================================
# VIEW: PageInventario
# Responsabilidade: Gestão de Catálogo, Cadastro de Produtos e Fornecedores
# =================================================================

import streamlit as st
import pandas as pd
from Controllers.ProdutoController import listar_produtos, cadastrar_produto, excluir_produto, listar_categorias
from Controllers.FornecedorController import listar_fornecedores, cadastrar_fornecedor
from Models.Produto import Produto
from streamlit_lottie import st_lottie
import requests

def load_lottieurl(url):
    """Auxiliar: Carrega animações via URL."""
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

def exibir_pagina():
    # 1. Título e Subtítulo Estilizados
    st.markdown("<h1 style='color: #FF6B6B; font-weight: 800; margin-bottom: 0px;'>Hub de Inventário</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #A1A1AA; font-size: 1.1rem;'>Controle total do seu patrimônio físico.</p>", unsafe_allow_html=True)
    
    lottie_success = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_7W9OfS.json")
    
    # 2. Divisão por Abas (Sub-navegação)
    tab_listagem, tab_cadastro, tab_fornecedor = st.tabs(["📋 Consulta", "➕ Adicionar Produto", "🤝 Novo Fornecedor"])
    
    # --- ABA 1: CONSULTA E EXCLUSÃO ---
    with tab_listagem:
        dados = listar_produtos()
        if dados:
            df = pd.DataFrame(dados, columns=[
                "Código", "Descrição", "Qtd", "Min", 
                "Venda", "Categoria", "Fornecedor", "Local", "Custo"
            ])
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            with st.container():
                st.markdown("### Ações de Gestão")
                col_sel, col_del = st.columns([3, 1])
                with col_sel:
                    produto_para_gerenciar = st.selectbox(
                        "Identifique o item na base:",
                        options=df["Código"].tolist(),
                        format_func=lambda x: f"{x} - {df[df['Código']==x]['Descrição'].values[0]}"
                    )
                with col_del:
                    st.write("") 
                    # Uso de Popover para confirmação de segurança antes da exclusão
                    with st.popover("🗑️ Excluir Item", use_container_width=True):
                        st.warning("Confirmar exclusão definitiva?")
                        if st.button("Confirmar", type="primary", use_container_width=True, key="del_prod_btn"):
                            if excluir_produto(produto_para_gerenciar):
                                st.toast("Item removido com sucesso.", icon="🗑️")
                                st.rerun()
        else:
            st.info("Inventário vazio.")

    # --- ABA 2: CADASTRO DE PRODUTO ---
    with tab_cadastro:
        st.markdown("<div class='styled-card'>", unsafe_allow_html=True)
        st.markdown("### 📦 Cadastro de Produto")
        placeholder_lottie = st.empty()
        
        with st.form("form_warm_prod", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                codigo = st.number_input("Código SKU", min_value=1, step=1)
                descricao = st.text_input("Descrição", placeholder="Ex: Monitor Dell 24 pol")
                
                # Dropdown dinâmico com dados do banco
                cats = listar_categorias()
                id_cat = st.selectbox("Categoria", options=[c[0] for c in cats], 
                                     format_func=lambda x: next(c[1] for c in cats if c[0] == x))
                
                # Multiselect para o relacionamento N:N com fornecedores
                forns = listar_fornecedores()
                ids_forns = st.multiselect("Vincular Fornecedores", 
                                         options=[f[0] for f in forns],
                                         format_func=lambda x: next(f[1] for f in forns if f[0] == x))
            with c2:
                qtd_i = st.number_input("Estoque de Abertura", min_value=0)
                qtd_m = st.number_input("Nível de Alerta (Mínimo)", min_value=1, value=5)
                v_venda = st.number_input("Preço Venda (R$)", format="%.2f", step=0.50)
                v_custo = st.number_input("Custo Unitário (R$)", format="%.2f", step=0.50)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.form_submit_button("💾 Salvar e Alocar no Estoque", type="primary", use_container_width=True):
                if not (descricao and ids_forns):
                    st.error("Campos obrigatórios: Descrição e Fornecedores.")
                else:
                    p = Produto(codigo, descricao, qtd_i, qtd_m, v_venda, id_cat, "Alocação Automática", v_custo, ids_forns)
                    if cadastrar_produto(p):
                        with placeholder_lottie:
                            if lottie_success: st_lottie(lottie_success, height=200, key="lottie_cad")
                        st.toast("Produto registrado!", icon="✅")
                    else:
                        st.error("Erro técnico ao salvar. Verifique o SKU.")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- ABA 3: CADASTRO DE FORNECEDOR ---
    with tab_fornecedor:
        st.markdown("<div class='styled-card'>", unsafe_allow_html=True)
        st.markdown("### 🤝 Novo Parceiro Comercial")
        with st.form("form_warm_forn", clear_on_submit=True):
            f1, f2 = st.columns(2)
            with f1:
                nf = st.text_input("Razão Social / Nome")
                cnf = st.text_input("CNPJ")
            with f2:
                ef = st.text_input("E-mail para Pedidos")
                tf = st.text_input("Telefone / WhatsApp")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.form_submit_button("✅ Cadastrar Fornecedor", type="primary", use_container_width=True):
                if nf and cnf:
                    if cadastrar_fornecedor(nf, cnf, ef, tf):
                        st.toast("Parceiro integrado com sucesso.", icon="🤝")
                    else:
                        st.error("Erro ao salvar. Verifique o CNPJ.")
        st.markdown("</div>", unsafe_allow_html=True)
