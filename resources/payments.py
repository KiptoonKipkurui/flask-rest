from flask import request
from flask_restful import Resource
from models import db,Payment,PaymentSchema

payments_schema=PaymentSchema(many=True)
payment_schema=PaymentSchema()

class PaymentResource(Resource):
    def get(self,id):
        if id is None:
            return {'error':'Id not supplied'},400
            
        payment=Payment.query.filter_by(id=id)

        payment=payment_schema.dump(payment).data

        return {payment},200

    def post(self):
        json_data=request.get_json(force=True)

        if json_data is None:
            return {'error':'No data supplied'},400

        #validate and deserialize the data
        data,errors=payment_schema.load(json_data).data

        if errors:
            return {'errors',errors},400
        
        #check if payment already exists
        payment=Payment.query.filter_by(id=data['id']).first()

        if payment:
            return{'error','payment already exists'}

        #create new payment 
        payment=Payment(amount=data['amount'],reference=data['reference'],user_id=data['user_id'])

        db.session.add(payment)
        db.session.commit()

        #return data 
        result =payment_schema.dump(payment).data

        return{result},200

        def put(self):
            json_data=request.get_json(force=True)

            if not json_data:
                return {'message':'No input provided'},400
            
            #validate and deserialize the input
            data,errors=payment_schema.load(json_data)
    
            if errors:
                return errors,422
    
            payment=Payment.query.filter_by(id=data['id']).first()
    
            if not payment:
                return {'message':'Payment does not exist'}
    
            payment.amount=data['amount']
            payment.user_id=data['user_id']
            payment.reference=data['reference']
    
            db.session.commit()
    
            result =payment_schema.dump(payment).data
    
            return {'status':'success','data':result},204

        def delete(self):

            json_data=request.get_json(force=True)

            if not json_data:
                return {'message': 'No input data provided '},400
    
            data,errors=payment_schema.load(json_data)
    
            if errors:
                return errors,422
    
            payment=Payment.query.filter_by(id=data['id']).delete()
    
            db.session.commit()
    
            result=payment_schema.dump(payment, annotate_fields=True, include_attributes=False).data
    
            return {'status':'success','data':result}
    
