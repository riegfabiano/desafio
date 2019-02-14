import requests
import os
from flask import Flask
from flask_graphql import GraphQLView
from graphene import (String, Int, Float, List, Schema, Field, ObjectType)


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
	fonteRenda = Field(FonteRenda)


# --- Evento
class MovtoFinanceiro(ObjectType):
	tipo = String()
	valor = Float()
	instituicao = String()


class UltimaCompraCartao(ObjectType):
	data = String()
	valor = Float()


class EventoCPF(ObjectType):
	ultimaConsulta = String()
	movtoFinanceiroList = List(MovtoFinanceiro)
	ultimaCompraCartao = Field(UltimaCompraCartao)


# --- Geral
class ConsultaCPF(ObjectType):
	situacao = Field(SituacaoCPF)
	score = Field(ScoreCPF)
	evento = Field(EventoCPF)


class Query(ObjectType):
	consultaCPF = Field(
		ConsultaCPF,
		cpf=String(required=True),
		username=String(required=True),
		password=String(required=True)
	)

	def resolve_consultaCPF(self, info, cpf, username, password):
		return ConsultaCPF(
			make_situacao(cpf, username, password),
			make_score(cpf, username, password),
			make_evento(cpf, username, password)
		)


def make_situacao(cpf, username, password):
	access_token = call_ws_login(os.getenv('HOST_A', 'localhost'), username, password)
	result = call_ws(os.getenv('HOST_A', 'localhost'), "cpf/situacao", cpf, access_token)

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


def make_score(cpf, username, password):
	host = os.getenv('HOST_B', 'localhost')
	access_token = call_ws_login(host, username, password)
	result = call_ws(host, "cpf/score", cpf, access_token)

	E = Endereco(
		logradouro=result['endereco']['logradouro'],
		numero=result['endereco']['numero'],
		bairro=result['endereco']['bairro'],
		cidade=result['endereco']['cidade'],
		uf=result['endereco']['uf'],
		cep=result['endereco']['cep']
	)
	FR = FonteRenda(
		cnpj=result['fonte_renda']['cnpj'],
		razaoSocial=result['fonte_renda']['razao_social'],
		salario=result['fonte_renda']['salario']
	)
	bem_list = []

	for bem_dict in result['bem_list']:
		bem_list.append(
			Bem(
				descricao=bem_dict['descricao'],
				valor=bem_dict['valor']
			)
		)

	return ScoreCPF(
		idade=result['idade'],
		bemList=bem_list,
		endereco=E,
		fonteRenda=FR
	)


def make_evento(cpf, username, password):
	host = os.getenv('HOST_C', 'localhost')
	access_token = call_ws_login(host, username, password)
	result = call_ws(host, "cpf/evento", cpf, access_token)

	UCC = UltimaCompraCartao(
		data=result['ultima_compra_cartao']['data'],
		valor=result['ultima_compra_cartao']['valor']
	)
	movto_list = []

	for movto_dict in result['movto_financeiro_list']:
		movto_list.append(
			MovtoFinanceiro(
				tipo=movto_dict['tipo'],
				valor=movto_dict['valor'],
				instituicao=movto_dict['instituicao']
			)
		)

	return EventoCPF(
		ultimaConsulta=result['ultima_consulta'],
		movtoFinanceiroList=movto_list,
		ultimaCompraCartao=UCC
	)


def call_ws_login(host, username, password):
	"""
	Obtem Token
	"""

	url = "http://%s:5000/login" % host
	headers = {
		'Content-Type': 'application/json'
	}
	data = {
		'username': username,
		'password': password
	}
	return requests.post(url, headers=headers, json=data).json()['access_token']


def call_ws(host, urn, cpf, access_token):
	"""
	Obtem dados
	"""

	url = "http://%s:5000/%s" % (host, urn)
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
	app.run(host='0.0.0.0')
