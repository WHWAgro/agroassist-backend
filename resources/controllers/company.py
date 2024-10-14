from flask import Response, request
from flask_restful import Resource
import json
from datetime import datetime
#import pandas as pd
#from get_project_root import root_path
from resources.errors import  InternalServerError
from database.models.Program import CompanyClass,db
from resources.services.programServices import *
from flask_jwt_extended import jwt_required,get_jwt_identity



class CompanyVisibilityApi(Resource):
  

  @jwt_required()
  def get(self):
  
    try:
      response={}
      response['status']=200
      response['message']=0
      
      user_id =  get_jwt_identity()
      

      data={}
      

      

      #####
    
      user_companies=getUserCompanies(user_id)
      
      

      data["visible"]=user_companies[0]['visible']
      print(user_companies[0])
      





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

        visibility=body.get("visible")
        
        user_id =  get_jwt_identity()
        user_companies=getUserCompanies(user_id)

        company_id=user_companies[0]['_id']
        
        company=CompanyClass.query.get(company_id)
        company.visible=visibility
        db.session.add(company)
        db.session.commit()

      
        data={}
        data["visible"]=visibility     

      
        
        
        response['data']=data
        
        if response.get('status') == 200:
            

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

