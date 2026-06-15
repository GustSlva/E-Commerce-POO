import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from excecoes import ErroValidacao, ErroProdutoSemCategoria, ErroPrecoInvalido, ErroQuantidadeInvalida

class Categoria:
    def __init__(self, id, nome):
        if not nome or not nome.strip():
            raise ErroValidacao("O nome da categoria nao pode ser vazio.")
        self.id = id
        self.nome = nome
        self.promocao_ativa = False
        self.desconto = 0.0
        self.inicio_promocao = None
        self.fim_promocao = None

    def __str__(self):
        return f"{self.id} - {self.nome}"


class Produto:
    def __init__(self, id, nome, preco, quantidade, categoria, imagem=None):
        if categoria is None:
            raise ErroProdutoSemCategoria("O produto precisa ter uma categoria.")
        if preco < 0:
            raise ErroPrecoInvalido("O preco nao pode ser negativo.")
        if quantidade < 0:
            raise ErroQuantidadeInvalida("A quantidade nao pode ser negativa.")
        self.id = id
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.categoria = categoria
        self.imagem = imagem

    def preco_com_desconto(self):
        if self.categoria.promocao_ativa and self.categoria.desconto > 0:
            return self.preco * (1 - self.categoria.desconto / 100)
        return self.preco

    def __str__(self):
        return (f"ID: {self.id} | {self.nome} | "
                f"Preco: R${self.preco:.2f} | "
                f"Qtd: {self.quantidade} | "
                f"Categoria: {self.categoria.nome}")