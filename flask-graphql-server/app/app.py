import json
import requests
import os
from flask import Flask
import graphene
from flask_graphql import GraphQLView


# app initialization
app = Flask(__name__)
app.debug = True


class Endereco(graphene.ObjectType):
	# class Meta:
	# 	default_resolver = dict_resolver

	logradouro = graphene.String()
	numero = graphene.Int()
	bairro = graphene.String()
	cidade = graphene.String()
	uf = graphene.String()
	cep = graphene.String()


class Divida(graphene.ObjectType):
	# class Meta:
	# 	default_resolver = dict_resolver

	credor_nome = graphene.String()
	credor_cnpj = graphene.String()
	valor = graphene.Float()
	nr_contrato = graphene.String()


class SituacaoCPF(graphene.ObjectType):
	# class Meta:
	# 	default_resolver = dict_resolver

	cpf = graphene.String(required=True)
	nome = graphene.String()
	endereco = graphene.Field(Endereco)
	divida_list = graphene.List(Divida)


class Query(graphene.ObjectType):
	situacao = graphene.Field(SituacaoCPF, cpf=graphene.String(required=True))

	#@classmethod
	def resolve_situacao(self, info, cpf):
		import pdb; pdb.set_trace()
		teste = call_ws(os.getenv('HOST_A', 'localhost'), cpf)
		return teste

	# def resolve_score(self, info):
	# 	return call_ws(os.getenv('HOST_B', 'localhost'), info)

	# def resolve_evento(self, info):
	# 	return call_ws(os.getenv('HOST_C', 'localhost'), info)


def call_ws(host, cpf):
	# Obtem Token
	url = "http://%s:5001/login" % os.getenv('HOST_A', 'localhost')
	headers = {
		'Content-Type': 'application/json'
	}
	data = {
		'username': 'admin',
		'password': 'exemplo'
	}
	access_token = requests.post(url, headers=headers, json=data).json()['access_token']

	# Obtem dados
	url = "http://%s:5001/cpf/situacao" % os.getenv('HOST_A', 'localhost')
	headers['Authorization'] = 'Bearer %s' % access_token
	data = {
		'cpf': cpf
	}
	req = requests.get(url, headers=headers, json=data)

	return req.json()


schema = graphene.Schema(query=Query)

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

	#print(call_ws('localhost', '29922693364'))
