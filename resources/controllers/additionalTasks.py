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
from resources.services.additionalTasksServices import *



class AdditionalTaskApi(Resource):
  

  @jwt_required()
  def post(self):
  
    try:
      response={}
      response['status']=500
      response['message']=0
      
      
      user_id =  get_jwt_identity()
      body = request.get_json()
      company_id=getUserCompanies(user_id)[0]["_id"]
      body['company_id']=company_id
      
      

      print('creando task de visita')


      created,rep_task=createAdditionalTask(body,user_id)
      
      if created== False:
        response['status']=400
        response['message']=1
      
      data={}
      data['task_id']=created     
      data['rep_task_id']=rep_task
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
    
      company_id=getUserCompanies(user_id)[0]["_id"]
      body['company_id']=company_id

      updated=updateAdditionalTask(task_id,body,user_id)
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
  def get(self):
  
    try:
      
      response={}
      response['status']=200
      response['message']=0
      
      user_id =  get_jwt_identity()
      

      data={}
      
      ##programs=getPrograms(user_id,companies)

      print('getting info')
      
      task_id=request.args.get('task_id')

      
      task_info=getAdditionalTaskInfo(task_id)
      if task_info==False:
        return {'response': response}, 400
      print('hola')
      print(task_info)
      del(task_info['created_at'])

      task_info['date_start']=task_info['date_start'].strftime('%Y-%m-%d')
      task_info['date_end']=task_info['date_end'].strftime('%Y-%m-%d')
      task_info['plots']=ast.literal_eval(task_info['plots'])

      if task_info['task_type_id'] !=1:
        del(task_info['wetting'])
        del(task_info['dosage_parts_per_unit'])
        del(task_info['objectives'])
        del(task_info['products'])
        del(task_info['products_phis'])
        del(task_info['reentry'])
        del(task_info['dosage'])
        if task_info['is_repeatable']==True:
          task_info['repeat_until']=task_info['repeat_until'].strftime('%Y-%m-%d')
        else:
          del(task_info['repeat_until'])
          del(task_info['repeat_frequency'])
          del(task_info['repeat_unit'])
      else:
        if task_info['is_repeatable']==True:
          task_info['repeat_until']=task_info['repeat_until'].strftime('%Y-%m-%d')
        else:
          del(task_info['repeat_until'])
          del(task_info['repeat_frequency'])
          del(task_info['repeat_unit'])
        task_info['dosage_parts_per_unit']=ast.literal_eval(task_info['dosage_parts_per_unit'])
        task_info['objectives']=ast.literal_eval(task_info['objectives'])
        task_info['products']=ast.literal_eval(task_info['products'])
        task_info['dosage']=ast.literal_eval(task_info['dosage'])
        task_info['products_phis']=ast.literal_eval(task_info['products_phis'])


      print('chao')
      
      
      editable=False
      if user_id== task_info['user_id']:
        editable=True

    

      task_info['editable']=editable
      task_info['out_platform']=False
     
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




