import streamlit as st
from interface import pagina_login, cadastro, pagina_listagem, pagina_resgates, pagina_tratamento, pagina_doacoes, pagina_vacinas, pagina_adocao, pagina_func_volun

menu = st.sidebar.selectbox("Navegar", ["Login", "Cadastro", "Listagem", "Resgates", "Tratamentos", "Doações", "Vacinas", "Adoção", "Cadastro Funcionários", "Sair"])

if menu == "Login":
    pagina_login()
elif menu == "Cadastro":
    if "usuario" in st.session_state:
        cadastro()
    else:
        st.warning("Faça login primeiro.")
elif menu == "Listagem":
    if "usuario" in st.session_state:
        pagina_listagem()
    else:
        st.warning("Faça login primeiro")
elif menu == "Resgates":
    if "usuario" in st.session_state:
        pagina_resgates()
    else:
        st.warning("Faça login primeiro")
elif menu == "Tratamentos":
    if "usuario" in st.session_state:
        pagina_tratamento()
    else:
        st.warning("Faça login primeiro")
elif menu == "Doações":
    if "usuario" in st.session_state:
        pagina_doacoes()
    else:
        st.warning("Faça login primeiro")
elif menu == "Vacinas":
    if "usuario" in st.session_state:
        pagina_vacinas()
    else:
        st.warning("Faça login primeiro")
elif menu == "Adoção":
    if "usuario" in st.session_state:
        pagina_adocao()
    else:
        st.warning("Faça login primeiro")
elif menu == "Cadastro Funcionários":
    if "usuario" in st.session_state:
        pagina_func_volun()
    else:
        st.warning("Faça login primeiro")
elif menu == "Sair":
    if "usuario" in st. session_state:
        st.logout()
    else:
        st.warning("Você não está conectado")