"""Verifica falhas de comunicação e respostas inválidas sem acessar a API."""

import unittest
from unittest.mock import patch

import httpx

from api_client import consultar_produto


class TestFalhasConsulta(unittest.TestCase):
    """Confere se falhas previsíveis retornam erros controlados."""

    @patch("api_client.httpx.get")
    def test_timeout(self, get_simulado):
        # Simula o esgotamento do tempo de espera durante a requisição.
        get_simulado.side_effect = httpx.ReadTimeout("Timeout simulado")

        resultado = consultar_produto("PRD-001")

        self.assertEqual(resultado["erro"], "tempo_esgotado")

    @patch("api_client.httpx.get")
    def test_json_invalido(self, get_simulado):
        # HTTP 200 não garante que o corpo seja um JSON válido.
        get_simulado.return_value = httpx.Response(
            200,
            text="Resposta que não é JSON",
            request=httpx.Request("GET", "http://teste/produtos/PRD-001"),
        )

        resultado = consultar_produto("PRD-001")

        self.assertEqual(resultado["erro"], "resposta_invalida")

    @patch("api_client.httpx.get")
    def test_dados_incompletos(self, get_simulado):
        # O JSON é válido, mas faltam campos obrigatórios de Produto.
        get_simulado.return_value = httpx.Response(
            200,
            json={"codigo": "PRD-001"},
            request=httpx.Request("GET", "http://teste/produtos/PRD-001"),
        )

        resultado = consultar_produto("PRD-001")

        self.assertEqual(resultado["erro"], "dados_invalidos")