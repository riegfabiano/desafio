from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources import UserLogin
from resources import EventoCPF


app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = '0fec2613-6739-42ce-ac64-21bc53898d1d'
app.config['JWT_SECRET_KEY'] = '660e0bda-e8de-476e-8165-2a94f9a5572c'
#app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

jwt = JWTManager(app)

api.add_resource(UserLogin, '/login')
api.add_resource(EventoCPF, '/cpf/evento')


if __name__ == '__main__':
	app.run('0.0.0.0', port=5003, debug=True)
