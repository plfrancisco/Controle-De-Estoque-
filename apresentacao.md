# 💎 Inventory. - Sistema de Gestão de Ativos e BI

*(Documento base para geração de apresentação visual no Gamma App)*

---

## 🎯 A Filosofia do Sistema
**Inventory.** não é apenas um controle de estoque, é uma ferramenta de **Inteligência de Negócios (BI) e Curadoria de Ativos**. Projetado com a estética "Corporate Edition" (Glassmorphism e Organic Flow), ele transforma dados complexos em uma experiência visual executiva e agradável.

---

## 🏗️ A Engenharia por Trás (Arquitetura)
O coração do Inventory. opera sob uma arquitetura limpa focada em performance e integridade de dados.

*   **Motor Principal:** Python 3.10+
*   **Interface (UI/UX):** Streamlit (com CSS Customizado para Glassmorphism)
*   **Gestão de Dados:** `database_engine.py` (Centralizador de Schema SQLite)
*   **Visualização Analítica:** Plotly Graph Objects e Pandas

---

## 🗄️ Modelagem de Dados (O Banco)
A infraestrutura de banco de dados relacional foi modelada para garantir total rastreabilidade corporativa.

### Entidades Principais:
1.  **Ativos (PRODUTO):** O núcleo do sistema. Registra SKU, custos de aquisição, valor de mercado e alertas de conformidade (estoque mínimo).
2.  **Infraestrutura (PRATELEIRA & ESTRUTURA):** Mapeamento físico 1:1 do almoxarifado, controlando a capacidade e ocupação de caixas e prateleiras.
3.  **Ecossistema (CATEGORIA & FORNECEDOR):** Tabelas de domínio para organizar o patrimônio.
4.  **Auditoria (MOVIMENTACAO & LOG_EXCLUSAO):** Tabelas imutáveis que garantem a gravação de todas as entradas, saídas e justificativas de exclusão.

### Relacionamentos Chave:
*   `PRODUTO_FORNECEDOR` (N:N) - Permite que um ativo seja suprido por múltiplos parceiros.
*   `MOVIMENTACAO -> PRODUTO` (1:N) - Rastreia o ciclo de vida completo de cada SKU.

---

## 🔄 Fluxos Operacionais (Os Controllers)
A inteligência do sistema reside nos Controladores, que atuam como guardiões das regras de negócio.

### 1. ProdutoController (Gestão de Ativos)
*   **Ingresso de Ativos:** Valida a unicidade do SKU e gerencia a associação automática com fornecedores.
*   **Auditoria de Registros:** Permite correções de dados mestre garantindo que o SKU base permaneça inalterado (Proteção de Chave Primária).
*   **Compliance de Exclusão:** Exige justificativa técnica obrigatória antes de realizar uma exclusão "soft" ou registrar no log de auditoria.

### 2. MovimentacaoController (O Motor de Fluxo)
*   **Protocolo de Entrada:** Registra suprimentos e calcula automaticamente o novo patrimônio ativo.
*   **Validação de Saída:** Impede fisicamente a saída de ativos se não houver saldo suficiente no banco de dados.
*   **Registro Transacional:** Cada operação é carimbada com data, tipo (Entrada/Saída) e justificativa técnica, construindo o histórico da empresa.

### 3. EstruturaController (Gestão Espacial)
*   **Expansão:** Cria dinamicamente novas zonas de armazenamento (Prateleiras) com capacidade customizável.
*   **Monitoramento:** Fornece os dados para o cálculo de eficiência (Percentual de Ocupação da Planta).
*   **Desmobilização:** Trava de segurança que impede a exclusão de estruturas que não estejam 100% vazias.

---

## 📊 Inteligência Executiva (A Visão)
A interface transforma as regras dos Controllers e os dados do Banco em inteligência acionável:

*   **Executive Data Grid:** Tabelas sem bordas, com "Glass Hover", que exibem os registros de forma minimalista.
*   **Curva ABC (Gráficos):** Classifica automaticamente os ativos em Prioritários (A), Estratégicos (B) e Operacionais (C) com base no valor patrimonial.
*   **Feedback de Sustentação:** UX cuidadosamente desenhada para dar tempo ao usuário de ler confirmações antes de transições de tela, garantindo tranquilidade operacional.
