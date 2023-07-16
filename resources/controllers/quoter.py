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
from functools import reduce
from itertools import chain


class QuoterApi(Resource):
  

  @jwt_required()
  def get(self):
  
    try:
      response={}
      response['status']=200
      response['message']=0
      
      user_id =  get_jwt_identity()
      

      programs = request.args.get('programs').split(",")
      
      date_begin = request.args.get('start_date')
      date_end = request.args.get('end_date')
      

      print(programs)
      print(date_begin)
      print(date_end)

      
      elements=getTable("products")
      
      final_list=[]
      

      for program in programs:
  
        moments=getMoments(program,date_begin,date_end)
        
        for objective in moments:
            products_list={}
            products_ids=[]
           
            products= list(chain.from_iterable( ast.literal_eval(objective["id_product"])))
            dosages=list(chain.from_iterable( ast.literal_eval(objective["dosage"])))
            for i,product in enumerate(products):
                if product in products_ids:
                    products_list[str(product)]["valid_hectares"]=products_list[str(product)]["valid_hectares"]+10
                else:
                    products_ids.append(product)
                    products_list[str(product)]={"valid_hectares":10,"objective":objective["id_objective"],"wetting":objective["wetting"],"dosage":dosages[i]}
             
            
 
            print(products)
            
            print(products_list)
            for id in products_ids:
                valid=list(filter(lambda product: product['_id'] == id, elements))
                compound=valid[0]["chemical_compounds"]
                
                el={"product_id":id, "objective_id":products_list[str(id)]["objective"],"wetting":products_list[str(id)]["wetting"],"program_id":int(program),"dosage":products_list[str(id)]["dosage"]}
                
                el["products_needed"]=round(((el["wetting"]/100.0)*el["dosage"])*products_list[str(id)]["valid_hectares"]/valid[0]["container_size"]+0.5)
                el["valid_hectares"]=products_list[str(id)]["valid_hectares"]
                alternatives=list(filter(lambda product: product['chemical_compounds'] == compound, elements))
                alternatives_list=[]
                for alternative in alternatives:
                   if alternative["_id"]==id:
                      continue
                   lol={"product_id":alternative["_id"],"objective_id":products_list[str(id)]["objective"],"wetting":products_list[str(id)]["wetting"],"program_id":int(program),"dosage":products_list[str(id)]["dosage"]}
                   lol["products_needed"]=round(((el["wetting"]/100.0)*el["dosage"])*products_list[str(id)]["valid_hectares"]/alternative["container_size"]+0.5)
                   lol["valid_hectares"]=products_list[str(id)]["valid_hectares"]
                   alternatives_list.append(lol)
                el["alternatives"]=alternatives_list
                final_list.append(el)

      data={}
      data["hectares"]=10*len(programs)
      data["usd2clp"]=811.69
      data["clp2usd"]=0.0012
      data["products"]=final_list

      
      
      if response.get('status') == 200:
        response["data"]=data
        #return {'response': json.dumps(response.get('data'), default=datetimeJSONConverter)}, 200
        return {'response': response}, 200
      
      else: 
        return {'response': response}, 400

    except Exception as e:
      print(e)
      response['status']=500
      response['message']=2
      return {'response': response}, 500