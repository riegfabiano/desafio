from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources import UserLogin
from resources import ScoreCPF


app = Flask(__name__)
app.debug = True
api = Api(app)

app.config['SECRET_KEY'] = 'f1c60c25-0a37-43d8-842a-b02faf3306e7'
app.config['JWT_SECRET_KEY'] = '6a3a824b-507b-4c33-9df8-f49dfb8fe92e'
#app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

jwt = JWTManager(app)

api.add_resource(UserLogin, '/login')
api.add_resource(ScoreCPF, '/cpf/score')


if __name__ == '__main__':
	app.run(port=5002)
