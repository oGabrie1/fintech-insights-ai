import os
import pandas as pd
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.dialects.postgresql import insert
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
    metadata = MetaData()
    tabela = Table("series_temporais", metadata, autoload_with=engine)

    registros = df.to_dict(orient="records")

    if not registros:
        return

    stmt = insert(tabela).values(registros)
    stmt = stmt.on_conflict_do_nothing(index_elements=["indicador_id", "data"])

    with engine.begin() as conn:
        conn.execute(stmt)