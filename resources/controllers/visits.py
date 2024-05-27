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
from resources.services.visitServices import *



class VisitTaskApi(Resource):
  

  @jwt_required()
  def post(self):
  
    try:
      response={}
      response['status']=500
      response['message']=0
      
      
      user_id =  get_jwt_identity()
      body = request.get_json()
      
      

      print('creando task de visita')


      created=createVisitTask(body)
      
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
      
      task_id=request.args.get('task_id')
      response={}
      response['status']=500
      response['message']=0
      
      
      user_id =  get_jwt_identity()
      body = request.get_json()
    
     
      
      


      updated=updateVisitTask(task_id,body)
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

      
      deleted=deleteVisitTask(task_id)
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

      
      task_info=getVisitTaskInfo(task_id)

      task_info['date_start']=task_info['date_start'].strftime('%Y-%m-%d')
      task_info['date_end']=task_info['date_end'].strftime('%Y-%m-%d')
      task_info['plots']=ast.literal_eval(task_info['plots'])

      if task_info['task_type_id'] !=1:
        del(task_info['wetting'])
        del(task_info['dosage_parts_per_unit'])
        del(task_info['objectives'])
        del(task_info['products'])
        del(task_info['dosage'])
      else:
        
        task_info['dosage_parts_per_unit']=ast.literal_eval(task_info['dosage_parts_per_unit'])
        task_info['objectives']=ast.literal_eval(task_info['objectives'])
        task_info['products']=ast.literal_eval(task_info['products'])
        task_info['dosage']=ast.literal_eval(task_info['dosage'])



      visit_info=getVisitInfo(task_info['visit_id'])
      
      editable=False
      if user_id== visit_info['user_id']:
        editable=True

      out_platform=False
      if  visit_info['company_id']==-1:
        out_platform=True

      task_info['editable']=editable
      task_info['out_platform']=out_platform
     
      print(task_info)
      
    
      
      
      data['task_details']=task_info
     
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
     

      created=createVisit(user_id,body)
      
      if created== False:
        response['status']=400
        response['message']=1
      
      data={}
      data['visit_id']=created
      response['data']=data
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        response['status']=400
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


      updated=updateVisit(user_id,visit_id,body)
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
      #ToDo verificar que el que borra sea el usuario que crea
      deleteVisit(visit_id)
      70
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
      visit_info=getVisitInfo(visit_id)
      visit_tasks=getVisitTasks(visit_id)
      print(visit_info)
      print(visit_tasks)
      editable=False
      if user_id== visit_info['user_id']:
        editable=True
      
      visit={'editable':editable,'_id':visit_id,
              'company_id':visit_info['company_id'],'company_name':visit_info['company_name'],
              'field_id':visit_info['field_id'],'field_name':visit_info['field_name'],
              'date':visit_info['created_at'].strftime('%Y-%m-%d'),
              'created_by':visit_info['user_name'],'user_id':visit_info['user_id'],'tasks':visit_tasks,"company_mail":visit_info['company_mail']}
      
      
      data={}
      data['visit_details']=visit
     
      response['data']=data
      
      if response.get('status') == 200 and visit_info!=False and visit_tasks !=False:

        return {'response': response}, 200
      
      else: 
        response['status']=400
        return {'response': response}, 400

    except Exception as e:
      print(e)
      response['status']=400
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
      
      
      user_company=[getUserCompanies(user_id)[0]]
      print(user_company)
  
      companies="( "
      for company in user_company:
        companies=companies+str(company["_id"])+","
      companies = companies[:-1]
      companies=companies+" )"
      print(user_id)
      print(companies)
      ##programs=getPrograms(user_id,companies)

      visits=getVisits(user_id,companies)

      for visit in visits:
        visit['date']=visit['date'].strftime('%Y-%m-%d')


      
      
      data["visits"]=visits
     
      response['data']=data
      
      if response.get('status') == 200:
        

        return {'response': response}, 200
      
      else: 
        response['status']=400
        return {'response': response}, 400

    except Exception as e:
      response['status']=400
      return {'response': response}, 400
    
class VisitPublishApi(Resource):

  @jwt_required()
  def put(self):
  
    try:
      response={}
      response['status']=200
      response['message']=0
      
      
      user_id =  get_jwt_identity()
      visit_id=request.args.get('visit_id')


      updated=publishVisit(user_id,visit_id)
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