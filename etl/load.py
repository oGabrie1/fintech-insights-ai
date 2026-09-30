import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    usuario = os.getenv("POSTGRES_USER")
    senha = os.getenv("POSTGRES_PASSWORD")
    banco = os.getenv("POSTGRES_DB")
    url = f"postgresql+psycopg2://{usuario}:{senha}@localhost:5432/{banco}"
    return create_engine(url)


def carregar_serie(df: pd.DataFrame):
    engine = get_engine()
    df.to_sql(
        "series_temporais",
        con=engine,
        if_exists="append",
        index=False,
    )