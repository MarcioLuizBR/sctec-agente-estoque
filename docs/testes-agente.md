# Validação manual do agente de estoque

## Como reproduzir

1. Iniciar a API do professor na porta 8000.
2. Ativar o ambiente virtual do projeto.
3. Configurar o `.env` conforme `.env.example`, com uma chave válida.
4. Executar `python main.py` para cada cenário abaixo.

As chamadas ao modelo utilizam a API da OpenAI.
Cada execução começa sem histórico de conversas anteriores.
A redação das respostas pode variar; a avaliação considera os dados
apresentados e a decisão de utilizar ou não a ferramenta.

## Cenário 1 — Produto existente

- Entrada: `Qual é a situação do estoque do produto PRD-001?`
- Esperado: consultar a ferramenta e informar quantidade 5, mínimo 10
  e situação de estoque baixo.
- Observado: uma execução da ferramenta; dados e classificação
  apresentados corretamente na resposta.
- Evidência: captura `03-primeira-execucao-agente.png`.

## Cenário 2 — Produto inexistente

- Entrada: `Qual é a situação do estoque do produto PRD-999?`
- Esperado: consultar a ferramenta e informar que o produto não existe,
  sem inventar quantidade ou classificação.
- Observado: uma execução da ferramenta, erro `produto_nao_encontrado`,
  HTTP 404 e resposta orientando a verificar o código.
- Evidência: captura `05-agente-produto-inexistente.png`.

## Cenário 3 — Pergunta conceitual

- Entrada: `O que significa estoque mínimo?`
- Esperado: explicar o conceito sem consultar a ferramenta.
- Observado: zero execuções de ferramenta e explicação conceitual.
- Evidência: captura `04-agente-pergunta-conceitual.png`.

## Organização das evidências

As capturas estão sendo coletadas durante o desenvolvimento.
Sua inclusão no repositório e os links serão organizados antes da entrega.