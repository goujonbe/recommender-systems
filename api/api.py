from flask import Flask
from flask_restful import Resource, Api
import redis

app = Flask(__name__)
api = Api(app)

class Recommandation(Resource):
    def get(self, user_id):
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        recommandations = redis_client.lrange('user:{}'.format(user_id), 0, -1)
        recommandations = \
            [int(recommandation.decode('utf-8')) for recommandation in recommandations ]
        return {user_id:recommandations}

api.add_resource(Recommandation, '/<int:user_id>')

if __name__ == '__main__':
    app.run(port='5001',debug=True)