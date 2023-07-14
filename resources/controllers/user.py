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
from flask_jwt_extended import jwt_required,get_jwt_identity
from sqlalchemy.orm import class_mapper




class CreateUserApi(Resource):
  
  
  def post(self):
  
    try:
      response={}
      response['status']=200
      response['message']=0
      user_name = request.form.get("user_name")
      email = request.form.get("email")
      phone = request.form.get("phone")
      password = request.form.get("password")
      password=generate_password_hash(password)
      

      if user_name is None or password is None or email is None:
        response['status']=400
        response['message']=1
    
      # Check for existing users
     
      if userClass.query.filter_by(email = email).first():
        
        response['status']=400
        response['message']=2
      else:
        
        user = userClass(user_name = user_name,email=email,phone_number=phone,password_hash = password)
        db.session.add(user)
        db.session.commit()
      
      data={}
      data['user']=email
      response['data']=data
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        
        return {'response': response}, 400

    except Exception as e:
      print(e)
      return {'response': response},500
    

class LoginUserApi(Resource):
  
  
  def post(self):
  
    try:

      response={}
      response['status']=200
      response['message']=0



      email=request.form.get("email")
      password = request.form.get("password")
      data={}
      data["email"]=email
     
      if verify_password(email,password)==True:
        token = g.user.generate_auth_token(600)

        
        user = userClass.query.filter_by(email=email).first()
        if user:
            columns = [c.key for c in class_mapper(userClass).columns]
            user_dict = {column: getattr(user, column) for column in columns}
            
            print(user_dict)
            data= { 'token': token, 'duration': 600 }
            data["user_data"]= user_dict
            data["products"]=getTable("products")
            data["markets"] =getTable("market")
            data["species"] =getTable("species")
            data["phenological_stages"] =getTable("phenological_stages")
            data["moment_types"]=getTable("task_types")
            data["company"]=getUserCompanies(user_dict["_id"])
            data["products"]=getTable("products")
            data["objectives"]=getTable("objectives")
            data["units"]=getTable("units")
            data["product_types"]=getTable("product_types")
            response['data']=data
        
        

            return {'response': response}, 200
      
        

      else: 
        response['status']=400
        response['message']=1
        return {'response': response}, 400

    except Exception as e:
      print(e)
      response['status']=500
      response['message']=2
      return {'response': response}, 500