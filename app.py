from pathlib import Path
import pandas as pd

# CONFIGURAÇÃO

PASTA_2025 = Path("dados/Cotacoes_2025")
PASTA_2026 = Path("dados/Cotacoes_2026")
PASTA_RESULTADOS = Path("resultados")

PASTA_RESULTADOS.mkdir(exist_ok=True)


# FUNÇÃO PARA CARREGAR TODOS OS CSVs DE UMA PASTA

def carregar_arquivos(pasta):

    arquivos = sorted(pasta.glob("*.csv"))

    if not arquivos:
        raise FileNotFoundError(
            f"Nenhum arquivo CSV encontrado em: {pasta}"
        )

    tabelas = []

    for arquivo in arquivos:

        print(f"Lendo: {arquivo.name}")

        tabela = pd.read_csv(
            arquivo,
            sep=";",
            encoding="latin1",
            low_memory=False
        )

        tabelas.append(tabela)

    return pd.concat(tabelas, ignore_index=True)


# CONVERSÃO DE VALORES BRASILEIROS

def converter_valor(coluna):

    return (
        coluna
        .astype(str)
        .str.strip()
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .replace(["nan", "None", ""], "0")
        .astype(float)
    )


# CARREGAR BASES

print("\n==============================")
print(" CARREGANDO BASE 2025")
print("==============================")

base_2025 = carregar_arquivos(PASTA_2025)

print(f"\nTotal de registros 2025: {len(base_2025):,}")


print("\n==============================")
print(" CARREGANDO BASE 2026")
print("==============================")

base_2026 = carregar_arquivos(PASTA_2026)

print(f"\nTotal de registros 2026: {len(base_2026):,}")

# VERIFICAR COLUNA PRINCIPAL

if "NOME PAGADOR" not in base_2025.columns:
    raise ValueError(
        'A coluna "NOME PAGADOR" não foi encontrada na base de 2025.'
    )

if "NOME PAGADOR" not in base_2026.columns:
    raise ValueError(
        'A coluna "NOME PAGADOR" não foi encontrada na base de 2026.'
    )

# PADRONIZAR NOME DOS CLIENTES

base_2025["NOME PAGADOR"] = (
    base_2025["NOME PAGADOR"]
    .astype(str)
    .str.strip()
)

base_2026["NOME PAGADOR"] = (
    base_2026["NOME PAGADOR"]
    .astype(str)
    .str.strip()
)


# Remover registros sem nome de cliente

base_2025 = base_2025[
    base_2025["NOME PAGADOR"].notna()
    & (base_2025["NOME PAGADOR"] != "")
    & (base_2025["NOME PAGADOR"] != "nan")
]

base_2026 = base_2026[
    base_2026["NOME PAGADOR"].notna()
    & (base_2026["NOME PAGADOR"] != "")
    & (base_2026["NOME PAGADOR"] != "nan")
]


# CONJUNTO DE CLIENTES

clientes_2025 = set(
    base_2025["NOME PAGADOR"].unique()
)

clientes_2026 = set(
    base_2026["NOME PAGADOR"].unique()
)


clientes_que_sumiram = clientes_2025 - clientes_2026


print("\n==============================")
print(" COMPARAÇÃO")
print("==============================")

print(f"Clientes distintos 2025: {len(clientes_2025):,}")
print(f"Clientes distintos 2026: {len(clientes_2026):,}")

print(
    f"Clientes de 2025 que não aparecem em 2026: "
    f"{len(clientes_que_sumiram):,}"
)


# FILTRAR SOMENTE CLIENTES QUE NÃO COTARAM EM 2026

clientes_perdidos = base_2025[
    base_2025["NOME PAGADOR"].isin(clientes_que_sumiram)
].copy()


# CONVERTER COLUNAS NUMÉRICAS

colunas_valor = [
    "VALOR NF",
    "PROPOSTA ATUAL",
    "FRETE CTRC"
]

for coluna in colunas_valor:

    if coluna in clientes_perdidos.columns:

        clientes_perdidos[coluna] = converter_valor(
            clientes_perdidos[coluna]
        )


# CONVERTER DATA

clientes_perdidos["DATA HORA INCLUSAO"] = pd.to_datetime(
    clientes_perdidos["DATA HORA INCLUSAO"],
    dayfirst=True,
    errors="coerce"
)


# RESUMO COMERCIAL POR CLIENTE

resumo = (
    clientes_perdidos
    .groupby("NOME PAGADOR")
    .agg(
        COTACOES_2025=("NOME PAGADOR", "size"),

        VALOR_NF_2025=("VALOR NF", "sum"),

        PROPOSTA_ATUAL_2025=("PROPOSTA ATUAL", "sum"),

        FRETE_CTRC_2025=("FRETE CTRC", "sum"),

        PRIMEIRA_COTACAO_2025=(
            "DATA HORA INCLUSAO",
            "min"
        ),

        ULTIMA_COTACAO_2025=(
            "DATA HORA INCLUSAO",
            "max"
        )
    )
    .reset_index()
)


# VENDEDOR

vendedores = (
    clientes_perdidos[
        ["NOME PAGADOR", "VENDEDOR"]
    ]
    .dropna(subset=["VENDEDOR"])
    .drop_duplicates("NOME PAGADOR")
)

resumo = resumo.merge(
    vendedores,
    on="NOME PAGADOR",
    how="left"
)

# STATUS

resumo["STATUS"] = "NÃO COTOU EM 2026"

# ORDENAR POR VOLUME DE COTAÇÕES

resumo = resumo.sort_values(
    by="COTACOES_2025",
    ascending=False
)

# GERAR EXCEL

arquivo_saida = (
    PASTA_RESULTADOS
    / "resultado_comercial.xlsx"
)


with pd.ExcelWriter(
    arquivo_saida,
    engine="openpyxl"
) as writer:

    # Aba principal
    resumo.to_excel(
        writer,
        sheet_name="Clientes_que_sumiram",
        index=False
    )

    # Resumo geral
    resumo_geral = pd.DataFrame({
        "INDICADOR": [
            "Registros 2025",
            "Registros 2026",
            "Clientes distintos 2025",
            "Clientes distintos 2026",
            "Clientes que não cotaram em 2026"
        ],

        "VALOR": [
            len(base_2025),
            len(base_2026),
            len(clientes_2025),
            len(clientes_2026),
            len(clientes_que_sumiram)
        ]
    })

    resumo_geral.to_excel(
        writer,
        sheet_name="Resumo",
        index=False
    )

# FINAL

print("\n==============================")
print(" CONCLUÍDO")
print("==============================")

print(
    f"\nArquivo gerado:\n"
    f"{arquivo_saida}"
)

print(
    f"\nClientes encontrados: "
    f"{len(resumo):,}"
)