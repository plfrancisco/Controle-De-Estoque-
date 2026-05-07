class Produto:
    def __init__(self, codigo, descricao, quantidade, quantidade_minima, valor_unitario, categoria, localizacao, preco_custo):
        self._codigo = codigo
        self._descricao = descricao
        self._quantidade = quantidade
        self._quantidade_minima = quantidade_minima
        self._valor_unitario = valor_unitario
        self._categoria = categoria
        self._localizacao = localizacao
        self._preco_custo = preco_custo

    def get_codigo(self): return self._codigo
    def get_descricao(self): return self._descricao
    def get_quantidade(self): return self._quantidade
    def get_quantidade_minima(self): return self._quantidade_minima
    def get_valor_unitario(self): return self._valor_unitario
    def get_categoria(self): return self._categoria
    def get_localizacao(self): return self._localizacao
    def get_preco_custo(self): return self._preco_custo
