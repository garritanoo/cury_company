# Projeto: Cury Company
Dataset Food Delivery: [Food Delivery](https://www.kaggle.com/datasets/gauravmalik26/food-delivery-dataset?select=train.csv)

## 1. Problema de negócio

A Cury Company é uma empresa de tecnologia que criou um aplicativo que conecta restaurantes, entregadores e pessoas.
Através desse aplicativo, é possível realizar o pedido de uma refeição, em qualquer restaurante cadastrado, e recebê-lo no conforto da sua casa por um entregador
também cadastrado no aplicativo da Cury Company.

A empresa realiza negócios entre restaurantes, entregadores e pessoas, e gera muitos dados sobre entregas, tipos de pedidos, condições climáticas, avaliação dos
entregadores e etc. Apesar da entrega estar crescento, em termos de entregas, o CEO não tem visibilidade completa dos KPIs de crescimento da empresa.

Você foi contratado como um Cientista de Dados para criar soluções de dados para entrega, mas antes de treinar algoritmos, a necessidade da empresa é ter um os
principais KPIs estratégicos organizados em uma única ferramenta, para que o CEO possa consultar e conseguir tomar decisões simples, porém importantes.

A Cury Company possui um modelo de negócio chamado Marketplace, que fazer o intermédio do negócio entre três clientes principais: Restaurantes, entregadores e
pessoas compradoras. Para acompanhar o crescimento desses negócios, o CEO gostaria de ver as seguintes métricas de crescimento:

### Do lado da empresa:
1. Pedidos por dia
2. Porcentagem de pedidos por condição de transito
3. Quantidade de pedidos por tipo e por cidade
4. Pedidos por semana
5. Quantidade de pedidos por tipo de entrega
6. Quantidade de pedidos por condições de transito e tipo de cidade
    
### Do lado dos restaurantes:
1. Quantidade de pedidos únicos
2. Distância média percorrida
3. Tempo médio de entrega durante o festival e dias normais
4. Desvio padrão do tempo de entrega durante festivais e dias normais
5. Tempo de entrega médio por cidade
6. Distribuição do tempo médio de entrega por cidade
7. Tempo médio de entrega por tipo de pedido
    
### Do lado dos entregadores
1. Idade do entregador mais velho e mas novo
2. Avaliação do melhor e pior veículo
3. Avaliação média por entregador
4. Avaliação média por condições de transito
5. Avaliação média por condições climáticas
6. Tempo médio do entregador mais rápido
7. Tempo médio do entregador mais rápido por cidade

## 2. Premissas do negócio

1. Análise foi realizada com dados entre 11/02/2022 a 06/04/2022
2. Marketplace foi o modelo de negócio assumido
3. As 3 principais visões do negócio foram: Visão transação do pedido, Visão Restaurante, Visão Entregadores

## 3. Estratégia da solução

O painel estratégico foi desenvolvido utilizando as métrica que refletem as 3 principais visões do modelo de negócio da empresa

1. Visão de crescimento da empresa
2. Visão de crescimento dos restaurantes
3. Visão de crescimento dos entregadores

Cada visão é representada pelo seguinte conjunto de métricas:

### Visão de crescimento da empresa

1. Pedidos por dia
2. Porcentagem de pedidos por condição de transito
3. Quantidade de pedidos por tipo e por cidade
4. Pedidos por semana
5. Quantidade de pedidos por tipo de entrega
6. Quantidade de pedidos por condições de transito e tipo de cidade
    
### Visão de crescimento dos restaurantes

1. Quantidade de pedidos únicos
2. Distância média percorrida
3. Tempo médio de entrega durante o festival e dias normais
4. Desvio padrão do tempo de entrega durante festivais e dias normais
5. Tempo de entrega médio por cidade
6. Distribuição do tempo médio de entrega por cidade
7. Tempo médio de entrega por tipo de pedido
    
### Visão de crescimento dos entregadores

1. Idade do entregador mais velho e mas novo
2. Avaliação do melhor e pior veículo
3. Avaliação média por entregador
4. Avaliação média por condições de transito
5. Avaliação média por condições climáticas
6. Tempo médio do entregador mais rápido
7. Tempo médio do entregador mais rápido por cidade

## 4. Top 3 Insights

1. Sazonalidade dos pedidos é diária. Há uma variação de aproximadamente 10% do número de pedidos em sequencia.
2. As cidades do tipo Semi-Urban não possuem condições baixa de trânsito
3. As maiores variações no tempo de entrega, acontecem durante o clima ensolarado

## 5. O produto final

Painel online hospedada em uma Cloud e disponível para acesso em qualquer dispositivo conectado a internet.

O painel pode ser acessado através do link: [Dashboard - Cury Company](https://juarez-cury-company.streamlit.app/)

## 6. Conclusão

O objetivo desse projeto foi criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO.

Da visão da Empresa, podemos concluir que o número de pedidos cresceu entre a semana 06 e a semana 13 do ano de 2022
