class Venda:
    def __init__(self, id, cliente, itens):
        self.id = id
        self.cliente = cliente
        self.itens = itens
        self.status_entrega = "Pendente"  # Novo atributo
        self.entregador = None            # Novo atributo

    def total(self):
        return sum(item.produto.preco * item.quantidade for item in self.itens)

    def __str__(self):
        texto = f"Venda #{self.id} | Cliente: {self.cliente.nome} | Total: R${self.total():.2f}\n"
        for item in self.itens:
            texto += f"  - {item}\n"
        return texto