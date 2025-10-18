import requests
import json
from datetime import datetime
import os
import logging

def ingest_raw_data():
    """
    Ingere dados de voos da API OpenSky e os salva na camada Bronze.
    """
    url = "https://opensky-network.org/api/states/all"
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        ingestion_time = datetime.now()
        file_path = f"data/bronze/flights_raw_{ingestion_time.strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w') as f:
            json.dump(data, f)

        logging.info(f"✅ Dados brutos ingeridos com sucesso em: {file_path}")
        return file_path

    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Erro ao acessar a API: {e}")
        raise

if __name__ == "__main__":
    ingest_raw_data()
