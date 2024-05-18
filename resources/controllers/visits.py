from flask import Response, request,send_file
from flask_restful import Resource
import json
from datetime import datetime
#import pandas as pd
#from get_project_root import root_path
from resources.errors import  InternalServerError
from database.models.Program import ProgramClass,db
from resources.services.programServices import *
from flask_jwt_extended import jwt_required,get_jwt_identity
from functools import reduce
from itertools import chain
from resources.services.programServices import *
from resources.services.generatePDF import *



class VisitTaskApi(Resource):
  

  @jwt_required()
  def post(self):
  
    try:
      response={}
      response['status']=500
      response['message']=0
      
      
      user_id =  get_jwt_identity()
      body = request.get_json()
      date_start=body['date_start']
      date_end=body['date_end']
      observations=body['observations']
      wetting=0
      objectives=0
      products=0
      dosage=0
      dosage_parts_per_unit=0
      
      if body['task_type_id']==1:
        wetting=body['wetting']
        objectives=body['objectives']
        products=body['products']
        dosage=body['dosage']
        dosage_parts_per_unit=body['dosage_parts_per_unit']




      created=4
      
      if created== False:
        response['status']=400
        response['message']=1
      
      data={}
      data['task_id']=created
      response['data']=data

      response['status']=200
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        
        return {'response': response}, 400

    except Exception as e:
      print(e)
      return {'response': response},500

  @jwt_required()
  def put(self):
  
    try:
      
      visit_id=request.args.get('task_id')
      response={}
      response['status']=500
      response['message']=0
      
      
      user_id =  get_jwt_identity()
      body = request.get_json()
      date_start=body['date_start']
      date_end=body['date_end']
      observations=body['observations']
      wetting=0
      objectives=0
      products=0
      dosage=0
      dosage_parts_per_unit=0
      
      if body['task_type_id']==1:
        wetting=body['wetting']
        objectives=body['objectives']
        products=body['products']
        dosage=body['dosage']
        dosage_parts_per_unit=body['dosage_parts_per_unit']


      updated=visit_id
      data={}
      response['status']=200
      if response.get('status') == 200 and updated != False:
            
            data['task_id']=request.args.get('task_id')
            response['data']=data
      if updated== False:
        response['status']=400
        response['message']=1
      
      
      
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        
        return {'response': response}, 400

    except Exception as e:
      print(e)
      return {'response': response},500
  
  
  @jwt_required()
  def delete(self):
  
    try:
      response={}
      response['status']=500
      response['status']=200
      response['message']=0
      

      print('hola')
      task_id=request.args.get('task_id')

      
      deleted=True
      if deleted== False:
        response['status']=400 
        response['message']=1
      

      data={}
      response['data']=data
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        
        return {'response': response}, 400

    except Exception as e:
      print(e)
      return {'response': response},500
    
  @jwt_required()
  def get(self):
  
    try:
      
      response={}
      response['status']=200
      response['message']=0
      
      user_id =  get_jwt_identity()
      

      data={}
      
      ##programs=getPrograms(user_id,companies)
      
      task_id=request.args.get('task_id')
     
      
    
      if int(task_id)==1:
        print('entro')

        task_details= {"editable":True,
                     "_id": 1,
                    "task_type_id": 2,
                    "date_start": "2024-05-25",
                    "date_end": "2024-05-29",
                    "observations": "no usar en dias con luna llena"
                }
      else:
        print('no entro')
        task_details= {"editable":True,"_id": 4,
                    "task_type_id": 1,
                    "date_start": "2024-05-25",
                    "date_end": "2024-05-29",
                    "objectives": [1,2],
                    "products": [[[5],[1]],[[1]]],
                    "dosage": [[[10],[5.4]],[[20]]],
                    "dosage_parts_per_unit": [[[1],[1]],[[2],]],
                    "wetting": 400,
                    "observations": "no usar en dias con luna llena"
                }
      
      data['task_details']=task_details
     
      response['data']=data
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        return {'response': response}, 400

    except Exception as e:
      print(e)
      return {'response': response}, 400







class VisitApi(Resource):
  

  @jwt_required()
  def post(self):
  
    try:
      response={}
      response['status']=200
      response['message']=0
      
      
      user_id =  get_jwt_identity()
      body = request.get_json()
      company_id = body["company_id"]
      if company_id == -1:
        company_name = 'new company'
     
      field_id = body["field_id"]
      if field_id == -1:
        field_name = 'new field'

      created=3
      
      if created== False:
        response['status']=400
        response['message']=1
      
      data={}
      data['visit_id']=created
      response['data']=data
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        
        return {'response': response}, 400

    except Exception as e:
      print(e)
      return {'response': response},500

  @jwt_required()
  def put(self):
  
    try:
      response={}
      response['status']=200
      response['message']=0
      
      
      user_id =  get_jwt_identity()
      body = request.get_json()
      print(body)
      visit_id=request.args.get('visit_id')


      updated=visit_id
      data={}
      if response.get('status') == 200 and updated != False:
            
            data['visit_id']=request.args.get('visit_id')
            response['data']=data
      if updated== False:
        response['status']=400
        response['message']=1
      
      
      
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        
        return {'response': response}, 400

    except Exception as e:
      print(e)
      return {'response': response},500
  
  
  @jwt_required()
  def delete(self):
  
    try:
      response={}
      response['status']=500
      response['status']=200
      response['message']=0
      

      
      visit_id=request.args.get('visit_id')

      
      deleted=True
      if deleted== False:
        response['status']=400 
        response['message']=1
      

      data={}
      response['data']=data
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        
        return {'response': response}, 400

    except Exception as e:
      print(e)
      return {'response': response},500
    
  @jwt_required()
  def get(self):
  
    try:
      
      response={}
      response['status']=200
      response['message']=0
      
      user_id =  get_jwt_identity()
      

      data={}
      
      ##programs=getPrograms(user_id,companies)
      
      visit_id=request.args.get('visit_id')
     
      visits={'editable':True,'_id':1,'company_id':1,'company_name':'compania 1','field_id':1,'field_name':'campo 1','date':'2024-05-10','created_by':'asesor 1','user_id':1,'tasks':[1]}
      
      
      data={}
      data['visit_details']=visits
     
      response['data']=data
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        return {'response': response}, 400

    except Exception as e:
      print(e)
      return {'response': response}, 400




class VisitListApi(Resource):
  
  
  
  @jwt_required()
  def get(self):
  
    try:
      
      response={}
      response['status']=200
      response['message']=0
      
      user_id =  get_jwt_identity()
      

      data={}
      
      
      user_company=getUserCompanies(user_id)
  
      companies="( "
      for company in user_company:
        companies=companies+str(company["_id"])+","
      companies = companies[:-1]
      companies=companies+" )"
      print(user_id)
      ##programs=getPrograms(user_id,companies)
      

     
      visits=[{'_id':1,'field_id':1,'field_name':'campo 1','date':'2024-05-10','created_by':'asesor 1'},{'_id':2,'field_id':-1,'field_name':'campo extra','date':'2024-05-15','created_by':'asesor 1'}]
      
      
      data["visits"]=visits
     
      response['data']=data
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        return {'response': response}, 400

    except Exception as e:
      print(e)
      return {'response': response}, 400