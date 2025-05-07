import streamlit as st
import os
from dotenv import load_dotenv
from supabase import create_client
import pandas as pd
import matplotlib.pyplot as plt

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Cria o cliente Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def pagina_login():
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

def cadastro():
    st.title("🐶 Cadastro de Animais - Canil Municipal")
    # --- FORMULÁRIO DE CADASTRO ---
    st.subheader("Cadastrar novo animal")
        
    with st.form("form_cadastro"):
        nome = st.text_input("Nome")
        especie = st.selectbox("Espécie", ["Cachorro", "Gato"])
        raca = st.text_input("Raça")
        porte = st.selectbox("Porte", ["Pequeno", "Médio", "Grande"])
        sexo = st.selectbox("Sexo", ["M", "F"])
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

def pagina_func_volun():   
        st.subheader("Cadastrar voluntário")

        with st.form("form_cadastro_voluntario"):
            nome = st.text_input("Nome")
            contato = st.text_input("Contato")
            areaatuacao = st.text_input("Área de atuação")
            cadastrarvoluntario = st.form_submit_button("Cadastrar Voluntário")

            if cadastrarvoluntario:
                dados = {
                    "nome": nome,
                    "contato": contato,
                    "areaatuacao": areaatuacao
                }
                supabase.table("voluntarios").insert(dados).execute()
                st.success("Voluntário cadastrado com sucesso!")

        st.subheader("Cadastrar Funcionário")

        with st.form("form_funcionario"):
            nome = st.text_input("Nome")
            cargo = st.text_input("Cargo")
            telefone = st.text_input("Telefone")
            email = st.text_input("Email")
            cadastrarfuncionario = st.form_submit_button("Cadastrar Funcionário")

            if cadastrarfuncionario:
                dados = {
                    "nome": nome,
                    "cargo": cargo,
                    "telefone": telefone,
                    "email": email
                }
                supabase.table("funcionarios").insert(dados).execute()
                st.success("Funcionário cadastrado com sucesso!")

def pagina_listagem():
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

    # Painel de Indicadores
    st.subheader("📊 Painel de Indicadores")
    dados = supabase.table("animais").select("*").execute().data
    total = len(dados)
    adotados = len([a for a in dados if a.get("status", "").lower() == "adotado"])
    media_idade = sum([a["idade"] for a in dados]) / total if total > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de animais", total)
    col2.metric("Adotados", adotados)
    col3.metric("Idade média", f"{media_idade:.1f} anos")

def pagina_tratamento():
    st.subheader("Registrar Tratamento")

    # Buscar animais para associar
    animais_data = supabase.table("animais").select("id", "nome").execute().data
    opcoes_animais = {f'{a["nome"]} (ID: {a["id"]})': a["id"] for a in animais_data}

    with st.form("form_tratamento"):
        animal_escolhido = st.selectbox("Animal", list(opcoes_animais.keys()))
        descricao = st.text_area("Descrição do tratamento")
        datainicio = st.date_input("Data de início")
        datafim = st.date_input("Data de término")
        registrar = st.form_submit_button("Registrar Tratamento")

        if registrar:
            tratamento = {
                "animalid": opcoes_animais[animal_escolhido],
                "descricao": descricao,
                "datainicio": str(datainicio),
                "datafim": str(datafim)
            }
            supabase.table("tratamentos").insert(tratamento).execute()
            st.success("Tratamento registrado com sucesso!")

    st.subheader("Tratamentos Registrados")
    tratamentos_data = supabase.table("tratamentos").select("*").execute().data

    if tratamentos_data:
        df_trat = pd.DataFrame(tratamentos_data)
        st.dataframe(df_trat)
    else:
        st.info("Nenhum tratamento registrado ainda.")

def pagina_doacoes():
    st.subheader("Registrar Doação")

    voluntarios_data = supabase.table("voluntarios").select("id").execute().data
    opcoes_voluntarios = {f'{a["id"]}': a["id"] for a in voluntarios_data}
    
    with st.form("form_doacao"):
        voluntarioid = st.selectbox("Voluntário", list(opcoes_voluntarios.keys()))
        tipo = st.selectbox("Tipo de doação", ["Ração", "Remédio", "Dinheiro", "Outros"])
        item = st.text_input("Item")
        quantidade = st.number_input("Quantidade", min_value=0, max_value=30, step=1)
        datadoacao = st.date_input("Data da doação")
        doar = st.form_submit_button("Registrar Doação")

        if doar:
            dados_doacao = {
                "voluntarioid": voluntarioid,
                "tipo": tipo,
                "item": item,
                "quantidade": quantidade,
                "datadoacao": str(datadoacao)
            }
            supabase.table("doacoes").insert(dados_doacao).execute()
            estoque = supabase.table("estoque").select("*").eq("tipo", tipo).execute().data
            st.success("Doação registrada com sucesso!")

    st.subheader("Doações Registradas")
    doacoes = supabase.table("doacoes").select("*").execute().data
    if doacoes:
        df_doacoes = pd.DataFrame(doacoes)
        st.dataframe(df_doacoes)
    else:
        st.info("Nenhuma doação registrada.")

def pagina_vacinas():
    st.subheader("Cadastrar Nova Vacina")

    with st.form("form_vacina"):
        nome_vacina = st.text_input("Nome da vacina")
        fabricante = st.text_input("Fabricante (opcional)")
        cadastrar_vacina = st.form_submit_button("Cadastrar Vacina")

        if cadastrar_vacina:
            supabase.table("vacinas").insert({
                "nome": nome_vacina,
                "fabricante": fabricante
            }).execute()
            st.success("Vacina cadastrada com sucesso!")

    st.subheader("Registrar Vacinação")

    # Obter lista de animais e vacinas
    animais = supabase.table("animais").select("id", "nome").execute().data
    vacinas = supabase.table("vacinas").select("id", "nome").execute().data

    if animais and vacinas:
        nome_animal = st.selectbox("Animal", [f'{a["id"]} - {a["nome"]}' for a in animais])
        id_animal = int(nome_animal.split(" - ")[0])
        nome_vacina = st.selectbox("Vacina", [f'{v["id"]} - {v["nome"]}' for v in vacinas])
        id_vacina = int(nome_vacina.split(" - ")[0])
        data_aplicacao = st.date_input("Data da aplicação")
        registrar = st.button("Registrar vacinação")

        if registrar:
            supabase.table("vacinacoes").insert({
                "animalid": id_animal,
                "vacinaid": id_vacina,
                "dataaplicacao": str(data_aplicacao)
            }).execute()
            st.success("Vacinação registrada com sucesso!")
    else:
        st.info("Cadastre animais e vacinas antes de registrar uma vacinação.")

def pagina_resgates():
    st.subheader("Registrar Resgate de Animal")
    # Buscar lista de animais
    animais = supabase.table("animais").select("id", "nome").execute().data

    if animais:
        animal_escolhido = st.selectbox("Animal resgatado", [f'{a["id"]} - {a["nome"]}' for a in animais])
        animal_id = int(animal_escolhido.split(" - ")[0])
        localresgate = st.text_input("Local do resgate")
        dataresgate = st.date_input("Data do resgate")
        responsavel = st.text_input("Responsável")
        registrar = st.button("Registrar resgate")

        if registrar:
            dados = {
                "animalid": animal_id,
                "dataresgate": str(dataresgate),
                "localresgate": localresgate,
                "responsavel": responsavel
            }
            supabase.table("resgates").insert(dados).execute()
            st.success("Resgate registrado com sucesso!")
    else:
        st.info("Cadastre animais antes de registrar resgates.")

def pagina_adocao():
    st.subheader("Dar baixa em animal adotado")

    # Busca os animais disponíveis
    resposta = supabase.table("animais").select("*").eq("status", "Disponível").execute()
    animais_disponiveis = resposta.data

    if not animais_disponiveis:
        st.info("Nenhum animal disponível para adoção.")

    # Lista os nomes dos animais para seleção
    nomes_animais = [f"{a['id']} - {a['nome']}" for a in animais_disponiveis]
    escolha = st.selectbox("Selecione o animal adotado:", nomes_animais)

    if st.button("Dar baixa como adotado"):
        animal_id = int(escolha.split(" - ")[0])  # extrai o ID
        try:
            supabase.table("animais").update({"status": "Adotado"}).eq("id", animal_id).execute()
            st.success("Animal marcado como adotado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao atualizar status: {e}")
    