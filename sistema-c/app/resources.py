from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required)


class UserLogin(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('username', help='Campo não informado', required=True)
		parser.add_argument('password', help='Campo não informado', required=True)
		data = parser.parse_args()

		if data['username'] != 'admin':
			return {'message': 'Usuário {} não existe'.format(data['username'])}

		if data['password'] == 'exemplo':
			access_token = create_access_token(identity=data['username'])
			refresh_token = create_refresh_token(identity=data['username'])
			return {
				'message': 'Logado como {}'.format(data['username']),
				'access_token': access_token,
				'refresh_token': refresh_token
			}
		else:
			return {'message': 'Credencial inválida'}


class EventoCPF(Resource):
	@jwt_required
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('cpf', help='Campo não informado', required=True)
		data = parser.parse_args()

		# Caso venha formatado ;)
		cpf_sem_formatacao = "".join([x for x in data['cpf'] if x.isdigit()])

		return self.__get_info_mock(cpf_sem_formatacao) \
			or {'message': 'CPF {} não encontrado'.format(data['cpf'])}

	def __get_info_mock(self, cpf):
		"""
		Este método buscaria na base externa C, então fiz uma mock com 10 CPFs diferentes para teste.
		Organizei as informações em um dicionário com eu faria ao processar os dados do banco,
		facilitando depois a conversão para JSON.
		"""

		mock_base_dict = {
			'55669863402': {
				'ultima_consulta': '2019-01-18',
				'movto_financeiro_list': [
					{
						'tipo': 'Financimento',
						'valor': 35000.0,
						'instituicao': 'Itau S.A.'
					}
				],
				'ultima_compra_cartao': {
					'data': '2019-01-18',
					'valor': 180.0
				}
			},
			'29922693364': {
				'ultima_consulta': '2019-01-31',
				'movto_financeiro_list': [
					{
						'tipo': 'Financimento',
						'valor': 100000.0,
						'instituicao': 'Banco do Brasil S.A.'
					}
				],
				'ultima_compra_cartao': {
					'data': '2019-01-18',
					'valor': 180.0
				}
			},
			'72488187046': {
				'ultima_consulta': '2019-01-20',
				'movto_financeiro_list': [
					{
						'tipo': 'Financimento',
						'valor': 90000.0,
						'instituicao': 'Santander S.A.'
					}
				],
				'ultima_compra_cartao': {
					'data': '2019-01-18',
					'valor': 390.0
				}
			},
			'59029146044': {
				'ultima_consulta': '2019-01-09',
				'movto_financeiro_list': [
					{
						'tipo': 'Financimento',
						'valor': 87000.0,
						'instituicao': 'Bando do Brasil S.A.'
					}
				],
				'ultima_compra_cartao': {
					'data': '2019-01-20',
					'valor': 590.0
				}
			},
			'75658854016': {
				'ultima_consulta': '2019-01-06',
				'movto_financeiro_list': [
					{
						'tipo': 'Financimento',
						'valor': 10000.0,
						'instituicao': 'Bradesco S.A.'
					}
				],
				'ultima_compra_cartao': {
					'data': '2019-01-08',
					'valor': 80.0
				}
			},
			'22477358006': {
				'ultima_consulta': '2019-01-02',
				'movto_financeiro_list': [
					{
						'tipo': 'Financimento',
						'valor': 35000.0,
						'instituicao': 'Itau S.A.'
					}
				],
				'ultima_compra_cartao': {
					'data': '2019-01-09',
					'valor': 67.0
				}
			},
			'59949360498': {
				'ultima_consulta': '2019-01-15',
				'movto_financeiro_list': [
					{
						'tipo': 'Financimento',
						'valor': 35000.0,
						'instituicao': 'Itau S.A.'
					}
				],
				'ultima_compra_cartao': {
					'data': '2019-01-06',
					'valor': 4000.0
				}
			},
			'73223714456': {
				'ultima_consulta': '2019-01-20',
				'movto_financeiro_list': [
					{
						'tipo': 'Financimento',
						'valor': 5000.0,
						'instituicao': 'Bradesco S.A.'
					}
				],
				'ultima_compra_cartao': {
					'data': '2019-01-08',
					'valor': 500.0
				}
			},
			'16663144049': {
				'ultima_consulta': '2019-01-30',
				'movto_financeiro_list': [
					{
						'tipo': 'Financimento',
						'valor': 35000.0,
						'instituicao': 'Itau S.A.'
					},
					{
						'tipo': 'Emprestimo',
						'valor': 12000.0,
						'instituicao': 'Santander S.A.'
					}
				],
				'ultima_compra_cartao': {
					'data': '2019-01-10',
					'valor': 180.0
				}
			},
			'46118742499': {
				'ultima_consulta': '2019-02-08',
				'movto_financeiro_list': [
					{
						'tipo': 'Financimento',
						'valor': 135000.0,
						'instituicao': 'Banco do Brasil S.A.'
					}
				],
				'ultima_compra_cartao': {
					'data': '2019-02-10',
					'valor': 380.0
				}
			}
		}

		return mock_base_dict.get(cpf)
