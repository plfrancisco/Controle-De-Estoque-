# 📊 Documentação de Dados - Controle de Estoque (Fiel ao BD)

Esta documentação descreve a estrutura física e lógica real do banco de dados `Estoque.db`.

## 1. Modelo Entidade-Relacionamento (MER)

### Entidades e Atributos

- **USUARIO**: Operadores do sistema.
    - `id` (PK), `login` (Único), `senha`, `nivel_acesso`.

- **PRODUTO**: Itens do inventário.
    - `codigo` (PK), `descricao`, `quantidade`, `quantidade_minima`, `valor_unitario`, `preco_custo`, `localizacao`, `id_categoria` (FK), `id_fornecedor` (FK).

- **CATEGORIA**: Agrupamento lógico.
    - `id` (PK), `nome`.

- **FORNECEDOR**: Parceiros comerciais.
    - `id` (PK), `nome`, `contato`, `cnpj`, `email`, `telefone`.

- **MOVIMENTACAO**: Histórico de transações.
    - `id` (PK), `tipo`, `codigo_produto` (FK), `quantidade`, `id_usuario` (FK), `data_hora`.

- **ESTRUTURA_ARMAZENAMENTO**: Gestão física de espaço.
    - `id` (PK), `prateleira`, `caixa`, `ocupacao`, `capacidade_max`, `produto_codigo` (FK).

- **PRODUTO_FORNECEDOR**: Tabela de ligação (N:N).
    - `produto_codigo` (FK), `fornecedor_id` (FK).

- **CATEGORIAS_LOG**: Tabela utilitária de sistema.
    - `nome` (Único).

---

## 2. Diagrama Entidade-Relacionamento (DER)

```mermaid
erDiagram
    USUARIO ||--o{ MOVIMENTACAO : "realiza"
    CATEGORIA ||--o{ PRODUTO : "classifica"
    FORNECEDOR ||--o{ PRODUTO : "fornece (1:N)"
    PRODUTO ||--o{ MOVIMENTACAO : "registra"
    PRODUTO ||--o{ ESTRUTURA_ARMAZENAMENTO : "localizado em"
    PRODUTO ||--o{ PRODUTO_FORNECEDOR : "tem"
    FORNECEDOR ||--o{ PRODUTO_FORNECEDOR : "fornece"

    USUARIO {
        int id PK
        string login
        string nivel_acesso
    }

    CATEGORIA {
        int id PK
        string nome
    }

    FORNECEDOR {
        int id PK
        string nome
        string cnpj
        string email
        string telefone
    }

    PRODUTO {
        int codigo PK
        string descricao
        int quantidade
        float valor_unitario
        float preco_custo
        string localizacao
        int id_categoria FK
    }

    ESTRUTURA_ARMAZENAMENTO {
        int id PK
        string prateleira
        int caixa
        int ocupacao
        int capacidade_max
        int produto_codigo FK
    }

    MOVIMENTACAO {
        int id PK
        string tipo
        int quantidade
        int codigo_produto FK
        datetime data_hora
    }

    PRODUTO_FORNECEDOR {
        int produto_codigo FK
        int fornecedor_id FK
    }
```

---
**Sincronização Final:** 17 de Maio de 2026 (Refletindo esquema físico real).

---
**Última Atualização:** 17 de Maio de 2026
**Status:** Sincronizado com v6.0 do Sistema.
