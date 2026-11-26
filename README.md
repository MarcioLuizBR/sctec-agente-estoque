# Agente de Análise de Estoque

Projeto acadêmico individual do módulo Aperfeiçoar — Agentes de IA,
do SCTEC/SENAI, ministrado pelo professor Wanderson Souza.

**Autor:** Márcio Luiz

## Objetivo

Interpretar solicitações em linguagem natural, consultar produtos na API
de estoque disponibilizada pelo professor e apresentar uma análise
fundamentada na quantidade atual e no estoque mínimo.

Após uma consulta bem-sucedida, a aplicação pode enviar os dados da análise
a um workflow complementar no n8n.

## Tecnologias

- Python 3.11 e uv para gerenciamento do ambiente e das dependências.
- LangChain Core e integração OpenAI para o modelo e a ferramenta.
- LangGraph para estado compartilhado e controle do fluxo.
- HTTPX para comunicação HTTP.
- Pydantic para validação de entradas e respostas.
- n8n para recebimento e organização das análises.
- unittest para testes automatizados dos componentes.

## Arquitetura

1. O usuário informa uma pergunta pelo terminal.
2. O nó agente utiliza o LLM para interpretar a solicitação.
3. Uma transição condicional encaminha a execução à ferramenta,
   quando necessária, ou ao encerramento.
4. A ferramenta consulta a API, valida os dados e classifica o estoque.
5. O resultado retorna ao agente para elaboração da resposta.
6. Análises bem-sucedidas são enviadas ao n8n, quando configurado.

O estado utiliza MessagesState. O grafo possui os nós agente e ferramentas.
A execução pelo terminal possui limite de oito passos do LangGraph.

Perguntas conceituais podem ser respondidas sem ferramenta.
Cada execução começa sem memória de conversas anteriores.

## Regras de classificação

| Condição | Situação |
|---|---|
| Quantidade atual igual a zero | Esgotado |
| Quantidade positiva e menor ou igual ao mínimo | Baixo |
| Quantidade maior que o mínimo | Normal |

A igualdade com o mínimo é incluída em estoque baixo.
As comparações são realizadas em Python; o LLM explica o resultado.

## API de apoio

A API foi disponibilizada pelo professor e deve ser executada separadamente:

https://github.com/wangsouza/api-estoque

Este repositório contém a implementação do agente e suas integrações.
A aplicação utiliza consultas, sem cadastrar ou modificar produtos.

## Testes e evidências

Os cenários de execução, resultados observados e capturas estão em
[Validação do agente](docs/testes-agente.md).

O workflow exportado está em
[workflows/analise-estoque.json](workflows/analise-estoque.json).



## Requisitos

- Python 3.11, Git e uv.
- Chave de API da OpenAI com acesso ao modelo configurado.
- API de estoque do professor em execução para consultar produtos.
- n8n Cloud ou instalação local para demonstrar a automação complementar.

As chamadas ao LLM utilizam a API da OpenAI e podem gerar custos.
A chave deve ser configurada localmente e não deve ser versionada.

## Instalação do agente

Os exemplos abaixo utilizam o terminal PowerShell no Windows.

### 1. Obter o projeto

Na pasta em que deseja guardar o repositório:

```powershell
git clone https://github.com/MarcioLuizBR/sctec-agente-estoque.git
cd sctec-agente-estoque
```

### 2. Instalar as dependências

```powershell
uv sync --locked
.\.venv\Scripts\Activate.ps1
```

O uv utiliza a versão indicada em `.python-version` e instala as
dependências registradas em `uv.lock`, criando o ambiente `.venv`.

### 3. Configurar o ambiente

Na primeira instalação, copie o arquivo de exemplo:

```powershell
Copy-Item .env.example .env
```

Se já existir um `.env`, edite o arquivo existente para preservar
sua configuração.

Preencha no `.env`:

| Variável | Finalidade |
|---|---|
| `LLM_PROVIDER` | Provedor utilizado: `openai` |
| `OPENAI_API_KEY` | Sua chave de API da OpenAI |
| `OPENAI_MODEL` | Modelo utilizado: `gpt-4.1-mini` |
| `N8N_WEBHOOK_URL` | URL de produção do seu workflow n8n |

Deixe `N8N_WEBHOOK_URL` vazio para executar o agente sem enviar análises
ao n8n. Para reproduzir a integração completa, configure um workflow ativo.

O arquivo `.env` é ignorado pelo Git. O `.env.example` contém apenas
a configuração de referência, sem credenciais.


## Preparar e iniciar a API de estoque

Utilize um segundo terminal, separado do terminal do agente.

Na pasta em que guarda seus repositórios, obtenha a API do professor:

```powershell
git clone https://github.com/wangsouza/api-estoque.git
cd api-estoque
uv venv --python 3.11
.\.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
```

Se a API já estiver instalada, acesse sua pasta e ative seu ambiente,
sem repetir a clonagem e a instalação.

Inicie o servidor:

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Mantenha esse terminal aberto durante as consultas.

- Verificação de disponibilidade: http://127.0.0.1:8000/health
- Documentação interativa: http://127.0.0.1:8000/docs

O cliente do agente utiliza o endereço `http://127.0.0.1:8000`.
Se alterar a porta da API, ajuste também `BASE_URL` em `api_client.py`.

## Executar o agente

No terminal do agente, dentro de `sctec-agente-estoque`, com seu
ambiente virtual ativo:

```powershell
python main.py
```

Digite uma pergunta quando solicitado. Exemplos:

- `Qual é a situação do estoque do produto PRD-001?`
- `Qual é a situação do estoque do produto PRD-999?`
- `O que significa estoque mínimo?`
- `Esse produto está acabando?`

O programa apresenta a quantidade de execuções de ferramenta,
seus retornos e a resposta final do agente.

Quando existe uma análise bem-sucedida, tenta enviá-la ao n8n.
Perguntas sem ferramenta e consultas com erro não geram eventos.
Cada execução recebe uma pergunta; execute novamente para outra consulta.

## Executar os testes automatizados

Na raiz do repositório, com o ambiente virtual do agente ativo:

```powershell
python -m unittest discover -s tests -v
```

Esses testes verificam timeout, JSON inválido, dados incompletos e
seis casos de classificação de estoque. Não exigem API ligada,
acesso à OpenAI ou conexão com o n8n.

Os testes manuais do agente completo estão documentados em
[docs/testes-agente.md](docs/testes-agente.md).
