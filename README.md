# Data Pipeline Flights

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Airflow](https://img.shields.io/badge/Airflow-2.8.0-orange)
![Docker](https://img.shields.io/badge/Docker-Yes-blue)

## Descrição do Projeto

Este projeto implementa uma **pipeline de dados de voos** utilizando **Apache Airflow** e **Docker**, seguindo a arquitetura **Medallion** (Bronze, Silver e Gold).  
A pipeline realiza:

- Ingestão de dados brutos da API pública [OpenSky Network](https://opensky-network.org/) na camada Bronze.  
- Processamento e limpeza dos dados na camada Silver.  
- Transformações analíticas e geração de arquivos finais na camada Gold, que podem ser consumidos em **Power BI** ou outras ferramentas de análise.

O objetivo é simular um fluxo de dados real, do **raw data até a análise final**, mostrando todo o processo de ETL e modelagem de dados.

---

## Estrutura de Pastas




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
