from exceptions import ProdutoInvalidoException, PromocaoInvalidaException
from datetime import date

class Usuario:
    def __init__(self, id: int, nome: str, email: str, senha: str):
        self._id = id
        self._nome = nome
        self._email = email
        self._senha = senha

    @property
    def email(self):
        return self._email

    # O e-mail será validado no DAO para evitar duplicações no banco de dados.

class Cliente(Usuario):
    def __init__(self, id: int, nome: str, email: str, senha: str):
        super().__init__(id, nome, email, senha)

class Admin(Usuario):
    def __init__(self, id: int, nome: str, email: str, senha: str):
        super().__init__(id, nome, email, senha)

class Entregador(Usuario):
    def __init__(self, id: int, nome: str, email: str, senha: str, cnh: str):
        super().__init__(id, nome, email, senha)
        self._cnh = cnh

class Categoria:
    def __init__(self, id: int, nome: str):
        self._id = id
        self._nome = nome

class Produto:
    def __init__(self, id: int, nome: str, preco: float, id_categoria: int, caminho_imagem: str = ""):
        self._id = id
        self._nome = nome
        self._preco = preco
        self._caminho_imagem = caminho_imagem
        # O setter realizará a validação exigida
        self.id_categoria = id_categoria

    @property
    def id_categoria(self):
        return self._id_categoria

    @id_categoria.setter
    def id_categoria(self, valor):
        if not valor or valor <= 0:
            raise ProdutoInvalidoException("O produto deve estar obrigatoriamente vinculado a uma categoria válida.")
        self._id_categoria = valor

class Promocao:
    def __init__(self, id: int, id_categoria: int, percentual_desconto: float, data_inicio: date, data_fim: date):
        self._id = id
        self._id_categoria = id_categoria
        self._percentual_desconto = percentual_desconto
        self._data_inicio = data_inicio
        self.data_fim = data_fim # Passa pelo setter para validação

    @property
    def data_fim(self):
        return self._data_fim

    @data_fim.setter
    def data_fim(self, valor):
        if valor < self._data_inicio:
            raise PromocaoInvalidaException("A data de término não pode ser anterior à data de início da promoção.")
        self._data_fim = valor
class ItemPedido:
    def __init__(self, id_produto: int, quantidade: int, preco_unitario: float):
        self.id_produto = id_produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario

class Pedido:
    def __init__(self, id: int, id_cliente: int, itens: list):
        self._id = id
        self._id_cliente = id_cliente
        self._itens = itens
        self._status_entrega = "Pendente"
        self._id_entregador = None

    @property
    def status_entrega(self):
        return self._status_entrega

    @status_entrega.setter
    def status_entrega(self, novo_status):
        # Aqui poderíamos colocar uma validação de regras de negócio 
        # para não permitir voltar atrás num status, por exemplo.
        self._status_entrega = novo_status