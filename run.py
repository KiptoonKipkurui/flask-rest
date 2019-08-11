#local imports 
from flask import Flask

#function to create flask application

def create_app(config_filename):
    app=Flask(__name__)

    #configure the application
    app.config.from_object(config_filename)

    from app import api_bp 
    app.register_blueprint(api_bp,url_prefix='/api')


    # get database
    from models import db 
    db.init_app(app)

    return app


if __name__=="__main__":
    app=create_app('config')
    app.run(debug=True)

    
