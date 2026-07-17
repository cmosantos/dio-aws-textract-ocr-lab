# OCR de Imagens com Amazon Textract

Projeto desenvolvido como desafio prático da **DIO**, dentro do conteúdo **Análise Avançada de Imagens e Texto com IA na AWS**.

A solução utiliza Python e o SDK `boto3` para enviar uma imagem ao Amazon Textract, identificar linhas de texto e armazenar os resultados em arquivos TXT e JSON.

## Objetivo

O laboratório simula a leitura automática de uma lista de materiais escolares. O objetivo principal é compreender como um serviço de inteligência artificial pode transformar o conteúdo visual de um documento em dados estruturados, reduzindo tarefas manuais de digitação.

Essa abordagem pode ser aplicada em comprovantes, formulários, fichas cadastrais, notas, contratos, listas, documentos digitalizados e processos de atendimento que recebem anexos em imagem.

## Arquitetura

O processo funciona da seguinte forma:

1. O usuário informa o caminho de uma imagem PNG ou JPEG.
2. O script Python lê o arquivo em formato binário.
3. O SDK `boto3` envia os bytes ao método `DetectDocumentText`.
4. O Amazon Textract retorna blocos com palavras, linhas e metadados.
5. A aplicação seleciona os blocos do tipo `LINE`.
6. O resultado é salvo em TXT e a resposta completa é registrada em JSON.

## Tecnologias utilizadas

- Python
- Amazon Textract
- AWS IAM
- AWS CLI
- boto3
- Git e GitHub
- unittest

## Estrutura do repositório

```text
dio-aws-textract-ocr-lab/
├── assets/
│   ├── execucao_terminal.png
│   └── resultado_textract.png
├── docs/
│   └── COMO_ADICIONAR_PRINTS.md
├── outputs/
│   ├── exemplo_response.json
│   └── exemplo_resultado.txt
├── src/
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── test_extracao.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Pré-requisitos

Antes da execução, é necessário possuir:

- Python 3.10 ou superior
- Conta AWS
- AWS CLI configurada
- Usuário ou perfil IAM com permissão para executar `textract:DetectDocumentText`

A permissão deve seguir o princípio do menor privilégio. Credenciais nunca devem ser inseridas diretamente no código ou publicadas no GitHub.

## Configuração no Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
aws configure
```

## Execução

```powershell
python src/main.py assets/lista_material_escolar.png --region us-east-1
```

Também é possível escolher outro diretório de saída:

```powershell
python src/main.py assets/lista_material_escolar.png --saida resultados
```

## Arquivos gerados

Após uma execução bem-sucedida, a aplicação gera:

```text
outputs/lista_material_escolar_texto.txt
outputs/lista_material_escolar_response.json
```

O arquivo TXT contém somente as linhas reconhecidas. O JSON preserva a resposta completa, incluindo tipos de bloco, níveis de confiança, geometrias e metadados.

## Testes

```powershell
python -m unittest discover -v
```

## Evidências da execução

Adicione seus prints reais da AWS na pasta `assets` e depois habilite estas linhas:

```markdown
![Execução do projeto](assets/execucao_terminal.png)

![Resultado do Textract](assets/resultado_textract.png)
```

Antes de publicar, confirme que as imagens não exibem Access Key, Secret Access Key, tokens, IDs sensíveis ou dados pessoais.

## Insights e aprendizados

Durante o desenvolvimento, foi possível perceber que OCR não é apenas a conversão de uma imagem em texto. O Amazon Textract devolve uma estrutura com diferentes tipos de blocos, níveis de confiança, posições e relações entre os elementos identificados.

Outro aprendizado importante foi a separação entre o acesso ao serviço e o tratamento do resultado. O `boto3` realiza a comunicação com a AWS, enquanto a aplicação decide quais blocos serão utilizados. Neste exemplo, foram selecionados somente blocos do tipo `LINE`, mas o mesmo retorno pode ser explorado para palavras, tabelas, formulários e coordenadas.

Também ficou evidente a importância da segurança. Chaves de acesso não devem estar no código, no README, em prints ou em arquivos enviados ao GitHub. A configuração deve ser realizada localmente pela AWS CLI ou por mecanismos seguros de identidade.

## Possibilidades de evolução

Como continuidade, o projeto pode receber uma interface com Streamlit ou Gradio, integração com Amazon S3, processamento de vários arquivos, armazenamento dos resultados em banco de dados, validação por nível de confiança e classificação automática do documento.

Uma evolução alinhada a cenários de suporte técnico seria receber anexos de chamados, extrair mensagens de erro presentes em prints e encaminhar o texto para um agente de IA responsável por classificar o incidente e sugerir verificações iniciais.

## Referência

Projeto inspirado no repositório educacional da Digital Innovation One:

`digitalinnovationone/nexa-analise-avancada-de-imagens-e-texto-com-ia-na-aws`

## Autor

**Cláudio Menezes**

Analista de Suporte Júnior em desenvolvimento nas áreas de Inteligência Artificial, automação e computação em nuvem.
