"""Contratos de dados utilizados pelo agente de estoque."""

from pydantic import BaseModel, ConfigDict, Field


class Produto(BaseModel):
    """Define o contrato esperado para um produto recebido da API.

    A validação exige os seis campos utilizados na consulta e verifica
    seus tipos e restrições. As quantidades devem ser inteiros não negativos,
    e o código deve seguir o formato PRD-XXX.

    O modo estrito impede conversões automáticas, como aceitar o texto "5"
    no lugar do inteiro 5. Isso ajuda a detectar respostas incompatíveis
    antes de utilizar os dados na análise de estoque.

    Este modelo valida a estrutura dos dados. A classificação do estoque
    será realizada separadamente pelas regras de negócio da aplicação.
    """

    model_config = ConfigDict(strict=True)

    codigo: str = Field(pattern=r"^PRD-[0-9]{3}$")
    nome: str = Field(min_length=1)
    categoria: str = Field(min_length=1)
    quantidade_atual: int = Field(ge=0)
    estoque_minimo: int = Field(ge=0)
    unidade: str = Field(min_length=1)

class ConsultaProduto(BaseModel):
    """Define o contrato de entrada para consultar um produto.

    Exige um código textual com o prefixo PRD- e exatamente três dígitos.
    A validação ocorre antes da requisição HTTP, evitando acessar a API
    com um identificador fora do formato esperado.

    Um código válido não garante que o produto esteja cadastrado:
    essa verificação depende da resposta da API.
    """

    model_config = ConfigDict(strict=True)

    codigo: str = Field(pattern=r"^PRD-[0-9]{3}$")