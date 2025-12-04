# 🧬 Projeto: Geração e Anonimização de Dados — Perfil Estefânia

Este projeto demonstra a criação, anonimização e agrupamento de dados sintéticos baseados em um perfil específico (Estefânia), utilizando **Python**, **Faker**, **Pandas** e **Jupyter Notebook**.  
Ele foi desenvolvido como um exercício de **anonimização de dados pessoais** e **simulação de perfis similares**, explorando etapas de pseudonimização e filtragem de registros com base em critérios definidos.

---

## 📘 Estrutura do Projeto

```

📂 projeto_estefania/
├── 📓 script_integrado_estefania.ipynb   ← Notebook principal
├── 📁 dados_anonimizados/                ← Saída com CSVs gerados (20 registros cada)
├── 📁 agrupamentos/                      ← Saída com agrupamentos filtrados (perfil Estefânia)
├── 📄 README.md                          ← Este arquivo de documentação

````

---

## ⚙️ Objetivo

Gerar **10 conjuntos de dados** contendo informações aleatórias de vacinação, incluindo:
- 1 registro base da Estefânia,
- 5 registros similares ao perfil dela,
- 14 registros completamente aleatórios.

Em seguida, o notebook aplica uma **etapa de anonimização** (pseudonimização dos nomes) e executa um **filtro de agrupamento** para identificar registros compatíveis com o perfil da Estefânia.

---

## 🧩 Tecnologias Utilizadas

- ![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white) **Python 3.8+**
- ![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white) **Pandas** → manipulação e filtragem de dados tabulares
- ![Faker](https://img.shields.io/badge/Faker-pt__BR-orange?logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMTIgMEM1LjM3IDAgMCA1LjM3IDAgMTJDMCAxOC42MyA1LjM3IDI0IDEyIDI0QzE4LjYzIDI0IDI0IDE4LjYzIDI0IDEyQzI0IDUuMzcgMTguNjMgMCAxMiAwWk0xMiAyMkM2LjQ4IDIyIDIgMTcuNTIgMiAxMkMyIDYuNDggNi40OCAyIDEyIDJDMTcuNTIgMiAyMiA2LjQ4IDIyIDEyQzIyIDE3LjUyIDE3LjUyIDIyIDEyIDIyWk0xMyAxN0gxMVYxNUgxM1YxN1pNMTMgMTJIMTFWN0gxM1YxMlpNMTMgNUgxMVYzSDEzVjVaIiBmaWxsPSJ3aGl0ZSIvPjwvc3ZnPg==) **Faker (pt_BR)** → geração de dados sintéticos realistas
- ![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white) **Jupyter Notebook** → execução passo a passo e análise interativa


---

## 📦 Instalação e Configuração do Ambiente

### 1️⃣ Crie e ative um ambiente virtual (recomendado)
```bash
# Criar o ambiente
python -m venv venv

# Ativar no Windows
venv\Scripts\activate

# Ativar no macOS/Linux
source venv/bin/activate

# Instalar Jupyter Notebook
pip install notebook
````

### 2️⃣ Inicie o Jupyter Notebook

```bash
jupyter notebook
```

O navegador será aberto automaticamente mostrando o painel de controle do Jupyter.

---

## 🚀 Execução do Notebook

1. Abra o arquivo **`script_integrado_estefania.ipynb`** no Jupyter.

2. Execute as células **em ordem**, do início ao fim, usando:

   * Menu: **Kernel → Restart & Run All**, ou
   * Atalho: **Ctrl + Enter** (executa célula atual)
     **Shift + Enter** (executa e avança para a próxima)

3. O notebook irá:

   * Criar as pastas `dados_anonimizados/` e `agrupamentos/`
   * Gerar 10 arquivos CSV com 20 registros cada (anônimos)
   * Filtrar e salvar os grupos que coincidem com o perfil da Estefânia

---

## 🧠 Lógica do Projeto

### 1️⃣ Geração de Dados Sintéticos

Utiliza o pacote `faker` (localização `pt_BR`) para criar pessoas com nome, idade, sexo, data e local de vacinação.
A Estefânia é definida manualmente com informações fixas, enquanto os demais registros são aleatórios.

### 2️⃣ Anonimização (Pseudonimização)

Os nomes reais são substituídos por identificadores genéricos:

```
Pessoa_1, Pessoa_2, Pessoa_3, ...
```

A Estefânia é sempre **Pessoa_1** em todos os arquivos, preservando o vínculo lógico sem revelar identidade.

### 3️⃣ Agrupamento (Filtragem)

É aplicado um filtro com base em critérios predefinidos:

| Critério           | Valor          |
| ------------------ | -------------- |
| Idade              | 20–30 anos     |
| Sexo               | Feminino (`F`) |
| Tomou vacina       | Sim            |
| Mês de vacinação   | Fevereiro (2)  |
| Ano de vacinação   | 2021           |
| Local de vacinação | UBS Centro     |

Os registros que atendem a **todas** essas condições são exportados para a pasta `agrupamentos/`.

---

## 📁 Saídas Geradas

Após a execução completa, você terá duas pastas:

```
📁 dados_anonimizados/
 ├── dados_anon_1.csv
 ├── dados_anon_2.csv
 ├── ...
 └── dados_anon_10.csv

📁 agrupamentos/
 ├── grupo_estefania_1.csv
 ├── grupo_estefania_2.csv
 ├── ...
 └── grupo_estefania_10.csv
```

Cada arquivo em `agrupamentos/` contém **apenas** as linhas compatíveis com o perfil da Estefânia.
Caso nenhum registro atenda aos critérios, o CSV ainda será criado, mas vazio.

---

## 🔍 Exemplo de Visualização no Notebook

Após a execução, você pode inspecionar os resultados diretamente com:

```python
import pandas as pd

df = pd.read_csv("agrupamentos/grupo_estefania_1.csv")
df.head()
```

Isso exibirá as primeiras linhas do grupo identificado no **arquivo 1**.

---

## 💡 Observações Importantes

* O projeto é **totalmente sintético** (nenhum dado real é utilizado).
* As datas e nomes são **gerados aleatoriamente** em cada execução.
* O processo garante **reprodutibilidade** e **anonimização completa**.
* Pode ser adaptado facilmente para outros perfis ou critérios de filtragem.

---

## ✍️ Autores

**Projeto desenvolvido por:**

<div align="center">

| [<img src="https://avatars.githubusercontent.com/u/98980071" width=115><br><sub>Victor Cardoso</sub>](https://github.com/vek03) | [<img src="https://avatars.githubusercontent.com/u/99426563" width=115><br><sub>Júlio Neves</sub>](https://github.com/juliosn) | [<img src="https://media.licdn.com/dms/image/v2/D4E03AQE5Io8F_zO-yg/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1728952801590?e=2147483647&v=beta&t=eNaTOIkCqpNOEqECVg35Vr7nv4ok8TRkHpwHP44YS3s" width=115><br><sub>Gabriel Mendes</sub>](https://github.com/gabrielMendes21) |
| :---: | :---: | :---: |

</div>

---
