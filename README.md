# desafio
Desafio

Na arquitetura que pensei, todos os três sistemas acessariam diretamente suas respectivas bases externas, mas dependendo da demanda de acessos talvez precisássemos pensar em replicar os dados para uma base local do micro serviço respectivo de modo a melhorar a performance. A interface de comunicação com os micros serviço’s é via API REST, de forma que ao receber uma requisição o mesmo acessa a base de dados externa processa e retorna o Payload via JSON.
Abaixo descrevo como seria a arquitetura e stack usadas para resolver o problema:

Sistema 1 (Base A) – Lista de dívidas:
Escrever o sistema em arquitetura de micro serviço, com a linguagem Python e que seja executado dentro de um container Docker para posterior deploy em nuvem pública. Este micro serviço deve ter seus endpoints expostos via API REST usando o framework Flask, com autenticação JWT.
Este sistema consumirá os seguintes dados da base A: CPF, Nome, Endereço e Lista de dívidas.
Este sistema deve disponibilizar os dados citados acima através de um endpoint que deve receber como parâmetro um CPF (GET /divida/{cpf}).

Sistema 2 (Base B) – Score de crédito:
Escrever o sistema em arquitetura de micro serviço, com a linguagem Python e que seja executado dentro de um container Docker para posterior deploy em nuvem pública. Este micro serviço deve ter seus endpoints expostos via API REST usando o framework Flask, com autenticação JWT. Neste serviço usaria o Redis para trabalhar com cache de informações para melhorar performance.
Este sistema consumirá os seguintes dados da base B: Idade, Lista de bens, Endereço e Fonte de renda.
Este sistema deve disponibilizar os dados citados através de um endpoint que deve receber como parâmetro um CPF (GET /score/{cpf}).

Sistema 3 (Base C) – Eventos do CPF:
Escrever o sistema em arquitetura de micro serviço, com a linguagem Python e que seja executado dentro de um container Docker para posterior deploy em nuvem pública. Este micro serviço deve ter seus endpoints expostos via API REST usando o framework Flask, com autenticação JWT. Neste serviço usaria o Redis para trabalhar com cache de informações para melhorar a performance.
Como o objetivo deste sistema é rastrear eventos ligado à um CPF, utilizaria o Elasticsearch para buscar de forma mais performática as informações na base C, para posterior processamento e disponibilização.
Este sistema consumirá os seguintes dados da base C: Última consulta ao CPF, Movimentação financeira do CPF, Dados da última compra com cartão de crédito do CPF.
Este sistema deve disponibilizar os dados citados atrvés de um ou mais endpoints que deve(m) receber como parâmetro um CPF (GET /evento/{cpf}, GET /evento/movtofinanceiro/{cpf}, GET /evento/ultcompracartao/{cpf}).
