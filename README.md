# Brewery ETL Pipeline

Este projeto implementa um pipeline ETL (Extração, Transformação e Carga) para coletar, transformar e agregar dados de cervejarias utilizando a Open Brewery DB API. O pipeline está dividido em três camadas (bronze, silver e gold).

### _Estrutura do Pipeline_

1. Camada Bronze: Armazena os dados brutos extraídos da API.
2. Camada Silver: Realiza transformações nos dados e particiona por state e country.
3. Camada Gold: Agrega os dados em dois níveis:
   - Agrupamento por ``brewery_type`` e ``state``.
   - Agrupamento por ``brewery_type`` e ``country``.

### _Requisitos_

- [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/)
- [Python 3.12.6](https://www.python.org/downloads/)

### _Instalação_

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

### _Como Executar o Pipeline_

1. Inicie o Airflow
2. Acesse a interface do Airflow através do navegador no endereço http://localhost:8080.
3. O login e senha se encontra dentro do ``docker-compose.yaml``
   - Geralmente o login/senha é ``airflow``
4. No Airflow, localize o DAG brewery_etl_pipeline e ative-o.




## Dashboard - Data Breweries

O objetivo da criação do dashboard é visualizar os dados brutos da API e poder analisar por tipos de cervejaria, a quantidade alocada por estado e país, sendo possível acessar o website da companhia.

Para interarir aos dados, basta acessar [Data Breweries](https://app.powerbi.com/view?r=eyJrIjoiMWI2ZDBiNjMtMmY2OS00ODg5LTk2ZmMtNGM3NjlmMTEzMDEzIiwidCI6ImNjOTNmYTIzLTEyMmYtNDZhYi04MjZiLTllZGIxZDJhMTVlZCJ9), a base de dados utilizada é a que consta como ``data.csv`` no diretório do git.

![dashboard_data_breweries_view](https://github.com/user-attachments/assets/e21f7689-5ef0-4df6-bd80-01dac93efb94)

