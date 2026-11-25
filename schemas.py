"""Contratos de dados utilizados pelo agente de estoque."""

from pydantic import BaseModel, ConfigDict, Field


class Produto(BaseModel):
    """Representa os dados esperados de um produto da API."""

    model_config = ConfigDict(strict=True)

    codigo: str = Field(pattern=r"^PRD-[0-9]{3}$")
    nome: str = Field(min_length=1)
    categoria: str = Field(min_length=1)
    quantidade_atual: int = Field(ge=0)
    estoque_minimo: int = Field(ge=0)
    unidade: str = Field(min_length=1)

class ConsultaProduto(BaseModel):
    """Valida o código informado para uma consulta de estoque."""

    model_config = ConfigDict(strict=True)

    codigo: str = Field(pattern=r"^PRD-[0-9]{3}$")