# StockMaster - Controle de Estoque Inteligente

Sistema de gestão de estoque desenvolvido em Python/Flask, focado em alta usabilidade, inteligência operacional e alocação dinâmica de armazenamento.

## 🚀 Funcionalidades Principais

*   **Dashboard Estratégico:** Visão 360° com KPIs de Lucro Potencial, Saúde do Estoque, Dias de Suprimento e Ocupação do Armazém.
*   **Movimentação Inteligente:** Registro de Entradas e Saídas com **Autocomplete** e preview em tempo real.
*   **Alocação Automática:** Gerenciamento de 450 posições (Prateleiras/Caixas) com alocação automática de itens (limite de 10 por caixa).
*   **Inteligência de Reabastecimento:** Sugestão de compra baseada na média de consumo diário dos últimos 30 dias.
*   **Auditoria Completa:** Histórico detalhado de todas as operações com filtros dinâmicos.
*   **Relatórios e Exportação:** Auditoria de inventário com exportação para CSV e suporte a Impressão/PDF.

## 📊 Arquitetura do Banco de Dados (MER)

O sistema utiliza um banco de dados SQLite modelado para garantir integridade e rastreabilidade.

```mermaid
erDiagram
    USUARIO ||--o{ MOVIMENTACAO : "realiza"
    CATEGORIA ||--o{ PRODUTO : "pertence"
    FORNECEDOR ||--o{ PRODUTO : "fornece"
    PRODUTO ||--o{ MOVIMENTACAO : "sofre"
    PRODUTO ||--o{ ESTRUTURA_ARMAZENAMENTO : "armazenado em"

    USUARIO {
        int id PK
        string login
        string senha
        string nivel_acesso
    }

    CATEGORIA {
        int id PK
        string nome
    }

    FORNECEDOR {
        int id PK
        string nome
        string contato
    }

    PRODUTO {
        int codigo PK
        string descricao
        int quantidade
        int quantidade_minima
        float valor_unitario
        float preco_custo
        string localizacao
        int id_categoria FK
        int id_fornecedor FK
    }

    MOVIMENTACAO {
        int id PK
        string tipo
        int quantidade
        int codigo_produto FK
        int id_usuario FK
        datetime data_hora
    }

    ESTRUTURA_ARMAZENAMENTO {
        int id PK
        string prateleira
        int caixa
        int ocupacao
        int capacidade_max
        int produto_codigo FK
    }
```

## 🛠️ Tecnologias Utilizadas

*   **Backend:** Python 3 + Flask
*   **Banco de Dados:** SQLite
*   **Frontend:** HTML5, CSS3 (Untitled UI Design System), JavaScript Vanilla
*   **Gráficos:** Chart.js

## 🏁 Como Iniciar

1. Instale as dependências:
   ```bash
   pip install flask
   ```
2. Inicialize o banco de dados (se necessário):
   ```bash
   python Services/inicializar_db.py
   ```
3. Execute o servidor:
   ```bash
   python app_flask.py
   ```
4. Acesse em seu navegador: `http://localhost:5000`

---
*Desenvolvido como projeto de Laboratório de Estudos - 2026*
