from flask import Response, request
from flask_restful import Resource
#from bson.json_util import dumps
from pathlib import Path
import json
from datetime import datetime
#from sshtunnel import SSHTunnelForwarder
#from get_project_root import root_path
from resources.errors import InternalServerError
from database.models.Program import ProgramClass
#from database.models.ProgramTasks import ProgramTasksClass
from resources.services.programServices import *
from flask_jwt_extended import jwt_required,get_jwt_identity



class CalendarApi(Resource):
  
  @jwt_required()
  def get(self):
  
    try:
      
      response={}
      response['status']=200
      response['message']=0
      
      user_id =  get_jwt_identity()
      

      data={}
      
      field = request.args.get('id_field')

      company=getCompanyFromField(field)
      if company== False:
        response['status']=400
        response['message']=1

      tasks=getTasks(company[0]['company_id'])
      if tasks== False:
        response['status']=400
        response['message']=1

      
      # id,id_user,program_name,species_name,market_name

      tasks_format=[]

        
      
      for task in tasks:
        result={}
        result['_id']= task['_id']
        result['date_start']= str(task['date_start'])
        result['date_end']= str(task['date_end'])
        result['id_task_type']= task['id_task_type']
        result['time_indicator']= task['time_indicator']
        result['status']= task['status']

        tasks_format.append(result)

   
      data["tasks"]=tasks_format
     
      response['data']=data
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        return {'response': response}, 400

    except Exception as e:
      print(e)
      return {'response': response}, 400
    

class TaskInsApi(Resource):
  

  @jwt_required()
  def get(self):
  
    try:
      
        response={}
        response['status']=200
        response['message']=0
        
        user_id =  get_jwt_identity()
        

        data={}
        
        task = request.args.get('id_task')

      
      

        task_info=getTask(task)
        data={}
        if len(task_info)>0:
            task_details=task_info[0]
           
            
            tasks=getTaskDetails(task_details['id_moment'])
            
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
                
                dosage_parts_per_unit=ast.literal_eval(task['dosage_parts_per_unit'])
                objectives= task['id_objective']
                if id in dic_result:
                    dic_result[id]["objectives"].append(objectives)
                    dic_result[id]["products"].append(products)
                    dic_result[id]["dosage"].append(dosage)
                    
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
                    
                    dic_result[id]["dosage_parts_per_unit"]=[dosage_parts_per_unit]
                    
                    dic_result[id]["wetting"] = task['wetting']
                    dic_result[id]["observations"] = task['observations']

        



        
        
            tasks_format= [{'id_moment_type': dict["id_moment_type"],'moment_value': dict["moment_value"] ,'objectives': list(filter(None,dict["objectives"])) ,'products': list(filter(None,dict["products"])),'dosage': list(filter(None,dict["dosage"])),'dosage_parts_per_unit': list(filter(None,dict["dosage_parts_per_unit"])),'wetting': dict["wetting"],'observations':dict['observations']} for id, dict in dic_result.items()]
            print(tasks_format)
            result={}
            result['_id']= task_details['_id']
            result['date_start']= str(task_details['date_start'])
            result['date_end']= str(task_details['date_end'])
            result['id_task_type']= task_details['id_task_type']
            result['time_indicator']= task_details['time_indicator']
            result['status']= task_details['status']
            result['cuarteles']= []
        
        
            if len(tasks_format)==0:
                response['status']=400
                response['message']=1
        
            else:
                for ind,val in tasks_format[0].items():
                    result[ind]=val
                
                data["task_details"]=result  

      
      # id,id_user,program_name,species_name,market_name

      
   
      
     
        response['data']=data
        
        if response.get('status') == 200:

            return {'response': response}, 200
        
        else: 
            return {'response': response}, 400

    except Exception as e:
      print(e)
      return {'response': response}, 400
    

  @jwt_required()
  def put(self):
  
    try:
        response={}
        response['status']=200
        response['message']=0
        body = request.get_json()

        
        
        id_task=request.args.get('id_task')
        task = updateTaskIns(id_task,body)  

       

      
        data={}
       
        
        if response.get('status') == 200 and task != False:
            print("dds")
            data['id_task']=id_task
            response['data']=data

            return {'response': response}, 200
        
        else: 
            
            response['status']=400
            response['message']=1
            
            return {'response': response}, 400
    except Exception as e:
      print(e)
      response['message']=2
      response['status']=500
      return {'response': response},500
    


class WeatherApi(Resource):
  
  @jwt_required()
  def get(self):
  
    try:
      
      response={}
      response['status']=200
      response['message']=0
      
      user_id =  get_jwt_identity()
      

      data={}
      
      field = request.args.get('id_field')

      

      weather=[
          {
            "date": '2023-08-24',
            "description": 'Despejado',
            "icon":'icono_1',
            "temperature": { "min": '0', "max": '15' },
            "wind": "10",
            "humidity": "30",
          },
          {
            "date": '2023-08-25',
            "description": 'Nubes',
            "icon":'icono_2',
            "temperature": { "min": '-1', "max": '17' },
            "wind": "20",
            "humidity": "35",
          },
          {
            
            "date": '2023-08-26',
            "description": 'Lluvia',
            "icon":'icono_3',
            "temperature": { "min": '-1', "max": '12' },
            "wind": "35",
            "humidity": "65",
          },
          {
            "date": '2023-08-27',
            "description": 'Lluvia',
            "icon": 'icono_3',
            "temperature": { "min": '-1', "max": '19' },
            "wind": "21",
            "humidity": "70",
          },
          {
            "date": '2023-08-28',
            "description": 'Lluvia',
            "icon":'icono_3',
            "temperature": { "min": '-1', "max": '20' },
            "wind": "14",
            "humidity": "72",
          },
          
      ]
      
     

   
      data["forecast"]=weather
     
      response['data']=data
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        return {'response': response}, 400

    except Exception as e:
      print(e)
      return {'response': response}, 400