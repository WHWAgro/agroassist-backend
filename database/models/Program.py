
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
import jwt
import time
db = SQLAlchemy()
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity


auth = HTTPBasicAuth()



class ProgramClass(db.Model):

  __tablename__ = 'programs'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  id_user = db.Column(db.Integer, nullable=False)
  id_species = db.Column(db.Integer, nullable=True, )
  program_name = db.Column(db.String(80), nullable=False)
  published = db.Column(db.Boolean, nullable=False)
  
  def __repr__(self):
        return '<program %r>' % self.program_name
  
class taskTypeClass(db.Model):

  __tablename__ = 'task_types'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  task_type_name = db.Column(db.String(80), nullable=False)
  
  def __repr__(self):
        return '<task type %r>' % self.type_name

class ProgramTaskClass(db.Model):

  __tablename__ = 'program_tasks'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  id_program = db.Column(db.Integer, nullable=False)
  id_type = db.Column(db.Integer, nullable=True)
  fecha_inicio=db.Column(db.DateTime, nullable=True)
  id_phenological_stage=db.Column(db.Integer, nullable=True)
  validity_period=db.Column(db.Integer, nullable=True)
  dosage=db.Column(db.Integer, nullable=True)
  dosage_unit=db.Column(db.String(40), nullable=True)
  objective=db.Column(db.String(200), nullable=True)
  wetting=db.Column(db.Integer, nullable=True)

  
  
  
  def __repr__(self):
        return '<task %r>' % self.program_name
  

class PhenologicalStageClass(db.Model):

  __tablename__ = 'phenological_stages'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  phenological_stage_name = db.Column(db.String(80), nullable=False)

class TaskProductClass(db.Model):

  __tablename__ = 'task_product'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  id_task = db.Column(db.Integer, nullable=False)
  id_product = db.Column(ARRAY(db.Integer), nullable=False)
  
class ProductClass(db.Model):
  __tablename__ = 'products'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  product_name = db.Column(db.String(80), nullable=False)
  
  def __repr__(self):
        return '<product %r>' % self.product_name

  
class userClass(db.Model):

  __tablename__ = 'users'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  password_hash = db.Column(db.String(102), nullable=False)
  
  user_name = db.Column(db.String(80), nullable=False)
  email= db.Column(db.String(80), nullable=True)
  phone_number= db.Column(db.String(80), nullable=True)
  title_register= db.Column(db.String(80), nullable=True)
  role=db.Column(db.String(80), nullable=True)
  
  def __repr__(self):
        return '<user %r>' % self.user_name
  
  def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
  def generate_auth_token(self, expires_in = 600):
        return create_access_token(identity=self._id)

  @staticmethod
  def verify_auth_token(token):
        try:
            current_user = get_jwt_identity()
        except:
            return 
        return userClass.query.get(current_user)
  

  
  
class SpeciesClass(db.Model):

  __tablename__ = 'species'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  
  #speed = db.Column(db.Integer, nullable=False)
  #statechange = db.Column(db.Integer, nullable=False)
  #unixtime = db.Column(db.Integer, nullable=False)
  species_name = db.Column(db.String(80), nullable=False)
  
  
  def __repr__(self):
        return '<species %r>' % self.species_name
  
class CompanyClass(db.Model):

  __tablename__ = 'company'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  
  #speed = db.Column(db.Integer, nullable=False)
  #statechange = db.Column(db.Integer, nullable=False)
  #unixtime = db.Column(db.Integer, nullable=False)
  company_name = db.Column(db.String(80), nullable=False)
  
  
  def __repr__(self):
        return '<company %r>' % self.company_name

class UserCompanyClass(db.Model):

  __tablename__ = 'user_company'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  company_id = db.Column(db.Integer, nullable=False)
  user_id=db.Column(db.Integer, nullable=False)
  
class MarketProgramClass(db.Model):

  __tablename__ = 'market_program'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  market_id = db.Column(db.Integer, nullable=False)
  program_id=db.Column(db.Integer, nullable=False)

class MarketClass(db.Model):

  __tablename__ = 'market'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  market_name = db.Column(db.String(80), nullable=False)
  
  def __repr__(self):
        return '<market %r>' % self.market_name
  

class FieldClass(db.Model):

  __tablename__ = 'field'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  company_id = db.Column(db.Integer, nullable=False)
 
  field_name = db.Column(db.String(80), nullable=False)
  
  def __repr__(self):
        return '<field %r>' % self.field_name
  
  
 