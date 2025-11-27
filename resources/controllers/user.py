from flask import Response, request,jsonify, g
from flask_restful import Resource
import json
from datetime import datetime
#import pandas as pd
#from get_project_root import root_path
from resources.errors import  InternalServerError

from database.models.Program import UserCompanyClass,CompanyClass,userClass,db,InvitationsClass,ProgramCompaniesClass,PasswordRecoveryClass
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
      email = body.get("email")
      invitation=None
      if "invitation_code" in body:
        if body["invitation_code"]!=None and body["invitation_code"]!="":
          invitation=InvitationsClass.query.filter_by(email=email,invitation_code=body["invitation_code"],accepted=1).first()
          if invitation==None:
            data={}
            data['user']=email
            response['data']=data
            response['status']=400
            print("chao")
            return {'response': response}, 400

      


      user_name = body.get("name")+" "+body.get("surname")
      
     
      phone = body.get("phone_number")
      password = body.get("password")
      role=body.get("id_user_type")
      
      
      password=generate_password_hash(password)
      print("password")

      if user_name is None or password is None or email is None:
        response['status']=400
        response['message']=1
    
      # Check for existing users
     
      user=userClass.query.filter_by(email = email).first()
      
      if user and body.get("add_companies")==False:
        
        response['status']=400
        response['message']=2
      else:
        print("holag")

        if user==None:
          user = userClass(user_name = user_name,email=email,phone_number=phone,password_hash = password,role=role,password=body.get("password"))
          db.session.add(user)
          db.session.commit()
        if role==1:

          print("holags")

          for company_info in body.get("company_info"):

            company_exists=CompanyClass.query.filter_by(rut = company_info['rut']).first()
            
            if company_exists!=None:
            
             

              if UserCompanyClass.query.filter_by(user_id=user._id,company_id=company_exists._id).first()==None:
                user_company = UserCompanyClass( company_id=company_exists._id,user_id=user._id,role=1)
                db.session.add(user_company)
                db.session.commit()
            else:
              company = CompanyClass( company_name= company_info['company_name'],rut=company_info['rut'],business_activity=company_info['business_activity'])
              db.session.add(company)
              db.session.commit()

              
              user_company = UserCompanyClass( company_id=company._id,user_id=user._id,role=1)
              db.session.add(user_company)
              db.session.commit()

        if "invitation_code" in body:
          if body["invitation_code"]!=None and body["invitation_code"]!="":
            invitation.accepted=2
            db.session.add(invitation)
            programs=getInvitedPrograms(invitation.company_id,email)
            print(programs)
            if programs!=False:
              for program in programs:
                program_update=ProgramClass.query.get(program["_id"] )
                

                send_to_list = program_update.send_to.split(";;;")

                # Remove the specific element from the list
                
                if email in send_to_list:
                    send_to_list.remove(email)
                    updated_send_to = ";;;".join(send_to_list) if send_to_list else None
                    program_update.send_to=updated_send_to
                    db.session.add(program_update)
                    program_company = ProgramCompaniesClass( id_program=program["_id"],id_company=company._id)
                    db.session.add(program_company)
                    new_program_tasks=createTasksNewUser(program["_id"],company._id)
            company_users=getCompanyMainUsers(invitation.company_id)
            if company_users !=False:
              for us in company_users:
                us_new_company=UserCompanyClass(company_id=company._id,user_id=us["user_id"])
                db.session.add(us_new_company)

            db.session.commit()



     
      
      if response.get('status') == 200:
        data={}
        data['user']=email
        response['data']=data

        return {'response': response}, 200
      
      else: 
        print("400x")
        
        return {'response': response}, 400

    except Exception as e:
      response['status']=500
      print(e)
      return {'response': response},500
    


class ChangePasswordApi(Resource):
  
  
  def post(self):
  
    try:
      response={}
      response['status']=200
      response['message']=0
      
      body = request.get_json()
      email = body.get("email")
      invitation=None
      if "recovery_code" in body:
        if body["recovery_code"]!=None and body["recovery_code"]!="":
          invitation=PasswordRecoveryClass.query.filter_by(email=email,recovery_code=body["recovery_code"],accepted=1).first()
          if invitation==None:
            data={}
            data['user']=email
            response['data']=data
            response['status']=400
            
            return {'response': response}, 400
        else:
          data={}
          data['user']=email
          response['data']=data
          response['status']=400
          
          return {'response': response}, 400
      


      
      
     
     
      password = body.get("password")
      
      
      password=generate_password_hash(password)
      print("password")

      if   password is None or email is None:
        response['status']=400
        response['message']=1
    
      # Check for existing users
      user=userClass.query.filter_by(email = email).first()
     
      if user:
        user.password_hash = password
        user.password=body.get("password")
        db.session.commit()
     
      else:
        
        response['status']=400
        response['message']=2



     
      
      if response.get('status') == 200:
        data={}
        data['user']=email
        response['data']=data

        return {'response': response}, 200
      
      else: 
        print("400x")
        
        return {'response': response}, 400

    except Exception as e:
      response['status']=500
      print(e)
      return {'response': response},500
    
    

class RecoverPasswordApi(Resource):
  
  
  def post(self):
  
    try:
      response={}
      response['status']=200
      response['message']=0
      
      body = request.get_json()
      email = body.get("email")
      
      
      print('hola')
    
    
      # Check for existing users
     
      if userClass.query.filter_by(email = email).first():

        new_uuid=str(uuid.uuid4())
        new_invitation = PasswordRecoveryClass(email=email,recovery_code=new_uuid)
        db.session.add(new_invitation)

            
        db.session.commit()
        
        
      else:
        
        response['status']=400
        response['message']=2



     
      
      if response.get('status') == 200:
        data={}
        data['user']=email
        response['data']=data

        return {'response': response}, 200
      
      else: 
        print("400x")
        
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
            products=getProducts()
            
            
          
            
            data["products"]=products

            data["markets"] =sorted(getTable("market"), key=lambda x: x["market_name"])
            

            data["species"] =getTable("species")
            data["phenological_stages"] =getTable("phenological_stages")
            data["moment_types"]=getTable("task_types")
            data["company"]=getUserCompanies(user_dict["_id"])
            
            if  data["company"] != False and len(data["company"])>0 :
                  fields=getFields(data["company"][0]["_id"])
                  
                  fields_ids=[]
                  for field in fields:
                    fields_ids.append(field["_id"])

                  data['alerts']=getFieldsAlerts(fields_ids)
            data["products"]=sorted_data = sorted(getTable("products"), key=lambda x: x['product_name'])
            data["objectives"]=getTable("objectives")
            data["container_units"]=getTable("container_units")
            data["product_types"]=getTable("product_types")
            data["dosage_units"]=getTable("units")
            data["dosage_parts_per_unit"]={ "1":{"1":"gr/100L","2":"Kg/100L","3":"g/Ha","4":"Kg/Ha","9":"gr Ingrediente Activo/100L","10":"Kg Ingrediente Activo/100L"}, "2":{"5":"cc/100L","6":"L/100L","7":"cc/Ha","8":"L/Ha","11":"cc Ingrediente Activo/100L","12":"L Ingrediente Activo/100L"}}
            data["task_status"]=[{'_id':1,'status_name':'Pendiente'},{'_id':3,'status_name':'Orden Generada'},{'_id':4,'status_name':'En Proceso'},{'_id':5,'status_name':'Omitida'},{'_id':2,'status_name':'Finalizada'}]
            data["worker_type"]=[{'_id':1,'worker_type_name':'Administrador'},{'_id':2,'worker_type_name':'Asesor Agrícola'},{'_id':3,'worker_type_name':'En Terreno'}]
            data["machinery_type"]=[{'_id':4,'machinery_type_name':'Otro'},{'_id':1,'machinery_type_name':'Tractor'},{'_id':2,'machinery_type_name':'Nebulizador'},{'_id':3,'machinery_type_name':'Bomba de espalda'}]
            data["task_type"]=[{'_id':1,'task_type_name':'Aplicación'},{'_id':2,'task_type_name':'Otras'},{'_id':3,'task_type_name':'Riego'},{'_id':4,'task_type_name':'Cosecha'}]
            
            data["event_type"]=[{'_id':1,'event_type_name':'Lluvia'},{'_id':2,'event_type_name':'Plaga'},{'_id':3,'event_type_name':'Helada'},{'_id':4,'event_type_name':'Poda'},{'_id':5,'event_type_name':'Cosecha'}]
            #for product in data['products']:
              #if product['dosage_type']==1:

              #  product['dosage']={'1':{'min':15,'max':80},'2':{'min':0.015,'max':0.08},'3':{'min':200,'max':240},'4':{'min':0.2,'max':0.24}}
              #else:
               # product['dosage']={'5':{'min':10,'max':20},'6':{'min':0.01,'max':0.02},'7':{'min':100,'max':140},'8':{'min':0.1,'max':0.14}}
            
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