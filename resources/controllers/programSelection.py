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




class ProgramApi(Resource):
  

  @jwt_required()
  def get(self):
  
    try:
      response={}
      response['status']=200
      response['message']=0
      
      user_id =  get_jwt_identity()
      program_id = request.args.get('id_program')

      data={}
      

      programs,assigned_companies,tasks=getProgramDetails(user_id,program_id)
      dic_result = {}

      for program in programs:
        id = program['_id']
        market = program['market_id']
        
        if id in dic_result:
            dic_result[id]["markets"].append(market)
        else:
            dic_result[id]={}
            dic_result[id]["id_user"] = program['id_user']
            dic_result[id]["program_name"] = program['program_name']
            dic_result[id]["id_species"] = program['id_species']
            dic_result[id]["markets"] = [market]
            dic_result[id]["published"] = program['published']
            dic_result[id]["updated_at"] = str(program['updated_at'])
      
      programs_format= [{'_id': id,'id_user': dict["id_user"],'program_name': dict["program_name"],'id_species': dict["id_species"] , 'markets': list(filter(None,set(dict["markets"]))),'published': dict["published"],'updated_at':dict["updated_at"]} for id, dict in dic_result.items()]
      program=""
      if len(programs_format)==0:
        response['status']=400
        response['message']=1
        
      else:
        program=programs_format[0]
      data["program_details"]=program
      
      
      
      #pt._id as _id,id_type,fecha_inicio,id_phenological_stage,validity_period,dosage,dosage_unit,objective,wetting,id_product

      
      task_ids= []
      for task in tasks:
        task_ids.append(task['_id'])

      print(task_ids)

      data["moments"]=[]
      for task_un in task_ids:
        if task_un not in data["moments"] and task_un is not None:
          data["moments"].append(task_un)


      #####
      dic_result = {}
      companies_ids= []
      data["assigned_companies"]=assigned_companies
      for companies in assigned_companies:
        companies_ids.append(companies['_id'])

    
      data["assigned_companies"]=list(filter(None,set(companies_ids)))





      #####
      
      
      response['data']=data
      
      
      if response.get('status') == 200:
        #return {'response': json.dumps(response.get('data'), default=datetimeJSONConverter)}, 200
        return {'response': response}, 200
      
      else: 
        return {'response': response}, 400

    except Exception as e:
      response['status']=400
      response['message']=2
      return {'response': response}, 500
  
  @jwt_required()
  def put(self):
  
    try:
        response={}
        response['status']=200
        response['message']=0
        body = request.get_json()

        
        
        id_program=request.args.get('id_program')
        program = updateProgram(id_program,body)  

        create_tasks =  createTasks(id_program,body)

        print("hola")
        print(id_program)
      
        data={}
        data['id_program']=id_program
        response['data']=data
        
        if response.get('status') == 200 and program != False:
            print("dds")

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



  @jwt_required()
  def post(self):
  
    try:
      response={}
      response['status']=200
      response['message']=0
      
      
      user_id =  get_jwt_identity()
      body = request.get_json()
      program_name = body["program_name"]
      species = body["species"]

      print(program_name)
      print(species)

      created = createProgram(program_name,user_id,species)
      if created== False:
        response['status']=400
        response['message']=1
      
      data={}
      data['id_program']=created
      response['data']=data
      
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
      response['status']=200
      response['message']=0
      

      user_id =  get_jwt_identity()
      program_id=request.args.get('id_program')

      print('fdsfdsf')
      deleted = deleteProgram(program_id,user_id)
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



class ProgramPublishApi(Resource):


  @jwt_required()
  def post(self):
  
    try:
      response={}
      response['status']=200
      response['message']=0
      
      
      
      #user_id =  get_jwt_identity()
      id_program = request.form.get("id_program")
      
      published = publishProgram(id_program)
      
      if published== False:
        response['status']=400
        response['message']=1
      
      data={}
      data['id_program']=published
      response['data']=data
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        
        return {'response': response}, 400

    except Exception as e:
      print(e)
      return {'response': response},500



class ProgramSelectionApi(Resource):
  
  
  
  @jwt_required()
  def get(self):
  
    try:
      
      response={}
      response['status']=200
      response['message']=0
      
      user_id =  get_jwt_identity()
      

      data={}
      
      
      user_company=getUserCompanies(user_id)
      print(user_company)
      companies="( "
      for company in user_company:
        companies=companies+str(company["_id"])+","
      companies = companies[:-1]
      companies=companies+" )"
      print(user_id)
      programs=getPrograms(user_id,companies)
      

      dic_result = {}

      # id,id_user,program_name,species_name,market_name
      
      for program in programs:
        id = program['_id']
        market = program['market_name']
        
        if id in dic_result:
            dic_result[id]["markets"].append(market)
        else:
            dic_result[id]={}
            dic_result[id]["id_user"] = program['id_user']
            dic_result[id]["program_name"] = program['program_name']
            dic_result[id]["species_name"] = program['species_name']
            dic_result[id]["markets"] = [market]
            dic_result[id]["published"] = program['published']
            dic_result[id]["updated_at"] = str(program['updated_at'])

      
      programs_format= [{'_id': id,'id_user': dict["id_user"],'program_name': dict["program_name"],'species_name': dict["species_name"] , 'markets':list(filter(None, dict["markets"])),'published': dict["published"],'updated_at':dict["updated_at"]} for id, dict in dic_result.items()]

      data["programs"]=programs_format
     
      response['data']=data
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        return {'response': response}, 400

    except Exception as e:
      print(e)
      return {'response': response}, 400
  
  
  
  
  
