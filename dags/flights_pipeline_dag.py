from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Garante que o Airflow encontre os scripts no diretório 'scripts/'
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))

# Importa as funções de cada camada
from bronze_ingestion import ingest_raw_data
from silver_processing import process_bronze_to_silver
from gold_analytics import generate_gold_analytics


# Argumentos padrão da DAG
default_args = {
    "owner": "deivisson",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Criação da DAG
with DAG(
    dag_id="flights_data_pipeline",
    default_args=default_args,
    description="Pipeline de dados de voos ",
    schedule_interval="@daily",   # Executa 1x por dia (pode ajustar para @hourly, etc.)
    start_date=datetime(2025, 10, 14),
    catchup=False,
    tags=["data-pipeline", "airflow", "medalhao"],
) as dag:

    # Task 1 - Bronze
    bronze_task = PythonOperator(
        task_id="bronze_ingestion",
        python_callable=ingest_raw_data,
    )

    # Task 2 - Silver
    silver_task = PythonOperator(
        task_id="silver_processing",
        python_callable=process_bronze_to_silver,
    )

    # Task 3 - Gold
    gold_task = PythonOperator(
        task_id="gold_analytics",
        python_callable=generate_gold_analytics,
    )

    # Define a sequência das tasks
    bronze_task >> silver_task >> gold_task
