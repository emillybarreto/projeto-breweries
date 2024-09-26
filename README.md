# Brewery ETL Pipeline

Este projeto implementa um pipeline ETL (Extração, Transformação e Carga) para coletar, transformar e agregar dados de cervejarias utilizando a Open Brewery DB API. O pipeline está dividido em três camadas (bronze, silver e gold).

## Estrutura do Pipeline

1. Camada Bronze: Armazena os dados brutos extraídos da API.
2. Camada Silver: Realiza transformações nos dados e particiona por state e country.
3. Camada Gold: Agrega os dados em dois níveis:
   - Agrupamento por ``brewery_type`` e ``state``.
   - Agrupamento por ``brewery_type`` e ``country``.

## Requisitos
- [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/)
- [Python 3.12.6](https://www.python.org/downloads/)

## Instalação

1. Clone este repositório:

    ```bash
    git clone https://github.com/emillybarreto/projeto-breweries.git
    ```

2. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```
    
3. Crie um arquivo docker-compose.yaml dentro do editor de código, com o código do link abaixo:
- [Docker Compose Airflow](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)

4. Configure o Airflow:

Defina o diretório do Airflow em seu sistema. Certifique-se de configurar o caminho correto no ``docker-compose.yaml``, como no exemplo:
    
      ```
      volumes:
    - ${AIRFLOW_PROJ_DIR:-.}/dags:/opt/airflow/dags
    - ${AIRFLOW_PROJ_DIR:-.}/logs:/opt/airflow/logs
    - ${AIRFLOW_PROJ_DIR:-.}/config:/opt/airflow/config
    - ${AIRFLOW_PROJ_DIR:-.}/plugins:/opt/airflow/plugins
    - C:/opt/data/bronze:/opt/data/bronze  # Mapeamento para a camada Bronze
    - C:/opt/data/silver:/opt/data/silver  # Mapeamento para a camada Silver
    - C:/opt/data/gold:/opt/data/gold  # Mapeamento para a camada Gold
      ```

## Como Executar o Pipeline
1. Inicie o Airflow
2. Acesse a interface do Airflow através do navegador no endereço http://localhost:8080.
3. O login e senha se encontra dentro do ``docker-compose.yaml``
   - Geralmente o login/senha é ``airflow``
4. No Airflow, localize o DAG brewery_etl_pipeline e ative-o.
