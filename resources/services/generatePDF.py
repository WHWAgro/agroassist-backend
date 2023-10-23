from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak, Frame, Flowable
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import uuid
import json
from database.models.Program import PurchaseOrderClass,TaskOrderClass,PlotClass,TaskClass,QuoterClass,QuoteClass,ProgramCompaniesClass,MarketProgramClass,ProgramClass,userClass,SpeciesClass,FieldClass,ProgramTaskClass,TaskObjectivesClass, db,auth
from sqlalchemy import  text,select
from flask import g
import jwt
import time
from sqlalchemy.orm import class_mapper
import ast
from datetime import datetime  
from resources.services.programServices import *
from flask_jwt_extended import jwt_required,get_jwt_identity

def getTableDict(table):
    table_elements=getTable(table)
    products_dict={}
    for el in table_elements:
        products_dict[el["_id"]]=el

    return products_dict
def find_element_index(matrix, element):
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value == element:
                return i, j
    return None  

def getCompanyTaskOrders(id_company):
    try:
        
        query="""SELECT *
                    FROM task_orders
                    WHERE id_company = """+ str(id_company)+"""
                    order by order_number desc
                
             """
        
        
        rows=[]
        with db.engine.begin() as conn:
            result = conn.execute(text(query)).fetchall()
            for row in result:
                row_as_dict = row._mapping
                print(row_as_dict)
                rows.append(dict(row_as_dict))
            return rows

    except Exception as e:
        print(e)
        return False
    
def getCompanyPurchaseOrders(id_company):
    try:
        
        query="""SELECT *
                    FROM purchase_orders
                    WHERE id_company = """+ str(id_company)+"""
                    order by order_number desc
                
             """
        
        
        rows=[]
        with db.engine.begin() as conn:
            result = conn.execute(text(query)).fetchall()
            for row in result:
                row_as_dict = row._mapping
                print(row_as_dict)
                rows.append(dict(row_as_dict))
            return rows

    except Exception as e:
        print(e)
        return False
    


# Define a custom Flowable for horizontal lines
class HorizontalLine(Flowable):
    def __init__(self, width, thickness=1):
        super().__init__()
        self.width = width
        self.thickness = thickness

    def draw(self):
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)




def generateTaskOrder(body):

    try:

        print(1)
        # Create a PDF document
        user_id =  get_jwt_identity()
        myuuid = uuid.uuid4()
        doc_name = str(myuuid)+".pdf"
        doc = SimpleDocTemplate("files/"+doc_name, pagesize=letter, topMargin=10,leftMargin=10)
        print(str(myuuid)+".pdf")
        
        company_id=1
        id_task=int(body['id_task'])
        user_name=getUserData(user_id)
        
        order_creator=user_name[0]["user_name"]
        order_number=1

        company_task_orders = getCompanyTaskOrders(1)
        print(2)
        if len(company_task_orders)>0:
           order_number = company_task_orders[0]['order_number']+1
        
        #-----------------------pdf begins here-------------------
        print('----------')
        # Create a list to hold the content of the PDF
        pdf_content = []

        # Header: "AgroAssist" in green letters
        #header_style = getSampleStyleSheet()["Heading1"]
        #header_style.textColor = colors.green
        #header = Paragraph("AgroAssist", header_style)
        #pdf_content.append(header)

        # Section 1: Title
        title_style = getSampleStyleSheet()["Title"]
        title_style.alignment = 0 
        title = Paragraph("Orden de Aplicación Nº "+str(order_number), title_style)
        pdf_content.append(title)
        print('----------')
        # Section 2: Subtitles (aligned to the left and in gray)
        subtitle_style = getSampleStyleSheet()["Normal"]
        subtitle_style.alignment = 0  # Align left
        subtitle_style.textColor = colors.grey
        print('----------')
        subtitle1 = Paragraph("Orden emitida por "+order_creator, subtitle_style)
        today_date = datetime.now().strftime("%Y-%m-%d")  # Example: "2023 September 04"
        subtitle2 = Paragraph(f"Fecha emisión: {today_date}", subtitle_style)
        pdf_content.extend([subtitle1, Spacer(1, 5), subtitle2, Spacer(1, 5)])
        print('----------')
        pdf_content.append(Spacer(1,10))      
        pdf_content.append(HorizontalLine(550))  # Adjust the width as needed
        pdf_content.append(Spacer(1,10))
        # Section 5: Two Columns
        # Replace this with your actual data
        products=getTableDict("Products")
        

        companies=getUserCompanies(user_id)
        empresa_data = companies[0]["company_name"]
        print('----------1')
        fields=getTableDict("field")
        campo_data = fields[body['id_field']]["field_name"]

        cultivo_data = "Cereza"

        plots=getTableDict("plots")
        plots_names = ''
        total_plot_size=0
        print('----------2')
        ##tablas
        objectives=getTableDict("objectives")
        products=getTableDict("products")
        tasks=getTableDict("tasks")
        moments=getTableDict("program_tasks")
        moment_objectives=getTableDict("task_objectives")
        moment_id=tasks[int(body["id_task"])]["id_moment"]

        wetting=moments[moment_id]["wetting"]

        for id_plot in body['id_plots']:
            print(id_plot)
            print(plots[id_plot]["name"] )
            plots_names = plots_names +', '+plots[id_plot]["name"] 
            print(plots_names)  
            total_plot_size=total_plot_size+plots[id_plot]["size"]
            print(total_plot_size)  
        if len(plots_names)>0:
            plots_names=plots_names[1:]   
        total_hectareas_data = total_plot_size
        print('----------3')
        # Create a table with two columns
        section5_table_data = [
            ["Empresa:", empresa_data, "Cultivo:", cultivo_data],
            ["Campo:", campo_data, "Total Hectareas:", total_hectareas_data],
            ['Mojamieto',str(wetting)+"L",'','']
        ]
        print('----------4')

        section5_table = Table(section5_table_data, colWidths=[80, 150, 80, 150])
        section5_table_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica')])
        section5_table.setStyle(section5_table_style)
        print('----------5')
        pdf_content.append( section5_table)
        pdf_content.append(Spacer(1,10))
        pdf_content.append(HorizontalLine(550))  # Adjust the width as needed
        pdf_content.append(Spacer(1,10))
        application_date = body['application_date']
        
        
        section3_table_data = [
            ["Fecha de aplicacion:", application_date, "Cuarteles:", plots_names]
            
        ]
        print('hola-1')

        section3_table = Table(section3_table_data, colWidths=[100, 150, 100, 150])
        section3_table_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica')])
        section3_table.setStyle(section3_table_style)
        
        pdf_content.append( section3_table)
        pdf_content.append(Spacer(1,10))
        pdf_content.append(HorizontalLine(550))  # Adjust the width as needed
        pdf_content.append(Spacer(1,10))

        ##operadores----------------
        data_list = body['asignees']
        

        # Create a list to hold the table data
        table_data = [['Operador','Tractor','Rociador']]  # Start with the headers as the first row

        # Add the data rows
        workers=getTableDict("workers")
        machinery=getTableDict("machinery")
        for item in data_list:
            row_data = [workers[item["id_operator"]]["name"],machinery[item["id_tractor"]]["name"],machinery[item["id_sprayer"]]["name"]]
            table_data.append(row_data)

        # Create a table with the data
        table = Table(table_data,colWidths=[150, 150, 150 ])

        # Add style to the table
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),  # Header background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center-align all cells
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
            
            ('GRID', (0, 0), (-1, -1), 1, colors.green)  # Gridlines
        ])

        table.setStyle(table_style)
        pdf_content.append(table)



        #----productos-----
        print('hola0')
        pdf_content.append(Spacer(1,10))
        pdf_content.append(HorizontalLine(550))  # Adjust the width as needed
        pdf_content.append(Spacer(1,10))
        data_list2 = body['products']
        

        # Create a list to hold the table data
        table_data2 = [['Producto','Objetivo','Dosis x 100 Lt','Total Producto']] # Start with the headers as the first row

        print('hola-productos')
        # Add the data rows
       

        
        
        k_filter1 = "id_task"
        v_match1 = moment_id
      
        filtered_data = {key: value for key, value in moment_objectives.items() if (value.get(k_filter1) == v_match1 )}
        
        print("$$$$##############$$$$$")
        
        
        phi_list=[]
        reentry_period_list=[]
        for item in data_list2:
            k_filter1 = "id_objective"
            v_match1 = item["id_objective"]
            filtered_data2={key: value for key, value in filtered_data.items() if (value.get(k_filter1) == v_match1 )}
            
            
            dosage=0
            dosage_unit=1
            for key ,value in filtered_data2.items():
                
                product=ast.literal_eval(value["id_product"])
                i,j=find_element_index(product,item["id_product"])
                dosage=ast.literal_eval(value["dosage"])[i][j]
                dosage_unit=ast.literal_eval(value["dosage_parts_per_unit"])[i][j]
            unit=""
            total_product=0
            if dosage_unit == 1:
                unit=" gr"
                total_product=str(dosage*(wetting/100)*total_hectareas_data)
            elif dosage_unit == 2:
                unit=" Kg"
                total_product=str(dosage*(wetting/100)*total_hectareas_data)
            elif dosage_unit == 3:
                unit=" gr"
                total_product=str(dosage*total_hectareas_data/(wetting/100))
            elif dosage_unit == 4:
                unit=" Kg"
                total_product=str(dosage*total_hectareas_data/(wetting/100))
            if dosage_unit == 5:
                unit=" cc"
                total_product=str(dosage*(wetting/100)*total_hectareas_data)
            elif dosage_unit == 6:
                unit=" L"
                total_product=str(dosage*(wetting/100)*total_hectareas_data)
            elif dosage_unit == 7:
                unit=" cc"
                total_product=str(dosage*total_hectareas_data/(wetting/100))
            elif dosage_unit == 8:
                unit=" L"
                total_product=str(dosage*total_hectareas_data/(wetting/100))

            phi_list.append(products[item["id_product"]]["phi"])
            reentry_period_list.append(products[item["id_product"]]["reentry_period"])
        
            row_data = [products[item["id_product"]]["product_name"],objectives[item["id_objective"]]["objective_name"],str(dosage)+unit,total_product+unit]
            
            table_data2.append(row_data)
        print('hola-footer')
        # Create a table with the data
        table2 = Table(table_data2,colWidths=[150, 150, 100,100 ])
        print('hola3')
        # Add style to the table
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),  # Header background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center-align all cells
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
            
            ('GRID', (0, 0), (-1, -1), 1, colors.green)  # Gridlines
        ])

        table2.setStyle(table_style)
        pdf_content.append(table2)
        pdf_content.append(Spacer(1,15))


        section6_table_data = [
            ["Reingreso:", str(max(reentry_period_list))+" hrs", "Carencia:", str(max(phi_list))+" días"]
            
        ]
        print('hola-0')

        section6_table = Table(section6_table_data, colWidths=[100, 150, 100, 150])
        section6_table_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica')])
        section6_table.setStyle(section6_table_style)
        
        pdf_content.append( section6_table)

        #----observaciones
        pdf_content.append(Spacer(1,10))
        pdf_content.append(HorizontalLine(550))  # Adjust the width as needed
        pdf_content.append(Spacer(1,10))

        par_style = getSampleStyleSheet()["Normal"]
        par_style.alignment = 0  # Align left
        print('----------')
        par2_style = getSampleStyleSheet()["Normal"]
        par2_style.alignment = 0  # Align left
        par2_style.textColor = colors.darkgrey
        par1 = Paragraph("Observaciones", par_style)
        par2 = Paragraph(body['observations'], par2_style)
        pdf_content.append(par1)
        pdf_content.append(par2)

        pdf_content.append(Spacer(1,10))
        pdf_content.append(HorizontalLine(550))  # Adjust the width as needed
        pdf_content.append(Spacer(1,10))


        
        # Build the PDF document
        doc.build(pdf_content)

        new_task_order = TaskOrderClass( id_company=company_id,id_task=id_task,file_name=doc_name,order_number=order_number)
        db.session.add(new_task_order)
        db.session.commit()
        
        print('hola')
        return(str(myuuid)+".pdf")
    
    except Exception as error: 
        print(error)
        return False
    

def generatePurchaseOrder(body):

    try:
        print(1)
        # Create a PDF document

        myuuid = uuid.uuid4()
        doc_name = str(myuuid)+".pdf"
        doc = SimpleDocTemplate("files/"+doc_name, pagesize=letter, topMargin=10,leftMargin=10)
        print(str(myuuid)+".pdf")

        company_id=1
        order_creator='John Doe'
        order_number=1
        print("hola")
        company_purchase_orders = getCompanyPurchaseOrders(1)
        print('hola1233')
        print(company_purchase_orders)
        if len(company_purchase_orders)>0:
           order_number = company_purchase_orders[0]['order_number']+1
        
        #-----------------------pdf begins here-------------------
        print('----------')
        # Create a list to hold the content of the PDF
        pdf_content = []

        # Header: "AgroAssist" in green letters
        header_style = getSampleStyleSheet()["Heading1"]
        header_style.textColor = colors.green
        header = Paragraph("AgroAssist", header_style)
        pdf_content.append(header)

        # Section 1: Title
        title_style = getSampleStyleSheet()["Title"]
        title_style.alignment = 0 
        title = Paragraph("Orden de Compra Nº "+str(order_number), title_style)
        pdf_content.append(title)
        print('----------')
        # Section 2: Subtitles (aligned to the left and in gray)
        subtitle_style = getSampleStyleSheet()["Normal"]
        subtitle_style.alignment = 0  # Align left
        subtitle_style.textColor = colors.grey
        print('----------')
        subtitle1 = Paragraph("Orden emitida por "+order_creator, subtitle_style)
        today_date = datetime.now().strftime("%Y-%m-%d")  # Example: "2023 September 04"
        subtitle2 = Paragraph(f"Fecha emisión: {today_date}", subtitle_style)
        pdf_content.extend([subtitle1, Spacer(1, 5), subtitle2, Spacer(1, 5)])
        print('----------')
        pdf_content.append(Spacer(1,10))      
        pdf_content.append(HorizontalLine(550))  # Adjust the width as needed
        pdf_content.append(Spacer(1,10))
        # Section 2: Information in Two Columns
        # Load JSON data (replace this with your actual JSON data)4
        json_data = {
            "rut": "123456789",
            "direccion": "123 Main Street",
            "comuna": "City",
            "telefono": "555-555-5555",
            "enviar_a": "John Doe"
        }

        # Create a table with two columns
        info_table_data = [
            ["RUT:", json_data["rut"], "Teléfono:", json_data["telefono"]],
            ["Dirección:", json_data["direccion"], "Enviar a:", json_data["enviar_a"]],
            ["Comuna:", json_data["comuna"]]
        ]

        info_table = Table(info_table_data, colWidths=[100, 150, 100, 150])
        info_table_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica')])
        info_table.setStyle(info_table_style)
        pdf_content.append(info_table)

        # Section 3: Table with Product Names and Prices
        # Replace this with your actual product data (a list of dictionaries)
        product_data = [
            {"name": "Product 1", "price": 100},
            {"name": "Product 2", "price": 200},
            {"name": "Product 3", "price": 150}
        ]

        # Create a table for product data
        product_table_data = [["Product Name", "Price"]]
        total_price = 0
        for product in product_data:
            product_table_data.append([product["name"], f"${product['price']}"])
            total_price += product["price"]

        product_table = Table(product_table_data, colWidths=[300, 80])
        pdf_content.append(product_table)

        # Add the total price
        pdf_content.append(Paragraph(f"Total: ${total_price}", title_style))

        # Build the PDF document
        doc.build(pdf_content)

        print('hola---------')
        new_purchase_order = PurchaseOrderClass( id_company=company_id,id_quote=body['id_quote'],file_name=doc_name,order_number=order_number)
        db.session.add(new_purchase_order)
        db.session.commit()

        return(str(myuuid)+".pdf")
    except Exception as e:
        print(e) 
        return False
    

def generateQuoterProducts(body):

    try:
        print(1)
        # Create a PDF document

        myuuid = uuid.uuid4()
        doc_name = str(myuuid)+".pdf"
        doc = SimpleDocTemplate("files/"+doc_name, pagesize=letter, topMargin=10,leftMargin=10)
        print(str(myuuid)+".pdf")

        company_id=1
        order_creator='John Doe'
        order_number=1
        print("hola")
        
        print('hola1233')
       
        
        #-----------------------pdf begins here-------------------
        print('----------')
        # Create a list to hold the content of the PDF
        pdf_content = []

        # Header: "AgroAssist" in green letters
        #header_style = getSampleStyleSheet()["Heading1"]
        #header_style.textColor = colors.green
        #header = Paragraph("AgroAssist", header_style)
        #pdf_content.append(header)

        # Section 1: Title
        title_style = getSampleStyleSheet()["Title"]
        title_style.alignment = 0 
        title = Paragraph("Productos a cotizar", title_style)
        pdf_content.append(title)
        print('----------')
        # Section 2: Subtitles (aligned to the left and in gray)
        subtitle_style = getSampleStyleSheet()["Normal"]
        subtitle_style.alignment = 0  # Align left
        subtitle_style.textColor = colors.grey
        
        today_date = datetime.now().strftime("%Y-%m-%d")  # Example: "2023 September 04"
        subtitle2 = Paragraph(f"Fecha emisión: {today_date}", subtitle_style)
        pdf_content.extend([ subtitle2, Spacer(1, 5)])
        print('----------')
        pdf_content.append(Spacer(1,10))      
        pdf_content.append(HorizontalLine(550))  # Adjust the width as needed
        pdf_content.append(Spacer(1,10))
        # Section 2: Information in Two Columns
        # Load JSON data (replace this with your actual JSON data)
        json_data = {
            "rut": "123456789",
            "direccion": "123 Main Street",
            "comuna": "City",
            "telefono": "555-555-5555",
            "enviar_a": "John Doe"
        }

        print("holas")

        product_data=[]
        
        products=getTableDict("Products")
        print(products)
        for key,section in body.items():
            print(section)
            print("------")
            print(section["product_id"])
            print(section["product_needed"])
            print("prdo")
            print(products[section["product_id"]])
            
            row={"name":products[section["product_id"]]["product_name"],"price":str(section["product_needed"]-section["product_stored"])+" cc"}
            product_data.append(row)
            for alternative in section["alternatives"]:
                row={"name":products[section["product_id"]]["product_name"],"price":str(alternative["product_needed"]-alternative["product_stored"])+" cc"}
                product_data.append(row)
        print("chao")  

        # Section 3: Table with Product Names and Prices
        # Replace this with your actual product data (a list of dictionaries)
       

        # Create a table for product data
        product_table_data = [["Producto", "cantidad"]]
        
        for product in product_data:
            product_table_data.append([product["name"], product['price']])
            

        product_table = Table(product_table_data, colWidths=[300, 80])
        pdf_content.append(product_table)

        # Add the total price
        print(pdf_content)
        

        # Build the PDF document
        doc.build(pdf_content)

       

        return(str(myuuid)+".pdf")
    except Exception as e:
        print(e) 
        return False