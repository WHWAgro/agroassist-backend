
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
import jwt
import time
db = SQLAlchemy()
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from datetime import timedelta


auth = HTTPBasicAuth()

class InvitationsClass(db.Model):

  __tablename__ = 'invitations'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  accepted= db.Column(db.Integer, nullable=False,default=1)
  email=db.Column(db.String(100), nullable=False)
  company_id= db.Column(db.Integer, nullable=False)
  invitation_code=db.Column(db.String(100), nullable=False)
  program_id=db.Column(db.String(100), nullable=False)
  to_send = db.Column(db.Boolean, nullable=False,default=False)
  created_at = db.Column(db.DateTime, default=db.func.now())
  updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
  
class PasswordRecoveryClass(db.Model):

  __tablename__ = 'password_recovery'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  accepted= db.Column(db.Integer, nullable=False,default=1)
  email=db.Column(db.String(100), nullable=False)
  recovery_code=db.Column(db.String(100), nullable=False)
  to_send = db.Column(db.Boolean, nullable=False,default=False)
  created_at = db.Column(db.DateTime, default=db.func.now())
  updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())



class WeatherLocationsClass(db.Model):

  __tablename__ = 'weather_locations'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  location_key = db.Column(db.Integer, nullable=False)
  location_long=db.Column(db.String(50), nullable=False)
  location_lat=db.Column(db.String(50), nullable=False)

class FieldWeatherLocationsAssignClass(db.Model):

  __tablename__ = 'field_weather_location_assign'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  field_id = db.Column(db.Integer, nullable=False)
  weather_locations_id = db.Column(db.Integer, nullable=False)
  
class WeatherDayClass(db.Model):

  __tablename__ = 'weather_day'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  field_id = db.Column(db.Integer, nullable=False)
  weather_locations_id = db.Column(db.Integer, nullable=False)
  date=db.Column(db.String(75), nullable=False)
  description=db.Column(db.String(150), nullable=False)
  icon = db.Column(db.Integer, nullable=False)
  temperature_min = db.Column(db.Integer, nullable=False)
  temperature_max = db.Column(db.Integer, nullable=False)
  wind = db.Column(db.Integer, nullable=False)
  humidity = db.Column(db.Integer, nullable=False)
  
  

class ProgramClass(db.Model):

  __tablename__ = 'programs'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  id_user = db.Column(db.Integer, nullable=False)
  id_species = db.Column(db.Integer, nullable=True )
  program_name = db.Column(db.String(80), nullable=False)
  published = db.Column(db.Boolean, nullable=False)
  fields = db.relationship('ProgramCompaniesClass', backref='program')
  updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
  send_to = db.Column(db.String(2000), nullable=True)
  file= db.Column(db.String(100), nullable=True)
  def __repr__(self):
        return '<program %r>' % self.program_name
  


class VisitTaskClass(db.Model):

  __tablename__ = 'visit_tasks'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  visit_id = db.Column(db.Integer, nullable=False)
  task_type_id = db.Column(db.Integer, nullable=False)
  date_start=db.Column(db.DateTime, nullable=False)
  date_end=db.Column(db.DateTime, nullable=False)
  wetting=db.Column(db.Integer, nullable=True)
  observations=db.Column(db.String(500), nullable=True)
  plots=db.Column(db.String(500), nullable=True)
  objectives = db.relationship('VisitTaskObjectivesClass', backref='visit_task')  
  is_repeatable = db.Column(db.Boolean, nullable=False, default=False)
  repeat_frequency =db.Column(db.Integer, nullable=True)
  repeat_unit =db.Column(db.Integer, nullable=True)
  repeat_until= db.Column(db.DateTime, nullable=True)
  main_visit_task_id = db.Column(db.Integer, nullable=True)

class VisitTaskObjectivesClass(db.Model):

  __tablename__ = 'visit_task_objectives'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  visit_task_id = db.Column(db.Integer,db.ForeignKey('visit_tasks._id'), nullable=False)
  objectives = db.Column(db.String(400), nullable=True)
  products = db.Column(db.String(400), nullable=True)
  dosage=db.Column(db.String(400), nullable=True)
  dosage_parts_per_unit=db.Column(db.String(400), nullable=True)


class AdditionalTaskClass(db.Model):

  __tablename__ = 'additional_tasks'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  user_id = db.Column(db.Integer, nullable=False)
  user_name = db.Column(db.String(200), nullable=False)
  company_id = db.Column(db.Integer, nullable=False )
  field_id = db.Column(db.Integer, nullable=False )
  task_type_id = db.Column(db.Integer, nullable=False)
  date_start=db.Column(db.DateTime, nullable=False)
  date_end=db.Column(db.DateTime, nullable=False)
  wetting=db.Column(db.Integer, nullable=True)
  observations=db.Column(db.String(500), nullable=True)
  plots=db.Column(db.String(500), nullable=True)
  objectives = db.relationship('AdditionalTaskObjectivesClass', backref='additional_task')  
  is_repeatable = db.Column(db.Boolean, nullable=False, default=False)
  repeat_frequency =db.Column(db.Integer, nullable=True)
  repeat_unit =db.Column(db.Integer, nullable=True)
  repeat_until= db.Column(db.DateTime, nullable=True)
  main_additional_task_id = db.Column(db.Integer, nullable=True)
  created_at=db.Column(db.DateTime, default=db.func.now())

class AdditionalTaskObjectivesClass(db.Model):

  __tablename__ = 'additional_task_objectives'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  additional_task_id = db.Column(db.Integer,db.ForeignKey('additional_tasks._id'), nullable=False)
  objectives = db.Column(db.String(400), nullable=True)
  products = db.Column(db.String(400), nullable=True)
  dosage=db.Column(db.String(400), nullable=True)
  dosage_parts_per_unit=db.Column(db.String(400), nullable=True)
  products_phis=db.Column(db.String(400), nullable=True)
  reentry = db.Column(db.Double, nullable=True,default=0)
  objectives_name = db.Column(db.String(400), nullable=True)
  products_name = db.Column(db.String(400), nullable=True)
  products_ingredients = db.Column(db.String(400), nullable=True)
class VisitClass(db.Model):

  __tablename__ = 'visits'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  user_id = db.Column(db.Integer, nullable=False)
  user_name = db.Column(db.String(200), nullable=False)
  company_id = db.Column(db.Integer, nullable=False )
  company_name = db.Column(db.String(200), nullable=False)
  company_mail = db.Column(db.String(200), nullable=False)
  field_id = db.Column(db.Integer, nullable=False )
  field_name = db.Column(db.String(200), nullable=False)
  published = db.Column(db.Boolean, nullable=False, default=False)
  created_at=db.Column(db.DateTime, default=db.func.now())


  #max_applications=db.Column(db.String(400), nullable=True)
  
  
 
  
  

  
class QuoterClass(db.Model):

  __tablename__ = 'quoter'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  id_user = db.Column(db.Integer, nullable=False)
  id_programs = db.Column(db.String(400), nullable=True)
  start_date=db.Column(db.DateTime, nullable=True)
  end_date=db.Column(db.DateTime, nullable=True)
  quotes = db.relationship('QuoteClass', backref='quoter')
  updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
  created_at = db.Column(db.DateTime, server_default=db.func.now())
  total_hectares = db.Column(db.Double, nullable=True)
  products = db.relationship('QuoterProductClass', backref='quoter')

class QuoteClass(db.Model):

  __tablename__ = 'quote'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  id_quoter = db.Column(db.Integer,db.ForeignKey('quoter._id'), nullable=False)
  provider_name = db.Column(db.String(400), nullable=True)
  rows = db.relationship('QuoteRowClass', backref='quote')
  

class QuoterProductClass(db.Model):

  __tablename__ = 'quoter_products'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  id_quoter = db.Column(db.Integer,db.ForeignKey('quoter._id'), nullable=False)
  cluster_id=db.Column(db.String(400), nullable=True)
  cluster_master=db.Column(db.Boolean, nullable=True)
  product_row_id=db.Column(db.Integer, nullable=False)
  product_id=db.Column(db.String(100), nullable=False)
  product_needed=db.Column(db.Integer, nullable=False)
  product_stored=db.Column(db.Integer, nullable=False)
  product_needed_unit_id=db.Column(db.Integer, nullable=False)
  valid_hectares=db.Column(db.Double, nullable=False)

class QuoteRowClass(db.Model):

  __tablename__ = 'quote_rows'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  quote_id = db.Column(db.Integer,db.ForeignKey('quote._id'), nullable=False)
  product_row_id=db.Column(db.Integer, nullable=False)
  container_size=db.Column(db.Integer, nullable=False)
  container_unit_id=db.Column(db.Integer, nullable=False)
  container_price_clp=db.Column(db.Integer, nullable=False)
  checked = db.Column(db.Boolean, nullable=False)
  
  
 
  

  
class ProgramCompaniesClass(db.Model):

  __tablename__ = 'program_companies'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  id_program = db.Column(db.Integer,db.ForeignKey('programs._id'), nullable=False)
  id_company = db.Column(db.Integer, nullable=False )
  
  
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
  id_moment_type = db.Column(db.Integer, nullable=False)
  start_date=db.Column(db.DateTime, nullable=True)
  end_date=db.Column(db.DateTime, nullable=True)
  moment_value=db.Column(db.Integer, nullable=True)
  wetting=db.Column(db.Integer, nullable=True)
  phi=db.Column(db.Double, nullable=True,default=0)
  reentry=db.Column(db.Double, nullable=True,default=0)
  observations=db.Column(db.String(400), nullable=True)
  objectives = db.relationship('TaskObjectivesClass', backref='task')  
  ignore = db.Column(db.Boolean, nullable=True, default=False)
  is_repeatable = db.Column(db.Boolean, nullable=False, default=False)
  repeat_frequency =db.Column(db.Integer, nullable=True, default=None)
  repeat_unit =db.Column(db.Integer, nullable=True, default=None)
  repeat_until= db.Column(db.DateTime, nullable=True, default=None)
  main_program_task_id = db.Column(db.Integer, nullable=True, default=None)
  
  def __repr__(self):
        return '<task %r>' % self.program_name
  
class TaskObjectivesClass(db.Model):

  __tablename__ = 'task_objectives'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  id_task = db.Column(db.Integer,db.ForeignKey('program_tasks._id'), nullable=False)
  id_objective = db.Column(db.Integer, nullable=True)
  id_product = db.Column(db.String(400), nullable=True)
  dosage=db.Column(db.String(400), nullable=True)
  dosage_parts_per_unit=db.Column(db.String(400), nullable=True)
  products_name=db.Column(db.String(400), nullable=True)
  products_ingredients=db.Column(db.String(400), nullable=True)
  products_phis=db.Column(db.String(400), nullable=True)
  objective_name=db.Column(db.String(400), nullable=True)
  #max_applications=db.Column(db.String(400), nullable=True)
  
  
  def __repr__(self):
        return '<task %r>' % self.program_name
  

class TaskClass(db.Model):

  __tablename__ = 'tasks'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  id_moment = db.Column(db.Integer, nullable=False)
  id_task_type = db.Column(db.Integer, nullable=False)
  date_start=db.Column(db.DateTime, nullable=True)
  date_end=db.Column(db.DateTime, nullable=True)
  time_indicator=db.Column(db.String(80), nullable=False)
  id_status=db.Column(db.Integer, nullable=False)
  id_company=db.Column(db.Integer, nullable=False)
  ignore = db.Column(db.Boolean, nullable=True, default=False)
  

class PlotClass(db.Model):

  __tablename__ = 'plots'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100), nullable=True)
  id_field = db.Column(db.Integer, nullable=False)
  id_program = db.Column(db.Integer, nullable=True)
  size = db.Column(db.Double, nullable=False,default=0)
  id_species = db.Column(db.Integer, nullable=False)
  variety = db.Column(db.String(100), nullable=True)
  id_phenological_stage = db.Column(db.Integer, nullable=False)

class PlotTasksClass(db.Model):

  __tablename__ = 'plot_tasks'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  plot_id = db.Column(db.Integer, nullable=False)
  task_id = db.Column(db.Integer, nullable=False)
  status_id = db.Column(db.Integer, nullable=False)
  from_program=db.Column(db.Boolean, nullable=False,default=True)
  date_start=db.Column(db.DateTime, nullable=True)
  date_end=db.Column(db.DateTime, nullable=True)
  task_source=db.Column(db.Integer, nullable=False,default=True)
  
  

class TaskOrderClass(db.Model):

  __tablename__ = 'task_orders'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  id_company = db.Column(db.Integer, nullable=False)
  id_task = db.Column(db.Integer, nullable=False)
  file_name=db.Column(db.String(100), nullable=True)
  order_number=db.Column(db.Integer, nullable=False)
  wetting=db.Column(db.Integer, nullable=False)
  application_date=db.Column(db.DateTime, server_default=db.func.now())
  application_date_end=db.Column(db.DateTime, server_default=db.func.now())
  plots=db.Column(db.String(200), nullable=True)
  time_start=db.Column(db.String(20), nullable=True,default='10:00')
  time_end=db.Column(db.String(20), nullable=True,default='11:00')
  alias=db.Column(db.String(200), nullable=True,default='ODA.pdf')
  reentry = db.Column(db.Double,default=0)
  phi = db.Column(db.Double,default=0)
  objectives=db.Column(db.String(400), nullable=True)
  products=db.Column(db.String(400), nullable=True)
  ingredients=db.Column(db.String(400), nullable=True)
  dosage=db.Column(db.String(400), nullable=True)
  dosage_unit=db.Column(db.String(400), nullable=True)
  application_method=db.Column(db.Integer, nullable=True)
  dosage_responsible=db.Column(db.String(400), nullable=True)
  operators=db.Column(db.String(400), nullable=True)
  sprayer=db.Column(db.String(400), nullable=True)
  tractor=db.Column(db.String(400), nullable=True)
  volumen_total=db.Column(db.Double, nullable=True)
  field_id=db.Column(db.Integer, nullable=True)
  
  





class MachineryClass(db.Model):

  __tablename__ = 'machinery'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  id_field = db.Column(db.Integer, nullable=False)
  name=db.Column(db.String(100), nullable=True)
  model=db.Column(db.String(100), nullable=True)
  id_machinery_type=db.Column(db.Integer, nullable=False)
  size=db.Column(db.Double, nullable=False)

class PurchaseOrderClass(db.Model):

  __tablename__ = 'purchase_orders'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  id_company = db.Column(db.Integer, nullable=False)
  id_quote = db.Column(db.Integer, nullable=False)
  file_name=db.Column(db.String(100), nullable=True)
  order_number=db.Column(db.Integer, nullable=False)
  created_at = db.Column(db.DateTime, server_default=db.func.now())
  alias=db.Column(db.String(200), nullable=True,default='ODC.pdf')

class PhenologicalStageClass(db.Model):

  __tablename__ = 'phenological_stages'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  phenological_stage_name = db.Column(db.String(80), nullable=False)

class ProductTypeClass(db.Model):

  __tablename__ = 'product_types'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  product_type_name = db.Column(db.String(80), nullable=False)



  
class ProductClass(db.Model):
  __tablename__ = 'products'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  product_name = db.Column(db.String(80), nullable=False)
  lower_dosage = db.Column(db.Integer)
  upper_dosage = db.Column(db.Integer)
  dosage_unit = db.Column(db.Integer)
  dosage_type = db.Column(db.Integer)
  container_size = db.Column(db.Integer)
  container_unit = db.Column(db.Integer)
  id_product_type=db.Column(db.Integer)
  chemical_compounds = db.Column(db.String(180), nullable=True)
  max_applications = db.Column(db.Integer)
  id_objective=db.Column(db.Integer, nullable=True)
  reentry_period = db.Column(db.Double,default=0)
  phi = db.Column(db.Double,default=0)
  chemical_compounds = db.Column(db.String(250), nullable=True)

  def __repr__(self):
        return '<product %r>' % self.product_name
  
class ObjectiveClass(db.Model):
  __tablename__ = 'objectives'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  objective_name = db.Column(db.String(80), nullable=False)

  def __repr__(self):
        return '<objective %r>' % self.objective_name

class UnitClass(db.Model):
  __tablename__ = 'units'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  unit_name = db.Column(db.String(80), nullable=False)

  def __repr__(self):
        return '<unit %r>' % self.unit_name
  
class ContainerUnitClass(db.Model):
  __tablename__ = 'container_units'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  container_unit_name = db.Column(db.String(80), nullable=False)

class WorkersClass(db.Model):

  __tablename__ = 'workers'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(80), nullable=False)
  email= db.Column(db.String(80), nullable=True)
  phone_number= db.Column(db.String(80), nullable=True)
  id_worker_type=db.Column(db.Integer, nullable=True)
  id_field=db.Column(db.Integer, nullable=True)
  
class userClass(db.Model):

  __tablename__ = 'users'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  password_hash = db.Column(db.String(102), nullable=False)
  password = db.Column(db.String(102), nullable=True)
  
  user_name = db.Column(db.String(80), nullable=False)
  email= db.Column(db.String(80), nullable=True)
  phone_number= db.Column(db.String(80), nullable=True)
  title_register= db.Column(db.String(80), nullable=True)
  role=db.Column(db.String(80), nullable=True)
  active=db.Column(db.Boolean, nullable=False,default=True)
  
  def __repr__(self):
        return '<user %r>' % self.user_name
  
  def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
  def generate_auth_token(self, expires_in = 600):
        return create_access_token(identity=self._id,expires_delta=timedelta(minutes=3600))

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
  
 
  species_name = db.Column(db.String(80), nullable=False)
  
  
  def __repr__(self):
        return '<species %r>' % self.species_name
  
class CompanyClass(db.Model):

  __tablename__ = 'company'
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  
  
  company_name = db.Column(db.String(80), nullable=False)
  rut = db.Column(db.String(80), nullable=False)
  business_activity = db.Column(db.String(80), nullable=True)
  visible = db.Column(db.Boolean, nullable=False,default=False)
  
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
  program_id=db.Column(db.Integer,db.ForeignKey('programs._id'), nullable=False)

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
  sag_code = db.Column(db.String(80), nullable=False)
  location = db.Column(db.String(120), nullable=True,default='Rancagua')
  latitude = db.Column(db.String(100), nullable=True,default='-34.17083')
  longitude = db.Column(db.String(100), nullable=True,default='-70.74444')
  
  
  
  
 