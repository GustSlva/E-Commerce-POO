class ItemCarrinho:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade

    def __str__(self):
        total = self.produto.preco * self.quantidade
        return (f"{self.produto.nome} | "
                f"Preco unitario: R${self.produto.preco:.2f} | "
                f"Quantidade: {self.quantidade} | "
                f"Total: R${total:.2f}")