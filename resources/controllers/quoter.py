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

def getTableDict(table):
    table_elements=getTable(table)
    products_dict={}
    for el in table_elements:
        products_dict[el["_id"]]=el

    return products_dict



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
      plots=getTableDict("plots")
      

      total_hectares=0
      for program in programs:
        program_hectares=0

        print("######$$$$#####new program")
        print(program)
        k_filter1 = "id_program"
        v_match1 = int(program)

       

        filtered_data = {key: value for key, value in plots.items() if (str(value.get(k_filter1)) == str(v_match1) )}
        
        for key,value in filtered_data.items():
          total_hectares=total_hectares+value["size"]
          program_hectares=program_hectares+value["size"]
          
        if program_hectares==0:
          print("0 hectares")
          continue
  
        moments=getMoments(program,date_begin,date_end)
        print("moments:")
        print(moments)
        for objective in moments:
            
            products_list={}
            products_ids=[]
            id_objective=objective["id_objective"]
            products= list(chain.from_iterable( ast.literal_eval(objective["id_product"])))
            dosages=list(chain.from_iterable( ast.literal_eval(objective["dosage"])))
            dosages_unit=list(chain.from_iterable( ast.literal_eval(objective["dosage_parts_per_unit"])))
            
            for i,product in enumerate(products):
                if product in products_ids:
                    products_list[str(product)]["n_applications"]=products_list[str(product)]["n_applications"]+1
                else:
                    products_ids.append(product)
                    products_list[str(product)]={"valid_hectares":program_hectares,"objective":objective["id_objective"],"wetting":objective["wetting"],"dosage":dosages[i],"product_needed_unit":dosages_unit[i]}
                    products_list[str(product)]["n_applications"]=1
            
            
 
            

            for p_id,p_value in products_list.items():
              dosage=p_value["dosage"]
              wetting=p_value["wetting"]
              total_hectareas_data=p_value["valid_hectares"]
              n_app=p_value["n_applications"]

              total_product=0
              if p_value["product_needed_unit"] == 1:
                
                total_product=(dosage*(wetting/100)*total_hectareas_data)*n_app
              elif p_value["product_needed_unit"] == 2:
                
                total_product=(dosage*(wetting/100)*total_hectareas_data)*1000*n_app
              elif p_value["product_needed_unit"] == 3:
                
                total_product=(dosage*total_hectareas_data)*n_app
              elif p_value["product_needed_unit"] == 4:
                
                total_product=(dosage*total_hectareas_data)*1000*n_app
              if p_value["product_needed_unit"] == 5:
                
                total_product=(dosage*(wetting/100)*total_hectareas_data)*n_app
              elif p_value["product_needed_unit"] == 6:
                
                total_product=(dosage*(wetting/100)*total_hectareas_data)*1000*n_app
              elif p_value["product_needed_unit"] == 7:
                
                total_product=(dosage*total_hectareas_data)*n_app
              elif p_value["product_needed_unit"] == 8:
                
                total_product=(dosage*total_hectareas_data)*1000*n_app
              products_list[p_id]["product_needed"]=int(total_product)
           
            for id in products_ids:
                valid=list(filter(lambda product: product['_id'] == id , elements))
                print(valid)
                print("chao")
                compound=valid[0]["chemical_compounds"]
                
                
                el={"product_id":id, "objective_id":products_list[str(id)]["objective"],"wetting":products_list[str(id)]["wetting"],"program_id":int(program),"dosage":products_list[str(id)]["dosage"]}
                el["product_needed_unit"]=products_list[str(id)]["product_needed_unit"]
                el["products_needed"]=products_list[str(id)]["product_needed"]
                #el["products_needed"]=round(((el["wetting"]/100.0)*el["dosage"])*products_list[str(id)]["valid_hectares"])
                el["valid_hectares"]=products_list[str(id)]["valid_hectares"]
                
                alternatives=list(filter(lambda product: product['chemical_compounds'] == compound and product['id_objective'] == id_objective and product['product_name'] != valid[0]["product_name"] , elements))
                print('producto')
                print(str(id))
                print(products_list[str(id)])
                print('alternativas')
                #print(product['product_name'])
                
                print(alternatives)
                alternatives_list=[]
                for alternative in alternatives:
                   if alternative["_id"]==id:
                      continue
                   lol={"product_id":alternative["_id"]}
                   lol["product_needed_unit"]=products_list[str(id)]["product_needed_unit"]
                   #lol["products_needed"]=round(((el["wetting"]/100.0)*el["dosage"])*products_list[str(id)]["valid_hectares"])
                   lol["products_needed"]=products_list[str(id)]["product_needed"]
                   alternatives_list.append(lol)
                el["alternatives"]=alternatives_list
                final_list.append(el)

      data={}
      data["hectares"]=total_hectares
      data["usd2clp"]=901.31
      data["clp2usd"]=0.0011
      data["products"]=final_list

      consolidated_products=[]
      used_products=[]
      for product in data["products"]:
       
        if product['product_id'] not in used_products:
         
          used_products.append(product["product_id"])
          for alternative in product["alternatives"]:
            used_products.append(alternative["product_id"])
          consolidated_products.append(product)
          
        else: 
          
          for c_product in consolidated_products:
            c_alternatives=[c_alternative["product_id"] for c_alternative in c_product["alternatives"]]
            if product["product_id"]==c_product["product_id"] or c_product["product_id"] in c_alternatives :
              
              c_product['wetting']=c_product['wetting']+product['wetting']
              c_product['products_needed']=c_product['products_needed']+product['products_needed']
              c_product['valid_hectares']=c_product['valid_hectares']+product['valid_hectares']
              for c_alternative in c_product["alternatives"]:
               
                c_alternative['products_needed']=c_product['products_needed']+product['products_needed']
                

      data['products']=consolidated_products

          



      
      
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
  def put(self):
  
    try:
      response={}
      response['status']=200
      response['message']=0
      
      
      user_id =  get_jwt_identity()
      body = request.get_json()
      

      updated = updateQuotes(body)
      data={}
      if response.get('status') == 200 and updated != False:
            print("dds")
            data['quoter_id']=request.args.get('quoter_id')
            response['data']=data
      if updated== False:
        response['status']=400
        response['message']=1
      
      
      
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        
        return {'response': response}, 400

    except Exception as e:
      print(e)
      return {'response': response},500





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



      quoter_products =getQuoterProducts(quoter_id)

      print('fdsfdsfdsfdfdfdf$$$$^%^^^')
     

      
      products={}
      for product in quoter_products:

        del product['_id']
        del product['id_quoter']

        if product['cluster_id'] not in products:
          products[product['cluster_id']]={'alternatives':[]}


        if product['cluster_master']==True:
          product['alternatives']= products[product['cluster_id']]['alternatives']
          products[product['cluster_id']]= product
        else:
            products[product['cluster_id']]['alternatives'].append(product)
      print(products) 
      
      data={}
     
      data["usd2clp"]=901.31
      data["clp2usd"]=0.0011

      
      quoter_rows = getQuoter(user_id,quoter_id)
      

      
      print(quoter_rows)
      if quoter_rows== False or len(quoter_rows)==0:
        response['status']=400
        response['message']=1
        if len(quoter_rows)==0:
          response['message']="id not available"
        return {'response': response}, 400
      else:
        if len(quoter_rows)>0:
          data['programs_id']=ast.literal_eval(quoter_rows[0]['id_programs'])
          data['start_date']=str(quoter_rows[0]['start_date'])
          data['end_date']=str(quoter_rows[0]['end_date'])
          data['total_hectares']=str(quoter_rows[0]['total_hectares'])
          data['quotes']=[]
          data['products']=[]
          for key,value in products.items():
            data['products'].append(value)

          print(data)
          quotes={}
          ci=0
          colors=['#E3F461', '#C8D8CF', '#AAB9EE', '#FFBB33']
          for row in quoter_rows:
            if row['quote_id'] not in quotes:
              purchase_orders=getProviderPurchaseOrders(row['quote_id'])
              quotes[row['quote_id']]={'quote_id':row['quote_id'],'provider_name':row['provider_name'],'hex_color':colors[ci],'purchase_orders':purchase_orders,'rows':[]}
              ci=ci+1
              
            quotes[row['quote_id']]['rows'].append({'product_row_id': row['product_row_id'],  
              'container_size': row['container_size'], 'container_price_clp': row['container_price_clp'], 'container_unit_id': row['container_unit_id'], 'checked': row['checked'],'_id':row['row_id']})
            
          for key,value in quotes.items():
            data['quotes'].append(value)
          
        
              


      

      data['products'].sort(key=lambda x: x['product_row_id'], reverse=False)
      for product in data['products']:
        product['alternatives'].sort(key=lambda x: x['product_row_id'], reverse=False)
      for quote in data['quotes']:
        quote['rows'].sort(key=lambda x: x['product_row_id'], reverse=False)
      response['data']=data
      data['quotes'].sort(key=lambda x: x['quote_id'], reverse=False)
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        
        return {'response': response}, 400

    except Exception as e:
      print(e)
      response['message']=2
      response['status']=500
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
      print(quoters)
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
        print("-----")
        print(taskOrderFile)
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
        response['message']=e
        response['status']=500
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
        response['message']=e
        response['status']=500
     
        return {'response': response},500
      


class QuoterProductsApi(Resource):
  

    @jwt_required()
    def get(self):
    
      try:
        response={}
        response['status']=200
        response['message']=0
        
        print("quoter")
        id_quoter = request.args.get('id_quoter')
        print(id_quoter)
        quoter_products =getQuoterProducts(id_quoter)

       
      

        
        products={}
        for product in quoter_products:

          del product['_id']
          del product['id_quoter']
          print(product)

          if product['cluster_id'] not in products:
            products[product['cluster_id']]={'alternatives':[]}


          if product['cluster_master']==True:
            product['alternatives']= products[product['cluster_id']]['alternatives']
            products[product['cluster_id']]= product
          else:
              products[product['cluster_id']]['alternatives'].append(product)

        
        taskOrderFile = generateQuoterProducts(products)
        print("-----")
        print(taskOrderFile)
        if taskOrderFile== False:
          response['status']=400 
          response['message']=1
          return {'response': response}, 400
        
        else:

          file_path='files/'+taskOrderFile
        
        
          if True:
            return send_file(file_path, as_attachment=True)
          
          
            
            
        
      except Exception as e:
        print(e)
        response['message']=2
        return {'response': response},500