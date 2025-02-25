from flask_restx import Resource

from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from src.models import User, Role
from src.api.nsmodels import accounts_ns, user_model

@accounts_ns.route('/user')
@accounts_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class UserApi(Resource):
    @jwt_required()
    @accounts_ns.doc(security='JsonWebToken')
    @accounts_ns.marshal_with(user_model)
    def get(self):
        ''' საკუთარი მონაცემების მიღება '''
        identity = get_jwt_identity()
        user = User.query.filter_by(uuid=identity).first()

        if not user:
            return {'error': 'თქვენ არ ხართ ვერიფიცირებული'}, 404

        return user, 200
        
