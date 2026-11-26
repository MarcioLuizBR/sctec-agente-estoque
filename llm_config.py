"""Configuração do modelo de linguagem utilizado pelo agente."""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


def criar_modelo() -> ChatOpenAI:
    """Carrega a configuração local e prepara o cliente da OpenAI.

    A criação do cliente não envia mensagens ao modelo.
    As chamadas ocorrerão posteriormente, durante a execução do agente.
    """
    # Localiza o .env em relação a este arquivo, independentemente
    # da pasta a partir da qual o programa foi executado.
    caminho_env = Path(__file__).resolve().parent / ".env"
    load_dotenv(caminho_env)

    provedor = os.getenv("LLM_PROVIDER", "openai").strip()
    modelo = os.getenv("OPENAI_MODEL", "").strip()
    chave = os.getenv("OPENAI_API_KEY", "").strip()

    # Detecta configurações ausentes antes de iniciar o agente.
    # As mensagens de erro nunca devem incluir o conteúdo da chave.
    if provedor != "openai":
        raise ValueError("Este projeto está configurado para o provedor OpenAI.")

    if not modelo or not chave:
        raise ValueError("Configure OPENAI_MODEL e OPENAI_API_KEY no .env.")

    return ChatOpenAI(
        model=modelo,
        api_key=chave,
        temperature=0,
        timeout=30,
        max_retries=1,
    )