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
        id_moment=request.args.get('id_moment')

        tasks=getTaskDetails(id_moment)
        
        dic_result = {}
        if tasks==False:
            response['status']=400
            response['message']=1
            response['data']={}
            return {'response': response}, 400
        for task in tasks:
            id = task['_id']
            products = ast.literal_eval(task['id_product'])
            dosage = ast.literal_eval(task['dosage'])
            max_applications = ast.literal_eval(task['max_applications'])
            dosage_parts_per_unit=ast.literal_eval(task['dosage_parts_per_unit'])
            objectives= task['id_objective']
            if id in dic_result:
                dic_result[id]["objectives"].append(objectives)
                dic_result[id]["products"].append(products)
                dic_result[id]["dosage"].append(dosage)
                dic_result[id]["max_applications"].append(max_applications)
                dic_result[id]["dosage_parts_per_unit"].append(dosage_parts_per_unit)
            else:
                dic_result[id]={}
                dic_result[id]["id_program"] = task['id_program']
                dic_result[id]["id_moment_type"] = task["id_moment_type"] 
                dic_result[id]["start_date"] = str(task['start_date'])
                dic_result[id]["moment_value"] = task['moment_value']
                dic_result[id]["objectives"] = [objectives]
                dic_result[id]["products"] = [products]
                dic_result[id]["dosage"] = [dosage]
                dic_result[id]["max_applications"] = [max_applications]
                dic_result[id]["dosage_parts_per_unit"]=[dosage_parts_per_unit]
                
                dic_result[id]["wetting"] = task['wetting']
                dic_result[id]["observations"] = task['observations']

        print(dic_result)



        
        data={}
        tasks_format= [{'_id': id,'id_program': dict["id_program"],'id_moment_type': dict["id_moment_type"],'start_date': dict["start_date"],'moment_value': dict["moment_value"] ,'objectives': list(filter(None,dict["objectives"])) ,'products': list(filter(None,dict["products"])),'dosage': list(filter(None,dict["dosage"])),'max_applications': list(filter(None,dict["max_applications"])),'dosage_parts_per_unit': list(filter(None,dict["dosage_parts_per_unit"])),'wetting': dict["wetting"],'observations':dict['observations']} for id, dict in dic_result.items()]
        
        
        if len(tasks_format)==0:
            response['status']=400
            response['message']=1
        
        else:
            task=tasks_format[0]
            data["moment_details"]=task
            
            
      
      


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
        data['id_moment']=task
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

        

        id_moment=request.args.get('id_moment')
        task = updateTask(id_moment,body)    

      
        data={}
        data['id_moment']=task
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
      

      
      id_moment=request.args.get('id_moment')

      
      deleted = deleteTask(id_moment)
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