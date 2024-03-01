from flask import Response, request,send_file
import pandas as pd
from flask_restful import Resource
import json
from datetime import datetime
#import pandas as pd
#from get_project_root import root_path
from resources.errors import  InternalServerError
from database.models.Program import ProgramClass,db
from resources.services.programServices import *
from flask_jwt_extended import jwt_required,get_jwt_identity
import xlsxwriter




class FieldBookApi(Resource):
  

  @jwt_required()
  def get(self):
    try:
        response={}
        response['status']=200
        response['message']=0
        user_id =  get_jwt_identity()
      

        data={}
        
        
        user_company=getUserCompanies(user_id)
        
        companies="( "
        for company in user_company:
            companies=companies+str(company["_id"])+","
        companies = companies[:-1]
        companies=companies+" )"
        markets = request.args.get('markets').split(",")
        print("hola0")
        markets_format="( "
        for market in markets:
            markets_format=markets_format+str(market)+","
        markets_format = markets_format[:-1]
        markets_format=markets_format+" )"
        print(companies)
        print(markets_format)
        print("hola1")
        
        programs=getProgramsMarketFilter(user_id,companies,markets_format)

        progrmas_format="( "
        for program in programs:
            progrmas_format=progrmas_format+str(program["_id"])+","
        progrmas_format = progrmas_format[:-1]
        progrmas_format=progrmas_format+" )"
        
        

        print(programs)
        fields = getFieldMarketFilter(progrmas_format)
        
        if fields== False:
            response['status']=400 
            response['message']=1
        

        data={}
        data['fields']=fields
        response['data']=data
        
        if response.get('status') == 200:

            return {'response': response}, 200
        
        else: 
            
            return {'response': response}, 400

    except Exception as e:
        print(e)
        response['message']=2
        return {'response': response},500
  
  
  
  
  

  
  
  
class FieldBookFullApi(Resource):
  

  @jwt_required()
  def get(self):
    try:
        response={}
        response['status']=200
        response['message']=0
        user_id =  get_jwt_identity()
      

        data={}
        
        
        user_company=getUserCompanies(user_id)
        
        companies="( "
        for company in user_company:
            companies=companies+str(company["_id"])+","
        companies = companies[:-1]
        companies=companies+" )"
        markets = request.args.get('markets').split(",")
        print("hola0")
        markets_format="( "
        for market in markets:
            markets_format=markets_format+str(market)+","
        markets_format = markets_format[:-1]
        markets_format=markets_format+" )"
        print(companies)
        print(markets_format)
        print("hola1")
        
        programs=getProgramsMarketFilter(user_id,companies,markets_format)

        progrmas_format="( "
        for program in programs:
            progrmas_format=progrmas_format+str(program["_id"])+","
        progrmas_format = progrmas_format[:-1]
        progrmas_format=progrmas_format+" )"
        
        

        print(programs)
        fields = getFieldMarketFilter(progrmas_format)
        
        if fields== False:
            response['status']=400 
            response['message']=1
        

        data={}
        data['fields']=fields
        response['data']=data


        data = {'tasks': ['test1', 'test2', 'test3'],
            }
        df = pd.DataFrame(data)
        fields_format="( "
        for field in fields:
            fields_format=fields_format+str(field["sag_code"])+","
        fields_format = fields_format[:-1]
        fields_format=fields_format+" )"
        
        title = pd.DataFrame({'Title': ['Cuaderno de campo']})
        subtitle = pd.DataFrame({'Información': ['Campos:'+fields_format, 'Mercados: '+markets_format]})

        # Write dataframes to Excel
         # Write the dataframe to an Excel file
        myuuid = uuid.uuid4()
        doc_name = "files/fieldbooks/"+str(myuuid)+".xlsx"
        
        
        with pd.ExcelWriter(doc_name, engine='xlsxwriter') as writer:
            workbook = writer.book
            worksheet = workbook.add_worksheet()

            # Write title and subtitles
            worksheet.write('A1', 'Title:')
            worksheet.write('B1', title.iloc[0, 0])
            worksheet.write('A2', 'Información:')
            for i, sub in enumerate(subtitle['Información']):
                worksheet.write('B{}'.format(i + 2), sub)

            # Write data
            df.to_excel(writer, sheet_name='Sheet1', startrow=4, startcol=0, index=False)


           

        
        

        # Send the Excel file as a response
        return send_file(doc_name, as_attachment=True)
        
        if response.get('status') == 200:

            return {'response': response}, 200
        
        else: 
            
            return {'response': response}, 400

    except Exception as e:
        print(e)
        response['message']=2
        return {'response': response},500
  
  
  
  
class FieldBookExportApi(Resource):
  

  @jwt_required()
  def get(self):
    try:
        response={}
        response['status']=200
        response['message']=0
        user_id =  get_jwt_identity()
      

        data={}
        
        
        user_company=getUserCompanies(user_id)
        
        companies="( "
        for company in user_company:
            companies=companies+str(company["_id"])+","
        companies = companies[:-1]
        companies=companies+" )"
        markets = request.args.get('markets').split(",")
        print("hola0")
        markets_format="( "
        for market in markets:
            markets_format=markets_format+str(market)+","
        markets_format = markets_format[:-1]
        markets_format=markets_format+" )"
        print(companies)
        print(markets_format)
        print("hola1")
        
        programs=getProgramsMarketFilter(user_id,companies,markets_format)

        progrmas_format="( "
        for program in programs:
            progrmas_format=progrmas_format+str(program["_id"])+","
        progrmas_format = progrmas_format[:-1]
        progrmas_format=progrmas_format+" )"
        
        

        print(programs)
        fields = getFieldMarketFilter(progrmas_format)
        
        if fields== False:
            response['status']=400 
            response['message']=1
        

        data={}
        data['fields']=fields
        response['data']=data


        data = {'tasks': ['test1', 'test2', 'test3'],
            }
        df = pd.DataFrame(data)
        fields_format="( "
        for field in fields:
            fields_format=fields_format+str(field["sag_code"])+","
        fields_format = fields_format[:-1]
        fields_format=fields_format+" )"
        
        title = pd.DataFrame({'Title': ['Protocolo de Exportación']})
        subtitle = pd.DataFrame({'Información': ['Campos:'+fields_format, 'Mercados: '+markets_format]})

        # Write dataframes to Excel
         # Write the dataframe to an Excel file
        myuuid = uuid.uuid4()
        doc_name = "files/fieldbooks/"+str(myuuid)+".xlsx"
        
        
        with pd.ExcelWriter(doc_name, engine='xlsxwriter') as writer:
            workbook = writer.book
            worksheet = workbook.add_worksheet()

            # Write title and subtitles
            worksheet.write('A1', 'Title:')
            worksheet.write('B1', title.iloc[0, 0])
            worksheet.write('A2', 'Informacion:')
            for i, sub in enumerate(subtitle['Información']):
                worksheet.write('B{}'.format(i + 2), sub)

            # Write data
            df.to_excel(writer, sheet_name='Sheet1', startrow=4, startcol=0, index=False)


           

        
        

        # Send the Excel file as a response
        return send_file(doc_name, as_attachment=True)
        
        if response.get('status') == 200:

            return {'response': response}, 200
        
        else: 
            
            return {'response': response}, 400

    except Exception as e:
        print(e)
        response['message']=2
        return {'response': response},500
  
  
  
  
  

  


  
