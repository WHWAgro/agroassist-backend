from flask import Response, request
from flask_restful import Resource
import json
from datetime import datetime
#import pandas as pd
#from get_project_root import root_path
from resources.errors import  InternalServerError
from database.models.Program import ProgramClass,db
from resources.services.programServices import *
from flask_jwt_extended import jwt_required,get_jwt_identity
from sqlalchemy.orm import class_mapper



class FieldsListApi(Resource):
  

  @jwt_required()
  def get(self):
  
    try:
      response={}
      response['status']=200
      response['message']=0
      program_id=request.args.get('id_company')

      
      fields = getFields(program_id)
      
      if fields== False:
        response['status']=400 
        response['message']=1
      

      data={}
      data['fields']=fields
      response['data']=data
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        
        return {'response': response}, 400

    except Exception as e:
      print(e)
      response['message']=2
      return {'response': response},500
    

class TaskApi(Resource):
  

  @jwt_required()
  def get(self):
  
    try:
        response={}
        response['status']=200
        response['message']=0
        id_task=request.args.get('id_task')

        print(1222)
        tasks=getTaskDetails(id_task)
        print(44444)
        dic_result = {}
        if tasks==False:
            response['status']=400
            response['message']=1
            response['data']={}
            return {'response': response}, 400
        for task in tasks:
            id = task['_id']
            products = task['id_product']
            
            if id in dic_result:
                dic_result[id]["products"].append(products)
            else:
                dic_result[id]={}
                dic_result[id]["id_program"] = task['id_program']
                dic_result[id]["id_type"] = task["id_type"] 
                dic_result[id]["start_date"] = task['start_date']
                dic_result[id]["id_phenological_stage"] = task['id_phenological_stage']
                dic_result[id]["products"] = [products]
                dic_result[id]["validity_period"] = task['validity_period']
                dic_result[id]["dosage"] = task['dosage']
                dic_result[id]["dosage_unit"] = task['dosage_unit']
                dic_result[id]["objective"] = task['objective']
                dic_result[id]["wetting"] = task['wetting']

        print(dic_result)


        
        data={}
        tasks_format= [{'_id': id,'id_program': dict["id_program"],'id_type': dict["id_type"],'start_date': dict["start_date"],'id_phenological_stage': dict["id_phenological_stage"] , 'products': list(filter(None,dict["products"])),'validity_period': dict["validity_period"],'dosage': dict["dosage"],'objective': dict["objective"],'wetting': dict["wetting"]} for id, dict in dic_result.items()]
        if len(tasks_format)==0:
            response['status']=400
            response['message']=1
        
        else:
            task=tasks_format[0]
            data["task_details"]=task
            
            
      
      


        response['data']=data
        
        if response.get('status') == 200:

            return {'response': response}, 200
        
        else: 
            
            return {'response': response}, 400

    except Exception as e:
      print(e)
      response['message']=2
      response['status']=500
      return {'response': response},500




  @jwt_required()
  def post(self):
  
    try:
        response={}
        response['status']=200
        response['message']=0
        body = request.get_json()

        products = body.get('products')

        task = createTask(body)    
      
      
        data={}
        data['id_task']=task
        response['data']=data
        
        if response.get('status') == 200:

            return {'response': response}, 200
        
        else: 
            
            return {'response': response}, 400

    except Exception as e:
      print(e)
      response['message']=2
      response['status']=500
      return {'response': response},500
    


  @jwt_required()
  def put(self):
  
    try:
        response={}
        response['status']=200
        response['message']=0
        body = request.get_json()

        

        id_task=request.args.get('id_task')
        task = updateTask(id_task,body)    

      
        data={}
        data['id_task']=task
        response['data']=data
        
        if response.get('status') == 200:

            return {'response': response}, 200
        
        else: 
            
            return {'response': response}, 400

    except Exception as e:
      print(e)
      response['message']=2
      response['status']=500
      return {'response': response},500
    

  @jwt_required()
  def delete(self):
  
    try:
      response={}
      response['status']=500
      response['status']=200
      response['message']=0
      

      
      id_task=request.args.get('id_task')

      
      deleted = deleteTask(id_task)
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