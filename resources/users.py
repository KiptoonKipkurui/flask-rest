from flask import request
from flask_restful import Resource 
from models import db,User,UserSchema


users_schema=UserSchema(many=True)

user_schema=UserSchema()

class Users(Resource):
    def get(self):
        """get all users
        
        """
        #get all users
        users=User.query.all()
        users=user_schema.dumps(users).data

        #return response
        return {'users':users}

class UserResource(Resource):        
    def get(self):
        id=request.args.get('id')

        if not id:
            return {'error':'Not found'}

        user=User.query.filter_by(id=id).first()

        #serialize to json
        user=user_schema.dump(user)

        return user,200

    def post(self):
        #TODO:better model validation
        #parse the json data from the request
        json_data=request.get_json(force=True)

        if not json_data:
            return {"error":"No input provided"},400

        #validate the data and deserialize the input
        data,errors=user_schema.load(json_data)

        #return errors if any
        if errors:
            return{'status':'error','data':errors},400

        #ensure user with email does not exist
        user=User.query.filter_by(email=data['email']).first()

        if user:
            return {'status':'error','message':'user already exists'},400
        
        #create new user
        user=User(name=data['name'],email=data['email'],phone_number=data['phone_number'],age=data['age'])
        
        #add user to database
        db.session.add(user)

        #save changes
        db.session.commit()

        #return results
        return {user}

    def put(self):
        
        #get json data from the request
        json_data=request.get_json(force=True)

        if not json_data:
            return {'message':'No data supplied'}

        #validate and deseriliaze the input
        data,errors=user_schema.load(json_data)

        if errors:
            return errors,400

        #ensure a user record exists 
        user=User.query.filter_by(id=data['id']).first() 

        if not user:
            return {'message':'User not found'},204

        #update user record
        #TODO:better model update
        user.name=data['name']
        user.email=data['email']
        user.phone_number=data['phone_number']
        user.age=data['age']
       
        #add changes to database
        db.session.commit()


    def delete(self,id):
        #TODO:query parameters
        json_data=request.get_json(force=True)

        if not json_data:
            return {'error':'No data supplied'},400

        #load data
        data,errors=user_schema.load(json_data)

        #return errors if any
        if errors:
            return {errors},422

        user=User.query.filter_by(id=data['id']).delete()
        
        db.session.commit()

        user=user_schema.dump(user,annotate_fields=True,include_attributes=False).data 

        return {'status':'success','data':user}

    
