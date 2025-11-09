# script_integrado_estefania.py
import os
import random
from datetime import date
import pandas as pd
from faker import Faker

# Configura Faker
fake = Faker('pt_BR')

# Cria pasta de saída
os.makedirs("dados_anonimizados", exist_ok=True)
os.makedirs("agrupamentos", exist_ok=True)


# Perfil fixo da Estefânia
estefania = {
    "nome": "Estefânia",
    "idade": 25,
    "sexo": "F",
    "tomou_vacina": "Sim",
    "data_vacinacao": "2021-02-16",
    "local_vacinacao": "UBS Centro"
}

# Função para gerar uma pessoa aleatória
def gerar_pessoa():
    sexo = random.choice(["M", "F"])
    nome = fake.first_name_female() if sexo == "F" else fake.first_name_male()
    return {
        "nome": nome,
        "idade": random.randint(18, 80),
        "sexo": sexo,
        "tomou_vacina": random.choice(["Sim", "Não"]),
        "data_vacinacao": fake.date_between(start_date=date(2021, 1, 1), end_date=date(2021, 12, 31)).isoformat(),
        "local_vacinacao": random.choice(["UBS Norte", "UBS Sul", "UBS Centro", "UBS Leste", "UBS Oeste"])
    }

# Função para gerar registros similares à Estefânia
def gerar_registros_estefania(quantidade=5):
    rng = random.Random()
    registros = []
    for _ in range(quantidade):
        registros.append({
            "nome": "Estefânia",
            "idade": rng.randint(20, 30),  # idade aleatória entre 20 e 30
            "sexo": "F",
            "tomou_vacina": "Sim",
            "data_vacinacao": fake.date_between(start_date=date(2021, 2, 1), end_date=date(2021, 2, 28)).isoformat(),
            "local_vacinacao": "UBS Centro"
        })
    return registros

# Gera 10 arquivos CSV
for i in range(1, 11):
    filename_csv = f"dados_anonimizados/dados_anon_{i}.csv"
    
    # 1 registro da Estefânia + 5 similares + 14 aleatórios = 20 registros
    pessoas = [estefania] + gerar_registros_estefania(5) + [gerar_pessoa() for _ in range(14)]
    
    # Cria DataFrame
    df = pd.DataFrame(pessoas)
    
    # ----------------------
    # Etapa de anonimização
    # ----------------------
    
    # Pseudonimiza os nomes
    df["nome"] = [f"Pessoa_{j+1}" for j in range(len(df))]
    
    # Força Estefânia como Pessoa_1
    df.loc[0, "nome"] = "Pessoa_1"
    
    # Salva CSV anonimizado
    df.to_csv(filename_csv, index=False, encoding="utf-8")
    
    print(f"✅ Arquivo {filename_csv} criado com sucesso! Estefânia é Pessoa_1")


# ------------------------------
# PARTE 2: AGRUPAMENTO DE ESTEFÂNIA
# ------------------------------

def agrupar_registros_estefania(arquivo_entrada, arquivo_saida):
    try:
        df = pd.read_csv(arquivo_entrada)
    except FileNotFoundError:
        print(f"⚠️ Arquivo não encontrado: {arquivo_entrada}")
        return
    
    criterios_estefania = {
        "idade": (20,30),
        "sexo": "F",
        "tomou_vacina": "Sim",
        "mes_vacinacao": 2,
        "ano_vacinacao": 2021,
        "local_vacinacao": "UBS Centro"
    }
    
    df["data_vacinacao"] = pd.to_datetime(df["data_vacinacao"], errors='coerce')
    
    filtro = (
        (df["idade"].between(*criterios_estefania["idade"])) &
        (df["sexo"] == criterios_estefania["sexo"]) &
        (df["tomou_vacina"] == criterios_estefania["tomou_vacina"]) &
        (df["data_vacinacao"].dt.month == criterios_estefania["mes_vacinacao"]) &
        (df["data_vacinacao"].dt.year == criterios_estefania["ano_vacinacao"]) &
        (df["local_vacinacao"] == criterios_estefania["local_vacinacao"])
    )
    
    grupo_estefania = df[filtro]
    
    grupo_estefania.to_csv(arquivo_saida, index=False)
    
    if not grupo_estefania.empty:
        print(f"✅ {len(grupo_estefania)} registros coincidem com o perfil da Estefânia em {arquivo_entrada}.")
        print(f"   → Resultado salvo em: {arquivo_saida}")
    else:
        print(f"⚠️ Nenhum registro correspondente encontrado em {arquivo_entrada}.")

def processar_todos_os_arquivos():
    pasta_entrada = "dados_anonimizados"
    pasta_saida = "agrupamentos"
    
    for i in range(1,11):
        arquivo_entrada = os.path.join(pasta_entrada, f"dados_anon_{i}.csv")
        arquivo_saida = os.path.join(pasta_saida, f"grupo_estefania_{i}.csv")
        agrupar_registros_estefania(arquivo_entrada, arquivo_saida)
    
    print("\n✅ Processamento concluído para todos os arquivos!")

if __name__ == "__main__":
    processar_todos_os_arquivos()
