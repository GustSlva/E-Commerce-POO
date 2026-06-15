class ErroValidacao(Exception):
    pass

class ErroClienteDuplicado(ErroValidacao):
    pass

class ErroProdutoSemCategoria(ErroValidacao):
    pass

class ErroPrecoInvalido(ErroValidacao):
    pass

class ErroQuantidadeInvalida(ErroValidacao):
    pass

class ErroEstoqueInsuficiente(ErroValidacao):
    pass

class ErroLoginVazio(ErroValidacao):
    pass