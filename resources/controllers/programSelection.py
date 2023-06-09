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
      

      programs,assigned_fields,tasks=getProgramDetails(user_id,program_id)
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

      
      programs_format= [{'_id': id,'id_user': dict["id_user"],'program_name': dict["program_name"],'id_species': dict["id_species"] , 'markets': list(filter(None,set(dict["markets"]))),'published': dict["published"]} for id, dict in dic_result.items()]
      program=""
      if len(programs_format)==0:
        response['status']=400
        response['message']=1
        
      else:
        program=programs_format[0]
      data["program_details"]=program
      
      data["assigned_fields"]=assigned_fields
      
      #pt._id as _id,id_type,fecha_inicio,id_phenological_stage,validity_period,dosage,dosage_unit,objective,wetting,id_product

      dic_result = {}
      task_ids= []
      for program in tasks:
        task_ids.append(program['_id'])
        id = program['_id']
        id_product = program['id_product']
        
        if id in dic_result:
            dic_result[id]["products"].append(id_product)
        else:
            dic_result[id]={}
            dic_result[id]["id_type"] = program["id_type"] 
            dic_result[id]["start_date"] = program['start_date']
            dic_result[id]["id_phenological_stage"] = program['id_phenological_stage']
            dic_result[id]["products"] = [id_product]
            dic_result[id]["validity_period"] = program['validity_period']
            dic_result[id]["dosage"] = program['dosage']
            dic_result[id]["dosage_unit"] = program['dosage_unit']
            dic_result[id]["objective"] = program['objective']
            dic_result[id]["wetting"] = program['wetting']
      
      programs_format= [{'_id': id,'id_type': dict["id_type"],'start_date': dict["start_date"],'id_phenological_stage': dict["id_phenological_stage"] , 'products': dict["products"],'validity_period': dict["validity_period"],'dosage': dict["dosage"],'objective': dict["objective"],'wetting': dict["wetting"]} for id, dict in dic_result.items()]
      
    
      data["tasks"]=list(filter(None,set(task_ids)))


      #####
      dic_result = {}
      task_ids= []
      for program in assigned_fields:
        task_ids.append(program['_id'])

    
      data["assigned_fields"]=list(filter(None,set(task_ids)))





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

      
        data={}
        data['id_program']=program
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
      
      
      user_id =  get_jwt_identity()
      program_name = request.form.get("program_name")
      species = request.form.get("species")

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
      
      

      programs=getPrograms(user_id)
      

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

      
      programs_format= [{'_id': id,'id_user': dict["id_user"],'program_name': dict["program_name"],'species_name': dict["species_name"] , 'markets': dict["markets"],'published': dict["published"]} for id, dict in dic_result.items()]

      data["programs"]=programs_format
     
      response['data']=data
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        return {'response': response}, 400

    except Exception as e:
      print(e)
      return {'response': response}, 400
  
  
  
  
  
