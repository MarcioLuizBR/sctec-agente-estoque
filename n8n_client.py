"""Envio complementar de análises ao workflow n8n."""

import os
from pathlib import Path

import httpx
from dotenv import load_dotenv


def enviar_analise(analise: dict) -> dict:
    """Envia uma análise ao Webhook e informa o resultado do envio.

    A integração é opcional: URL vazia desabilita o envio.
    Uma confirmação HTTP indica recebimento, não a conclusão de todos
    os nós do workflow. Falhas retornam dados, sem interromper o agente.
    """
    caminho_env = Path(__file__).resolve().parent / ".env"
    load_dotenv(caminho_env)
    url = os.getenv("N8N_WEBHOOK_URL", "").strip()

    if not url:
        return {"status": "desabilitado"}

    # Resultados de consulta com erro não representam análises de estoque.
    if "erro" in analise:
        return {"status": "ignorado", "motivo": "consulta_com_erro"}

    try:
        resposta = httpx.post(
            url,
            json={"evento": "estoque.analisado", "produto": analise},
            timeout=10.0,
        )
        resposta.raise_for_status()
    except httpx.TimeoutException:
        return {"status": "falhou", "motivo": "tempo_esgotado"}
    except httpx.RequestError:
        return {"status": "falhou", "motivo": "falha_comunicacao"}
    except httpx.HTTPStatusError as erro:
        return {
            "status": "falhou",
            "motivo": "erro_http",
            "status_http": erro.response.status_code,
        }

    return {"status": "recebido", "status_http": resposta.status_code}