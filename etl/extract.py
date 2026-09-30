import requests
from datetime import date

BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"

def buscar_serie(codigo_sgs: int, data_inicial: str, data_final: str) -> list[dict]:
    """
    Busca uma série temporal do BACEN.
    Datas no formato dd/mm/yyyy.
    Retorna lista de dicts: [{"data": "...", "valor": "..."}]
    """
    url = BASE_URL.format(codigo=codigo_sgs)
    params = {
        "formato": "json",
        "dataInicial": data_inicial,
        "dataFinal": data_final,
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()