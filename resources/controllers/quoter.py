from flask import Response, request,send_file
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
from resources.services.programServices import *
from resources.services.generatePDF import *


class QuoterInitApi(Resource):
  

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
                
                el["products_needed"]=round(((el["wetting"]/100.0)*el["dosage"])*products_list[str(id)]["valid_hectares"])
                el["product_needed_unit"]=1
                el["valid_hectares"]=products_list[str(id)]["valid_hectares"]
                
                alternatives=list(filter(lambda product: product['chemical_compounds'] == compound, elements))
                alternatives_list=[]
                for alternative in alternatives:
                   if alternative["_id"]==id:
                      continue
                   lol={"product_id":alternative["_id"]}
                   lol["products_needed"]=round(((el["wetting"]/100.0)*el["dosage"])*products_list[str(id)]["valid_hectares"])
                   lol["product_needed_unit"]=1
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
    


class QuoterApi(Resource):
  @jwt_required()
  def post(self):
  
    try:
      response={}
      response['status']=200
      response['message']=0
      
      
      user_id =  get_jwt_identity()
      body = request.get_json()
      

      created = createQuoter(body,user_id)
      if created== False:
        response['status']=400
        response['message']=1
      
      data={}
      data['id_quoter']=created
      response['data']=data
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        
        return {'response': response}, 400

    except Exception as e:
      print(e)
      return {'response': response},500
    




  @jwt_required()
  def get(self):
  
    try:
      response={}
      response['status']=200
      response['message']=0
      


      
      user_id =  get_jwt_identity()
      quoter_id=request.args.get('quoter_id')



      quoter_rows = getQuoter(user_id,quoter_id)
      data={}
      if quoter_rows== False:
        response['status']=400
        response['message']=1
      else:
        if len(quoter_rows)>0:
          data['programs_id']=ast.literal_eval(quoter_rows[0]['id_programs'])
          data['start_date']=str(quoter_rows[0]['start_date'])
          data['end_date']=str(quoter_rows[0]['end_date'])
          data['total_hectares']=str(quoter_rows[0]['total_hectares'])
          data['quotes']=[]
          
          quotes={}
          clusters=[]
          for row in quoter_rows:
            if row['quote_id'] not in quotes:
              quotes[row['quote_id']]={'quote_id':row['quote_id'],'provider_name':row['provider_name'],'products':[]}
            if row['product_id']is not None:
              if row['cluster_id'] not in clusters:
                clusters.append(row['cluster_id'])
                quotes[row['quote_id']]['products'].append({'cluster_id':row['cluster_id'],'quote_product_index': None,  'product_id': None, 'product_needed': None, 'product_needed_unit': None,
             'valid_hectares': None, 'container_size': None, 'container_cost_clp': None, 'container_unit': None, 'checked': False,'alternatives':[]})
              
              for cluster in quotes[row['quote_id']]['products']:
                if cluster['cluster_id']==row['cluster_id']:
                  if row['cluster_master']==True:
                    cluster['quote_product_index']=row['id_quote_product']
                    cluster['product_id']=row['product_id']
                    cluster['product_needed']=row['product_needed']
                    cluster['product_needed_unit']=row['product_needed_unit']
                    cluster['valid_hectares']=row['valid_hectares']
                    cluster['container_size']=row['container_size']
                    cluster['container_cost_clp']=row['container_cost_clp']
                    cluster['container_unit']=row['container_unit']
                    cluster['checked']=row['checked']

                  else:
                    
                    
                    alternative={}
                    alternative['quote_product_index']=row['id_quote_product']
                    alternative['product_id']=row['product_id']
                    alternative['product_needed']=row['product_needed']
                    alternative['product_needed_unit']=row['product_needed_unit']
                    alternative['valid_hectares']=row['valid_hectares']
                    alternative['container_size']=row['container_size']
                    alternative['container_cost_clp']=row['container_cost_clp']
                    alternative['container_unit']=row['container_unit']
                    alternative['checked']=row['checked']

                    
                    cluster['alternatives'].append(alternative)

            
                    
          
                  break
              


          for key,value in quotes.items():
            data['quotes'].append(value)

      
      response['data']=data
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        
        return {'response': response}, 400

    except Exception as e:
      print(e)
      return {'response': response},500
    



class QuoterSelectionApi(Resource):
  
  @jwt_required()
  def get(self):
  
    try:
      
      response={}
      response['status']=200
      response['message']=0
      
      user_id =  get_jwt_identity()
      

      data={}
      
      

      quoters=getQuoters(user_id)
      if quoters== False:
        response['status']=400
        response['message']=1

      
      # id,id_user,program_name,species_name,market_name

      quoters_format=[]
      
      for quoter in quoters:
        result={}
        result['_id']= quoter['_id']
        result['id_programs']= ast.literal_eval(quoter['id_programs'])
        result['start_date']= str(quoter['start_date'])
        result['end_date']= str(quoter['end_date'])
        result['updated_at']= str(quoter['updated_at'])
        result['created_at']= str(quoter['created_at'])
        result['total_hectares']= quoter['total_hectares']

        quoters_format.append(result)

   
      data["quoters"]=quoters_format
     
      response['data']=data
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        return {'response': response}, 400

    except Exception as e:
      print(e)
      return {'response': response}, 400
     


class PurchaseOrderApi(Resource):
  

    @jwt_required()
    def post(self):
    
      try:
        response={}
        response['status']=200
        response['message']=0
        

        body = request.get_json()
        
        taskOrderFile = generatePurchaseOrder(body)
        
        if taskOrderFile== False:
          response['status']=400 
          response['message']=1
        
        else:

          data={}
          data['purchase_order']=taskOrderFile
          response['data']=data
        
        if response.get('status') == 200:

          return {'response': response}, 200
        
        else: 
          
          return {'response': response}, 400

      except Exception as e:
        print(e)
        response['message']=2
        return {'response': response},500
      
    @jwt_required()
    def get(self):
    
      try:
        response={}
        response['status']=200
        response['message']=0
        

        id_task= request.args.get('id_quoter')
        
        taskOrderFile = getTaskOrders('id_quoter')
        
        if taskOrderFile== False:
          response['status']=400 
          response['message']=1
        
        else:

          data={}
          data['purchase_orders']=taskOrderFile
          response['data']=data
        
        if response.get('status') == 200:

          return {'response': response}, 200
        
        else: 
          
          return {'response': response}, 400

      except Exception as e:
        print(e)
        response['message']=2
        return {'response': response},500
      

class DowloadPurchaseOrderApi(Resource):
  

    @jwt_required()
    def get(self):
    
      try:
        response={}
        response['status']=200
        response['message']=0
        

        
        
        
        file_path='files/'+str(request.args.get('file_name'))
        
        
        if True:
           return send_file(file_path, as_attachment=True)
        
        else: 
          
          return {'response': response}, 400

      except Exception as e:
        print(e)
        response['message']=2
        return {'response': response},500