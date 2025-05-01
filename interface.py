import streamlit as st
from dotenv import load_dotenv
from supabase import create_client
import os
import pandas as pd
import matplotlib.pyplot as plt

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

st.title("🐶 Cadastro de Animais - Canil Municipal")

# --- FORMULÁRIO DE CADASTRO ---
st.subheader("Cadastrar novo animal")

with st.form("form_cadastro"):
    nome = st.text_input("Nome")
    especie = st.selectbox("Espécie", ["Cachorro", "Gato"])
    raca = st.text_input("Raça")
    porte = st.selectbox("Porte", ["Pequeno", "Médio", "Grande"])
    sexo = st.selectbox("Sexo", ["Macho", "Fêmea"])
    idade = st.number_input("Idade", min_value=0, max_value=30, step=1)
    cor = st.text_input("Cor")
    dataentrada = st.date_input("Data de entrada")
    status = st.selectbox("Status", ["Disponível", "Adotado"])
    cadastrar = st.form_submit_button("Cadastrar")

    if cadastrar:
        dados = {
            "nome": nome,
            "especie": especie,
            "raca": raca,
            "porte": porte,
            "sexo": sexo,
            "idade": idade,
            "cor": cor,
            "dataentrada": str(dataentrada),
            "status": status
        }
        supabase.table("animais").insert(dados).execute()
        st.success("Animal cadastrado com sucesso!")

# --- LISTAGEM DE ANIMAIS ---
st.subheader("Animais Cadastrados")
dados = supabase.table("animais").select("*").execute()
animais = dados.data

if animais:
    especies = list(set([a["especie"] for a in animais]))
    escolha = st.selectbox("Filtrar por espécie", ["Todas"] + especies)
    filtrados = [a for a in animais if escolha == "Todas" or a["especie"] == escolha]
    df = pd.DataFrame(filtrados)
    st.dataframe(df)

    contagem = df["especie"].value_counts()
    fig, ax = plt.subplots()
    contagem.plot(kind="bar", ax=ax)
    ax.set_ylabel("Quantidade")
    ax.set_title("Animais por Espécie")
    st.pyplot(fig)
else:
    st.warning("Nenhum animal cadastrado.")

# --- LOGIN ---
st.subheader("Login de usuário")
email = st.text_input("Email")
senha = st.text_input("Senha", type="password")

if st.button("Entrar"):
    try:
        user = supabase.auth.sign_in_with_password({
            "email": email,
            "password": senha
        })
        st.success(f"Bem-vindo, {email}!")
        st.session_state['usuario'] = email
    except Exception:
        st.error("Login inválido")

# --- CRIAR NOVA CONTA --- 
st.subheader("🔐 Criar nova conta")

with st.form("form_signup"):
    novo_email = st.text_input("Novo email", key="signup_email")
    nova_senha = st.text_input("Nova senha", type="password", key="signup_senha")
    confirmar = st.text_input("Confirmar senha", type="password", key="signup_confirma")
    criar = st.form_submit_button("Criar conta")

    if criar:
        if not novo_email or not nova_senha or not confirmar:
            st.warning("Preencha todos os campos.")
        elif nova_senha != confirmar:
            st.error("As senhas não coincidem.")
        else:
            try:
                res = supabase.auth.sign_up({
                    "email": novo_email,
                    "password": nova_senha
                })
                st.success("Conta criada com sucesso! Faça login acima.")
            except Exception as e:
                st.error(f"Erro ao criar conta: {e}")

# --- PAINEL APÓS LOGIN ---
if "usuario" in st.session_state:
    st.subheader("Painel de Indicadores")
    dados = supabase.table("animais").select("*").execute().data
    total = len(dados)
    adotados = len([a for a in dados if a.get("status", "").lower() == "adotado"])
    media_idade = sum([a["idade"] for a in dados]) / total if total > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de animais", total)
    col2.metric("Adotados", adotados)
    col3.metric("Idade média", f"{media_idade:.1f} anos")
else:
    st.info("Faça login para visualizar indicadores.")
