import streamlit as st
from controllers import ProdutoController, AutenticacaoController, PedidoController
from exceptions import RegraNegocioException

# Configuração da Página
st.set_page_config(page_title="E-Commerce POO", layout="wide")

# Instância dos Controladores
# Em uma aplicação real, você pode injetar essas dependências ou usar Singleton
produto_controller = ProdutoController()
auth_controller = AutenticacaoController()
pedido_controller = PedidoController()

def inicializar_sessao():
    """Inicializa as variáveis de sessão para controle de estado do usuário."""
    if 'usuario_logado' not in st.session_state:
        st.session_state['usuario_logado'] = None
    if 'perfil' not in st.session_state:
        st.session_state['perfil'] = 'Visitante' # Pode ser 'Cliente', 'Admin', 'Entregador'
    if 'carrinho' not in st.session_state:
        st.session_state['carrinho'] = []

def renderizar_autenticacao():
    st.title("Bem-vindo ao E-Commerce")
    tab_login, tab_registro = st.tabs(["Entrar", "Abrir Conta"])
    
    with tab_registro:
        st.subheader("Crie sua conta de Cliente")
        with st.form("form_registro"):
            nome = st.text_input("Nome Completo")
            email = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Registrar")
            
            if submit:
                # O bloco try/except captura regras de negócio, como Email Duplicado
                try:
                    auth_controller.registrar_cliente(nome, email, senha)
                    st.success("Conta criada com sucesso! Você já pode fazer login.")
                except RegraNegocioException as e:
                    st.error(f"Não foi possível criar a conta: {str(e)}")
                except Exception as e:
                    st.error("Ocorreu um erro inesperado no sistema.")

def renderizar_admin():
    st.title("Painel Administrativo")
    menu = st.sidebar.radio("Navegação Admin", ["Cadastrar Produto", "Listar Vendas", "Promoções", "Alocar Entregadores"])
    
    if menu == "Cadastrar Produto":
        st.subheader("Novo Produto")
        with st.form("form_produto"):
            nome = st.text_input("Nome do Produto")
            preco = st.number_input("Preço (R$)", min_value=0.01, step=0.01)
            id_categoria = st.number_input("ID da Categoria", min_value=1, step=1)
            
            # Componente Streamlit para Upload de Imagem
            imagem_arquivo = st.file_uploader("Upload da Imagem do Produto", type=['png', 'jpg', 'jpeg'])
            
            submit = st.form_submit_button("Salvar Produto")
            
            if submit:
                try:
                    # Lê os bytes e o nome do arquivo, se o usuário fez o upload
                    img_bytes = imagem_arquivo.read() if imagem_arquivo else b""
                    nome_arq = imagem_arquivo.name if imagem_arquivo else ""
                    
                    produto_controller.cadastrar_produto(nome, preco, id_categoria, img_bytes, nome_arq)
                    st.success("Produto cadastrado com sucesso!")
                except RegraNegocioException as e:
                    # Captura ProdutoInvalidoException se a categoria não for válida, por exemplo
                    st.warning(str(e)) 

def renderizar_cliente():
    st.title("Vitrine de Produtos")
    st.write("Aproveite nossas ofertas!")
    
    # Chama a lógica de negócio que já calcula preços promocionais
    vitrine = produto_controller.listar_vitrine()
    
    if not vitrine:
        st.info("Nenhum produto cadastrado no momento.")
        return

    # Organiza os produtos em colunas dinâmicas (grid)
    cols = st.columns(3)
    for index, produto in enumerate(vitrine):
        with cols[index % 3]:
            # Mostra a imagem, se houver caminho e ele existir no disco
            if produto["caminho_imagem"]:
                try:
                    st.image(produto["caminho_imagem"], use_container_width=True)
                except Exception:
                    st.image("https://via.placeholder.com/150", use_container_width=True, caption="Imagem indisponível")
            
            st.subheader(produto["nome"])
            
            # Destaca preços promocionais
            if produto["em_promocao"]:
                st.markdown(f"~~De: R$ {produto['preco_original']:.2f}~~")
                st.markdown(f"**Por: R$ {produto['preco_promocional']:.2f}**")
            else:
                st.markdown(f"**R$ {produto['preco_original']:.2f}**")
                
            if st.button("Adicionar ao Carrinho", key=f"btn_add_{produto['id']}"):
                st.session_state['carrinho'].append(produto)
                st.success(f"{produto['nome']} adicionado ao carrinho!")

# ==========================================
# Roteamento Principal
# ==========================================
def main():
    inicializar_sessao()
    
    # Simulação de botões de navegação rápida para teste da arquitetura de papéis
    st.sidebar.title("Simulador de Sessão")
    papel = st.sidebar.selectbox("Selecione seu perfil (Simulação):", ["Visitante", "Cliente", "Admin"])
    st.session_state['perfil'] = papel

    if st.session_state['perfil'] == 'Visitante':
        renderizar_autenticacao()
    elif st.session_state['perfil'] == 'Admin':
        renderizar_admin()
    elif st.session_state['perfil'] == 'Cliente':
        renderizar_cliente()

if __name__ == "__main__":
    main()