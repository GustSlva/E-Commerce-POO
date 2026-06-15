class RegraNegocioException(Exception):
    """Exceção base para violações de regras de negócio."""
    pass

class EmailDuplicadoException(RegraNegocioException):
    def __init__(self, email):
        super().__init__(f"O e-mail '{email}' já está em uso por outro cliente.")

class ProdutoInvalidoException(RegraNegocioException):
    def __init__(self, mensagem="Produto não possui uma categoria válida."):
        super().__init__(mensagem)

class ExclusaoInvalidaException(RegraNegocioException):
    def __init__(self, entidade):
        super().__init__(f"Não é possível excluir: {entidade} possui histórico de transações vinculadas.")

class PromocaoInvalidaException(RegraNegocioException):
    def __init__(self, mensagem="A data de término não pode ser anterior à data de início."):
        super().__init__(mensagem)