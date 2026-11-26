"""Executa uma solicitação de análise de estoque pelo terminal."""

from langchain_core.messages import HumanMessage, ToolMessage
from langgraph.errors import GraphRecursionError
from openai import OpenAIError

from agent_graph import criar_grafo


def main():
    """Recebe uma pergunta e executa o grafo com limite de passos."""
    pergunta = input("Sua pergunta sobre estoque: ").strip()

    if not pergunta:
        print("Informe uma pergunta para iniciar a análise.")
        return

    try:
        grafo = criar_grafo()

        # Limita os passos do grafo para interromper possíveis repetições.
        resultado = grafo.invoke(
            {"messages": [HumanMessage(content=pergunta)]},
            config={"recursion_limit": 8},
        )
    except GraphRecursionError:
        print("A execução atingiu o limite de passos. Reformule a solicitação.")
        return
    except OpenAIError:
        # Evita exibir detalhes da exceção que possam conter dados sensíveis.
        print("Não foi possível concluir a chamada ao modelo. Verifique o acesso.")
        return
    except ValueError:
        print("Verifique a configuração do modelo e o formato dos parâmetros.")
        return

    # Registra resultados de ferramentas para tornar a consulta verificável.
    consultas = [
        mensagem
        for mensagem in resultado["messages"]
        if isinstance(mensagem, ToolMessage)
    ]

    print(f"\nExecuções de ferramenta: {len(consultas)}")
    for consulta in consultas:
        print(f"Retorno da ferramenta: {consulta.content}")

    print("\nResposta do agente:")
    print(resultado["messages"][-1].content)


if __name__ == "__main__":
    main()