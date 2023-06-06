import json
from database.models.Program import ProgramClass, db


from flask import Response, request
from flask_restful import Resource
import json
from datetime import datetime
#import pandas as pd
#from get_project_root import root_path
from resources.errors import  InternalServerError
from database.models.Program import ProgramClass,db
from resources.services.programServices import *


class CreationApi(Resource):
  
  
  def get(self):
  

    
    try:
      

     
      create_logic()

      response={'status':200,'data':"hola"}
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        return {'error': response}, 400

    except Exception as e:
      print(e)
      raise InternalServerError

    
    


