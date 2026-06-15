# 🛒 Sistema de Loja Virtual (E-Commerce)

Uma aplicação de e-commerce completa com interface gráfica baseada em **Streamlit**, desenvolvida em Python utilizando o padrão **DAO (Data Access Object)** para persistência simulada em memória e os conceitos de **Orientação a Objetos (POO)**.

---

## 📌 Sobre o Projeto

O projeto simula o ecossistema de uma loja virtual, dividindo as permissões entre **Clientes** (que podem navegar, gerenciar um carrinho e realizar compras) e **Administradores** (que controlam o estoque, aplicam promoções e visualizam o histórico de vendas).

### 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.x
* **Interface Gráfica:** Streamlit
* **Arquitetura:** Camada de Dados (DAOs), Camada de Modelos (POO) e Camada de Exceções customizadas.

---

## 📐 Arquitetura e Diagrama de Classes (UML)

O projeto adota uma arquitetura em camadas para separar a lógica de negócio da persistência de dados. O padrão DAO foi implementado para isolar o dicionário do "Banco" das regras de manipulação.

### Diagrama Caso de Uso

![Diagrama de Caso de uso](/diagramas/caso%20de%20uso.png)

### Diagrama Modelos

![Diagrama de Modelos](/diagramas/modelos.png)

### Diagrama de View

![Diagrama de View](/diagramas/componentes%20de%20VIEW.png)

---

## 📦 Estrutura do Diretório

```text
├── dados/
│   ├── banco.py          # Simulador de persistência em memória (Dicionários)
│   ├── dao.py            # Classe genérica Data Access Object
│   └── daos.py           # Especializações (UsuarioDAO, ProdutoDAO, etc.)
├── modelos/
│   ├── carrinho.py       # Classe ItemCarrinho
│   ├── produto.py        # Classes Produto e Categoria
│   ├── usuario.py        # Classes Usuario, Cliente e Admin (Herança)
│   └── venda.py          # Classe Venda
├── app.py                # Interface gráfica com Streamlit (Ponto de entrada)
├── excecoes.py           # Tratamento de erros customizados do sistema
└── README.md             # Documentação do projeto
```

## ⚙️ Funcionalidades

### 👤 Área do Cliente
* **Criar Conta e Login:** Cadastro completo com validações e suporte a herança de múltiplos tipos de usuários.
* **Catálogo de Produtos:** Visualização de itens com suporte a imagens, quantidade disponível e preços promocionais.
* **Carrinho Dinâmico:** Adicionar itens, atualizar quantidades e somatório automático do valor total.
* **Validação de Estoque:** Impede a inserção ou finalização de compra caso o estoque do produto seja insuficiente.
* **Histórico de Compras:** Painel para o cliente verificar suas compras finalizadas.

### 👑 Área do Administrador
* **Painel de Vendas:** Monitoramento global de todas as vendas realizadas na plataforma, identificando cliente, itens e faturamento.
* **Gerenciamento de Estoque:** Visualização rápida dos produtos cadastrados e quantidade disponível.
* **Controle de Promoções:** Definição de descontos percentuais aplicados a categorias, com estipulação de datas de início e fim.
* **Upload de Imagens:** Permite atualizar a imagem de qualquer produto cadastrado via upload de arquivo.

---

## 🛡️ Tratamento de Exceções Customizadas

Para garantir a robustez do sistema, foram mapeadas regras de negócio rígidas através de exceções personalizadas:
* `ErroLoginVazio` / `ErroValidacao`: Disparados quando campos obrigatórios estão em branco ou logins são inválidos.
* `ErroQuantidadeInvalida`: Impede o envio de valores menores ou iguais a zero para o carrinho.
* `ErroEstoqueInsuficiente`: Validação de segurança acionada antes de debitar produtos do estoque.