"""Comunicação HTTP com a API de estoque do professor."""

import httpx
from pydantic import ValidationError
from schemas import ConsultaProduto, Produto

BASE_URL = "http://127.0.0.1:8000"


def consultar_produto(codigo: str) -> dict:
    """Consulta e valida os dados de um produto na API do professor.

    A execução ocorre em etapas: validação do código, requisição HTTP,
    verificação do status, leitura do JSON e validação dos dados recebidos.
    Essa ordem impede que uma resposta de erro seja interpretada como produto.

    Args:
        codigo: Identificador no formato PRD-XXX, como PRD-001.

    Returns:
        Dicionário com os dados validados do produto, em caso de sucesso.
        Nas falhas tratadas, retorna os campos 'erro' e 'mensagem'.
        Quando a API responde com erro HTTP, inclui também 'status_http'.

    A função realiza somente consultas. A classificação da situação do
    estoque será implementada separadamente, comparando a quantidade atual
    com o estoque mínimo.
    """
    
    # Recusa códigos inválidos antes de acessar a API.
    try:
        consulta = ConsultaProduto(codigo=codigo)
    except ValidationError:
        return {
            "erro": "codigo_invalido",
            "mensagem": "Use um código no formato PRD-XXX, como PRD-001.",
        }

    codigo = consulta.codigo
    
    try:
        resposta = httpx.get(
            f"{BASE_URL}/produtos/{codigo}",
            timeout=5.0,
        )
    except httpx.TimeoutException:
        return {
            "erro": "tempo_esgotado",
            "mensagem": "A API demorou demais para responder.",
        }
    except httpx.RequestError:
        return {
            "erro": "falha_comunicacao",
            "mensagem": "Não foi possível comunicar com a API.",
        }

    # Transforma falhas HTTP em dados que o agente poderá interpretar.
    try:
        resposta.raise_for_status()
    except httpx.HTTPStatusError:
        erros = {
            404: ("produto_nao_encontrado", "Produto não encontrado."),
            422: ("codigo_invalido", "Use um código no formato PRD-XXX."),
            503: ("servico_indisponivel", "Serviço temporariamente indisponível."),
        }

        erro, mensagem = erros.get(
            resposta.status_code,
            ("erro_http", "A API retornou um erro inesperado."),
        )

        return {
            "erro": erro,
            "mensagem": mensagem,
            "status_http": resposta.status_code,
        }

    # Verifica se a resposta contém um JSON válido.
    try:
        dados = resposta.json()
    except ValueError:
        return {
            "erro": "resposta_invalida",
            "mensagem": "A API retornou uma resposta que não é um JSON válido.",
        }

    # Confere campos, tipos e limites definidos no contrato Produto.
    try:
        produto = Produto.model_validate(dados)
    except ValidationError:
        return {
            "erro": "dados_invalidos",
            "mensagem": "Os dados recebidos não seguem o contrato esperado.",
        }

    return produto.model_dump()


if __name__ == "__main__":
    produto = consultar_produto("PRD-001")
    print(produto)