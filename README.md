# Resumo da Solução do Desafio:

Na arquitetura que pensei, todos os três sistemas acessam diretamente suas respectivas bases externas. A interface de comunicação com os micros serviços é via API REST, de forma que ao receber uma requisição o mesmo acessa a base de dados externa processa e retorna o Payload via JSON.
Abaixo descrevo como seria a arquitetura e stack usadas para resolver o problema:

Escrever os sistemas em arquitetura de micro serviço, com a linguagem Python e que seja executado dentro de um container Docker para posterior deploy em nuvem pública. Este micro serviço deve ter seus Endpoints expostos via API REST usando o framework Flask, com autenticação JWT.
Este sistema deve disponibilizar os dados através de um Endpoint que deve receber como parâmetro um CPF.

E para disponibilizar os dados utilizei o GraphQL fazendo a junção das 3 API de forma transparente para os clientes, que podem utilizar das mais diversas formas possíveis os dados retornados.


# Informações para execução dos sistemas de exemplo:

As APIs dos serviços estão disponíveis também em containers no Docker Hub em riegfabiano/desafio,
além disso disponibilizei os serviços no Azure que podem ser acessados conforme abaixo:

As APIs de consulta de dados abaixo possuem um Endpoint "/login" para obter o Token de acesso aos dados disponibilizados pelos
Endpoints de cada um, utilizei usuário e senha padrões que são respectivamente "admin" e "exemplo".

* desafio-sistema-a.westus.azurecontainer.io:5000/cpf/situacao
* desafio-sistema-b.westus.azurecontainer.io:5000/cpf/score
* desafio-sistema-c.westus.azurecontainer.io:5000/cpf/evento

API do GraphQL para obter todos os dados desejados em uma só consulta:
* desafio-graphql-server.westus.azurecontainer.io:5000/graphql

Exemplo de consulta:
{
  consultaCPF(cpf: "299.226.933-64", username: "admin", password: "exemplo"){
    situacao {
      cpf
      nome
      endereco {
        logradouro
        numero
        bairro
        cidade
        uf
        cep
      }
      dividaList {
        credorNome
        credorCnpj
        valor
        nrContrato
      }
    }
    score {
      idade
      bemList {
        descricao
        valor
      }
      fonteRenda {
        cnpj
        razaoSocial
        salario
      }
    }
    evento {
      ultimaConsulta
      movtoFinanceiroList {
        tipo
        valor
        instituicao
      }
      ultimaCompraCartao {
        data
        valor
      }
    }
  }
}

Para executar o sistema na máquina local é só subir a imagem Docker ou através dos fontes executando python app/app.py na pasta
app de cada sistema.

* Todos os serviços rodam na porta 5000.