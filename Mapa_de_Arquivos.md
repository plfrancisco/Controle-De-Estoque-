# 📍 Mapa de Arquivos - Controle de Estoque (v2.0 Flask)

## 📂 Localização de Contexto
- **Este Arquivo:** `02_Laboratorio_Estudos/Controle_de_estoque/Mapa_de_Arquivos.md`
- **Log Factual & Diretrizes:** `99_Bastidores/Contexto_Projetos/Controle_de_estoque_Context/LOG_FACTUAL.md`

## 📂 Estrutura de Código (.)
- **app_flask.py**: Servidor principal (Backend Flask).
- **templates/**: Interface HTML (Login, Dashboard, Cadastro).
- **static/**: Arquivos estáticos (CSS, Imagens).
- **Controllers/**: Lógica de negócio e acesso ao banco.
    - `ProdutoController.py`: Gestão de produtos e alocação.
    - `MovimentacaoController.py`: Lógica de entradas e saídas.
- **Models/**: Classes de dados (Produto, Usuario).
- **Services/**: Banco de dados e inicialização.
- **qrcodes/**: Armazenamento de etiquetas geradas (Ignorado pelo Git).
- **MER_Diagrama.md**: Documentação visual do banco de dados (Mermaid).


## 🔡 Dicionário de Símbolos
- **P[n]-C[n]**: Sistema de localização (Prateleira-Caixa).
- **KPI Estratégico**: Lucro Potencial, Saúde do Estoque e Dias de Suprimento.
- **Curva ABC (Pareto)**: Top 5 produtos por lucro gerado em saídas reais.
- **Shadow Layer**: Pasta `.skills/` contendo inteligência local para o projeto.
