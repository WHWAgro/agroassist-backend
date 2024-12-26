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
      print('---------new quoter')
      response={}
      response['status']=200
      response['message']=0
      
      user_id =  get_jwt_identity()
      

      fields = request.args.get('programs').split(",")
      fields_raw = request.args.get('programs')
      
      date_begin = request.args.get('start_date')
      date_end = request.args.get('end_date')
      

      print(fields)
      print(date_begin)
      print(date_end)

      
      elements=getTable("products")
      
      final_list=[]
      plots=getTableDict("plots")
      

      total_hectares=0
      plots_visited=[]
      user_plots,user_plots_calendar_tasks=getUserValidPlots(user_id,fields_raw)
      print(user_plots)
      print('////////////*************////////////////')
      print(user_plots_calendar_tasks)
      print('rorororrororo')
      for program in fields :
        program_hectares=0

        print("######$$$$#####new program")
        
        k_filter1 = "id_field"
        v_match1 = int(program)

       
        
        
        
        
        filtered_data = {str(value["_id"])+'-'+str(value["moment_id"]):value  for  value in user_plots if (str(value.get(k_filter1)) == str(v_match1) )}
        print('filtered data')
        
        
        
        for key,value in filtered_data.items():
          if value['_id'] not in plots_visited:
            
            plots_visited.append(value['_id'])
            total_hectares=total_hectares+value["size"]
            program_hectares=program_hectares+value["size"]
          
        if program_hectares==0:
          print("0 hectares")
          continue

        print('momentos')
  
        moments,add_tasks=getMoments(program,date_begin,date_end)

        print('hola--')
        
        add_tasks_format=[]
        for task in add_tasks:
          print('----------s')
          print(task)
          products=  ast.literal_eval(task["id_product"])
          dosages= ast.literal_eval(task["dosage"])
          dosages_unit= ast.literal_eval(task["dosage_parts_per_unit"])
          id_objective=ast.literal_eval(task["id_objective"])
          print(id_objective)
          objective_names=[]
          if task["objective_name"]== None or task["objective_name"]=='None':
            objective_names=id_objective
          else:
            objective_names= ast.literal_eval(task["objective_name"])
          
          products_ingredients=[]
          if task["products_ingredients"]== None or task["products_ingredients"]=='None':
            products_ingredients=products
          else:
            products_ingredients= ast.literal_eval(task["products_ingredients"])
          
          products_name=[]
          if task["products_name"]== None or task["products_name"]=='None':
            products_name=products
          else: 
            products_name=ast.literal_eval(task["products_name"])

          print(products_ingredients)
          print(products_name)
          print(dosages)
          print(products)
          for idx,objective in enumerate(id_objective):
            task_format=task.copy()
            task_format['id_objective']=objective
            task_format['objective_name']=str(objective_names[idx])
            
            task_format['products_ingredients']=str(products_ingredients[idx])
            task_format['products_name']=str(products_name[idx])
            task_format['dosage']=str(dosages[idx])
            task_format['dosage_parts_per_unit']=str(dosages_unit[idx])
            task_format['id_product']=str(products[idx])

            
            add_tasks_format.append(task_format)
       
        moments=moments+add_tasks_format
        
        
        for objective in moments:
            print('objetivo-----******')
            objective_list=[]
            
            #print((objective))
            moment_hectares=objective["size"]
            
            #print(moment_hectares)
            products_list={}
            products_ids=[]
            id_objective=objective["id_objective"]
            
            products= list(chain.from_iterable( ast.literal_eval(objective["id_product"])))
            dosages=list(chain.from_iterable( ast.literal_eval(objective["dosage"])))
            dosages_unit=list(chain.from_iterable( ast.literal_eval(objective["dosage_parts_per_unit"])))
            objective_name=objective["objective_name"]
            products_ingredients=list(chain.from_iterable( ast.literal_eval(objective["products_ingredients"])))
            products_name=list(chain.from_iterable( ast.literal_eval(objective["products_name"])))
            
            #print(products)
            #print('enumernado------*****')
            for i,product in enumerate(products):
             
                if product in products_ids:
                    if product==0:
                      product=products_name[i]
                     

                    products_list[str(product)]["n_applications"]=products_list[str(product)]["n_applications"]+1
                else:
                    
                    obj_name=None
                    if objective["id_objective"]==0:
                      obj_name=objective["objective_name"]
                    else:
                      obj_name=objective["id_objective"]

                    if product==0:
                      
                      product=products_name[i]
                    

                    products_ids.append(product)
                    products_list[str(product)]={"product_ingredients":products_ingredients[i],"valid_hectares":moment_hectares,"objective":obj_name,"wetting":objective["wetting"],"dosage":float(dosages[i]),"product_needed_unit":dosages_unit[i]}
                    products_list[str(product)]["n_applications"]=1
            #print(products_ids)
            #print(products_list)
            
            
            #print("calulando cantidad por producto")
            for p_id,p_value in products_list.items():
              #print(p_id)
              
              dosage=p_value["dosage"]
              wetting=p_value["wetting"]
              total_hectareas_data=p_value["valid_hectares"]
              n_app=p_value["n_applications"]
              print('hola')
              print(wetting)
              print(total_hectareas_data)
              print(p_id)
              

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
              print(total_product)
              print('****')
           
            for id in products_ids:
                  
                
               
                
                
                  
                
                  
                  
                  
                  
                  
                  
                  
                  el={"product_id":id,"product_ingredients":products_list[str(id)]["product_ingredients"], "objective_id":products_list[str(id)]["objective"],"wetting":products_list[str(id)]["wetting"],"program_id":int(program),"dosage":products_list[str(id)]["dosage"]}
                  el["product_needed_unit"]=products_list[str(id)]["product_needed_unit"]
                  el["products_needed"]=products_list[str(id)]["product_needed"]
                
                  el["valid_hectares"]=products_list[str(id)]["valid_hectares"]

                  alternatives_pre=[]
                  if can_cast_to_number(id)==True:
                  
                    valid=list(filter(lambda product: product['_id'] == id , elements))
                    compound=valid[0]["chemical_compounds"]
                  
                    alternatives_pre=list(filter(lambda product: product['chemical_compounds'] == compound  and product['product_name'] != valid[0]["product_name"] , elements))
                  unique_products_name = []
                  alternatives=[]

                  
                  # Iterate over the list and add entries to the dictionary
                  for product in alternatives_pre:
                      product_name = product["product_name"]
                      if product_name not in unique_products_name:
                          unique_products_name.append(product_name)
                          alternatives.append( product)

                  
                  
                  #print(str(id))
                  #print(products_list[str(id)])
                  #print('alternativas')
                  #print(product['product_name'])
                  
                  #print(alternatives)
                  alternatives_list=[]
                  for alternative in alternatives:
                    if alternative["_id"]==id:
                        continue
                    lol={"product_id":alternative["_id"]}
                    lol["product_needed_unit"]=products_list[str(id)]["product_needed_unit"]
                    
                    lol["products_needed"]=products_list[str(id)]["product_needed"]
                    alternatives_list.append(lol)
                  el["alternatives"]=alternatives_list
                  
                  objective_list.append(el)
            
            consolidated_products=[]
            used_products=[]
            dict_list={}
            for product in objective_list:
              dict_list[product['product_id']]=product

            for product in objective_list:
              if product['product_id'] in dict_list:
                used_products.append(product)
                for alternative in product['alternatives']:
                  #print(alternative)
                  if alternative['product_id'] in dict_list:
                    del dict_list[alternative['product_id']]
           
            for product in used_products:
              final_list.append(product)
            

      data={}
      data["hectares"]=total_hectares
      #data["usd2clp"]=963.1
      #data["clp2usd"]=0.0011
      data["products"]=final_list

      #TO DO revisar como se consolidan los productos para el total hectareas
      consolidated_products=[]
      used_products=[]
      #print('------consolidando-----')
      for product in data["products"]:
        
       
        if product['product_id'] not in used_products:
        
         
          used_products.append(product["product_id"])
          for alternative in product["alternatives"]:
            used_products.append(alternative["product_id"])
          consolidated_products.append(product)
          
        else: 
         
          
          for c_product in consolidated_products:
            
            c_alternatives=[c_alternative["product_id"] for c_alternative in c_product["alternatives"]]
            
            if product["product_id"]==c_product["product_id"] or (product["product_id"] in c_alternatives) :
              
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
      
      print('creando quoter*********-----')
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
     
      data["usd2clp"]=983.25
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
     
      if quoters== False:
        response['status']=400
        response['message']=1

      user_company=getUserCompanies(user_id)
      
      companies="( "
      for company in user_company:
        companies=companies+str(company["_id"])+","
      companies = companies[:-1]
      companies=companies+" )"
      print(user_id)
      programs_raw=getPrograms(user_id,companies)
      print("$$$$$$$---------")

      programs={}
      for program in programs_raw:
        if (program['_id'] in programs)==False:
          programs[program['_id']]={}
          programs[program['_id']]["program_name"]=program['program_name']

      
      print(programs)
      
      # id,id_user,program_name,species_name,market_name

      quoters_format=[]
      
      for quoter in quoters:
        print(quoter['_id'])
        result={"programs":[]}
        result['_id']= quoter['_id']
        result['id_programs']= ast.literal_eval(quoter['id_programs'])
        print(result['id_programs'])
        for program in result['id_programs']:
          print("checkando programa")
          if program in programs:
            print("Esta")
            result["programs"].append(programs[program]["program_name"])

        #result['programs']=
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