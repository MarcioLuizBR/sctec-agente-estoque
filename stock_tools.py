"""Ferramentas de consulta e análise disponibilizadas ao agente."""

from langchain_core.tools import tool

from api_client import consultar_produto
from schemas import ConsultaProduto, Produto
from stock_analysis import classificar_estoque


@tool(args_schema=ConsultaProduto)
def analisar_estoque(codigo: str) -> dict:
    """Consulta um produto e informa sua situação de estoque.

    Use para perguntas sobre a quantidade disponível ou a situação de um
    produto identificado por código no formato PRD-XXX, como PRD-001.
    Não use para perguntas conceituais. A ferramenta apenas consulta dados,
    sem cadastrar ou modificar produtos.

    Args:
        codigo: Código do produto que será consultado na API.

    Returns:
        Dados do produto acompanhados do campo 'situacao'.
        Se a consulta falhar, retorna o erro sem classificar o estoque.
    """
    dados = consultar_produto(codigo)

    # Uma falha de consulta não significa que o produto esteja esgotado.
    # Preservamos o erro para o agente explicar o limite da consulta.
    if "erro" in dados:
        return dados

    # O modelo validado é a entrada exigida pela regra de classificação.
    produto = Produto.model_validate(dados)

    return {
        **produto.model_dump(),
        "situacao": classificar_estoque(produto),
    }