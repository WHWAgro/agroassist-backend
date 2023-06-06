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


class GenerateProgramApi(Resource):
  
 
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
      
      response={'status':200,'data':data}
  
      
      if response.get('status') == 200:
        #return {'response': json.dumps(response.get('data'), default=datetimeJSONConverter)}, 200
        return {'response': response}, 200
      
      else: 
        return {'error': response.get('data')}, 400

    except Exception as e:
      print(e)
      raise InternalServerError