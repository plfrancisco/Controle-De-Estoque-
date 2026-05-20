# =================================================================
# VIEW: PageInventario
# Responsabilidade: Gestão de Catálogo (Executive Data Grid Edition)
# =================================================================

import streamlit as st
import pandas as pd
import time
from Controllers.ProdutoController import (
    listar_produtos, cadastrar_produto, excluir_produto, listar_categorias, 
    buscar_produto_por_codigo, atualizar_produto, atualizar_localizacao_produto
)
from Controllers.FornecedorController import (
    listar_fornecedores, cadastrar_fornecedor, buscar_fornecedor_por_id, atualizar_fornecedor, excluir_fornecedor
)
from Controllers.EstruturaController import listar_prateleiras, cadastrar_prateleira, excluir_prateleira
from Models.Produto import Produto

def exibir_pagina():
    # 1. Título e Subtítulo Executivos (Estilo Corporate Edition)
    st.markdown("<h1 style='color: #FFFFFF; font-weight: 700; font-size: 2.5rem; letter-spacing: -1.5px; margin-bottom: 0px;'>Ativos.</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748B; font-size: 1.1rem; font-weight: 500;'>Controle de Inventário e Infraestrutura de Precisão</p>", unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
    
    # 2. Divisão por Abas
    tab_listagem, tab_cadastro, tab_fornecedor, tab_edicao = st.tabs([
        "✧ Consulta de Ativos", "⊕ Adicionar Item", "⊞ Novo Parceiro", "🛠 Auditoria de Registros"
    ])
    
    # --- ABA 1: CONSULTA (EXECUTIVE DATA GRID) ---
    with tab_listagem:
        dados = listar_produtos()
        if dados:
            rows = "".join([f"<tr><td class='mono-data'>{p[0]}</td><td style='font-weight: 500;'>{p[1]}</td><td class='mono-data'>{p[2]}</td><td class='mono-data'>{p[3]}</td><td class='mono-data'>R$ {p[4]:,.2f}</td><td style='color: #94A3B8; font-size: 0.8rem;'>{p[7]}</td></tr>" for p in dados])
            full_html = f"<table class='executive-grid'><thead><tr><th>ID</th><th>Descrição do Ativo</th><th>Saldo</th><th>Mínimo</th><th>Valor (R$)</th><th>Localização</th></tr></thead><tbody>{rows}</tbody></table>"
            st.markdown(full_html, unsafe_allow_html=True)
        else:
            st.info("Base de dados de inventário vazia.")

    # --- ABA 2: CADASTRO DE PRODUTO ---
    with tab_cadastro:
        st.markdown("<h3 style='color: #F8FAFC; margin-bottom: 25px;'>Ingressar Novo Ativo</h3>", unsafe_allow_html=True)
        with st.form("form_organic_prod", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                codigo = st.number_input("Código SKU", min_value=1, step=1)
                descricao = st.text_input("Descrição Técnica")
                cats = listar_categorias()
                id_cat = st.selectbox("Categoria", options=[c[0] for c in cats], format_func=lambda x: next(c[1] for c in cats if c[0] == x))
                forns = listar_fornecedores()
                ids_forns = st.multiselect("Fornecedores", options=[f[0] for f in forns], format_func=lambda x: next(f[1] for f in forns if f[0] == x))
            with c2:
                qtd_i = st.number_input("Estoque Inicial", min_value=0)
                qtd_m = st.number_input("Estoque Mínimo", min_value=1, value=5)
                v_venda = st.number_input("Preço Venda", format="%.2f")
                v_custo = st.number_input("Preço Custo", format="%.2f")
            if st.form_submit_button("Sincronizar Novo Ativo", type="primary", use_container_width=True):
                if descricao and ids_forns:
                    p = Produto(codigo, descricao, qtd_i, qtd_m, v_venda, id_cat, "Alocação Automática", v_custo, ids_forns)
                    if cadastrar_produto(p):
                        st.success("✅ Protocolo Concluído: Ativo devidamente integrado ao ecossistema.")
                        time.sleep(2.5)
                        st.rerun()
                else: st.error("Preencha os campos obrigatórios.")

    # --- ABA 3: CADASTRO DE FORNECEDOR ---
    with tab_fornecedor:
        st.markdown("<h3 style='color: #F8FAFC; margin-bottom: 25px;'>Registrar Parceiro</h3>", unsafe_allow_html=True)
        with st.form("form_organic_forn", clear_on_submit=True):
            f1, f2 = st.columns(2)
            with f1:
                nf = st.text_input("Razão Social"); cnf = st.text_input("CNPJ")
            with f2:
                ef = st.text_input("E-mail"); tf = st.text_input("Telefone")
            if st.form_submit_button("Ativar Parceiro", type="primary", use_container_width=True):
                if nf and cnf:
                    if cadastrar_fornecedor(nf, cnf, ef, tf):
                        st.success("✅ Parceiro comercial ativado e sincronizado com sucesso.")
                        time.sleep(2.5)
                        st.rerun()

    # --- ABA 4: AUDITORIA E AJUSTES ---
    with tab_edicao:
        st.markdown("<h3 style='color: #F8FAFC; margin-bottom: 25px;'>Auditoria de Registros</h3>", unsafe_allow_html=True)
        modo_edicao = st.radio("Selecione o módulo:", ["Ativo", "Fornecedor", "Estrutura"], horizontal=True)
        if modo_edicao == "Ativo":
            produtos = listar_produtos()
            if produtos:
                prod_sel = st.selectbox("Selecionar SKU:", options=[p[0] for p in produtos], format_func=lambda x: next(f"ID {p[0]}: {p[1]}" for p in produtos if p[0] == x))
                dados_atuais = buscar_produto_por_codigo(prod_sel)
                with st.form("form_audit_prod"):
                    c1, c2 = st.columns(2)
                    with c1:
                        nova_desc = st.text_input("Descrição", value=dados_atuais[1]); nova_local = st.text_input("Localização", value=dados_atuais[7])
                    with c2:
                        novo_min = st.number_input("Mínimo", value=dados_atuais[3]); novo_venda = st.number_input("Venda", value=dados_atuais[4])
                    if st.form_submit_button("Confirmar Ajustes", type="primary", use_container_width=True):
                        if atualizar_produto(prod_sel, nova_desc, novo_min, novo_venda, dados_atuais[5], 0.0):
                            st.success("✅ Ajustes de auditoria aplicados com sucesso.")
                            time.sleep(2.5)
                            st.rerun()
                if st.button("Excluir Ativo", type="primary", use_container_width=True):
                    if excluir_produto(prod_sel, "Auditoria"):
                        st.success("🗑 Registro removido do ecossistema.")
                        time.sleep(2.5)
                        st.rerun()
        elif modo_edicao == "Fornecedor":
            forns = listar_fornecedores()
            if forns:
                forn_sel = st.selectbox("Fornecedor:", options=[f[0] for f in forns], format_func=lambda x: next(f[1] for f in forns if f[0] == x))
                if st.button("Remover Fornecedor", type="primary"):
                    s, m = excluir_fornecedor(forn_sel)
                    if s: 
                        st.success("✅ Fornecedor removido com sucesso.")
                        time.sleep(2.5)
                        st.rerun()
                    else: st.error(m)
        else:
            st.markdown("#### Infraestrutura Física")
            prats = listar_prateleiras()
            if prats:
                rows_est = "".join([f"<tr><td style='font-weight: 600; color: #3B82F6;'>{p[0]}</td><td class='mono-data'>{p[1]}</td><td class='mono-data'>{p[2]}</td></tr>" for p in prats])
                html_est = f"<table class='executive-grid'><thead><tr><th>Local</th><th>Capacidade</th><th>Ocupação</th></tr></thead><tbody>{rows_est}</tbody></table>"
                st.markdown(html_est, unsafe_allow_html=True)
            with st.form("new_prat"):
                n = st.text_input("ID Prateleira"); q = st.number_input("Caixas", value=15)
                if st.form_submit_button("Criar"):
                    s, m = cadastrar_prateleira(n, q)
                    if s: 
                        st.success("✅ Nova estrutura criada e validada.")
                        time.sleep(2.5)
                        st.rerun()
