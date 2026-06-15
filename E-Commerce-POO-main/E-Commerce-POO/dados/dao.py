class DAO:
    def __init__(self, banco, colecao):
        self._banco = banco
        self._colecao = colecao

    def inserir(self, id, objeto):
        self._colecao[id] = objeto

    def buscar(self, id):
        return self._colecao.get(id)

    def listar(self):
        return list(self._colecao.values())

    def atualizar(self, id, objeto):
        if id not in self._colecao:
            raise Exception(f"Objeto com id {id} nao encontrado.")
        self._colecao[id] = objeto

    def excluir(self, id):
        if id not in self._colecao:
            raise Exception(f"Objeto com id {id} nao encontrado.")
        del self._colecao[id]