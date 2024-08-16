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

      tasks=getTasks2(company[0]['company_id'],field)
      if tasks== False:
        response['status']=400
        response['message']=1

      
      # id,id_user,program_name,species_name,market_name

      tasks_format=[]

        
      field_plots=getFieldPlotsDetails(field)
      field_plots_ids=[]
      for plot in field_plots:
        field_plots_ids.append(plot["_id"])
      print("field plots:")
      print(field_plots_ids)
      print("-------")

      visit_tasks=getVisitTasks(company[0]['company_id'],field)
      print(visit_tasks)
      tasks=tasks+visit_tasks
        
      for task in tasks:
        result={}
        result['_id']= task['_id']
        result['date_start']= str(task['date_start'])
        result['date_end']= str(task['date_end'])
        result['id_task_type']= task['id_task_type']
        result['time_indicator']= task['time_indicator']
        result['id_status']= task['id_status']
        result['from_program']= task['from_program']
        
        task_plots=[]
        
        aux_plots=getTaskPlots2(task['_id'],task['from_program'])
        
        if aux_plots !=False and len(aux_plots)>0:
           
           for a in aux_plots:
              task_plots.append(a['_id'])
        shared_elements = set(field_plots_ids) & set(task_plots)
       
        count_shared_elements = len(shared_elements)
        print("task plots:")
        
        if count_shared_elements==0:
           continue
        result['plots']=list(shared_elements)
        
        
        print(task_plots)
        
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
        print('*******begin*****')
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
         
            tasks=[]
            
            print(task_details)
            if task_details['from_program']==True:
              
              tasks=getTaskDetails(task_details['id_moment'])
            else:
               tasks=getVisitTaskDetails(task_details['id_moment'])


            print('hola///////*************')
            print(tasks)

            dic_result = {}
            if tasks==False:
                
                response['status']=400
                response['message']=1
                response['data']={}
                return {'response': response}, 400
            
            for task in tasks:
                print('---======-------======-')
                print(task)
                id = task['_id']

                products=None
                dosage=None
                dosage_parts_per_unit=None
                objectives=None

                objectives_name=''
                products_ingredients=None
                products_name=None


                
                if task['id_product']!=None:
                  products = ast.literal_eval(task['id_product'])
                  dosage = ast.literal_eval(task['dosage'])
                  products_ingredients=ast.literal_eval(task['products_ingredients'])
                  products_name=ast.literal_eval(task['products_name'])
                  
                  dosage_parts_per_unit=ast.literal_eval(task['dosage_parts_per_unit'])
                  
                  if task_details['from_program']==True:
                    objectives= task['id_objective']
                    objectives_name=task['objective_name']
                  else:
                    objectives= ast.literal_eval(task['id_objective'])
                    objectives_name=ast.literal_eval(task['objective_name'])
                  print('tiene productos')
                else:
                   print('no tiene productos')

                
                
                if id in dic_result:
                    
                    dic_result[id]["objectives"].append(objectives)
                    dic_result[id]["objectives_name"].append(objectives_name)
                    dic_result[id]["products"].append(products)
                    dic_result[id]["dosage"].append(dosage)
                    dic_result[id]["products_ingredients"].append(products_ingredients)
                    dic_result[id]["products_name"].append(products_name)
                    
                    dic_result[id]["dosage_parts_per_unit"].append(dosage_parts_per_unit)
                else:
                    if task_details['from_program']==True:
                      dic_result[id]={}
                      dic_result[id]["id_program"] = task['id_program']
                      dic_result[id]["id_moment_type"] = task["id_moment_type"] 
                      dic_result[id]["start_date"] = str(task['start_date'])
                      
                      dic_result[id]["moment_value"] = task['moment_value']
                      
                      print('is from program')
                      dic_result[id]["objectives"] = [objectives]
                      dic_result[id]["objectives_name"] = [objectives_name]
                      dic_result[id]["products"] = [products]
                      dic_result[id]["products_name"] = [products_name]
                      dic_result[id]["products_ingredients"] = [products_ingredients]
                      dic_result[id]["dosage"] = [dosage]
                      
                      dic_result[id]["dosage_parts_per_unit"]=[dosage_parts_per_unit]
                      
                      dic_result[id]["wetting"] = task['wetting']
                      dic_result[id]["phi"] = task['phi']
                      dic_result[id]["reentry"] = task['reentry']
                      dic_result[id]["observations"] = task['observations']
                    else:
                      print('is not from program')
                      dic_result[id]={}
                      dic_result[id]["id_program"] = task['id_program']
                      dic_result[id]["id_moment_type"] = task["id_moment_type"] 
                      dic_result[id]["start_date"] = str(task['start_date'])
                      
                      dic_result[id]["moment_value"] = task['moment_value']

                      print('is not from program2')
                      if dic_result[id]["id_moment_type"] ==1:
                        dic_result[id]["objectives"] = objectives
                        dic_result[id]["objectives_name"] = objectives_name
                        dic_result[id]["products"] = products
                        dic_result[id]["products_name"] = products_name
                        dic_result[id]["products_ingredients"] = products_ingredients
                        dic_result[id]["dosage"] = dosage
                        
                        dic_result[id]["dosage_parts_per_unit"]=dosage_parts_per_unit
                      else:
                        dic_result[id]["objectives"] = []
                        dic_result[id]["objectives_name"] = []
                        dic_result[id]["products"] = []
                        dic_result[id]["products_name"] = []
                        dic_result[id]["products_ingredients"] = []
                        dic_result[id]["dosage"] = []
                        
                        dic_result[id]["dosage_parts_per_unit"]=[]
                      print('is not from program3')
                      dic_result[id]["wetting"] = task['wetting']
                      dic_result[id]["phi"] = 0
                      dic_result[id]["reentry"] = 0
                      dic_result[id]["observations"] = task['observations']

        

            
            print('paso 2')
            print(dic_result)
            
        
            tasks_format= [{'id_moment_type': dict["id_moment_type"],'moment_value': dict["moment_value"] ,"objectives_name":dict["objectives_name"],"products_name":dict["products_name"],"products_ingredients":dict["products_ingredients"]  ,'objectives': dict["objectives"] ,'products': list(filter(None,dict["products"])),'dosage': list(filter(None,dict["dosage"])),'dosage_parts_per_unit': list(filter(None,dict["dosage_parts_per_unit"])),'wetting': dict["wetting"],'phi': dict["phi"],'reentry': dict["reentry"],'observations':dict['observations']} for id, dict in dic_result.items()]
            print('paso 2 y medio')
            result={}
            result['_id']= task_details['_id']
            result['date_start']= str(task_details['date_start'])
            result['date_end']= str(task_details['date_end'])
            result['id_task_type']= task_details['id_task_type']
            result['time_indicator']= task_details['time_indicator']
            result['id_status']= task_details['id_status']
            result['id_program']=None
            result['id_species']=None
            result['from_program']=task_details['from_program']
            task_plots=[]

            print('paso 3')
           
            
            aux_plots=getTaskPlots2(task_details['_id'],task_details['from_program'])
            if aux_plots !=False and len(aux_plots)>0:

              result['id_program']= aux_plots[0]['id_program']
              if task_details['from_program']==False:
                result['id_program']=task_details['id_program']
              result['id_species']= aux_plots[0]['id_species']
              for a in aux_plots:
                  task_plots.append(a['_id'])

            taskOrderFile,current_plot = getTaskOrdersNewFormat(task_details['_id'])
            print(taskOrderFile)
            
            print('paso 4')
        
            result['plots']=task_plots
           
            print('&&&&&&&&& task format')
            print(tasks_format)
        
        
            if len(tasks_format)==0:
                response['status']=400
                response['message']=1
        
            else:
                for ind,val in tasks_format[0].items():
                    result[ind]=val
                
                result['task_orders']=taskOrderFile
                data["task_details"]=result  

      
      # id,id_user,program_name,species_name,market_name

        products_list=data['task_details']['products']
        products_name=data['task_details']['products_name']
        data['task_details']['products_alt']=getProductsAlt(products_list,products_name)
        
   
      
     
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
      weather_raw=getFieldForecast(field)

      weather_format=[]
      
      icon_map={"1":"sunny","2":"sunny","3":"sunny","4":"sunny","5":"sunny","6":"cloudy","7":"cloudy","8":"cloudy","9":"cloudy","10":"cloudy","11":"cloudy",
                "12":"rainy",
                "13":"rainy","14":"rainy","15":"rainy","16":"rainy","17":"rainy","18":"rainy","19":"cloudy","20":"cloudy","21":"sunny",
                "22":"snowy","23":"snowy","24":"snowy",
                "25":"snowy","26":"snowy","27":"snowy","28":"snowy","29":"snowy"
                
                }
      for day in weather_raw:
         weather_format.append({
           "date": day["date"],
            "description": day["description"],
            "icon": icon_map[str(day["icon"])],
            "temperature": { "min": str(day["temperature_min"]), "max": str(day["temperature_max"]) },
            "wind": str(day["wind"]),
            "humidity": str(day["humidity"])
         })
         
      


      weather=[
          
           
           
            {
            "date": '2024-04-12',
            "description": 'Nublado',
            "icon": 'cloudy',
            "temperature": { "min": '7', "max": '19' },
            "wind": "7",
            "humidity": "13"
          },
          {
            "date": '2024-04-13',
            "description": 'Nublado',
            "icon": 'cloudy',
            "temperature": { "min": '8', "max": '18' },
            "wind": "7",
            "humidity": "25"
          },
          {
            "date": '2024-04-14',
            "description": 'Lluvia',
            "icon":'rainy',
            "temperature": { "min": '9', "max": '18' },
            "wind": "57",
            "humidity": "9"
          },
          {
            
            "date": '2024-04-15',
            "description": 'Soleado',
            "icon":'sunny',
            "temperature": { "min": '7', "max": '17' },
            "wind": "6",
            "humidity": "90"
          },
          {
            "date": '2024-04-16',
            "description": 'Soleado',
            "icon": 'sunny',
            "temperature": { "min": '4', "max": '21' },
            "wind": "7",
            "humidity": "9"
          },
          {
            "date": '2024-04-17',
            "description": 'Soleado',
            "icon": 'sunny',
            "temperature": { "min": '5', "max": '22' },
            "wind": "7",
            "humidity": "9"
          }
        
          
      ]
      
   
      data["forecast"]=weather_format
      
     
      response['data']=data
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        return {'response': response}, 400

    except Exception as e:
      print(e)
      return {'response': response}, 400