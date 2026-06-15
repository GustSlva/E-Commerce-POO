import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from datetime import date
from dados.banco import Banco
from modelos.usuario import Cliente, Admin
from modelos.produto import Produto, Categoria
from modelos.carrinho import ItemCarrinho
from modelos.venda import Venda
from excecoes import ErroValidacao, ErroEstoqueInsuficiente, ErroQuantidadeInvalida


banco = Banco()

if "admetop" not in banco.usuarios:
    admin_padrao = Admin(
        login="admetop",
        senha="admin",
        nome="Admin",
        email="administrador@admin.com",
        telefone="(84) 4002-8922"
    )
    banco.usuarios["admetop"] = admin_padrao

if len(banco.produtos) == 0:
    cat1 = Categoria(1, "Eletronicos")
    cat2 = Categoria(2, "Periféricos")
    cat3 = Categoria(3, "Música")

    banco.categorias[1] = cat1
    banco.categorias[2] = cat2
    banco.categorias[3] = cat3

    banco.produtos[1]  = Produto(1,  "Notebook",       3000.00, 5,  cat1, "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    banco.produtos[2]  = Produto(2,  "Iphone",     3500.00, 10,  cat1, "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    banco.produtos[3]  = Produto(3,  "Fone Bluetooth", 200.00, 5,   cat1, "https://images.unsplash.com/photo-1632200004922-bc18602c79fc?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    banco.produtos[4]  = Produto(4,  "Controle", 150.00,  10,  cat2, "https://images.unsplash.com/photo-1632312527375-bd5d5a0d3484?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    banco.produtos[5]  = Produto(5,  "Guitarra",          900.00,   5,  cat3, "https://images.unsplash.com/photo-1516924962500-2b4b3b99ea02?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    banco.produtos[6]  = Produto(6,  "Contrabaixo",        900.00,  3,  cat3, "https://images.unsplash.com/photo-1543060749-aa3f115aad09?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    banco.produtos[7]  = Produto(7,  "Mousepad",  45.00,   20,  cat2, "https://plus.unsplash.com/premium_photo-1664699099191-f67e1f4aef40?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    banco.produtos[8]  = Produto(8,  "Monitor",      3000.00,   10, cat1, "https://images.unsplash.com/photo-1666771410140-0573b232426e?q=80&w=1074&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    banco.produtos[9]  = Produto(9,  "Smartwatch",     350.00,   10, cat1, "https://images.unsplash.com/photo-1637160151663-a410315e4e75?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    banco.produtos[10] = Produto(10, "Tablet",      1800.00,   15,  cat1, "https://images.unsplash.com/photo-1561154464-82e9adf32764?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")


def inicializar_sessao():
    if "usuario" not in st.session_state:
        st.session_state.usuario = None
    if "tipo" not in st.session_state:
        st.session_state.tipo = None


def tela_inicial():
    st.title("LOJÃO DA ORDEM")
    aba = st.tabs(["Login", "Criar Conta"])

    with aba[0]:
        st.subheader("Login")
        login = st.text_input("Login", key="login_login")
        senha = st.text_input("Senha", type="password", key="login_senha")

        if st.button("Entrar"):
            try:
                usuario = banco.usuarios.get(login)
                if usuario is None:
                    raise ErroValidacao("Usuario nao encontrado.")
                if not usuario.verificar_senha(senha):
                    raise ErroValidacao("Senha incorreta.")
                st.session_state.usuario = usuario
                st.session_state.tipo = "admin" if isinstance(usuario, Admin) else "cliente"
                st.rerun()
            except ErroValidacao as e:
                st.error(str(e))

    with aba[1]:
        st.subheader("Criar Nova Conta")
        novo_login    = st.text_input("Login", key="cadastro_login")
        novo_nome     = st.text_input("Nome completo", key="cadastro_nome")
        novo_email    = st.text_input("E-mail", key="cadastro_email")
        novo_fone     = st.text_input("Telefone", key="cadastro_fone")
        novo_cpf      = st.text_input("CPF", key="cadastro_cpf")
        novo_endereco = st.text_input("Endereco", key="cadastro_endereco")
        nova_senha    = st.text_input("Senha", type="password", key="cadastro_senha")

        if st.button("Criar Conta"):
            try:
                if not novo_login or not novo_nome or not novo_email or not nova_senha:
                    raise ErroValidacao("Preencha todos os campos obrigatorios.")
                if novo_login in banco.usuarios:
                    raise ErroValidacao("Esse login ja esta em uso.")
                novo_cliente = Cliente(
                    login=novo_login,
                    senha=nova_senha,
                    nome=novo_nome,
                    email=novo_email,
                    telefone=novo_fone,
                    cpf=novo_cpf,
                    endereco=novo_endereco
                )
                banco.usuarios[novo_login] = novo_cliente
                st.success("Conta criada com sucesso! Faca o login.")
            except ErroValidacao as e:
                st.error(str(e))


def area_cliente():
    cliente = st.session_state.usuario
    st.sidebar.write(f"Logado como: {cliente.nome}")
    if st.sidebar.button("Sair"):
        st.session_state.usuario = None
        st.session_state.tipo = None
        st.rerun()

    aba = st.tabs(["Listar Produtos", "Inserir no Carrinho", "Visualizar Carrinho", "Comprar Carrinho", "Minhas Compras"])

    with aba[0]:
        listar_produtos_cliente()
    with aba[1]:
        inserir_no_carrinho(cliente)
    with aba[2]:
        visualizar_carrinho(cliente)
    with aba[3]:
        comprar_carrinho(cliente)
    with aba[4]:
        listar_minhas_compras(cliente)

def listar_produtos_cliente():
    st.subheader("Produtos Disponiveis")
    try:
        if len(banco.produtos) == 0:
            st.info("Nenhum produto cadastrado.")
            return

        for produto in banco.produtos.values():
            col1, col2 = st.columns([1, 3])
            with col1:
                if produto.imagem is not None:
                    st.image(produto.imagem, width=100)
                else:
                    st.write("Sem imagem")
            with col2:
                st.write(f"**{produto.nome}**")
                st.write(f"Categoria: {produto.categoria.nome}")
                if produto.categoria.promocao_ativa:
                    st.write(f"~~R${produto.preco:.2f}~~")
                    st.write(f"**Preco com desconto: R${produto.preco_com_desconto():.2f}**")
                    st.write(f"Desconto: {produto.categoria.desconto}%")
                else:
                    st.write(f"Preco: R${produto.preco:.2f}")
                st.write(f"Quantidade disponivel: {produto.quantidade}")
            st.divider()
    except ErroValidacao as e:
        st.error(str(e))

def inserir_no_carrinho(cliente):
    st.subheader("Inserir Produto no Carrinho")
    try:
        if len(banco.produtos) == 0:
            st.info("Nenhum produto disponivel.")
            return

        opcoes = [f"{p.id} - {p.nome} - R${p.preco:.2f}" for p in banco.produtos.values()]
        selecionado = st.selectbox("Selecione o produto", opcoes)
        quantidade = st.number_input("Quantidade", min_value=1, step=1)

        if st.button("Inserir no Carrinho"):
            if quantidade <= 0:
                raise ErroQuantidadeInvalida("A quantidade deve ser maior que zero.")

            id_produto = int(selecionado.split(" - ")[0])
            produto = banco.produtos.get(id_produto)

            if produto.quantidade == 0:
                raise ErroEstoqueInsuficiente(f"Produto {produto.nome} esta sem estoque.")

            for item in cliente.carrinho:
                if item.produto.id == produto.id:
                    item.quantidade += quantidade
                    st.success("Quantidade atualizada no carrinho!")
                    return

            novo_item = ItemCarrinho(produto, quantidade)
            cliente.carrinho.append(novo_item)
            st.success("Produto inserido no carrinho!")

    except ErroQuantidadeInvalida as e:
        st.error(f"Quantidade invalida: {str(e)}")
    except ErroEstoqueInsuficiente as e:
        st.error(f"Estoque insuficiente: {str(e)}")
    except ErroValidacao as e:
        st.error(str(e))

def visualizar_carrinho(cliente):
    st.subheader("Seu Carrinho")
    try:
        if len(cliente.carrinho) == 0:
            st.info("Carrinho vazio.")
            return

        itens = [
            {
                "Produto": item.produto.nome,
                "Preco Unitario": f"R${item.produto.preco:.2f}",
                "Quantidade": item.quantidade,
                "Total": f"R${item.produto.preco * item.quantidade:.2f}"
            }
            for item in cliente.carrinho
        ]
        st.dataframe(itens)
        total = sum(item.produto.preco * item.quantidade for item in cliente.carrinho)
        st.write(f"**Total geral: R${total:.2f}**")

    except ErroValidacao as e:
        st.error(str(e))

def comprar_carrinho(cliente):
    st.subheader("Comprar Carrinho")
    try:
        if len(cliente.carrinho) == 0:
            st.info("Carrinho vazio.")
            return

        visualizar_carrinho(cliente)

        if st.button("Confirmar Compra"):
            for item in cliente.carrinho:
                produto = banco.produtos.get(item.produto.id)
                if item.quantidade > produto.quantidade:
                    raise ErroEstoqueInsuficiente(
                        f"Estoque insuficiente para {produto.nome}. Disponivel: {produto.quantidade}"
                    )

            for item in cliente.carrinho:
                produto = banco.produtos.get(item.produto.id)
                produto.quantidade -= item.quantidade

            id_venda = banco.proximo_id_venda()
            nova_venda = Venda(id_venda, cliente, list(cliente.carrinho))
            banco.vendas.append(nova_venda)
            cliente.compras.append(nova_venda)
            cliente.carrinho = []
            st.success(f"Compra realizada! Total: R${nova_venda.total():.2f}")

    except ErroEstoqueInsuficiente as e:
        st.error(f"Erro no estoque: {str(e)}")
    except ErroValidacao as e:
        st.error(str(e))

def listar_minhas_compras(cliente):
    st.subheader("Minhas Compras")
    try:
        if len(cliente.compras) == 0:
            st.info("Voce ainda nao fez nenhuma compra.")
            return

        for venda in cliente.compras:
            st.write(f"**Venda #{venda.id} | Total: R${venda.total():.2f}**")
            itens = [
                {
                    "Produto": item.produto.nome,
                    "Quantidade": item.quantidade,
                    "Total": f"R${item.produto.preco * item.quantidade:.2f}"
                }
                for item in venda.itens
            ]
            st.dataframe(itens)

    except ErroValidacao as e:
        st.error(str(e))


def area_admin():
    st.sidebar.write(f"Logado como: {st.session_state.usuario.nome}")
    if st.sidebar.button("Sair"):
        st.session_state.usuario = None
        st.session_state.tipo = None
        st.rerun()

    aba = st.tabs(["Listar Vendas", "Gerenciar Produtos", "Promocoes", "Imagens"])

    with aba[0]:
        listar_vendas()
    with aba[1]:
        gerenciar_produtos()
    with aba[2]:
        gerenciar_promocoes()
    with aba[3]:
        gerenciar_imagens()

def listar_vendas():
    st.subheader("Todas as Vendas")
    if len(banco.vendas) == 0:
        st.info("Nenhuma venda realizada ainda.")
        return

    for venda in banco.vendas:
        st.write(f"**Venda #{venda.id} | Cliente: {venda.cliente.nome} | Total: R${venda.total():.2f}**")
        itens = [
            {
                "Produto": item.produto.nome,
                "Quantidade": item.quantidade,
                "Preco Unitario": f"R${item.produto.preco:.2f}",
                "Total": f"R${item.produto.preco * item.quantidade:.2f}"
            }
            for item in venda.itens
        ]
        st.dataframe(itens)
        st.divider()

def gerenciar_produtos():
    st.subheader("Produtos Cadastrados")
    if len(banco.produtos) == 0:
        st.info("Nenhum produto cadastrado.")
        return

    for produto in banco.produtos.values():
        col1, col2 = st.columns([1, 3])
        with col1:
            if produto.imagem is not None:
                st.image(produto.imagem, width=100)
            else:
                st.write("Sem imagem")
        with col2:
            st.write(f"**{produto.nome}**")
            st.write(f"Preco: R${produto.preco:.2f}")
            st.write(f"Quantidade: {produto.quantidade}")
            st.write(f"Categoria: {produto.categoria.nome}")
        st.divider()

def gerenciar_promocoes():
    st.subheader("Controle de Promocoes")
    aba = st.tabs(["Definir Promocao", "Produtos em Promocao"])

    with aba[0]:
        definir_promocao()
    with aba[1]:
        listar_promocoes()

def gerenciar_imagens():
    st.subheader("Gerenciar Imagens dos Produtos")

    if len(banco.produtos) == 0:
        st.info("Nenhum produto cadastrado.")
        return

    opcoes = [f"{p.id} - {p.nome}" for p in banco.produtos.values()]
    selecionado = st.selectbox("Selecione o produto", opcoes, key="select_imagem")
    imagem = st.file_uploader("Escolha uma imagem", type=["png", "jpg", "jpeg"])

    if st.button("Salvar Imagem"):
        try:
            if imagem is None:
                raise ErroValidacao("Selecione uma imagem.")
            id_produto = int(selecionado.split(" - ")[0])
            produto = banco.produtos.get(id_produto)
            produto.imagem = imagem.read()
            st.success(f"Imagem atualizada para {produto.nome}!")
        except ErroValidacao as e:
            st.error(str(e))

    st.divider()
    st.subheader("Imagens Atuais")
    for produto in banco.produtos.values():
        col1, col2 = st.columns([1, 3])
        with col1:
            if produto.imagem is not None:
                st.image(produto.imagem, width=80)
            else:
                st.write("Sem imagem")
        with col2:
            st.write(f"**{produto.nome}**")
        st.divider()

def definir_promocao():
    categorias = list(banco.categorias.values())
    if len(categorias) == 0:
        st.info("Nenhuma categoria cadastrada.")
        return

    opcoes = [f"{c.id} - {c.nome}" for c in categorias]
    selecionado = st.selectbox("Selecione a categoria", opcoes)
    desconto = st.number_input("Percentual de desconto (%)", min_value=1, max_value=100, step=1)
    inicio = st.date_input("Inicio da promocao", value=date.today())
    fim = st.date_input("Fim da promocao", value=date.today())

    if st.button("Ativar Promocao"):
        try:
            if fim < inicio:
                raise ErroValidacao("A data de fim deve ser maior que a data de inicio.")
            id_cat = int(selecionado.split(" - ")[0])
            categoria = banco.categorias.get(id_cat)
            categoria.promocao_ativa = True
            categoria.desconto = desconto
            categoria.inicio_promocao = inicio
            categoria.fim_promocao = fim
            st.success(f"Promocao de {desconto}% ativada para {categoria.nome} ate {fim}!")
        except ErroValidacao as e:
            st.error(str(e))

    if st.button("Desativar Promocao"):
        id_cat = int(selecionado.split(" - ")[0])
        categoria = banco.categorias.get(id_cat)
        categoria.promocao_ativa = False
        categoria.desconto = 0
        st.success(f"Promocao desativada para {categoria.nome}!")

def listar_promocoes():
    produtos_promocao = [p for p in banco.produtos.values() if p.categoria.promocao_ativa]

    if len(produtos_promocao) == 0:
        st.info("Nenhum produto em promocao no momento.")
        return

    for produto in produtos_promocao:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(f"**{produto.nome}**")
            st.write(f"Categoria: {produto.categoria.nome}")
            st.write(f"Preco original: R${produto.preco:.2f}")
            st.write(f"Desconto: {produto.categoria.desconto}%")
        with col2:
            st.metric("Preco com desconto", f"R${produto.preco_com_desconto():.2f}")
        st.divider()


inicializar_sessao()

if st.session_state.usuario is None:
    tela_inicial()
elif st.session_state.tipo == "cliente":
    area_cliente()
elif st.session_state.tipo == "admin":
    area_admin()