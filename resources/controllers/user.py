from flask import Response, request,jsonify, g
from flask_restful import Resource
import json
from datetime import datetime
#import pandas as pd
#from get_project_root import root_path
from resources.errors import  InternalServerError

from database.models.Program import userClass,db
from resources.services.programServices import *
from werkzeug.security import generate_password_hash, check_password_hash




class CreateUserApi(Resource):
  
  
  def post(self):
  
    try:
      
      user_name = request.form.get("user_name")
      email = request.form.get("email")
      phone = request.form.get("phone")
      password = request.form.get("password")
      password=generate_password_hash(password)
      

      if user_name is None or password is None or email is None:
        return {'error': {'status':400}}, 400
    
      # Check for existing users
      if userClass.query.filter_by(email = email).first():
        return {'error': {'status':400}}, 400
    
      user = userClass(user_name = user_name,email=email,phone_number=phone,password_hash = password)
      db.session.add(user)
      db.session.commit()
      
      
      response={'status':200,'user':email}
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        return {'error': response}, 400

    except Exception as e:
      print(e)
      raise InternalServerError
    

class LoginUserApi(Resource):
  
  
  def post(self):
  
    try:
      email=request.form.get("email")
      password = request.form.get("password")
      data={}
      response={'status':200}
      if verify_password(email,password)==True:
        token = g.user.generate_auth_token(600)
        
        data= { 'token': token, 'duration': 600 }
        
        
        
        if response.get('status') == 200:

            return {'response': response,'data':data}, 200
      
      else: 
        return {'error': "Unauthorized access"}, 400

    except Exception as e:
      print(e)
      raise InternalServerError