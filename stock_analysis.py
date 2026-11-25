"""Regras de negócio para interpretar os dados de estoque."""

from schemas import Produto


def classificar_estoque(produto: Produto) -> str:
    """Classifica o estoque usando os dados de um produto validado.

    Regras adotadas pelo projeto:
    - Quantidade zero: esgotado, independentemente do estoque mínimo.
    - Quantidade positiva até o mínimo, inclusive: baixo.
    - Quantidade acima do mínimo: normal.

    A comparação é feita em Python para produzir resultados reproduzíveis.
    O LLM utilizará essa classificação para explicar a situação ao usuário.
    """
    # Verificamos zero primeiro para distinguir falta total de estoque baixo.
    if produto.quantidade_atual == 0:
        return "esgotado"

    # A igualdade é incluída em "baixo", pois o produto atingiu o limite mínimo.
    if produto.quantidade_atual <= produto.estoque_minimo:
        return "baixo"

    return "normal"