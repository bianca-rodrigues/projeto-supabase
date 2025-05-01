import os
from dotenv import load_dotenv
from supabase import create_client

# Carrega as variáveis do arquivo .env
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Cria o cliente Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Função para listar todos os animais
def listar_animais():
    resposta = supabase.table("animais").select("*").execute()
    print("Animais cadastrados:")
    print(resposta.data)

# Função para cadastrar um novo animal
def cadastrar_animal(nome, especie, raca, porte, sexo, idade, cor, dataentrada, status):
    novo = {
        "nome": nome,
        "especie": especie,
        "raca": raca,
        "porte": porte,
        "sexo": sexo,
        "idade": idade,
        "cor": cor,
        "dataentrada": dataentrada,
        "status": False
    }
    resposta = supabase.table("animais").insert(novo).execute()
    print("Animal cadastrado:")
    print(resposta.data)

# Função para atualizar um animal para 'adotado'
def marcar_como_adotado(id_animal):
    resposta = supabase.table("animais").update({"adotado": True}).eq("id", id_animal).execute()
    print("Animal atualizado:")
    print(resposta.data)

# Função para deletar um animal por ID
def deletar_animal(id_animal):
    resposta = supabase.table("animais").delete().eq("id", id_animal).execute()
    print("Animal removido:")
    print(resposta.data)

    # Criar usuário
res = supabase.auth.sign_up({
    "email": "aluno@teste.com",
    "password": "senha_segura123"
})
print(res)

# Login
res = supabase.auth.sign_in_with_password({
    "email": "aluno@teste.com",
    "password": "senha_segura123"
})
print(res)
