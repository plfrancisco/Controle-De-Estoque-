# 📊 Modelo Entidade-Relacionamento (MER) - Controle de Estoque

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

---
**Nota:** Este diagrama utiliza a sintaxe **Mermaid**, que é renderizada automaticamente como uma imagem no **Obsidian** e no **GitHub**.
