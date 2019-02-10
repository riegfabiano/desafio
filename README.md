# desafio
Desafio

Na arquitetura que pensei, todos os três sistemas acessariam diretamente suas respectivas bases externas. A interface de comunicação com os micros serviços é via API REST, de forma que ao receber uma requisição o mesmo acessa a base de dados externa processa e retorna o Payload via JSON.
Abaixo descrevo como seria a arquitetura e stack usadas para resolver o problema:

Escrever os sistemas em arquitetura de micro serviço, com a linguagem Python e que seja executado dentro de um container Docker para posterior deploy em nuvem pública. Este micro serviço deve ter seus endpoints expostos via API REST usando o framework Flask, com autenticação JWT.
Este sistema deve disponibilizar os dados através de um endpoint que deve receber como parâmetro um CPF.

E para disponibilizar os dados utilizei o GraphQL fazendo a junção das 3 API de forma transparente para os clientes, que podem utilizar das mais diversas formas possíveis os dados retornados.