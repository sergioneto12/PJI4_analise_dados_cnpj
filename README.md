# Projeto Integrador 4 - Análise de criação de empresas entre 2018 e 2023

## Contexto
Com a pandemia da COVID-19, tivemos um impacto significativo nos negócios do mundo todo. Muitas pessoas foram demitidas de seus empregos, mas também muitas empresas fecharam as portas. Ainda assim, muitos brasileiros aproveitaram as oportunidades que surgiram desta janela, seja trocando de área de trabalho, seja abrindo seu próprio negócio. 
A segunda mudança citada, entretanto, não pode ser mensurada propriamente sem que haja uma análise profunda mostrando como foi o impacto da pandemia na abertura e fechamento de novas empresas, e qual é a tendência do mercado nos próximos anos dado o que ocorreu entre 2018 e 2023.

## Objetivo
O intuito deste projeto é apresentar uma análise sobre os dados brasileiros de criação de empresas entre os anos de 2018 e 2023.
O projeto se justifica pelo período determinado ser pré e pós-pandemia, fazendo assim uma análise acerca da forma como reagiram os empresários brasileiros diante de um cenário desafiador, além de entender como o desemprego pode ter impulsionado a criação de muitas empresas de empresários em MEIs ou MIs.

O trabalho está sendo baseado em linguagem python, divido em uma análise de dados baseado nos principais módulos para a matéria em questão, e a construção de um modelo de Machine Learning em um módulo em jupyter notebook que deve avaliar se uma empresa, dada as características que estão apresentadas no arquivo disponibilizado neste repositório, está ativa ou não.

## Etapas
### ETL
- Construção das bases: as bases desse trabalho foram retiradas de uma amostra dos dados disponibilizados pelo Governo Brasileiro, disponibilizados no link a seguir: https://dados.gov.br/dados/conjuntos-dados/cadastro-nacional-da-pessoa-juridica---cnpj.

- A estrutura dos dados está disponibilizada na segunda forma normal, distribuidos entre uma tabela fato principal e diversas tabelas dimensão que mostram informações características de cada coluna da fato.

- O processo de ETL foi realizado via python, por meio das bibliotecas pandas e polars, para melhor adaptação dos dados brutos a um módulo de maior poder de processamento (polars) e um módulo de maior flexibilidade na análise dos dados (pandas). Em seguida, foi feita a ingestão no Data Warehouse, escolhido pelo time como o Google Bigquery, do conjunto Google Cloud Platform.

### Análise e Discovery
- Em seguida, foram realizadas análises em cima dos dados, para o entedimento das principais características que formam a base, e em seguida foram realizadas análises estatísticas em cima do problema principal citado no objetivo deste documento. 

- Por fim, de forma a acelerar o processo de demonstração desses dados, foi realizada a criação de uma View dentro do banco para disponibilização dos dados à camada de visualização.

### Visualização
![image](https://user-images.githubusercontent.com/68286883/235372092-b77a8210-eb29-4659-9cf1-1cb9f630b857.png)

- A camada de visualização teve por ferramenta escolhida o looker studio, devido a compatibilidade com o bigquery e também ao custo de implementação (zero).

## Modelo de Machine Learning
Conforme necessário para o complemento deste trabalho, foi feito um estudo sobre a problemática da abertura e fechamento das empresas e então criado um modelo de machine learning para que pudéssemos compreender, dada as características de uma nova empresa, qual seria a compreensão da inteligência artificial para o status dessa empresa no futuro (Ativa, inativa etc.).

- Inicialmente, foi realizada a captura de uma quantidade de dados históricos, determinados em 100k casos de empresas.
- Em seguida foi feita a análise descritiva dos dados e avaliadas as principais variáveis a participar do processo de estudo.
- Fizemos uma análise sobre os dados e também a remoção dos principais outliers relacionados às rendas de cada empresa.
- O pré-processamento dos dados foi realizado de forma a adequar as variáveis ao que seria lido pelo modelo.
- Também foi criada uma variável categórica para os intervalos de renda, de forma a facilitar a leitura.
- Previamente ao passo de escolhermos o melhor modelo, foi realizada a montagem de um script para a escolha das melhores variáveis para os principais modelos de árvore de decisão.
- Em seguida, foram comparados alguns modelos, de forma a verificar qual modelo se encaixava no todo e também em trechos do dataset de amostra, por meio da validação cruzada.
- Por fim, dada a comparação e encontrado o melhor modelo, é feita a criação de um arquivo pickle do modelo para a criação de uma estrutura de backend que ficará responsável por trazer as respostas conforme for realizado o input de dados.

