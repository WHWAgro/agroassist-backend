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



class ProgramSelectionApi(Resource):
  
  
  
  @jwt_required()
  def post(self):
  
    try:

      user_id =  get_jwt_identity()
      program_name = request.form.get("program_name")
      program_id=request.form.get("program_id")
      action=request.form.get("action")

      success=""
      
      if action == "Add":
        created = createProgram(program_name,user_id)
        print(created)
        if created== False:
          success="New program couldn't be added"
        else:
          success="New program added successfully"

      if action == "Delete":
        deleted = deleteProgram(program_id,user_id)

        if deleted == False:
          success="Program couldn't be deleted"
        else:
          success="Program deleted successfully"  






      data={}
      data["user_id"]=user_id
      
      new_program=program_name



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
      data["new_program"]=new_program
      
      response={'status':200,'message':success,'data':data}
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        return {'error': response}, 400

    except Exception as e:
      print(e)
      raise InternalServerError
  
  
  
  
  
  @jwt_required()
  def get(self):
  
    try:

      user_id =  get_jwt_identity()
      data={}
      data["user_id"]=user_id
      

      programs=getPrograms(user_id)
      print(programs)

      dic_result = {}

      # id,id_user,program_name,species_name,market_name
      print(programs)
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
      
      
      response={'status':200,'data':data}
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        return {'error': response}, 400

    except Exception as e:
      print(e)
      raise InternalServerError