import pandas as pd

def tratar_serie(dados_brutos: list[dict], indicador_id: int) -> pd.DataFrame:
    """
    Recebe a lista de dicts vinda da API do BACEN e devolve um
    DataFrame pronto para carregar no banco.
    """
    df = pd.DataFrame(dados_brutos)

    # A API retorna data como string "dd/mm/yyyy" e valor como string
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y").dt.date
    df["valor"] = df["valor"].astype(float)

    # Remove linhas com data ou valor ausente (dado inconsistente)
    df = df.dropna(subset=["data", "valor"])

    # Remove duplicatas de data, mantendo o último valor
    df = df.drop_duplicates(subset=["data"], keep="last")

    df["indicador_id"] = indicador_id

    return df[["indicador_id", "data", "valor"]]