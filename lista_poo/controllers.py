import os
from datetime import date
from models import Produto, Cliente, Pedido, Promocao
from daos import ProdutoDAO, ClienteDAO
# Supondo a existência de PedidoDAO e PromocaoDAO estruturados de forma similar
from exceptions import RegraNegocioException

class ProdutoController:
    def __init__(self):
        self.produto_dao = ProdutoDAO()
        # Aqui instanciaríamos o PromocaoDAO real
        # self.promocao_dao = PromocaoDAO() 
        self.diretorio_imagens = "uploads/produtos"
        self._garantir_diretorio_imagens()

    def _garantir_diretorio_imagens(self):
        if not os.path.exists(self.diretorio_imagens):
            os.makedirs(self.diretorio_imagens)

    def cadastrar_produto(self, nome: str, preco: float, id_categoria: int, arquivo_imagem_bytes: bytes, nome_arquivo: str) -> int:
        """
        Orquestra a criação de um produto: salva a imagem no disco e persiste no banco.
        """
        caminho_imagem = ""
        if arquivo_imagem_bytes and nome_arquivo:
            caminho_imagem = os.path.join(self.diretorio_imagens, nome_arquivo)
            with open(caminho_imagem, "wb") as f:
                f.write(arquivo_imagem_bytes)

        # O modelo fará a validação da categoria através do seu setter
        novo_produto = Produto(id=0, nome=nome, preco=preco, id_categoria=id_categoria, caminho_imagem=caminho_imagem)
        
        return self.produto_dao.inserir(novo_produto)

    def listar_vitrine(self) -> list:
        """
        Retorna a lista de produtos calculando o preço final caso haja uma promoção ativa.
        Esta é uma lógica puramente de negócio.
        """
        produtos = self.produto_dao.listar_todos()
        # Exemplo simulado de busca de promoções ativas no dia de hoje
        # promocoes_ativas = self.promocao_dao.buscar_ativas_na_data(date.today())
        promocoes_ativas = {} # Dicionário simulado: {id_categoria: percentual_desconto}
        
        vitrine = []
        for p in produtos:
            desconto = promocoes_ativas.get(p.id_categoria, 0.0)
            preco_final = p._preco * (1 - (desconto / 100))
            
            vitrine.append({
                "id": p._id,
                "nome": p._nome,
                "preco_original": p._preco,
                "preco_promocional": preco_final,
                "em_promocao": desconto > 0,
                "caminho_imagem": p._caminho_imagem
            })
        return vitrine


class AutenticacaoController:
    def __init__(self):
        self.cliente_dao = ClienteDAO()

    def registrar_cliente(self, nome: str, email: str, senha: str) -> int:
        """
        Tenta registrar o cliente. Se o e-mail for duplicado, 
        a EmailDuplicadoException subirá naturalmente do DAO para a View.
        """
        # Validações básicas antes de instanciar
        if not nome or not email or not senha:
            raise RegraNegocioException("Todos os campos de registro são obrigatórios.")
            
        novo_cliente = Cliente(id=0, nome=nome, email=email, senha=senha)
        return self.cliente_dao.inserir(novo_cliente)


class PedidoController:
    def finalizar_compra(self, id_cliente: int, itens_carrinho: list) -> int:
        """
        Processa os itens do carrinho e gera um novo pedido com status inicial.
        """
        if not itens_carrinho:
            raise RegraNegocioException("Não é possível finalizar uma compra com o carrinho vazio.")

        # Na prática real, aqui instanciaríamos o Pedido, vincularíamos os itens e
        # chamaríamos o PedidoDAO para inserir de forma transacional.
        # return pedido_dao.inserir(novo_pedido)
        return 1 # ID mockado retornado em caso de sucesso