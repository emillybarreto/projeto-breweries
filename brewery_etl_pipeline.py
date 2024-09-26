from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import json
import pandas as pd
import os
import shutil

# Default args para o DAG (propriedades)
default_args = {
    'owner': 'Emilly Barreto',
    'depends_on_past': False,
    'retries': 1
}

# Função para extrair os dados da API usando sessão HTTP persistente
def api_breweries_data(**kwargs):
    url = "https://api.openbrewerydb.org/breweries"
    session = requests.Session()
    try:
        response = session.get(url)
        if response.status_code == 200:
            breweries_data = response.json()
            kwargs['ti'].xcom_push(key='breweries_data', value=breweries_data)
        else:
            raise Exception(f"Falha ao buscar dados da API. Status Code: {response.status_code}")
    finally:
        session.close()

# Função para salvar os dados brutos extraídos na camada bronze
def extract_data_bronze(**kwargs):
    breweries = kwargs['ti'].xcom_pull(key='breweries_data', task_ids='api_breweries_data')
    with open('/Users/emilly/airflow/data/bronze/breweries.json', 'w') as f:
        json.dump(breweries, f)

# Função para transformar e salvar os dados na camada silver
def transform_data_silver():
    # Carregar os dados da camada bronze
    with open('/Users/emilly/airflow/data/bronze/breweries.json') as f:
        breweries = json.load(f)

    df = pd.DataFrame(breweries)
    
    # Adicionar colunas brewery_type, state e country como colunas separadas e preencher valores ausentes de forma eficiente
    df.fillna({'brewery_type': 'unknown', 'state': 'unknown', 'country': 'unknown'}, inplace=True)
    
    # Verificar se há duplicatas
    duplicates = df[df.duplicated()]
    
    # Se houver duplicatas, exibir uma mensagem de alerta
    if not duplicates.empty:
        print(f"Foram encontradas {duplicates.shape[0]} linhas duplicadas.")
        # Remover duplicatas
        df = df.drop_duplicates()
        print("Linhas duplicadas removidas.")
    else:
        print("Nenhuma linha duplicada encontrada.")
    
    # Verificar se o caminho do arquivo já existe e se é um diretório
    parquet_file = '/Users/emilly/airflow/data/silver/breweries.parquet'
    if os.path.exists(parquet_file) and os.path.isdir(parquet_file):
        print(f"Removendo diretório existente: {parquet_file}")
        shutil.rmtree(parquet_file)
    
    # Salvar o DataFrame no formato Parquet
    df.to_parquet(parquet_file, engine='pyarrow')
    print(f"Arquivo Parquet salvo em: {parquet_file}")

# Função para agregação e salvar os dados na camada ouro
def load_data_gold():
    df = pd.read_parquet('/Users/emilly/airflow/data/silver/breweries.parquet')
    
    # Agrupando os dados por brewery_type e state
    df_grouped_state = df.groupby(['brewery_type', 'state']).size().reset_index(name='count')
    df_grouped_state.to_parquet('/Users/emilly/airflow/data/gold/breweries_state.parquet')
    
    # Agrupando os dados por brewery_type e country
    df_grouped_country = df.groupby(['brewery_type', 'country']).size().reset_index(name='count')
    df_grouped_country.to_parquet('/Users/emilly/airflow/data/gold/breweries_country.parquet')

# Definição do DAG
with DAG('brewery_etl_pipeline',
         default_args=default_args,
         description='Pipeline ETL para buscar dados das cervejarias e processá-las em camadas de DataLake',
         schedule_interval='@daily',  # Pode ser ajustado conforme a necessidade
         start_date=datetime(2024, 9, 25),
         catchup=False) as dag:

    # Tarefa para extrair os dados da API
    task_api_data = PythonOperator(
        task_id='api_breweries_data',
        python_callable=api_breweries_data
    )

    # Tarefa para salvar os dados brutos extraídos na camada bronze
    task_bronze = PythonOperator(
        task_id='extract_data_bronze',
        python_callable=extract_data_bronze
    )

    # Tarefa para transformar e salvar os dados na camada silver
    task_silver = PythonOperator(
        task_id='transform_data_silver',
        python_callable=transform_data_silver
    )

    # Tarefa para agregação e salvar os dados na camada ouro
    task_gold = PythonOperator(
        task_id='load_data_gold',
        python_callable=load_data_gold
    )

    # Paralelizar a execução onde possível
    task_api_data >> task_bronze >> task_silver >> task_gold
