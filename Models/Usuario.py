# =================================================================
# MODELO: Usuario
# Responsabilidade: Representação de um Operador do Sistema
# =================================================================

class Usuario:
    """
    Define os atributos de um usuário para fins de autenticação e
    controle de permissões no sistema.
    """
    def __init__(self, id, login, senha, nivel_acesso):
        self._id = id
        self._login = login
        self._senha = senha
        self._nivel_acesso = nivel_acesso

    # -----------------------------------------------------------------
    # MÉTODOS ACESSORES (Getters)
    # -----------------------------------------------------------------
    def get_id(self):
        return self._id

    def get_login(self):
        return self._login

    def get_senha(self):
        return self._senha

    def get_nivel_acesso(self):
        return self._nivel_acesso
