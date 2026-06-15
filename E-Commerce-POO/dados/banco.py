class Banco:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia

    def _inicializar(self):
        self.usuarios = {}
        self.categorias = {}
        self.produtos = {}
        self.vendas = []

        self._proximo_id_categoria = 1
        self._proximo_id_produto = 1
        self._proximo_id_venda = 1

    def proximo_id_categoria(self):
        id_atual = self._proximo_id_categoria
        self._proximo_id_categoria += 1
        return id_atual

    def proximo_id_produto(self):
        id_atual = self._proximo_id_produto
        self._proximo_id_produto += 1
        return id_atual

    def proximo_id_venda(self):
        id_atual = self._proximo_id_venda
        self._proximo_id_venda += 1
        return id_atual