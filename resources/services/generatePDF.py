from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak, Frame, Flowable
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import uuid
import json
from database.models.Program import TaskOrderClass,PlotClass,TaskClass,QuoterClass,QuoteClass,QuoteProductClass,ProgramCompaniesClass,MarketProgramClass,ProgramClass,userClass,SpeciesClass,FieldClass,ProgramTaskClass,TaskObjectivesClass, db,auth
from sqlalchemy import  text,select
from flask import g
import jwt
import time
from sqlalchemy.orm import class_mapper
import ast
from datetime import datetime  


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

        myuuid = uuid.uuid4()
        doc_name = str(myuuid)+".pdf"
        doc = SimpleDocTemplate("files/"+doc_name, pagesize=letter, topMargin=10,leftMargin=10)
        print(str(myuuid)+".pdf")

        company_id=1
        id_task=body['id_task']
        order_creator='John Doe'
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
        # Section 5: Two Columns
        # Replace this with your actual data
        empresa_data = "Agroassist test"
        campo_data = body['id_field']
        cultivo_data = "Cereza"
        total_hectareas_data = 10*len(body['id_plots'])
        print('----------3')
        # Create a table with two columns
        section5_table_data = [
            ["Empresa:", empresa_data, "Cultivo:", cultivo_data],
            ["Campo:", campo_data, "Total Hectareas:", total_hectareas_data],
            ['Mojamieto','','','']
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
        plots = ''
        for plot in body['id_plots']:
            plots = plots+' '+str(plot)
        
        section3_table_data = [
            ["Fecha de aplicacion:", application_date, "Cuarteles:", plots]
            
        ]
        print('hola-0')

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
        headers = list(data_list[0].keys())

        # Create a list to hold the table data
        table_data = [['Operador','Tractor','Rociador']]  # Start with the headers as the first row

        # Add the data rows
        for item in data_list:
            row_data = [item[header] for header in headers]
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
        data_list2 = body['asignees']
        headers2 = list(data_list2[0].keys())

        # Create a list to hold the table data
        table_data2 = [['Producto','Objetivo','Dosis x 100 Lt','Total Producto']] # Start with the headers as the first row

        print('hola1')
        # Add the data rows
        for item in data_list2:
            row_data = [item[header] for header in headers2]
            row_data = row_data[0:2]+['','']
            print(row_data)
            table_data2.append(row_data)
        print('hola2')
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
            ["Reingreso:", '', "Carencia:", '']
            
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
        # Create a PDF document

        myuuid = uuid.uuid4()

        doc = SimpleDocTemplate(str(myuuid)+".pdf", pagesize=letter)
        print(str(myuuid)+".pdf")

        # Create a list to hold the content of the PDF
        pdf_content = []

        # Section 1: Title
        title_style = getSampleStyleSheet()["Title"]
        title = Paragraph("Orden de Compra", title_style)
        pdf_content.append(title)

        # Section 2: Information in Two Columns
        # Load JSON data (replace this with your actual JSON data)
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

        return(str(myuuid)+".pdf")
    except: 
        return False