from flask import Flask, jsonify
from flask_restful import Api
#from sshtunnel import SSHTunnelForwarder
#from get_project_root import root_path
#from database.db_agroassist import initialize_agroassist_db
from resources.routes import initialize_routes
from resources.errors import errors
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from database.models.Program import db
from flask_jwt_extended import JWTManager

UPLOAD_FOLDER = '/public/storage'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','pdf'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:jaco1992@localhost/agroassist'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'
app.config["JWT_SECRET_KEY"] = "secret string"  
jwt = JWTManager(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config.from_object('config.Config')
api = Api(app)
api = Api(app, errors=errors)







# base error handler
@app.errorhandler(404)
def page_not_found(e):
    return jsonify(message=str(e), status=404), 404

@app.errorhandler(400)
def page_not_found(e):
    return jsonify(message=str(e), status=400), 400

# Routes api
initialize_routes(api)
db.init_app(app)
migrate = Migrate(app, db)  # Initializing the migration


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, threaded=True)