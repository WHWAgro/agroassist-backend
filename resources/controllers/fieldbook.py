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
from openpyxl import load_workbook, Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Border, Side





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
        markets_dict=getTableDict("market")
        markets_final=""
        companies="( "
        for company in user_company:
            companies=companies+str(company["_id"])+","
        companies = companies[:-1]
        companies=companies+" )"
        markets = request.args.get('markets').split(",")
        print("hola0")
        markets_format="( "
        for market in markets:
            markets_final=markets_final+str(markets_dict[int(market)]["market_name"])+","
            markets_format=markets_format+str(market)+","
        print("hola0")
        markets_format = markets_format[:-1]
        markets_format=markets_format+" )"
        markets_final = markets_final[:-1]
        print(companies)
        print(markets_format)
        print("hola1")

        

       
    
       
        
        ##programs=getProgramsMarketFilter(user_id,companies,markets_format)

        #progrmas_format="( "
        #for program in programs:
        #    progrmas_format=progrmas_format+str(program["_id"])+","
        #progrmas_format = progrmas_format[:-1]
        #progrmas_format=progrmas_format+" )"
        
        
        #print("programs")
        #print(programs)
        #fields_aux = getFieldMarketFilter(progrmas_format)
        fields = request.args.get('fields').split(",")
        
        
        if fields== False:
            response['status']=400 
            response['message']=1
        

        data={}
        data['fields']=fields
        response['data']=data


        data1 = {'tasks': ['test1', 'test2', 'test3'],
            }
        df1 = pd.DataFrame(data1)
        data2 = {'tasks': ['test5', 'test3', 'test4'],
            }
        df2 = pd.DataFrame(data2)

        dfs=[df1,df2]

        print("fields format")
        fields_format="( "
        for field in fields:
            fields_format=fields_format+str(field)+","
        
        fields_format = fields_format[:-1]
        
        fields_format=fields_format+" )"
        print(fields_format)

        field_book_data=getFieldBookData(fields_format)
        print(field_book_data)
        
        field_fb={
        }
        for field in fields:
            field_fb[str(field)]={"data":[],"company":"","CSG_code":"","location":"","varieties":[]}

        products=getTableDict("Products")
        objectives=getTableDict("Objectives")
        
        processed_rows=[]
        for row in field_book_data:
            if str(row["_id"])+'-'+str(row["f_id"])+'-'+str(row["to_id"]) in processed_rows:
             
                continue
            processed_rows.append(str(row["_id"])+'-'+str(row["f_id"])+'-'+str(row["to_id"]))
            field_fb[str(row["f_id"])]["company"]=row["company_name"]
            field_fb[str(row["f_id"])]["CSG_code"]=row["sag_code"]
            field_fb[str(row["f_id"])]["location"]=row["locat"]
            
            field_fb[str(row["f_id"])]["varieties"].append(row["variety"])
            products_id=ast.literal_eval(row["id_product"])
            dppus=ast.literal_eval(row["dosage_parts_per_unit"])
            dosages=ast.literal_eval(row["dosage"])
            date_start=row["date_start"].strftime("%d-%m-%Y")
            date_end=row["date_end"].strftime("%d-%m-%Y")
            if row["application_date"] is None or row["id_status"]!=2:
                continue
            application_date=row["application_date"].strftime("%d-%m-%Y")
            out_of_cover_days=calculate_date_difference(row["date_end"],row["application_date"])
            
            
            wetting=row["wetting"]

            for i in range(0,len(products_id)):
                product_id=products_id[i][0]
                product=products[product_id]
                product_name=product["product_name"]
                active_ingredient=product["chemical_compounds"]
                dosage=float(dosages[i][0])
                dosage_unit=dppus[i][0]
                unit_dosage=""
                
                
                
                if dosage_unit == 1:
                    print(" 1")
                    unit=" gr"
                    unit_dosage="gr/100L"
                    
                    unit_hectare="gr/Há"
                    dosage_hectare=dosage*(wetting/100)
                elif dosage_unit == 2:
                    print(" 2")
                    unit=" Kg"
                    unit_dosage="Kg/100L"
                    
                    unit_hectare="Kg/Há"
                    dosage_hectare=dosage*(wetting/100)
                elif dosage_unit == 3:
                    print(" 3")
                    unit=" gr"
                    unit_dosage="gr/100L"
                    
                    unit_hectare="gr/Há"
                    dosage_hectare=dosage
                    dosage=str(dosage/(wetting/100))
                elif dosage_unit == 4:
                    print(" 4")
                    unit=" Kg"
                    unit_dosage="Kg/100L"
                    
                    
                    unit_hectare="Kg/Há"
                    dosage_hectare=dosage
                    dosage=str(dosage/(wetting/100))
                if dosage_unit == 5:
                    print(" 5")
                    unit=" cc"
                    unit_dosage="cc/100L"
                    
                    unit_hectare="cc/Há"
                    dosage_hectare=dosage*(wetting/100)
                elif dosage_unit == 6:
                    print(" 6")
                    unit=" L"
                    unit_dosage="L/100L"
                    
                    unit_hectare="L/Há"
                    dosage_hectare=dosage*(wetting/100)
                elif dosage_unit == 7:
                    print(" 7")
                    unit=" cc"
                    unit_dosage="cc/100L"
                    
                    
                    unit_hectare="cc/Há"
                    dosage_hectare=dosage
                    dosage=str(dosage/(wetting/100))
                elif dosage_unit == 8:
                    print(" 8")
                    unit=" L"
                    unit_dosage="L/100L"
                    
                    unit_hectare="L/Há"
                    dosage_hectare=dosage
                    dosage=str(dosage/(wetting/100))
                dosage='{:,.2f}'.format(float(dosage)).replace(',','*').replace('.', ',').replace('*','.')


                objective=objectives[product["id_objective"]]["objective_name"]
                field_fb[str(row["f_id"])]["data"].append({"Objetivo":objective,
                                                            "Fecha Aplicacion":application_date,
                                                            "Producto Comercial":product_name,
                                                            "Ingredientes Activos":active_ingredient,
                                                            "Dosis/100L":dosage+unit,
                                                            "Días fuera cobertura":out_of_cover_days,
                                                            "Aplicacion en estado fenologico correcto":"Sí",
                                                            "Aplicacion producto en programa ":"Sí"})
                
                
            
            


        title = pd.DataFrame({'Title': ['Protocolo de Exportación']})
        subtitle = pd.DataFrame({'Información': ['Campos:'+fields_format, 'Mercados: '+markets_format]})
        print("c fb")
        # Write dataframes to Excel
         # Write the dataframe to an Excel file
        myuuid = uuid.uuid4()
        doc_name = "files/fieldbooks/"+str(myuuid)+".xlsx"

        template_path = "files/fieldbooks/tmp_exp.xlsx"
        wb = Workbook()
    
        # Access the active worksheet (assuming there's only one sheet)
        original_sheet = wb.active
        images = []
        start_row = 14  # For example, starting from row 4
        for img in original_sheet._images:
            images.append(img)

        # Create a new workbook
        
        
        for idx, field_id in enumerate(list(field_fb.keys()), start=0):
            print("new_sheet")
            print(idx)
            

            field_data=field_fb[field_id]
            if len(field_data["data"])==0:

                field_data["data"].append({"Objetivo":"No hay ODAs Completadas",
                                                            "Fecha Aplicacion":"",
                                                            "Producto Comercial":"",
                                                            "Ingredientes Activos":"",
                                                            "Dosis/100L":"",
                                                            "Días fuera cobertura":"",
                                                            "Aplicacion en estado fenologico correcto":"",
                                                            "Aplicacion producto en programa ":""})

            df=pd.DataFrame(field_data["data"])
            new_sheet = wb.copy_worksheet(original_sheet)
            new_sheet.title = f'Datos {field_data["CSG_code"]}' 
            
            print("hola")

            from datetime import datetime

            # Get the current date
            current_date = datetime.now()

            # Format the date as "day-month-year"
            date_string = current_date.strftime("%d-%m-%Y")

            varieties=set(field_data["varieties"])

            thick_border = Border(left=Side(style='medium'), 
                      right=Side(style='medium'), 
                      top=Side(style='medium'), 
                      bottom=Side(style='medium'))

            cell=new_sheet.cell(row=start_row+1, column=1, value="Código SAG predio (CSG): ")
            cell.border=thick_border
            cell=new_sheet.cell(row=start_row+1, column=2, value=" ")
            cell.border=thick_border
            new_sheet.merge_cells(start_row=start_row + 1, start_column=1, end_row=start_row + 1, end_column=2)
            cell=new_sheet.cell(row=start_row+1, column=3, value=field_data["CSG_code"])
            cell.border = thick_border

            cell=new_sheet.cell(row=start_row+2, column=1, value="Especie: ")
            cell.border=thick_border
            cell=new_sheet.cell(row=start_row+2, column=2, value=" ")
            cell.border=thick_border
            new_sheet.merge_cells(start_row=start_row + 2, start_column=1, end_row=start_row + 2, end_column=2)
            cell=new_sheet.cell(row=start_row+2, column=3, value="Cereza")
            cell.border = thick_border

            cell=new_sheet.cell(row=start_row+3, column=1, value="Variedad: ")
            cell.border=thick_border
            cell=new_sheet.cell(row=start_row+3, column=2, value=" ")
            cell.border=thick_border
            new_sheet.merge_cells(start_row=start_row + 3, start_column=1, end_row=start_row + 3, end_column=2)
            cell=new_sheet.cell(row=start_row+3, column=3, value=', '.join(varieties))
            cell.border = thick_border

            cell=new_sheet.cell(row=start_row+4, column=1, value="Región:")
            cell.border=thick_border
            cell=new_sheet.cell(row=start_row+4, column=2, value=" ")
            cell.border=thick_border
            new_sheet.merge_cells(start_row=start_row + 4, start_column=1, end_row=start_row + 4, end_column=2)
            cell=new_sheet.cell(row=start_row+4, column=3, value="VI")
            cell.border = thick_border

            cell=new_sheet.cell(row=start_row+5, column=1, value="Comuna: ")
            cell.border=thick_border
            cell=new_sheet.cell(row=start_row+5, column=2, value=" ")
            cell.border=thick_border
            new_sheet.merge_cells(start_row=start_row + 5, start_column=1, end_row=start_row + 5, end_column=2)
            cell=new_sheet.cell(row=start_row+5, column=3, value=field_data["location"])
            cell.border = thick_border
            print('dfsfdsfdsf')
            cell=new_sheet.cell(row=start_row+6, column=1, value="Paises a Exportar: ")
            cell.border=thick_border
            cell=new_sheet.cell(row=start_row+6, column=2, value=" ")
            cell.border=thick_border
            new_sheet.merge_cells(start_row=start_row + 6, start_column=1, end_row=start_row + 6, end_column=2)
            print('dfsfdsfdsf')
            cell=new_sheet.cell(row=start_row+6, column=3, value=markets_final)
            cell.border = thick_border
            print('dfsfdsfdsf2')
            
            

            
            
            
            
            light_border = Border( 
                      
                       
                      bottom=Side(style='thin'))
            rows = dataframe_to_rows(df)
            row_n=start_row+9
            for r_idx, row in enumerate(rows, start_row+8):  #starts at 3 as you want to skip the first 2 rows
                row_n=row_n+1
                for c_idx, value in enumerate(row, 1):
                    if c_idx==1:
                        continue
                    
                    cell = new_sheet.cell(row=r_idx, column=c_idx, value=value)
                    # Apply outer border to the cell
                    if r_idx == start_row + 6 or r_idx == row_n or c_idx == 1:
                        cell.border = thick_border
            

            
            


            
            
            
        print("file closing")
        wb.remove(original_sheet)
        print("file closing")

            # Write title and subtitles
    

        wb.save(doc_name)

           

        
        

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
        
        ##programs=getProgramsMarketFilter(user_id,companies,markets_format)

        #progrmas_format="( "
        #for program in programs:
        #    progrmas_format=progrmas_format+str(program["_id"])+","
        #progrmas_format = progrmas_format[:-1]
        #progrmas_format=progrmas_format+" )"
        
        
        #print("programs")
        #print(programs)
        #fields_aux = getFieldMarketFilter(progrmas_format)
        fields = request.args.get('fields').split(",")
        
        
        if fields== False:
            response['status']=400 
            response['message']=1
        

        data={}
        data['fields']=fields
        response['data']=data


        data1 = {'tasks': ['test1', 'test2', 'test3'],
            }
        df1 = pd.DataFrame(data1)
        data2 = {'tasks': ['test5', 'test3', 'test4'],
            }
        df2 = pd.DataFrame(data2)

        dfs=[df1,df2]

        print("fields format")
        fields_format="( "
        for field in fields:
            fields_format=fields_format+str(field)+","
        
        fields_format = fields_format[:-1]
        
        fields_format=fields_format+" )"
        print(fields_format)

        field_book_data=getFieldBookData(fields_format)
        print(field_book_data)
        
        field_fb={
        }
        for field in fields:
            field_fb[str(field)]={"data":[],"company":"","CSG_code":"","location":"","varieties":[]}

        products=getTableDict("Products")
        objectives=getTableDict("Objectives")
        processed_rows=[]
        for row in field_book_data:
            if str(row["_id"])+'-'+str(row["f_id"])+'-'+str(row["to_id"]) in processed_rows:
             
                continue
            processed_rows.append(str(row["_id"])+'-'+str(row["f_id"])+'-'+str(row["to_id"]))
            field_fb[str(row["f_id"])]["company"]=row["company_name"]
            field_fb[str(row["f_id"])]["CSG_code"]=row["sag_code"]
            field_fb[str(row["f_id"])]["location"]=row["locat"]
            field_fb[str(row["f_id"])]["varieties"].append(row["variety"])
            products_id=ast.literal_eval(row["id_product"])
            dppus=ast.literal_eval(row["dosage_parts_per_unit"])
            dosages=ast.literal_eval(row["dosage"])
            date_start=row["date_start"].strftime("%d-%m-%Y")
            if row["application_date"] is None or row["id_status"]!=2:
                continue
            application_date=row["application_date"].strftime("%d-%m-%Y")
            
            wetting=row["wetting"]

            for i in range(0,len(products_id)):
                product_id=products_id[i][0]
                product=products[product_id]
                product_name=product["product_name"]
                active_ingredient=product["chemical_compounds"]
                dosage=float(dosages[i][0])
                dosage_unit=dppus[i][0]
                unit_dosage=""
                
                
                
                if dosage_unit == 1:
                    print(" 1")
                    unit=" gr"
                    unit_dosage="gr/100L"
                    
                    unit_hectare="gr/Há"
                    dosage_hectare=dosage*(wetting/100)
                elif dosage_unit == 2:
                    print(" 2")
                    unit=" Kg"
                    unit_dosage="Kg/100L"
                    
                    unit_hectare="Kg/Há"
                    dosage_hectare=dosage*(wetting/100)
                elif dosage_unit == 3:
                    print(" 3")
                    unit=" gr"
                    unit_dosage="gr/100L"
                    
                    unit_hectare="gr/Há"
                    dosage_hectare=dosage
                    dosage=str(dosage/(wetting/100))
                elif dosage_unit == 4:
                    print(" 4")
                    unit=" Kg"
                    unit_dosage="Kg/100L"
                    
                    
                    unit_hectare="Kg/Há"
                    dosage_hectare=dosage
                    dosage=str(dosage/(wetting/100))
                if dosage_unit == 5:
                    print(" 5")
                    unit=" cc"
                    unit_dosage="cc/100L"
                    
                    unit_hectare="cc/Há"
                    dosage_hectare=dosage*(wetting/100)
                elif dosage_unit == 6:
                    print(" 6")
                    unit=" L"
                    unit_dosage="L/100L"
                    
                    unit_hectare="L/Há"
                    dosage_hectare=dosage*(wetting/100)
                elif dosage_unit == 7:
                    print(" 7")
                    unit=" cc"
                    unit_dosage="cc/100L"
                    
                    
                    unit_hectare="cc/Há"
                    dosage_hectare=dosage
                    dosage=str(dosage/(wetting/100))
                elif dosage_unit == 8:
                    print(" 8")
                    unit=" L"
                    unit_dosage="L/100L"
                    
                    unit_hectare="L/Há"
                    dosage_hectare=dosage
                    dosage=str(dosage/(wetting/100))
                dosage='{:,.2f}'.format(float(dosage)).replace(',','*').replace('.', ',').replace('*','.')


                objective=objectives[product["id_objective"]]["objective_name"]
                field_fb[str(row["f_id"])]["data"].append({"Objetivo":objective,
                                                            "Nombre Producto":product_name,
                                                            "Fecha":application_date,
                                                            "Ingredientes Activos":active_ingredient,
                                                            "Dosis/100L":dosage+unit})
                
                
            
            


        title = pd.DataFrame({'Title': ['Protocolo de Exportación']})
        subtitle = pd.DataFrame({'Información': ['Campos:'+fields_format, 'Mercados: '+markets_format]})
        print("c fb")
        # Write dataframes to Excel
         # Write the dataframe to an Excel file
        myuuid = uuid.uuid4()
        doc_name = "files/fieldbooks/"+str(myuuid)+".xlsx"

        template_path = "files/fieldbooks/tmp_exp.xlsx"
        wb = load_workbook(template_path)
    
        # Access the active worksheet (assuming there's only one sheet)
        original_sheet = wb.active
        images = []
        start_row = 14  # For example, starting from row 4
        for img in original_sheet._images:
            images.append(img)

        # Create a new workbook
        
        
        for idx, field_id in enumerate(list(field_fb.keys()), start=0):
            print("new_sheet")
            print(idx)
            

            field_data=field_fb[field_id]
            if len(field_data["data"])==0:

                field_data["data"].append({"Objetivo":"No hay ODAs Completadas",
                                                            "Nombre Producto":"",
                                                            "Fecha":"",
                                                            "Ingredientes Activos":"",
                                                            "Dosis/100L":""})
            df=pd.DataFrame(field_data["data"])
            new_sheet = wb.copy_worksheet(original_sheet)
            new_sheet.title = f'Datos {field_data["CSG_code"]}' 
            
            print("hola")

            from datetime import datetime

            # Get the current date
            current_date = datetime.now()

            # Format the date as "day-month-year"
            date_string = current_date.strftime("%d-%m-%Y")

            varieties=set(field_data["varieties"])


            new_sheet.cell(row=start_row+1, column=2, value="Fecha: "+ date_string)
            new_sheet.cell(row=start_row+2, column=2, value="Razón Social: "+field_data["company"])
            new_sheet.cell(row=start_row+3, column=2, value="Variedades: "+', '.join(varieties))
            new_sheet.cell(row=start_row+4, column=2, value="Código CSG: "+field_data["CSG_code"])
            
            thick_border = Border(left=Side(style='medium'), 
                      right=Side(style='medium'), 
                      top=Side(style='medium'), 
                      bottom=Side(style='medium'))
            light_border = Border( 
                      
                       
                      bottom=Side(style='thin'))
            rows = dataframe_to_rows(df)
            row_n=start_row+7
            for r_idx, row in enumerate(rows, start_row+6):  
                row_n=row_n+1
                for c_idx, value in enumerate(row, 1):
                    if c_idx==1:
                        continue
                    
                    cell = new_sheet.cell(row=r_idx, column=c_idx, value=value)
                    # Apply outer border to the cell
                    if r_idx == start_row + 6 or r_idx == row_n or c_idx == 1:
                        cell.border = thick_border
            new_sheet.cell(row=row_n, column=2, value="Certifica")
            for c_idx in range(2, 7):
                cell = new_sheet.cell(row=row_n+4, column=c_idx)
                cell.border = light_border

            new_sheet.cell(row=row_n+5, column=2, value="Nombre Profesiona o Ténico")
            new_sheet.cell(row=row_n+5, column=5, value="Firma")

            new_sheet.cell(row=row_n+7, column=2, value="Nota: - Formato referencial")
            


            
            
            
        print("file closing")
        wb.remove(original_sheet)
        print("file closing")

            # Write title and subtitles
    

        wb.save(doc_name)

           

        
        

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
  
  
  
  
  

  


  
