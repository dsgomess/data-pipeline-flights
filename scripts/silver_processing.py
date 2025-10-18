import os
import json
import pandas as pd
from datetime import datetime
import logging

def process_bronze_to_silver():
    """
    Processa os dados brutos da camada Bronze e salva a versão tratada na camada Silver.
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    bronze_dir = "data/bronze"
    silver_dir = "data/silver"
    os.makedirs(silver_dir, exist_ok=True)

    # Pega o arquivo mais recente da camada bronze
    bronze_files = sorted(
        [f for f in os.listdir(bronze_dir) if f.startswith("flights_raw_") and f.endswith(".json")],
        reverse=True
    )

    if not bronze_files:
        logging.warning("⚠️ Nenhum arquivo encontrado na camada Bronze.")
        return

    latest_file = os.path.join(bronze_dir, bronze_files[0])
    logging.info(f"🔹 Processando arquivo: {latest_file}")

    # Lê o JSON bruto
    with open(latest_file, "r") as f:
        data = json.load(f)

    # Extrai a lista de estados (cada item é uma lista de valores)
    states = data.get("states", [])
    if not states:
        logging.warning("⚠️ Nenhum dado de voo encontrado no arquivo.")
        return

    # Colunas da documentação da OpenSky API
    columns = [
        "icao24", "callsign", "origin_country", "time_position", "last_contact",
        "longitude", "latitude", "baro_altitude", "on_ground", "velocity",
        "true_track", "vertical_rate", "sensors", "geo_altitude",
        "squawk", "spi", "position_source"
    ]

    # Cria DataFrame
    df = pd.DataFrame(states, columns=columns)

    # 🧹 Limpeza básica
    df = df.dropna(subset=["latitude", "longitude"])  # Remove registros sem coordenadas
    df["callsign"] = df["callsign"].str.strip()  # Remove espaços extras
    df["ingestion_time"] = datetime.now()  # Adiciona timestamp da transformação

    # Caminho de saída
    silver_file = os.path.join(
        silver_dir,
        f"flights_clean_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet"
    )

    # Salva em formato Parquet
    df.to_parquet(silver_file, index=False)
    logging.info(f"✅ Dados tratados salvos em: {silver_file}")

    return silver_file


if __name__ == "__main__":
    process_bronze_to_silver()
