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


class ScoreCPF(Resource):
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
		Este método buscaria na base externa B, então fiz uma mock com 10 CPFs diferentes para teste.
		Organizei as informações em um dicionário com eu faria ao processar os dados do banco,
		facilitando depois a conversão para JSON.
		"""

		mock_base_a_dict = {
			'55669863402': {
				'idade': 18,
				'bem_list': [
					{
						'descicao': 'Carro',
						'valor': 35000.0
					}
				],
				'endereco': {
					'logradouro': 'Rua João Fausto de Figueiredo',
					'numero': 643,
					'bairro': 'Padre Zé',
					'cidade': 'João Pessoa',
					'uf': 'PB',
					'cep': '58026-037'
				},
				'fonte_renda': {
					'cnpj': '20562756000131',
					'razao_social': 'Vitor e Miguel Telas ME',
					'salario': 1500.5
				}
			},
			'29922693364': {
				'idade': 24,
				'bem_list': [
					{
						'descicao': 'Carro',
						'valor': 25000.0
					}
				],
				'endereco': {
					'logradouro': 'Rua Pio IX',
					'numero': 356,
					'bairro': 'São Pedro',
					'cidade': 'Teresina',
					'uf': 'PI',
					'cep': '64019-365'
				},
				'fonte_renda': {
					'cnpj': '74773232000119',
					'razao_social': 'Stella e Martin Informática Ltda',
					'salario': 2500.5
				}
			},
			'72488187046': {
				'idade': 19,
				'bem_list': [
					{
						'descicao': 'Carro',
						'valor': 70000.0
					}
				],
				'endereco': {
					'logradouro': 'Alameda Boliviana',
					'numero': 469,
					'bairro': 'Candelária',
					'cidade': 'Natal',
					'uf': 'RN',
					'cep': '59064-747'
				},
				'fonte_renda': {
					'cnpj': '01932441000194',
					'razao_social': 'Silvana e Sophie Restaurante Ltda',
					'salario': 3500.0
				}
			},
			'59029146044': {
				'idade': 62,
				'bem_list': [
					{
						'descicao': 'Carro',
						'valor': 85000.0
					},
					{
						'descricao': 'Casa',
						'valor': 250000
					}
				],
				'endereco': {
					'logradouro': 'Travessa Professor Afonso Adinolfi',
					'numero': 152,
					'bairro': 'Cambuci',
					'cidade': 'São Paulo',
					'uf': 'SP',
					'cep': '01538-010'
				},
				'fonte_renda': {
					'cnpj': '61904331000140',
					'razao_social': 'Bryan e Daiane Fotografias ME',
					'salario': 4000.0
				}
			},
			'75658854016': {
				'idade': 50,
				'bem_list': [
					{
						'descicao': 'Moto',
						'valor': 15000.0
					}
				],
				'endereco': {
					'logradouro': 'Rua Manoel José de Souza',
					'numero': 576,
					'bairro': 'Barra do Rio',
					'cidade': 'Itajaí',
					'uf': 'SC',
					'cep': '88305-565'
				},
				'fonte_renda': {
					'cnpj': '34632796000117',
					'razao_social': 'Luiza e Sabrina Buffet Ltda',
					'salario': 5500.0
				}
			},
			'22477358006': {
				'idade': 35,
				'bem_list': [
					{
						'descicao': 'Carro',
						'valor': 50000.0
					}
				],
				'endereco': {
					'logradouro': 'Rua Joaquim Nabuco',
					'numero': 341,
					'bairro': 'Mecejana',
					'cidade': 'Boa Vista',
					'uf': 'RR',
					'cep': '69304-390'
				},
				'fonte_renda': {
					'cnpj': '98986597000190',
					'razao_social': 'Isabelly e Levi Pizzaria Ltda',
					'salario': 6500.0
				}
			},
			'59949360498': {
				'idade': 32,
				'bem_list': [
					{
						'descicao': 'Apartamento',
						'valor': 500000.0
					},
					{
						'descricao': 'Casa',
						'valor': 300000.0
					},
					{
						'descricao': 'Carro',
						'valor': 100000.0
					}
				],
				'endereco': {
					'logradouro': 'Rua Santo Anastácio',
					'numero': 106,
					'bairro': 'Cidade Industrial',
					'cidade': 'Cidade Industrial',
					'uf': 'PR',
					'cep': '81305-090'
				},
				'fonte_renda': {
					'cnpj': '61314445000130',
					'razao_social': 'Sarah e Esther Joalheria ME',
					'salario': 12500.0
				}
			},
			'73223714456': {
				'idade': 20,
				'bem_list': [
					{
						'descicao': 'Apartamento',
						'valor': 150000.0
					}
				],
				'endereco': {
					'logradouro': 'Rua Orquídeas',
					'numero': 941,
					'bairro': 'Corujas',
					'cidade': 'Guapimirim',
					'uf': 'RJ',
					'cep': '25948-195'
				},
				'fonte_renda': {
					'cnpj': '07789763000102',
					'razao_social': 'Benedita e Malu Consultoria Financeira Ltda',
					'salario': 3250.0
				}
			},
			'16663144049': {
				'idade': 37,
				'bem_list': [
					{
						'descicao': 'Casa',
						'valor': 300000.0
					},
					{
						'descricao': 'Moto',
						'valor': 10000.0
					}
				],
				'endereco': {
					'logradouro': 'Quadra QR 214 Conjunto P',
					'numero': 584,
					'bairro': 'Santa Maria',
					'cidade': 'Brasília',
					'uf': 'DF',
					'cep': '72544-416'
				},
				'fonte_renda': {
					'cnpj': '12928306000191',
					'razao_social': 'Joaquim e Mateus Eletrônica Ltda',
					'salario': 3400.0
				}
			},
			'46118742499': {
				'idade': 40,
				'bem_list': [
					{
						'descicao': 'Carro',
						'valor': 15000.0
					},
					{
						'descricao': 'Casa',
						'valor': 100000.0
					}
				],
				'endereco': {
					'logradouro': 'Rua Principal 1',
					'numero': 796,
					'bairro': 'Pedro Roseno',
					'cidade': 'Rio Branco',
					'uf': 'AC',
					'cep': '69917-670'
				},
				'fonte_renda': {
					'cnpj': '08577741000141',
					'razao_social': 'Maya e Regina Lavanderia Ltda',
					'salario': 4900.0
				}
			}
		}

		return mock_base_a_dict.get(cpf)
