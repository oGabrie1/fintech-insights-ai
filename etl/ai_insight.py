import os
from dotenv import load_dotenv
from google import genai
from sqlalchemy import text

from etl.load import get_engine
from etl.analysis import calcular_correlacao

load_dotenv()

MODELO = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
ID_SELIC = 1
ID_CREDITO = 35

def obter_ultimos_valores() -> list[dict]:
    """Busca o valor mais recente de cada indicador."""

    query = text("""
        SELECT DISTINCT ON (s.indicador_id) 
        i.nome, i.unidade, s.data, s.valor
        FROM series_temporais s 
        JOIN indicadores i ON i.id = s.indicador_id
        ORDER BY s.indicador_id, s.data DESC
        """)

    with get_engine().connect() as conn:
        linhas = conn.execute(query).mappings().all()
    return [dict(l) for l in linhas]


def montar_prompt(correlacao: float, ultimos: list[dict]) -> str:
    resumo = "\n".join(f"- {u['nome']}: {u['valor']} {u['unidade']} (em {u['data']})" for u in ultimos)

    return f"""Você é um analista econômico escrevendo para um gestor de fintech
que não é técnico. Use SOMENTE os dados abaixo.

Correlação de Pearson entre Selic e Crédito Livre PF (médias mensais): {correlacao: .2f}

Últimos valores disponíveis:
{resumo}

Escreva em português, em no máximo 3 parágrafos curtos:
1. O que o valor da correlação indica (força e direção).
2. Uma explicação econômica plausível, sem afirmar causalidade.
3. Uma ressalva honesta sobre os limites dessa análise.
Não invente números que não estejam acima."""

def gerar_insight(correlacao: float, ultimos: list[dict]) -> str:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    resposta = client.models.generate_content(model=MODELO, contents=montar_prompt(correlacao, ultimos),)
    return resposta.text


def salvar_insight (conteudo: str, correlacao: float, data_referencia):
    query = text("""
        INSERT INTO insights (data_referencia, conteudo, correlacao_selic_credito) 
        VALUES (:data_ref, :conteudo, :corr)
        """)

    with get_engine().begin() as conn:
        conn.execute(query, {
            "data_ref": data_referencia,
            "conteudo": conteudo,
            "corr": correlacao,
        })

def gerar_e_salvar_insight():
    correlacao = float(calcular_correlacao(ID_SELIC, ID_CREDITO))
    ultimos = obter_ultimos_valores()
    data_referencia = max(u["data"] for u in ultimos)

    conteudo = gerar_insight(correlacao, ultimos)
    salvar_insight(conteudo, correlacao, data_referencia)

    return conteudo

if __name__ == "__main__":
    print(gerar_e_salvar_insight())




