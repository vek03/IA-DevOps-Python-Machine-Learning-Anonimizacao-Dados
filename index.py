import pandas as pd
import numpy as np
import random, math
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.cluster import KMeans
import inspect

K_ANON = 6 
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

DEFAULT_WEIGHTS = {
    'idade': 1.0,
    'sexo': 0.8,
    'tomou_vacina': 0.5,
    'data_vacinacao': 0.7,
    'local_vacinacao': 0.9
}

FIRST_NAMES = ["Ana","Bruno","Carlos","Daniela","Eduardo","Fabiana","Gustavo","Helena","Igor","Julia",
               "Lucas","Mariana","Natália","Otávio","Patrícia","Rafael","Sofia","Tiago","Vanessa"]
LAST_NAMES = ["Almeida","Barros","Castro","Dias","Esteves","Fernandes","Gomes","Henrique",
              "Lopes","Matos","Nogueira","Oliveira","Pereira","Ramos","Silva","Teixeira"]

def parse_date_to_days(series):
    """Converte datas para número de dias desde a menor data."""
    dates = pd.to_datetime(series, errors='coerce')
    min_date = dates.min()
    days = (dates - min_date).dt.days.fillna(-1)
    return days.astype(int), min_date

def generate_pseudonym():
    """Gera um nome falso aleatório."""
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def ensure_k_anonymity_assignments(df, labels, k=K_ANON):
    """Garante que cada cluster tenha pelo menos k registros."""
    df = df.copy()
    df['_cluster'] = labels
    while True:
        counts = df['_cluster'].value_counts()
        small = counts[counts < k]
        if small.empty:
            break
        small_cluster_id = small.idxmin()
        small_idx = df[df['_cluster'] == small_cluster_id].index
        feat_cols = [c for c in df.columns if c.startswith('feat_')]
        centroids = df.groupby('_cluster')[feat_cols].mean()
        c_small = centroids.loc[small_cluster_id].values.reshape(1, -1)
        others = centroids.drop(index=small_cluster_id)
        dists = ((others.values - c_small)**2).sum(axis=1)
        nearest_cluster_id = others.index[dists.argmin()]
        df.loc[small_idx, '_cluster'] = nearest_cluster_id
    return df['_cluster'].values


def microaggregate_and_synthesize(df_input, weights=DEFAULT_WEIGHTS, k=K_ANON, generate_extra=True):
    df = df_input.copy().reset_index(drop=True)
    required = ['nome','idade','sexo','tomou_vacina','data_vacinacao','local_vacinacao']
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Coluna obrigatória ausente: {col}")

    df['tomou_vacina'] = df['tomou_vacina'].map({True:1, False:0, 'True':1, 'False':0, 'SIM':1, 'NÃO':0, 'NAO':0}).fillna(0).astype(int)
    days, min_date = parse_date_to_days(df['data_vacinacao'])
    df['data_vac_days'] = days

    if 'sparse_output' in inspect.signature(OneHotEncoder).parameters:
        ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    else:
        ohe = OneHotEncoder(sparse=False, handle_unknown='ignore')

    cat_data = ohe.fit_transform(df[['sexo','local_vacinacao']].fillna('NA'))
    cat_names = ohe.get_feature_names_out(['sexo','local_vacinacao'])

    numeric = df[['idade','tomou_vacina','data_vac_days']].fillna(-1).values.astype(float)
    scaler = StandardScaler()
    numeric_scaled = scaler.fit_transform(numeric)
    numeric_weighted = numeric_scaled * np.array([
        weights.get('idade',1.0),
        weights.get('tomou_vacina',1.0),
        weights.get('data_vacinacao',1.0)
    ])

    cat_scaled = cat_data.copy()
    sexo_cols = [i for i,c in enumerate(cat_names) if c.startswith('sexo_')]
    local_cols = [i for i,c in enumerate(cat_names) if c.startswith('local_vacinacao_')]
    if sexo_cols:
        cat_scaled[:, sexo_cols] *= (weights.get('sexo',1.0) / max(1, len(sexo_cols)))
    if local_cols:
        cat_scaled[:, local_cols] *= (weights.get('local_vacinacao',1.0) / max(1, len(local_cols)))

    features = np.hstack([numeric_weighted, cat_scaled])
    feat_cols = [f'feat_{i}' for i in range(features.shape[1])]
    feat_df = pd.DataFrame(features, columns=feat_cols)

    n = len(df)
    n_clusters = max(1, n // k)
    kmeans = KMeans(n_clusters=n_clusters, random_state=RANDOM_SEED, n_init=10)
    labels = kmeans.fit_predict(features)

    feat_and_labels = feat_df.copy()
    feat_and_labels.index = df.index
    feat_and_labels['_cluster'] = labels
    merged_labels = ensure_k_anonymity_assignments(pd.concat([feat_and_labels, df], axis=1), labels, k=k)
    df['_cluster'] = merged_labels

    anonymized_rows = []

    for cluster_id, cluster in df.groupby('_cluster'):
        size = len(cluster)

        mean_idade = int(round(cluster['idade'].mean()))
        valid_days = cluster['data_vac_days'].replace(-1, np.nan).dropna()
        mean_days = int(round(valid_days.mean())) if len(valid_days)>0 else -1
        vac_sum = cluster['tomou_vacina'].sum()

        synth_count = size * 2 if generate_extra else size

        for _ in range(synth_count):
            pseud = generate_pseudonym()
            idade_synth = int(max(0, np.random.normal(mean_idade, 2.5)))
            if mean_days >= 0:
                days_synth = int(max(-1, np.random.normal(mean_days, 3.0)))
                date_synth = (min_date + pd.Timedelta(days=days_synth)).date().isoformat()
            else:
                date_synth = ""
            sexo_synth = cluster['sexo'].sample(1).iloc[0]
            local_synth = cluster['local_vacinacao'].sample(1).iloc[0]
            tomou_synth = int(np.random.choice([0,1], p=[1 - vac_sum/size, vac_sum/size]))

            anonymized_rows.append({
                'pseudonimo': pseud,
                'idade': idade_synth,
                'sexo': sexo_synth,
                'tomou_vacina': bool(tomou_synth),
                'data_vacinacao': date_synth,
                'local_vacinacao': local_synth
            })

    anonymized_df = pd.DataFrame(anonymized_rows)
    return anonymized_df

if __name__ == "__main__":
    data = [
        ["João Silva", 34, "M", True, "2021-02-15", "UBS Centro"],
        ["Maria Souza", 28, "F", True, "2021-02-16", "UBS Leste"],
        ["Pedro Lima", 45, "M", False, "", "UBS Oeste"],
        ["Ana Paula", 67, "F", True, "2021-02-20", "UBS Centro"],
        ["Carlos Alberto", 52, "M", True, "2021-02-18", "UBS Norte"],
        ["Mariana Rocha", 30, "F", False, "", "UBS Centro"],
        ["Rafael Costa", 41, "M", True, "2021-02-17", "UBS Norte"],
        ["Beatriz Nunes", 23, "F", False, "", "UBS Leste"],
        ["Felipe Martins", 59, "M", True, "2021-02-19", "UBS Oeste"],
        ["Luiza Fernandes", 36, "F", True, "2021-02-21", "UBS Centro"]
    ]
    df_example = pd.DataFrame(data, columns=['nome','idade','sexo','tomou_vacina','data_vacinacao','local_vacinacao'])

    print("=== ORIGINAL ===")
    print(df_example)

    print("\nGerando registros anonimizados e sintéticos...\n")
    anon = microaggregate_and_synthesize(df_example, weights=DEFAULT_WEIGHTS, k=K_ANON, generate_extra=True)

    print("=== ANONIMIZADOS (SINTÉTICOS) ===")
    print(anon)
    print(f"\nTotal de registros gerados: {len(anon)}")

    anon.to_csv("anonymized_output.csv", index=False)
    print("\nArquivo salvo: anonymized_output.csv")
