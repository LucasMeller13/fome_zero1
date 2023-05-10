## 1. O Problema do Negócio

A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core business é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.

Você foi contratado como Cientista de Dados pelo novo CEO da empresa, o qual te pediu um dashboard com várias métricas e informações do negócio para entender melhor as decisões estratégicas e alavancar ainda mais a empresa Fome Zero. Para isso, ele te pediu as seguintes páginas com informações em um dashboard para análises posteriores:

### Página Home
1.  Quantidade de restaurantes, países, cidades e culinárias cadastradas.
2. Quantidade total de avaliações na plataforma.
3. Mapa com a localidade de cada restaurante com as respectivas informações: nome do restaurnate, preço para servir duas pessoas, tipo de culinária e avaliação média.

### Página Cities
1. Top 10 Cidades com mais restaurantes cadastrados no banco de dados.
2. Top 7 Cidades com mais restaurantes cadastrados com avaliação média acima de 4.
3. Top 7 Cidades com mais restaurantes cadastrados com avaliação média abaixo de 2.
4. Top 10 Cidades com mais restaurantes com tipos de culinárias distintas.

### Página Countries
1. Quantidade de restaurantes registrados por país.
2. Quantidade de cidades registradas por país.
3. Média de avaliações feitas por país.
4. Preço Médio de um prato para duas pessoas por país.

### Página Cuisines
1. As 5 culinárias mais bem avaliadas e os restaurantes melhor avaliados das respectivas culinárias.
2. Top 1-20 Restaurantes mais bem avaliados com as seguintes informações: ID, nome, país, cidade, tipo de culinária, preço médio para duas pessoas, avaliação e quantidade de votos positivos.
3. Top 10 Tipos de Culinárias mais bem avaliadas.
4. Top 10 Tipos de Culinárias pior avaliadas.

> #### Observação
> Criar filtros por país, ranking e tipos de culinária para que seja possível análises de casos específicos.

## 2. Insights de Dados
1. Apesar da quantidade considerável de culinárias registradas, a culinária mais bem avaliada é a 'Others', ou seja, há tipos de gastronomias altamente valorizadas pelas pessoas que ainda não estão registradas no banco de dados.
2. Grande parte dos restaurantes mais bem avaliados não possuem o tipo de culinária da região em que se localizam.

## Dashboard Final do Projeto
Dashboard em Cloud com as páginas requisitadas e opção de filtro por país. Acesse por esse link: https://lucasmeller13-fome-zero1-home-05g20k.streamlit.app/
