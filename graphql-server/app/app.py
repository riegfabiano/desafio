import requests
import os
from flask import Flask
from flask_graphql import GraphQLView
from graphene import (String, Int, Float, DateTime, List, Schema, Field, ObjectType)


app = Flask(__name__)
app.debug = True


# --- Situação
class Endereco(ObjectType):
	logradouro = String()
	numero = Int()
	bairro = String()
	cidade = String()
	uf = String()
	cep = String()


class Divida(ObjectType):
	credorNome = String()
	credorCnpj = String()
	valor = Float()
	nrContrato = String()


class SituacaoCPF(ObjectType):
	cpf = String()
	nome = String()
	endereco = Field(Endereco)
	dividaList = List(Divida)


# --- Score
class Bem(ObjectType):
	descricao = String()
	valor = Float()


class FonteRenda(ObjectType):
	cnpj = String()
	razaoSocial = String()
	salario = Float()


class ScoreCPF(ObjectType):
	idade = Int()
	bemList = List(Bem)
	endereco = Field(Endereco)
	fonte_renda = FonteRenda


# --- Evento
class MovtoFinanceiro(ObjectType):
	tipo = String()
	valor = Float()
	instituicao = String()


class UltimaCompraCartao(ObjectType):
	data = DateTime()
	valor = Float()


class EventoCPF(ObjectType):
	ultimaConsulta = DateTime()
	movtoFinanceiroList = List(MovtoFinanceiro)
	ultimaCompraCartao = Field(UltimaCompraCartao)


# --- Geral
class ConsultaCPF(ObjectType):
	situacao = Field(SituacaoCPF)
	score = Field(ScoreCPF)
	evento = Field(EventoCPF)


class Query(ObjectType):
	login = String(
		username=String(required=True),
		password=String(required=True)
	)
	consultaCPF = Field(
		ConsultaCPF,
		cpf=String(required=True),
		access_token=String(required=True)
	)

	def resolve_login(self, info, username, password):
		return call_ws_login(os.getenv('HOST_A', 'localhost'), username, password)

	def resolve_consultaCPF(self, info, cpf, access_token):
		return ConsultaCPF(
			self.__make_situacao(cpf, access_token),
			self.__make_score(cpf, access_token),
			self.__make_evento(cpf, access_token)
		)

	def __make_situacao(self, cpf, access_token):
		result = call_ws(os.getenv('HOST_A', 'localhost'), cpf, access_token)

		E = Endereco(
			logradouro=result['endereco']['logradouro'],
			numero=result['endereco']['numero'],
			bairro=result['endereco']['bairro'],
			cidade=result['endereco']['cidade'],
			uf=result['endereco']['uf'],
			cep=result['endereco']['cep']
		)
		divida_list = []

		for divida_dict in result['divida_list']:
			divida_list.append(
				Divida(
					credorNome=divida_dict['credor_nome'],
					credorCnpj=divida_dict['credor_cnpj'],
					nrContrato=divida_dict['nr_contrato'],
					valor=divida_dict['valor']
				)
			)

		return SituacaoCPF(
			nome=result['nome'],
			cpf=cpf,
			endereco=E,
			dividaList=divida_list
		)

	def __make_score(self, cpf, access_token):
		pass

	def __make_evento(self, cpf, access_token):
		pass

	# def resolve_score(self, info):
	# 	return call_ws(os.getenv('HOST_B', 'localhost'), info)

	# def resolve_evento(self, info):
	# 	return call_ws(os.getenv('HOST_C', 'localhost'), info)


def call_ws_login(host, username, password):
	"""
	Obtem Token
	"""

	url = "http://%s:5001/login" % os.getenv('HOST_A', 'localhost')
	headers = {
		'Content-Type': 'application/json'
	}
	data = {
		'username': username,
		'password': password
	}
	return requests.post(url, headers=headers, json=data).json()['access_token']


def call_ws(host, cpf, access_token):
	"""
	Obtem dados
	"""

	url = "http://%s:5001/cpf/situacao" % os.getenv('HOST_A', 'localhost')
	headers = {
		'Content-Type': 'application/json',
		'Authorization': 'Bearer %s' % access_token
	}
	data = {
		'cpf': cpf
	}
	req = requests.get(url, headers=headers, json=data)

	return req.json()


schema = Schema(query=Query)

query = """
{
	situacao(cpf: "29922693364") {
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
}
"""

# Routes
app.add_url_rule(
	'/graphql',
	view_func=GraphQLView.as_view(
		'graphql',
		schema=schema,
		graphiql=True
	)
)


if __name__ == '__main__':
	app.run()
	#print(schema.execute(query).data)
