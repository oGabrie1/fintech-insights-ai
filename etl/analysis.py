import pandas as pd
from sqlalchemy import text
from etl.load import get_engine

def calcular_correlacao(indicador_a_id: int, indicador_b_id: int) -> float:
    """
    Calcula a correlação entre duas séries temporais já salvas no banco,
    alinhando pelas datas em comum.
    """

    engine = get_engine()

    query = text("""
        SELECT indicador_id, data, valor 
        FROM series_temporais
        WHERE indicador_id IN (:id_a, :id_b)
        ORDER BY data
    """)

    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"id_a": indicador_a_id, "id_b":indicador_b_id})

    if df.empty:
        raise ValueError("Sem dados para os indicadores informados.")

    df["data"] = pd.to_datetime(df["data"])
    df["ano_mes"] = df["data"].dt.to_period("M")

    mensal = df.groupby(["indicador_id", "ano_mes"])["valor"].mean().unstack(level=0)
    mensal.columns = ["valor_a", "valor_b"]
    mensal = mensal.dropna()

    if len(mensal) < 3:
        raise ValueError("Dados insuficientes para calcular correlação.")
 
    return mensal["valor_a"].corr(mensal["valor_b"])