from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources import UserLogin
from resources import DividaCPF


app = Flask(__name__)
app.debug = True
api = Api(app)

app.config['SECRET_KEY'] = "db0cf406-3609-4d94-bfc5-0233f3fa40e0"
app.config['JWT_SECRET_KEY'] = "a480e639-9713-4a17-ad4f-093232cfe801"
#app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

jwt = JWTManager(app)

api.add_resource(UserLogin, '/login')
api.add_resource(DividaCPF, '/consulta')


if __name__ == '__main__':
	app.run(port=5001)
