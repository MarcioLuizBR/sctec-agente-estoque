"""Verifica as classificações e os limites das regras de estoque."""

import unittest

from schemas import Produto
from stock_analysis import classificar_estoque


class TestClassificacaoEstoque(unittest.TestCase):
    """Usa produtos fictícios para verificar cada situação de estoque."""

    def test_classificacoes(self):
        # Cada caso contém quantidade atual, mínimo e resultado esperado.
        casos = [
            (40, 15, "normal"),
            (5, 10, "baixo"),
            (30, 30, "baixo"),
            (0, 20, "esgotado"),
            (0, 0, "esgotado"),
            (1, 0, "normal"),
        ]

        for quantidade, minimo, esperado in casos:
            # Identifica o caso na saída caso alguma comparação falhe.
            with self.subTest(quantidade=quantidade, minimo=minimo):
                produto = Produto(
                    codigo="PRD-001",
                    nome="Produto de teste",
                    categoria="Teste",
                    quantidade_atual=quantidade,
                    estoque_minimo=minimo,
                    unidade="un",
                )

                resultado = classificar_estoque(produto)

                self.assertEqual(resultado, esperado)