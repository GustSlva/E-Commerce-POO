from dao_base import GenericDAO
from models import Cliente, Produto
from exceptions import EmailDuplicadoException, ExclusaoInvalidaException
import sqlite3

class ClienteDAO(GenericDAO[Cliente]):
    def _criar_tabela(self):
        conn = self._get_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def _verificar_email_duplicado(self, email: str, id_ignorada: int = None):
        conn = self._get_connection()
        cursor = conn.cursor()
        if id_ignorada:
            cursor.execute("SELECT id FROM clientes WHERE email = ? AND id != ?", (email, id_ignorada))
        else:
            cursor.execute("SELECT id FROM clientes WHERE email = ?", (email,))
        
        if cursor.fetchone():
            conn.close()
            raise EmailDuplicadoException(email)
        conn.close()

    def inserir(self, obj: Cliente) -> int:
        self._verificar_email_duplicado(obj._email)
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clientes (nome, email, senha) VALUES (?, ?, ?)",
                       (obj._nome, obj._email, obj._senha))
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    def atualizar(self, obj: Cliente):
        self._verificar_email_duplicado(obj._email, obj._id)
        conn = self._get_connection()
        conn.execute("UPDATE clientes SET nome=?, email=?, senha=? WHERE id=?",
                     (obj._nome, obj._email, obj._senha, obj._id))
        conn.commit()
        conn.close()

    def excluir(self, id: int):
        conn = self._get_connection()
        conn.execute("DELETE FROM clientes WHERE id=?", (id,))
        conn.commit()
        conn.close()

    def buscar_por_id(self, id: int):
        conn = self._get_connection()
        cursor = conn.execute("SELECT * FROM clientes WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Cliente(row['id'], row['nome'], row['email'], row['senha'])
        return None

    def listar_todos(self):
        conn = self._get_connection()
        cursor = conn.execute("SELECT * FROM clientes")
        rows = cursor.fetchall()
        conn.close()
        return [Cliente(r['id'], r['nome'], r['email'], r['senha']) for r in rows]


class ProdutoDAO(GenericDAO[Produto]):
    def _criar_tabela(self):
        conn = self._get_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL,
                id_categoria INTEGER NOT NULL,
                caminho_imagem TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS itens_pedido (
                id_pedido INTEGER,
                id_produto INTEGER
            )
        ''')
        conn.commit()
        conn.close()

    def inserir(self, obj: Produto) -> int:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO produtos (nome, preco, id_categoria, caminho_imagem) VALUES (?, ?, ?, ?)",
                       (obj._nome, obj._preco, obj.id_categoria, obj._caminho_imagem))
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    def atualizar(self, obj: Produto):
        conn = self._get_connection()
        conn.execute("UPDATE produtos SET nome=?, preco=?, id_categoria=?, caminho_imagem=? WHERE id=?",
                     (obj._nome, obj._preco, obj.id_categoria, obj._caminho_imagem, obj._id))
        conn.commit()
        conn.close()

    def excluir(self, id: int):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM itens_pedido WHERE id_produto = ?", (id,))
        if cursor.fetchone():
            conn.close()
            raise ExclusaoInvalidaException(f"Produto ID {id}")
            
        cursor.execute("DELETE FROM produtos WHERE id = ?", (id,))
        conn.commit()
        conn.close()

    def buscar_por_id(self, id: int):
        conn = self._get_connection()
        cursor = conn.execute("SELECT * FROM produtos WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Produto(row['id'], row['nome'], row['preco'], row['id_categoria'], row['caminho_imagem'])
        return None

    def listar_todos(self):
        conn = self._get_connection()
        cursor = conn.execute("SELECT * FROM produtos")
        rows = cursor.fetchall()
        conn.close()
        return [Produto(r['id'], r['nome'], r['preco'], r['id_categoria'], r['caminho_imagem']) for r in rows]