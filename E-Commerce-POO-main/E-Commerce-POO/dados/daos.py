import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dados.dao import DAO
from dados.banco import Banco

class UsuarioDAO(DAO):
    def __init__(self):
        banco = Banco()
        super().__init__(banco, banco.usuarios)

class ProdutoDAO(DAO):
    def __init__(self):
        banco = Banco()
        super().__init__(banco, banco.produtos)

class CategoriaDAO(DAO):
    def __init__(self):
        banco = Banco()
        super().__init__(banco, banco.categorias)

class VendaDAO(DAO):
    def __init__(self):
        banco = Banco()
        super().__init__(banco, banco.vendas)