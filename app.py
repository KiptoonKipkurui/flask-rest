#local imports
from flask import Blueprint
from flask_restful import Api 
from resources.users import UserResource,Users
from resources.payments import PaymentResource

api_bp=Blueprint('api',__name__)

api=Api(api_bp)


#routes 
api.add_resource(Users,'/users')
api.add_resource(UserResource,'/user')
api.add_resource(PaymentResource,'/payment')

