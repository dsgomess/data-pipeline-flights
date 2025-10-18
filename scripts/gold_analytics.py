import os
import pandas as pd
from datetime import datetime
import logging

def generate_gold_analytics():
    """
    Lê os dados tratados da camada Silver, gera análises agregadas e salva a camada Gold.
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    silver_dir = "data/silver"
    gold_dir = "data/gold"
    os.makedirs(gold_dir, exist_ok=True)

    # Pega o arquivo mais recente da camada silver
    silver_files = sorted(
        [f for f in os.listdir(silver_dir) if f.startswith("flights_clean_") and f.endswith(".parquet")],
        reverse=True
    )

    if not silver_files:
        logging.warning("⚠️ Nenhum arquivo encontrado na camada Silver.")
        return

    latest_file = os.path.join(silver_dir, silver_files[0])
    logging.info(f"🔹 Gerando analytics a partir de: {latest_file}")

    # Lê o arquivo parquet
    df = pd.read_parquet(latest_file)

    # --- Exemplo de análises ---
    # 1️⃣ Total de voos por país de origem
    flights_by_country = (
        df.groupby("origin_country")
        .size()
        .reset_index(name="total_flights")
        .sort_values("total_flights", ascending=False)
    )

    # 2️⃣ Média de velocidade por país
    avg_velocity_by_country = (
        df.groupby("origin_country")["velocity"]
        .mean()
        .reset_index(name="avg_velocity")
        .sort_values("avg_velocity", ascending=False)
    )

    # 3️⃣ Combina os resultados
    analytics = pd.merge(flights_by_country, avg_velocity_by_country, on="origin_country", how="left")

    # Adiciona timestamp
    analytics["processing_time"] = datetime.now()

    # Caminho de saída
    gold_file = os.path.join(
        gold_dir,
        f"flights_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

    # Salva em CSV (fácil de importar no Power BI)
    analytics.to_csv(gold_file, index=False)
    logging.info(f"✅ Analytics gerados e salvos em: {gold_file}")

    return gold_file


if __name__ == "__main__":
    generate_gold_analytics()
