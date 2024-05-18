from flask import Response, request,jsonify, g
from flask_restful import Resource
import json
from datetime import datetime
#import pandas as pd
#from get_project_root import root_path
from resources.errors import  InternalServerError

from database.models.Program import UserCompanyClass,CompanyClass,userClass,db
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
      
      body = request.get_json()
      user_name = body.get("name")+" "+body.get("surname")
      email = body.get("email")
      phone = body.get("phone_number")
      password = body.get("password")
      role=body.get("id_user_type")

      
      password=generate_password_hash(password)
      

      if user_name is None or password is None or email is None:
        response['status']=400
        response['message']=1
    
      # Check for existing users
     
      if userClass.query.filter_by(email = email).first():
        
        response['status']=400
        response['message']=2
      else:
        
        user = userClass(user_name = user_name,email=email,phone_number=phone,password_hash = password,role=role)
        db.session.add(user)
        db.session.commit()
        if role==1:
          company_info=body.get("company_info")
          company = CompanyClass( company_name= company_info['company_name'],rut=company_info['rut'],business_activity=company_info['business_activity'])
          db.session.add(company)
          db.session.commit()
          user_company = UserCompanyClass( company_id=company._id,user_id=user._id)
          db.session.add(user_company)
          db.session.commit()
      
     
      
      if response.get('status') == 200:
        data={}
        data['user']=email
        response['data']=data

        return {'response': response}, 200
      
      else: 
        
        return {'response': response}, 400

    except Exception as e:
      response['status']=500
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
            data["container_units"]=getTable("container_units")
            data["product_types"]=getTable("product_types")
            data["dosage_units"]=getTable("units")
            data["dosage_parts_per_unit"]={ "1":{"1":"gr/100L","2":"kg/100L","3":"g/Ha",4:"Kg/Ha"}, "2":{"5":"cc/100L","6":"L/100L","7":"cc/Ha","8":"L/Ha"}}
            data["task_status"]=[{'_id':1,'status_name':'Pendiente'},{'_id':2,'status_name':'Finalizada'},{'_id':3,'status_name':'Orden Generada'},{'_id':4,'status_name':'En Proceso'}]
            data["worker_type"]=[{'_id':1,'worker_type_name':'Administrador'},{'_id':2,'worker_type_name':'Asesor Agrícola'},{'_id':3,'worker_type_name':'En Terreno'}]
            data["machinery_type"]=[{'_id':1,'machinery_type_name':'Tractor'},{'_id':2,'machinery_type_name':'Nebulizador'}]
            data["task_type"]=[{'_id':1,'task_type_name':'Fitosanitario'},{'_id':2,'task_type_name':'Raleo'},{'_id':3,'task_type_name':'Riego'},{'_id':4,'task_type_name':'Cosecha'}]
            for product in data['products']:
              if product['dosage_type']==1:

                product['dosage']={'1':{'min':15,'max':80},'2':{'min':0.015,'max':0.08},'3':{'min':200,'max':240},'4':{'min':0.2,'max':0.24}}
              else:
                product['dosage']={'5':{'min':10,'max':20},'6':{'min':0.01,'max':0.02},'7':{'min':100,'max':140},'8':{'min':0.1,'max':0.14}}
            
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