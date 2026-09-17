-- Tabela de referência dos indicadores acompanhados
CREATE TABLE indicadores (
    id SERIAL PRIMARY KEY,
    codigo_sgs INT NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    unidade VARCHAR(50) NOT NULL,
    frequencia VARCHAR(20) NOT NULL
);

-- Valores das séries temporais, um registro por data/indicador
CREATE TABLE series_temporais (
    id SERIAL PRIMARY KEY,
    indicador_id INT NOT NULL REFERENCES indicadores(id),
    data DATE NOT NULL,
    valor NUMERIC(15, 4) NOT NULL,
    criado_em TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (indicador_id, data)
);

CREATE INDEX idx_series_indicador_data
    ON series_temporais (indicador_id, data);

-- Insights gerados pela IA
CREATE TABLE insights (
    id SERIAL PRIMARY KEY,
    data_referencia DATE NOT NULL,
    conteudo TEXT NOT NULL,
    correlacao_selic_credito NUMERIC(5, 4),
    gerado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Registro de execuções do pipeline de ETL
CREATE TABLE execucoes_etl (
    id SERIAL PRIMARY KEY,
    executado_em TIMESTAMP NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL,
    registros_inseridos INT DEFAULT 0
);