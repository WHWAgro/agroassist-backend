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


class EditProgramApi(Resource):
  
  @jwt_required()
  def post(self):
  
    try:
      
      
      user_id =  get_jwt_identity()
      user_id = request.form.get("program_id")

      data={}
      data["user_id"]=user_id
      data["program_id"]=user_id
      
      data["products"]=getTable("products")
      data["markets"] =getTable("market")
      data["species"] =getTable("species")
      data["phenological_stages"] =getTable("phenological_stages")
      
      response={'status':200,'data':data}
  
      
      if response.get('status') == 200:
        #return {'response': json.dumps(response.get('data'), default=datetimeJSONConverter)}, 200
        return {'response': response}, 200
      
      else: 
        return {'error': response.get('data')}, 400

    except Exception as e:
      print(e)
      raise InternalServerError
    
  @jwt_required()
  def get(self):
  
    try:
      status=200
      
      user_id =  get_jwt_identity()
      program_id = request.args.get('id_program')



      data={}
      data["user_id"]=user_id
      data["program_id"]=program_id


      programs,tasks=getProgramDetails(user_id,program_id)
      dic_result = {}

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
      program=""
      if len(programs_format)==0:
        status=400
        
      else:
        program=programs_format[0]
      data["program_details"]=program
      
      #pt._id as _id,id_type,fecha_inicio,id_phenological_stage,validity_period,dosage,dosage_unit,objective,wetting,id_product

      dic_result = {}

      for program in tasks:
        id = program['_id']
        id_product = program['id_product']
        
        if id in dic_result:
            dic_result[id]["products"].append(id_product)
        else:
            dic_result[id]={}
            dic_result[id]["id_type"] = program["id_type"] 
            dic_result[id]["start_date"] = program['fecha_inicio']
            dic_result[id]["id_phenological_stage"] = program['id_phenological_stage']
            dic_result[id]["products"] = [id_product]
            dic_result[id]["validity_period"] = program['validity_period']
            dic_result[id]["dosage"] = program['dosage']
            dic_result[id]["dosage_unit"] = program['dosage_unit']
            dic_result[id]["objective"] = program['objective']
            dic_result[id]["wetting"] = program['wetting']
      
      programs_format= [{'_id': id,'id_type': dict["id_type"],'start_date': dict["start_date"],'id_phenological_stage': dict["id_phenological_stage"] , 'products': dict["products"],'validity_period': dict["validity_period"],'dosage': dict["dosage"],'objective': dict["objective"],'wetting': dict["wetting"]} for id, dict in dic_result.items()]
      
     
      data["tasks_details"]=programs_format


      #####
      
      data["products"]=getTable("products")
      data["markets"] =getTable("market")
      data["species"] =getTable("species")
      data["phenological_stages"] =getTable("phenological_stages")
      
      response={'status':status,'data':data}
      
      
      if response.get('status') == 200:
        #return {'response': json.dumps(response.get('data'), default=datetimeJSONConverter)}, 200
        return {'response': response}, 200
      
      else: 
        return {'error': response.get('data')}, 400

    except Exception as e:
      print(e)
      raise InternalServerError