from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources import UserLogin
from resources import SituacaoCPF


app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = "db0cf406-3609-4d94-bfc5-0233f3fa40e0"
app.config['JWT_SECRET_KEY'] = "a480e639-9713-4a17-ad4f-093232cfe801"
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

jwt = JWTManager(app)

api.add_resource(UserLogin, '/login')
api.add_resource(SituacaoCPF, '/cpf/situacao')


if __name__ == '__main__':
	app.run(host='0.0.0.0')
