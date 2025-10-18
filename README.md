data-pipeline-flights/
│
├── docker-compose.yml              # Configuração do ambiente Airflow + Postgres
├── requirements.txt                # Dependências Python
│
├── dags/                           # DAGs do Airflow
│   └── pipeline_dag.py
│
├── scripts/                        # Scripts Python para cada camada
│   ├── bronze_ingestion.py
│   ├── silver_processing.py
│   └── gold_analytics.py
│
└── data/                           # Camadas do Data Lake local
    ├── bronze/                     # Dados brutos (API)
    ├── silver/                     # Dados tratados
    └── gold/                       # Dados analíticos prontos para BI
