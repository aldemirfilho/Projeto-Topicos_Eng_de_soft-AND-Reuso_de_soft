import streamlit as st
from produtos_db import products
from users import User


st.session_state.setdefault("cart_items", [])
st.session_state.setdefault("order_history", [])
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("users", [])
st.session_state.setdefault("page", "home")


def show_products(products):
    for product in products:
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 3, 1, 1])
            with col1:
                if product["image_url"]:
                    st.image(product["image_url"], width=150) 
                else:
                    st.image("https://via.placeholder.com/150", width=150)
            with col2:
                st.subheader(product["name"])
                st.write(product["description"])
            with col3:
                st.subheader("R$ {:.2f}".format(product["price"]))
                quantity = st.number_input(f"Quantidade de '{product['name']}'",
                                           min_value=1, max_value=100, value=1)
            with col4:
                if st.button("Adicionar ao Carrinho", key=f"add_{product['name']}"):
                    cart_item = {"product": product, "quantity": quantity}
                    cart_items = st.session_state.get("cart_items", [])
                    cart_items.append(cart_item)
                    st.session_state["cart_items"] = cart_items
                    st.success("Produto adicionado ao carrinho!")
                    quantity = 1  # redefinir a quantidade para 1 após a adição
                    st.experimental_rerun()

        st.write("-----")

def show_order_history():
    order_history = st.session_state.get("order_history", [])
    st.sidebar.subheader("Histórico de Pedidos")
    if not order_history:
        st.sidebar.write("Nenhum pedido realizado.")
    else:
        for order in order_history:
            st.sidebar.write(f"Data do pedido: {order['date']}")
            st.sidebar.write("Produtos:")
            for item in order['cart_items']:
                st.sidebar.write(f"- {item['quantity']} x {item['product']['name']} - R$ {item['product']['price']}")
            st.sidebar.write(f"Total: R$ {order['total_price']}")
            st.sidebar.write("---")



import datetime

def save_order_history():
    cart_items = st.session_state.get("cart_items", [])
    if cart_items:
        order_history = st.session_state.get("order_history", [])
        total_price = sum([item["product"]["price"] * item["quantity"] for item in cart_items])
        order = {"date": datetime.datetime.now(), "cart_items": cart_items, "total_price": total_price}
        order_history.append(order)
        st.session_state["order_history"] = order_history
        st.session_state["cart_items"] = []

def show_cart():
    cart_items = st.session_state.get("cart_items", [])
    total_price = sum([item["product"]["price"] * item["quantity"] for item in cart_items])

    st.sidebar.subheader("Carrinho de compras")
    if not cart_items:
        st.sidebar.write("Seu carrinho está vazio.")
    else:
        for index, item in enumerate(cart_items):
            col1, col2, col3, col4 = st.sidebar.columns([2, 1, 1, 1])
            with col1:
                st.write(item["product"]["name"])
            with col2:
                quantity = st.number_input("Quantidade", value=item["quantity"], min_value=1, key=f"quantity_{index}")
                cart_items[index]["quantity"] = quantity
                st.write(quantity)
            with col3:
                st.write("R$ {:.2f}".format(item["product"]["price"] * item["quantity"]))
            with col4:
                if st.button("Remover", key=f"remove_{index}"):
                    cart_items.pop(index)
                    st.session_state["cart_items"] = cart_items
                    st.success("Produto removido do carrinho com sucesso!")
                    st.experimental_rerun()

        st.sidebar.write("---")
        st.sidebar.subheader("Total: R$ {:.2f}".format(total_price))

        st.sidebar.write("---")
        if st.sidebar.button("Limpar carrinho"):
            st.session_state["cart_items"] = []
            st.info("Carrinho limpo com sucesso!")
            st.experimental_rerun()

        st.sidebar.write("---")
        st.sidebar.subheader("Pagamento")
        options = ["Boleto", "Pix", "Crédito"]
        payment_method = st.sidebar.selectbox("Escolha o método de pagamento:", options)
        st.sidebar.write("---")
        st.sidebar.subheader("Endereço de entrega")
        delivery_address = st.sidebar.text_input("Digite o endereço de entrega:")
        if st.sidebar.button("Finalizar Compra"):
            save_order_history()
            cart_items = st.session_state.get("cart_items", [])
            if cart_items:
                orders = st.session_state.get("orders", [])
                orders.append(cart_items)
                st.session_state["orders"] = orders
                st.success("Compra finalizada com sucesso! Obrigado pela preferência.")
                st.session_state["cart_items"] = []
                st.experimental_rerun()
            else:
                st.warning("Seu carrinho está vazio. Adicione alguns itens antes de finalizar a compra.")
                st.experimental_rerun()




def main():
    st.set_page_config(page_title="E-commerce de tecnologia", page_icon=":computer:", layout="wide")
    
    st.markdown(
        """
        <div style='display: flex; justify-content: center; align-items: center; flex-direction: column;'>
            <img src='https://marketplace.canva.com/EAFDI4MVBvY/1/0/1600w/canva-logotipo-gaming-e-tecnologia-e-sports-ilustra%C3%A7%C3%A3o-verde-escuro-e-verde-neon-G2iq5Js0QFI.jpg' width='300'/>
            <h1 style='text-align: center; font-family: Arial, sans-serif; color: #006666; font-size: 48px; margin-top: 16px; margin-bottom: 32px;'>Aldarsan<span style='color: #00cc99;'>TECH</span></h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    categories = ["Todas as categorias", "Smartphones", "Notebooks", "PCs", "Acessórios"]
    form_submitted = False
    
    if st.session_state.get("page",) == "register":
        #session_users = st.session_state.get("users", [])
        st.session_state["users"] , form_submitted  = User.register_user(st.session_state.get("users", []), form_submitted)
    if form_submitted:
        st.session_state["page"] = "home"
        st.experimental_rerun()
    
    if st.session_state.get("page",) == "login":
        st.session_state["logged_in"] = User.login_user(st.session_state.get("users", []), st.session_state.get("logged_in",))
        
    if st.session_state.get("logged_in", True):
        st.session_state["page"] = "home"
        st.sidebar.button("Histórico de Pedidos", on_click=show_order_history)
        show_cart()
        if st.sidebar.button("Logout"):
            st.session_state["logged_in"] = False
            st.success("Logout realizado com sucesso!")
            st.experimental_rerun()
    else:
        if st.sidebar.button("Registrar-se"):
            st.session_state["page"] = "register"
            st.experimental_rerun()

        if st.sidebar.button("Entrar"):
            st.session_state["page"] = "login"
            st.experimental_rerun()
    
    selected_category = st.selectbox("Selecione a categoria", categories)

    if selected_category == "Todas as categorias":
        filtered_products = products
    else:
        filtered_products = [product for product in products if product["category"].lower() == selected_category.lower()]

    search_term = st.session_state.get("search_term", "")
    if search_term:
        filtered_products = [product for product in filtered_products if search_term.lower() in product["name"].lower()]
        st.session_state["selected_category"] = "Todas as categorias"

    st.write("### Produtos")

    # Adicionando barra de pesquisa
    search_term = st.text_input("Pesquisar", search_term)
    st.session_state["search_term"] = search_term

    st.write(f"Resultados para '{search_term}':")
    
    show_products(filtered_products)
    
if __name__ == "__main__":
    main()
