from flask_restx import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import User, Role
from src.api.nsmodels import accounts_ns, user_model, user_parser, request_password_reset_parser, password_reset_parser
from src.utils import mail, url_serializer

# API საკუთარი მონაცემების მიღებისთვის
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
            return {'error': 'მომხმარებელი ვერ მოიძებნა'}, 404

        return user, 200

# API რომელსაც გადაეცემა არგუმენტად მომხმარებლის ID
@accounts_ns.route('/user/<int:uuid>')
@accounts_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class UserActionsApi(Resource):
    @jwt_required()
    @accounts_ns.doc(security='JsonWebToken')
    def delete(self, uuid):
        ''' მომხმარებლის სისტემიდან წაშლა '''
        identity = get_jwt_identity()
        user = User.query.filter_by(uuid=identity).first()

        if not user:
            return {'error': 'მომხმარებელი ვერ მოიძებნა'}, 404
        
        if not user.check_permission():
            return {'error': 'თქვენ არ გაქვთ მომხმარებლის წაშლის უფლება უფლება'}, 403

        to_delete_user = User.query.filter_by(uuid = uuid).first()
        
        if not to_delete_user:
            return {'error': 'წასაშლელი მომხმარებელი ვერ მოიძებნა'}, 404
        
        try:
            to_delete_user.delete()
            return {'message': 'მომხმარებელი წარმატებით წაიშალა'},200
        except:
            return {'error': 'მომხმარებლის წაშლის დროს დაფიქსირდა შეცდომა'}, 400
        
    @jwt_required()
    @accounts_ns.doc(security='JsonWebToken')
    @accounts_ns.doc(parser=user_parser)
    def put(self, uuid):
        ''' მომხმარებლის რედაქტირება '''
        identity = get_jwt_identity()
        user = User.query.filter_by(uuid=identity).first()

        args = user_parser.parse_args()

        if not user:
            return {'error': 'მომხმარებელი ვერ მოიძებნა'}, 404
        
        if not user.check_permission():
            return {'error': 'თქვენ არ გაქვთ მომხმარებლის რედაქტირების უფლება უფლება'}, 403

        to_change_user = User.query.filter_by(uuid = uuid).first()
        
        if not to_change_user:
            return {'error': 'დასარედაქტირებელი მომხმარებელი ვერ მოიძებნა'}, 404
        
        role = Role.query.filter_by(name=args.get('role_name')).first()
        email = args.get('email')

        if not role:
            return {'error': 'როლი ვერ მოიძებნა'}, 400

        try:
            to_change_user.email = email
            to_change_user.role_id = role.id
            to_change_user.save()
            return {'message': 'მომხმარებელი წარმატებით დარედაქტირდა'}, 200
        except:
            return {'error': 'მომხმარებლის დარედაქტირების დროს დაფიქსირდა შეცდომა'}, 400

# API ყველა მომხმარებლის ინფორმაციისთვის
@accounts_ns.route('/users')
@accounts_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class UsersApi(Resource):
    @jwt_required()
    @accounts_ns.doc(security='JsonWebToken')
    @accounts_ns.marshal_with(user_model)
    def get(self):
        ''' ყველა მომხმარებლის მონაცემების მიღება '''
        identity = get_jwt_identity()
        user = User.query.filter_by(uuid=identity).first()

        if not user:
            return {'error': 'მომხმარებელი ვერ მოიძებნა'}, 404
        
        if not user.check_permission():
            return {'error': 'თქვენ არ გაქვთ მონაცემების მიღების უფლება'}, 403

        users = User.query.all()

        return users, 200

@accounts_ns.route('/request_reset_password')
@accounts_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class RequestResetPassword(Resource):
    @accounts_ns.doc(parser=request_password_reset_parser)
    def post(self):
        ''' პაროლის შეცვლის მოთხოვნის გაგზავნა '''
        args = request_password_reset_parser.parse_args()
        email = args.get('modalEmail')

        user = User.query.filter_by(email=email).first()

        if not user:
            return {'error' : 'მითითებული ელ.ფოსტით მომხმარებელი არ არსებობს'}, 400
        
        token = url_serializer.generate_token(data=user.uuid, salt='reset_password')
        reset_url = f'{request.url_root}reset_password/{token}'

        subject = 'პაროლის შეცვლა'
        message = f'მოგესალმებით,\nპაროლის შესაცვლელად გთხოვთ გადახვიდეთ ლინკზე: {reset_url}'

        try:
            status = mail.send_mail(emails=[email], subject=subject, message=message)

            if not status:
                return{'error': 'ელ.ფოსტის გაგზავნის დროს დაფიქსირდა შეცდომა'}, 400
            
            return {'message': 'გთხოვთ შეამოწმოთ ელ.ფოსტა, ვერიფიკაციის ლინკი გამოგზავნილია'}, 200
        except Exception as err:
            return {'error': f'ელ.ფოსტის გაგზავნის დროს დაფიქსირდა შეცდომა: {err}'}, 400
        

@accounts_ns.route('/reset_password')
@accounts_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class ResetPassword(Resource):
    @accounts_ns.doc(parser=password_reset_parser)
    def put(self):
        ''' პაროლის შეცვლა '''
        args = password_reset_parser.parse_args()

        token = args.get('token')
        uuid = url_serializer.unload_token(token=token,salt='reset_password', max_age_seconds=300)

        if uuid == 'invalid':
            return {'error': 'არასწორი ტოკენი'}, 400
        elif uuid == 'expired':
            return {'error': 'არსებულ ტოკენს გაუვიდა ვადა'}, 400
        
        user = User.query.filter_by(uuid=uuid).first()
        if not user:
            return {'error': 'მომხმარებელი ვერ მოიძებნა'}, 404
        
        if args.get('password') != args.get("retype_password"):
            return {"error": "პაროლები არ ემთხვევა."}, 400
        
        if len(args.get("password")) < 8:
            return {"error": "პაროლი უნდა იყოს მინიმუმ 8 სიმბოლო."}, 400
        

        password = args.get('password')
        try:
            user.password = password
            user.save()
            return {'message': 'პაროლი წარმატებით დარედაქტირდა'}, 200
        except:
            return {'error': 'პაროლის შეცვლის დროს დაფიქსირდა შეცდომა'}, 400

        


        



        



        

        
