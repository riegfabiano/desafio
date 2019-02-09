from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required)


class UserLogin(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('username', help='Campo username não informado', required=True)
		parser.add_argument('password', help='Campo password não informado', required=True)
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


class DividaCPF(Resource):
	@jwt_required
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('cpf', help='Campo CPF não informado', required=True)
		data = parser.parse_args()

		result = self.__get_cpf_mock(data['cpf'])

		if not result:
			return {'message': 'CPF {} não encontrado'.format(data['cpf'])}

		return result

	def __get_cpf_mock(self, cpf):
		"""
		Este método buscaria na base externa A, então fiz uma mock com 10 CPFs diferentes para teste.
		Organizei as informações em um dicionário com eu faria ao processar os dados do banco,
		facilitando depois a conversão para JSON.
		"""

		mock_base_a_dict = {
			'55669863402': {
				'nome': 'Guilherme César Oliver Peixoto',
				'endereco': {
					'logradouro': 'Rua João Fausto de Figueiredo',
					'numero': 643,
					'bairro': 'Padre Zé',
					'cidade': 'João Pessoa',
					'uf': 'PB',
					'cep': '58026-037'
				},
				'divida_list': []
			},
			'29922693364': {
				'nome': 'Hugo Luan Fábio Barros',
				'endereco': {
					'logradouro': 'Rua Pio IX',
					'numero': 356,
					'bairro': 'São Pedro',
					'cidade': 'Teresina',
					'uf': 'PI',
					'cep': '64019-365'
				},
				'divida_list': [
					{
						'credor_nome': 'Alana e Caleb Financeira ME',
						'credor_cnpj': '54.243.428/0001-94',
						'valor': 800.0,
						'nr_contrato': '64563457' 
					}
				]
			},
			'72488187046': {
				'nome': 'Antonella Aparecida Milena Nunes',
				'endereco': {
					'logradouro': 'Alameda Boliviana',
					'numero': 469,
					'bairro': 'Candelária',
					'cidade': 'Natal',
					'uf': 'RN',
					'cep': '59064-747'
				},
				'divida_list': [
					{
						'credor_nome': 'Maitê e Fátima Eletrônica ME',
						'credor_cnpj': '58.447.399/0001-33',
						'valor': 450.04,
						'nr_contrato': '0498509823' 
					}
				]
			},
			'59029146044': {
				'nome': 'Isabela Valentina Daniela Silva',
				'endereco': {
					'logradouro': 'Travessa Professor Afonso Adinolfi',
					'numero': 152,
					'bairro': 'Cambuci',
					'cidade': 'São Paulo',
					'uf': 'SP',
					'cep': '01538-010'
				},
				'divida_list': [
					{
						'credor_nome': 'Diego e Lorena Gráfica ME',
						'credor_cnpj': '62.918.637/0001-19',
						'valor': 280.90,
						'nr_contrato': '01029838' 
					}
				]
			},
			'75658854016': {
				'nome': 'Silvana Cláudia Allana Costa',
				'endereco': {
					'logradouro': 'Rua Manoel José de Souza',
					'numero': 576,
					'bairro': 'Barra do Rio',
					'cidade': 'Itajaí',
					'uf': 'SC',
					'cep': '88305-565'
				},
				'divida_list': [
					{
						'credor_nome': 'Arthur e Samuel Eletrônica Ltda',
						'credor_cnpj': '83.512.565/0001-85',
						'valor': 2800.0,
						'nr_contrato': '0875354372' 
					}
				]
			},
			'22477358006': {
				'nome': 'Anderson Bento Araújo',
				'endereco': {
					'logradouro': 'Rua Joaquim Nabuco',
					'numero': 341,
					'bairro': 'Mecejana',
					'cidade': 'Boa Vista',
					'uf': 'RR',
					'cep': '69304-390'
				},
				'divida_list': [
					{
						'credor_nome': 'Isabelle e Stefany Adega Ltda',
						'credor_cnpj': '19.572.833/0001-55',
						'valor': 100.67,
						'nr_contrato': '543312' 
					}
				]
			},
			'59949360498': {
				'nome': 'Tiago Pietro Thales Corte Real',
				'endereco': {
					'logradouro': 'Rua Santo Anastácio',
					'numero': 106,
					'bairro': 'Cidade Industrial',
					'cidade': 'Cidade Industrial',
					'uf': 'PR',
					'cep': '81305-090'
				},
				'divida_list': [
					{
						'credor_nome': 'Nicole e Enzo Telas ME',
						'credor_cnpj': '61.515.890/0001-69',
						'valor': 900.53,
						'nr_contrato': '90826534' 
					}
				]
			},
			'73223714456': {
				'nome': 'Lorenzo Cauê Manuel da Rocha',
				'endereco': {
					'logradouro': 'Rua Orquídeas',
					'numero': 941,
					'bairro': 'Corujas',
					'cidade': 'Guapimirim',
					'uf': 'RJ',
					'cep': '25948-195'
				},
				'divida_list': [
					{
						'credor_nome': 'Luna e Otávio Informática Ltda',
						'credor_cnpj': '81.277.013/0001-04',
						'valor': 890.79,
						'nr_contrato': '8276353' 
					}
				]
			},
			'16663144049': {
				'nome': 'Vera Isabel Bernardes',
				'endereco': {
					'logradouro': 'Quadra QR 214 Conjunto P',
					'numero': 584,
					'bairro': 'Santa Maria',
					'cidade': 'Brasília',
					'uf': 'DF',
					'cep': '72544-416'
				},
				'divida_list': [
					{
						'credor_nome': 'Clarice e Alexandre Pizzaria ME',
						'credor_cnpj': '97.335.254/0001-00',
						'valor': 549.0,
						'nr_contrato': '60982349' 
					}
				]
			},
			'46118742499': {
				'nome': 'Luciana Giovanna Larissa da Rosa',
				'endereco': {
					'logradouro': 'Rua Principal 1',
					'numero': 796,
					'bairro': 'Pedro Roseno',
					'cidade': 'Rio Branco',
					'uf': 'AC',
					'cep': '69917-670'
				},
				'divida_list': [
					{
						'credor_nome': 'Giovanna e Manoel Advocacia Ltda',
						'credor_cnpj': '30.407.240/0001-76',
						'valor': 239.39,
						'nr_contrato': '098234987/87' 
					}
				]
			}
		}

		return mock_base_a_dict.get(cpf)
