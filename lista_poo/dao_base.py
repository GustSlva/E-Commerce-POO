from inspect import _void
import sqlite3
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional

# Criação de um tipo genérico T para representar as entidades
T = TypeVar('T')

class GenericDAO(ABC, Generic[T]):
    """
    Classe base abstrata para o padrão Data Access Object.
    Todas as classes de persistência devem herdar desta classe.
    """
    
    def __init__(self, db_path: str = "ecommerce.db"):
        self.db_path = db_path
        self._criar_tabela()

    def _get_connection(self):
        """Retorna uma conexão com o banco SQLite."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
        return conn

    @abstractmethod
    def _criar_tabela(self) -> _void:
        """Método que as filhas devem implementar para garantir que a tabela exista."""
        pass

    @abstractmethod
    def inserir(self, obj: T) -> int:
        pass

    @abstractmethod
    def atualizar(self, obj: T) -> _void:
        pass

    @abstractmethod
    def excluir(self, id: int) -> _void:
        pass

    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[T]:
        pass

    @abstractmethod
    def listar_todos(self) -> List[T]:
        pass