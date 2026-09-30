from etl.extract import buscar_serie
from etl.transform import tratar_serie
from etl.load import carregar_serie

INDICADORES = [
    {"id": 1, "codigo_sgs": 432, "nome": "Selic"},
    {"id": 34, "codigo_sgs": 433, "nome": "IPCA"},
    {"id": 35, "codigo_sgs": 20570, "nome": "Crédito Livre PF"},]

def rodar_pipeline(data_inicial: str, data_final: str):
    for indicador in INDICADORES:
        try:
            print(f"Processando {indicador['nome']} ...")
            dados_brutos = buscar_serie(indicador["codigo_sgs"], data_inicial, data_final)
            df = tratar_serie(dados_brutos, indicador_id=indicador["id"])
            carregar_serie(df)
            print(f" {len(df)} registros carregados.")
        except Exception as e:
            print(f" Erro ao processar {indicador['nome']}: {e}")


if __name__ == "__main__":
    rodar_pipeline("01/04/2024", "30/04/2024")