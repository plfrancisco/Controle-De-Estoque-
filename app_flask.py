from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
import os
import sys
import csv
from io import StringIO
from datetime import datetime, timedelta

# Adiciona o diretório raiz ao path para importações dos Controllers
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Controllers.UsuarioController import autenticar_usuario
from Controllers.ProdutoController import (
    listar_produtos, listar_categorias, cadastrar_produto, gerar_qrcode_produto, buscar_produto_por_codigo
)
from Controllers.MovimentacaoController import registrar_movimentacao, listar_movimentacoes
from Models.Produto import Produto
from Services.database import conectaBD
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "chave_secreta_para_estoque_master"

@app.route('/', methods=['GET', 'POST'])
# ... (rest of the login route)
def login():
    # ... (mesmo código anterior)
    if 'usuario_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        usuario_input = request.form.get('usuario')
        senha_input = request.form.get('senha')
        
        user = autenticar_usuario(usuario_input, senha_input)
        if user:
            session['usuario_id'] = user.get_login()
            session['usuario_nome'] = user.get_login().upper()
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciais inválidas. Tente novamente.', 'error')
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
        
    # Filtros de Data
    data_inicio = request.args.get('data_inicio', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    data_fim = request.args.get('data_fim', datetime.now().strftime('%Y-%m-%d'))

    prods = listar_produtos()
    produtos_df = []
    total_itens = 0
    valor_total = 0
    itens_risco = 0
    
    if prods:
        for p in prods:
            qtd = p[2] if p[2] is not None else 0
            min_qtd = p[3] if p[3] is not None else 0
            custo = p[8] if p[8] is not None else 0.0
            venda = p[4] if p[4] is not None else 0.0
            
            prod_dict = {
                'sku': p[0], 'nome': p[1], 'qtd': qtd, 'min': min_qtd,
                'venda': venda, 'cat': p[5], 'custo': custo, 'lucro_un': venda - custo
            }
            produtos_df.append(prod_dict)
            total_itens += qtd
            valor_total += (qtd * custo)
            if qtd <= min_qtd: itens_risco += 1

    # Busca de Movimentações de Saída para o Gráfico de Pizza (Categorias)
    conexao = conectaBD()
    cursor = conexao.cursor()

    # Cálculo de Ocupação de Prateleiras
    cursor.execute("SELECT COUNT(*) FROM estrutura_armazenamento WHERE ocupacao > 0")
    caixas_ocupadas = cursor.fetchone()[0]
    total_caixas = 450 # 30 prateleiras * 15 caixas
    ocupacao_armazem = (caixas_ocupadas / total_caixas) * 100

    query_saidas = """
        SELECT c.nome, SUM(m.quantidade) 
        FROM movimentacao m
        JOIN produto p ON m.codigo_produto = p.codigo
        JOIN categoria c ON p.id_categoria = c.id
        WHERE m.tipo = 'SAIDA' AND date(m.data_hora) BETWEEN ? AND ?
        GROUP BY c.nome
    """
    cursor.execute(query_saidas, (data_inicio, data_fim))
    dados_grafico = cursor.fetchall()

    # 5. Valor por Localização (Agora baseado na tabela oficial de armazenamento)
    query_loc = """
        SELECT prateleira, SUM(ocupacao)
        FROM estrutura_armazenamento
        WHERE ocupacao > 0
        GROUP BY prateleira
    """
    cursor.execute(query_loc)
    dados_loc = cursor.fetchall()

    # Localização detalhada para a tabela (Primeira caixa onde o produto está)
    cursor.execute("SELECT produto_codigo, prateleira, caixa FROM estrutura_armazenamento WHERE ocupacao > 0")
    mapa_loc = {row[0]: f"{row[1]}-C{row[2]}" for row in cursor.fetchall()}

    # 4. Dias de Suprimento e Sugestão de Compra
    query_consumo_detalhado = """
        SELECT codigo_produto, SUM(quantidade) / 30.0 as media_diaria
        FROM movimentacao 
        WHERE tipo = 'SAIDA' AND data_hora >= date('now', '-30 days')
        GROUP BY codigo_produto
    """
    cursor.execute(query_consumo_detalhado)
    consumo_map = {row[0]: row[1] for row in cursor.fetchall()}
    
    query_consumo_total = "SELECT SUM(quantidade) / 30.0 FROM movimentacao WHERE tipo = 'SAIDA' AND data_hora >= date('now', '-30 days')"
    cursor.execute(query_consumo_total)
    consumo_diario_total = cursor.fetchone()[0] or 0
    dias_suprimento = total_itens / consumo_diario_total if consumo_diario_total > 0 else 999 

    conexao.close()

    # Atualiza a localização e adiciona sugestão de compra no dicionário de produtos
    for p in produtos_df:
        p['loc'] = mapa_loc.get(p['sku'], "Sem posição")
        media = consumo_map.get(p['sku'], 0)
        # Sugestão: Manter estoque para 15 dias caso esteja abaixo do mínimo
        if p['qtd'] <= p['min']:
            # Se não houve consumo, sugere repor até o dobro do mínimo por segurança
            p['sugestao'] = int(max((media * 15) - p['qtd'], p['min'] * 2 - p['qtd']))
        else:
            p['sugestao'] = 0

    # 3. Preparação para Curva ABC (Pareto) - Baseado em Saídas Reais no Período
    conexao = conectaBD()
    cursor = conexao.cursor()
    query_abc = """
        SELECT p.descricao, SUM(m.quantidade * (p.valor_unitario - p.preco_custo)) as lucro_total
        FROM movimentacao m
        JOIN produto p ON m.codigo_produto = p.codigo
        WHERE m.tipo = 'SAIDA' AND date(m.data_hora) BETWEEN ? AND ?
        GROUP BY p.codigo
        ORDER BY lucro_total DESC
        LIMIT 5
    """
    cursor.execute(query_abc, (data_inicio, data_fim))
    dados_abc = cursor.fetchall()
    conexao.close()

    labels_abc = [row[0] for row in dados_abc]
    valores_abc = [row[1] for row in dados_abc]

    # Se não houver saídas no período, mostrar fallback (Top 5 por estoque atual)
    if not labels_abc:
        produtos_ordenados_lucro = sorted(produtos_df, key=lambda x: x['qtd'] * x['lucro_un'], reverse=True)
        labels_abc = [x['nome'] for x in produtos_ordenados_lucro[:5]] 
        valores_abc = [x['qtd'] * x['lucro_un'] for x in produtos_ordenados_lucro[:5]]


    labels_pizza = [row[0] for row in dados_grafico]
    valores_pizza = [row[1] for row in dados_grafico]
    labels_loc = [row[0] for row in dados_loc]
    valores_loc = [row[1] for row in dados_loc]

    lucro_potencial = sum(p['qtd'] * (p['venda'] - p['custo']) for p in produtos_df)
    total_skus = len(produtos_df) if produtos_df else 1
    saude_estoque = ((total_skus - itens_risco) / total_skus) * 100

    return render_template('dashboard.html', 
                           produtos=produtos_df, 
                           total_itens=total_itens, 
                           valor_total=valor_total, 
                           lucro_potencial=lucro_potencial,
                           saude_estoque=saude_estoque,
                           itens_risco=itens_risco,
                           labels_pizza=labels_pizza,
                           valores_pizza=valores_pizza,
                           labels_abc=labels_abc,
                           valores_abc=valores_abc,
                           labels_loc=labels_loc,
                           valores_loc=valores_loc,
                           dias_suprimento=dias_suprimento,
                           ocupacao_armazem=ocupacao_armazem,
                           caixas_ocupadas=caixas_ocupadas,
                           data_inicio=data_inicio,
                           data_fim=data_fim)

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    categorias = listar_categorias()
    
    if request.method == 'POST':
        try:
            codigo = int(request.form.get('codigo'))
            descricao = request.form.get('descricao')
            qtd = int(request.form.get('quantidade'))
            min_qtd = int(request.form.get('quantidade_minima'))
            valor_un = float(request.form.get('valor_unitario'))
            cat_id = int(request.form.get('categoria'))
            loc = request.form.get('localizacao')
            custo = float(request.form.get('preco_custo'))
            
            novo_prod = Produto(codigo, descricao, qtd, min_qtd, valor_un, cat_id, loc, custo)
            
            if cadastrar_produto(novo_prod):
                gerar_qrcode_produto(codigo)
                flash(f'Produto {codigo} cadastrado com sucesso!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Erro: Já existe um produto com este código.', 'error')
        except ValueError:
            flash('Erro: Verifique se os campos numéricos estão corretos.', 'error')
            
    return render_template('cadastro.html', categorias=categorias)

@app.route('/movimentacao', methods=['GET', 'POST'])
def movimentacao():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    produtos = listar_produtos()
    
    if request.method == 'POST':
        try:
            codigo = int(request.form.get('codigo'))
            quantidade = int(request.form.get('quantidade'))
            tipo = request.form.get('tipo')
            usuario_id = session['usuario_id']
            
            # Validação básica
            produto = buscar_produto_por_codigo(codigo)
            if not produto:
                flash('Erro: Produto não encontrado.', 'error')
            elif tipo == 'SAIDA' and produto[2] < quantidade:
                flash(f'Erro: Estoque insuficiente ({produto[2]} disponíveis).', 'error')
            else:
                if registrar_movimentacao(codigo, quantidade, tipo, usuario_id):
                    flash(f'Movimentação de {tipo} registrada com sucesso!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Erro ao processar movimentação no banco de dados.', 'error')
        except ValueError:
            flash('Erro: Verifique se os campos numéricos estão corretos.', 'error')
            
    return render_template('movimentacao.html', produtos=produtos)

@app.route('/historico')
def historico():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    movs = listar_movimentacoes()
    historico_processado = []
    
    for m in movs:
        historico_processado.append({
            'id': m[0],
            'tipo': m[1],
            'sku': m[2],
            'nome': m[3],
            'qtd': m[4],
            'usuario': m[5],
            'data': datetime.strptime(m[6], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')
        })
        
    return render_template('historico.html', historico=historico_processado)

@app.route('/relatorios')
def relatorios():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    produtos = listar_produtos()
    produtos_processados = []
    
    # KPIs Rápidos para o Relatório
    total_itens = 0
    valor_estoque = 0
    itens_alerta = 0
    
    for p in produtos:
        qtd = p[2] or 0
        min_qtd = p[3] or 0
        custo = p[8] or 0.0
        venda = p[4] or 0.0
        
        produtos_processados.append({
            'sku': p[0], 'nome': p[1], 'qtd': qtd, 'min': min_qtd,
            'venda': venda, 'custo': custo, 'cat': p[5]
        })
        total_itens += qtd
        valor_estoque += (qtd * custo)
        if qtd <= min_qtd: itens_alerta += 1
        
    return render_template('relatorios.html', 
                           produtos=produtos_processados,
                           total_itens=total_itens,
                           valor_estoque=valor_estoque,
                           itens_alerta=itens_alerta)

@app.route('/exportar/csv')
def exportar_csv():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
        
    produtos = listar_produtos()
    
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['SKU', 'Produto', 'Quantidade', 'Qtd Minima', 'Preco Venda', 'Categoria', 'Preco Custo'])
    
    for p in produtos:
        cw.writerow([p[0], p[1], p[2], p[3], p[4], p[5], p[8]])
        
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=relatorio_estoque.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
