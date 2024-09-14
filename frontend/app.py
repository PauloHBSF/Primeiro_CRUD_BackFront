import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Cadastro de Produtos",
    layout="wide"
)


if 'novo_produto' not in st.session_state:
    st.session_state.novo_produto = False
if 'listar_produtos' not in st.session_state:
    st.session_state.listar_produtos = True
if 'listar_produto' not in st.session_state:
    st.session_state.listar_produto = False
if 'deletar_produto' not in st.session_state:
    st.session_state.deletar_produto = False
if 'atualizar_produto' not in st.session_state:
    st.session_state.atualizar_produto = False


session_dict = {
    'novo_produto': st.session_state.novo_produto,
    'listar_produtos': st.session_state.listar_produtos,
    'listar_produto': st.session_state.listar_produto,
    'deletar_produto': st.session_state.deletar_produto,
    'atualizar_produto': st.session_state.atualizar_produto
}

def change_state(state:str):
    for key in session_dict.keys():
        st.session_state[key] = False
    st.session_state[state] = True


def show_response_message(response):
    if response.status_code == 200:
        st.success("Operação realizada com sucesso!")
    else:
        try:
            data = response.json()
            if "detail" in data:
                if isinstance(data["detail"], list):
                    errors = "\n".join([error["msg"]
                                       for error in data["detail"]])
                    st.error(f"Erro: {errors}")

                else:
                    st.error(f"Erro: {data['detail']}")
        except:
            st.error("Erro desonhecido.")


st.title("Cadastro de Produtos")

c1, c2, c3, c4, c5 = st.columns(spec=5, vertical_alignment='center', gap='small')

with c1:
    st.button("Inserir Produto", on_click=change_state, args=['novo_produto'])

with c2:
    st.button("Visualizar todos os Produtos", on_click=change_state, args=['listar_produtos'])

with c3:
    st.button("Visualizar um Produto", on_click=change_state, args=['listar_produto'])

with c4:
    st.button("Deletar um Produto", on_click=change_state, args=['deletar_produto'])

with c5:
    st.button("Atualizar um Produto", on_click=change_state, args=['atualizar_produto'])


if st.session_state.novo_produto:
    with st.container(border=True):
        with st.form("new_product"):
            name = st.text_input("Nome do Produto")
            description = st.text_area("Descrição do Produto")
            price = st.number_input("Preço", min_value=0.01, format="%f")
            category = st.selectbox(
                "Categoria",
                ["Eletrônico", "Eletrodoméstico", "Móveis", "Roupas", "Calçados"],
            )
            email_fornecedor = st.text_input("Email do Fornecedor")
            submit_button = st.form_submit_button("Adicionar Produto")

            if submit_button:
                response = requests.post(
                    "http://backend:8000/products/",
                    json={
                        "name": name,
                        "description": description,
                        "price": price,
                        "category": category,
                        "supplier_email": email_fornecedor,
                    },
                )
                show_response_message(response)


if st.session_state.listar_produtos:
    with st.container(border=True):
        response = requests.get("http://backend:8000/products/")
        if response.status_code == 200:
            product = response.json()
            
            if product == []:
                st.warning("Ainda não há produtos cadastrados.")
            
            else:
                df = pd.DataFrame(product)
                
                df = df[
                    [
                        "id",
                        "name",
                        "description",
                        "price",
                        "category",
                        "supplier_email",
                        "created_at",
                    ]
                ]

                # Exibe o DataFrame sem o índice
                st.write(df.to_html(index=False, justify='center'), unsafe_allow_html=True)
        else:
            show_response_message(response)


if st.session_state.listar_produto:
    with st.container(border=True):
        get_id = st.number_input("ID do Produto", min_value=1, format="%d")
        if st.button("Buscar Produto"):
            response = requests.get(f"http://backend:8000/product/{get_id}")
            if response.status_code == 200:
                product = response.json()
                df = pd.DataFrame([product])

                df = df[
                    [
                        "id",
                        "name",
                        "description",
                        "price",
                        "category",
                        "supplier_email",
                        "created_at",
                    ]
                ]

                # Exibe o DataFrame sem o índice
                st.write(df.to_html(index=False, justify='center'), unsafe_allow_html=True)
            else:
                show_response_message(response)


if st.session_state.deletar_produto:
    with st.container(border=True):
        delete_id = st.number_input(
            "ID do Produto para Deletar", min_value=1, format="%d")
        if st.button("Deletar Produto"):
            response = requests.delete(
                f"http://backend:8000/product/{delete_id}")
            show_response_message(response)


if st.session_state.atualizar_produto:
    with st.container(border=True):
        with st.form("update_product"):
            update_id = st.number_input(
                "ID do Produto", min_value=1, format="%d")
            new_name = st.text_input("Novo Nome do Produto")
            new_description = st.text_area("Nova Descrição do Produto")
            new_price = st.number_input(
                "Novo Preço",
                min_value=float(0),
                format="%f",
            )
            new_categoria = st.selectbox(
                label = "Nova Categoria",
                options = ["Eletrônico", "Eletrodoméstico", "Móveis", "Roupas", "Calçados"],
                index=None,
                placeholder="Escolha uma opção."
            )
            new_email = st.text_input("Novo Email do Fornecedor")

            update_button = st.form_submit_button("Atualizar Produto")

            if update_button:
                update_data = {}
                if new_name:
                    update_data["name"] = new_name
                if new_description:
                    update_data["description"] = new_description
                if new_price > 0:
                    update_data["price"] = new_price
                if new_email:
                    update_data["supplier_email"] = new_email
                if new_categoria:
                    update_data["category"] = new_categoria

                if update_data:
                    response = requests.put(
                        f"http://backend:8000/product/{update_id}", json=update_data
                    )
                    show_response_message(response)
                else:
                    st.error("Nenhuma informação fornecida para atualização")
