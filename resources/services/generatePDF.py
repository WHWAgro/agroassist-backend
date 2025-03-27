import math
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak, Frame, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
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
from datetime import datetime  as daytime1
from resources.services.programServices import *
from flask_jwt_extended import jwt_required,get_jwt_identity


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
                
                rows.append(dict(row_as_dict))
            return rows

    except Exception as e:
       
        return False
    
def getFieldTaskOrders(field_id):
    try:
        
        query="""SELECT *
                    FROM task_orders
                    WHERE field_id = """+ str(field_id)+"""
                    order by order_number desc
                
             """
        rows=[]
        with db.engine.begin() as conn:
            result = conn.execute(text(query)).fetchall()
            for row in result:
                row_as_dict = row._mapping
                
                rows.append(dict(row_as_dict))
            return rows

    except Exception as e:
       
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

class HorizontalLine2(Flowable):
    def __init__(self, width, thickness=1):
        super().__init__()
        self.width = width
        self.thickness = thickness
        

    def draw(self):
        self.canv.setLineWidth(self.thickness)
        self.canv.line(375, 0, 375+self.width, 0)

def create_wrapped_paragraph(text):
    

    # Get the "BodyText" style from the sample style sheet
    body_text_style = getSampleStyleSheet()["BodyText"]

    par_style2 = getSampleStyleSheet()["BodyText"]
    par_style2.alignment = 1
    
    return Paragraph(text, par_style2)


def generateTaskOrder(body):

    try:
        print("Generando PDF $$$$$$$$$$$$$$$$$$$$$$$$")
        #print(1)
        # Create a PDF document
        user_id =  get_jwt_identity()
        
        myuuid = uuid.uuid4()
        doc_name = str(myuuid)+".pdf"
        
        doc = SimpleDocTemplate("files/"+doc_name, pagesize=letter, topMargin=10,leftMargin=10)
        print(str(myuuid)+".pdf")
        
        
        id_task=int(body['id_task'])
        user_name=getUserData(user_id)
        
        order_creator=user_name[0]["user_name"]
        order_number=1

        user_companies=getUserCompanies(user_id)
       
        company_id=user_companies[0]["_id"]
        print("compañia")
        print(company_id)
        print(body['id_field'])

        #cambiar nombres ya que ahora busca segun campo y no compañia ya que cada uno trabaja con distintas ordenes de aplicacion
        company_task_orders = getFieldTaskOrders(body['id_field'])


        #print(2)
        if len(company_task_orders)>0:
           order_number = company_task_orders[0]['order_number']+1
        
        #-----------------------pdf begins here-------------------
        #print('----------')
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
        #print('----------')
        # Section 2: Subtitles (aligned to the left and in gray)
        subtitle_style = getSampleStyleSheet()["Normal"]
        subtitle_style.alignment = 0  # Align left
        subtitle_style.textColor = colors.grey
        #print('----------')
        
        today_date = daytime1.now().strftime("%d-%m-%Y")  # Example: "2023 September 04"
        subtitle2 = Paragraph(f"Fecha emisión: {today_date}", subtitle_style)
        pdf_content.extend([ subtitle2, Spacer(1, 5)])
        #print('----------')
        pdf_content.append(Spacer(1,10))      
        pdf_content.append(HorizontalLine(550))  # Adjust the width as needed
        pdf_content.append(Spacer(1,10))
        # Section 5: Two Columns
        # Replace this with your actual data
        products=getTableDict("Products")
        

        companies=getUserCompanies(user_id)
        empresa_data = companies[0]["company_name"]
       # print('----------1')
        fields=getTableDict("field")
        campo_data = fields[body['id_field']]["field_name"]

        cultivo_data = "Cereza"

        plots=getTableDict("plots")
        plots_names = ''
        total_plot_size=0
       # print('----------2')
        ##tablas
        objectives=getTableDict("objectives")
        products=getTableDict("products")
        
             
        
        
        dict_species=getTableDict("species")

        
        
        #print(plots)
        for id_plot in body['id_plots']:
            
            id_species=plots[id_plot]["id_species"] 
            plots_names = plots_names +', '+plots[id_plot]["name"] 
            
            total_plot_size=total_plot_size+plots[id_plot]["size"]
            
            cultivo_data=dict_species[id_species]["species_name"]
           
        if len(plots_names)>0:
            
            plots_names=plots_names[1:]   
        total_hectareas_data = total_plot_size
       # print('----------3')
        # Create a table with two columns

        machinery=getTableDict("machinery")
       # print('machinery///////////1')
        sprayer_size=1
        data_list = body['asignees']
        print('QQQQWWWWWW')
        back_pump=False
        other_machinery=False
        if data_list[0]['id_sprayer']==None:
            back_pump=True
            print('hola8')
            
            for elem in data_list:
                print(elem)
                elem['id_sprayer']= elem['id_tractor']
       
        for item in data_list:
            sprayer_size=machinery[item["id_sprayer"]]["size"]+sprayer_size
            
        wetting=body['wetting']
        n_maquinadas=float(total_hectareas_data*(wetting/sprayer_size))

        section5_table_data = [
            [" ","Empresa:", empresa_data, " ","Cultivo:", cultivo_data],
            [" ","Campo:", campo_data, " ","Total Hectareas:", '{:,.1f}'.format(total_hectareas_data).replace(',','*').replace('.', ',').replace('*','.').replace(',0','')],
            [" ",'Mojamiento',str(wetting)+"L"," ",'N Maquinadas',  '{:,.1f}'.format(n_maquinadas).replace(',','*').replace('.', ',').replace('*','.').replace(',0','')]
        ]
        #print('----------4')

        section5_table = Table(section5_table_data, colWidths=[40,80, 150,70 ,80, 150])
        section5_table_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica')])
        section5_table.setStyle(section5_table_style)
       # print('----------5')
        pdf_content.append( section5_table)
        pdf_content.append(Spacer(1,10))
        pdf_content.append(HorizontalLine(550))  # Adjust the width as needed
        pdf_content.append(Spacer(1,10))
        application_date = body['application_date']
        
        
        section3_table_data = [
            ["Fecha de aplicación:", application_date, "Cuarteles:", plots_names],
             
            
        ]
        print(section3_table_data)
        wrapped_row1 = [[create_wrapped_paragraph(cell) for cell in section3_table_data[0]]]
        
        #print('hola-1')

        section3_table = Table(wrapped_row1, colWidths=[150, 150, 100, 150])
        
        section3_table_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica')])
        section3_table.setStyle(section3_table_style)

        section3_table_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica')])

        section3_table__0_data = [
            ["","Hora Inicio", "", "Hora Término", ""],
             
            
        ]
        section3_table_0 = Table(section3_table__0_data, colWidths=[45,150, 148, 100, 150])
        section3_table_0.setStyle(section3_table_style)
        
        pdf_content.append( section3_table)
        pdf_content.append( section3_table_0)
        pdf_content.append(Spacer(1,10))
        pdf_content.append(HorizontalLine(550))  # Adjust the width as needed
        pdf_content.append(Spacer(1,10))

        ##operadores----------------
        data_list = body['asignees']
        if back_pump:
           
            for elem in data_list:
                elem['id_sprayer']= elem['id_tractor']
            table_data = [['Operador','Bomba de espalda']]  # Start with the headers as the first row

            # Add the data rows
            workers=getTableDict("workers")
            machinery=getTableDict("machinery")
            #print('machinery///////////')
            sprayer_size=1
            for item in data_list:
                row_data = [workers[item["id_operator"]]["name"],machinery[item["id_sprayer"]]["name"]]
                sprayer_size=machinery[item["id_sprayer"]]["size"]
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

        else:
            
            
        # Create a list to hold the table data
            table_data = [['Operador','Tractor','Nebulizador']]  # Start with the headers as the first row
            

            # Add the data rows
            workers=getTableDict("workers")
            machinery=getTableDict("machinery")
            for item in data_list:
                if machinery[item["id_sprayer"]]["id_machinery_type"] == 4:
                    other_machinery=True

            if other_machinery==True:
                table_data = [['Operador','Tractor','Otro']]
            #print('machinery///////////')
            sprayer_size=1
            for item in data_list:
                if item["id_tractor"]==None:
                    row_data = [workers[item["id_operator"]]["name"],'',machinery[item["id_sprayer"]]["name"]]
                else:
                    row_data = [workers[item["id_operator"]]["name"],machinery[item["id_tractor"]]["name"],machinery[item["id_sprayer"]]["name"]]
                sprayer_size=machinery[item["id_sprayer"]]["size"]
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
        #print('hola0')
        pdf_content.append(Spacer(1,10))
        pdf_content.append(HorizontalLine(550))  # Adjust the width as needed
        pdf_content.append(Spacer(1,10))
        data_list2 = body['products']
        

        # Create a list to hold the table data
        table_data2 = [[" ",'Producto Comercial',"Compuesto Activo",'Objetivo','Dosis x Há','Dosis','Total Producto \n Comercial','Cantidad \n x Maquinada \n Completa']] # Start with the headers as the first row

        print('hola-productos')
        # Add the data rows
        
        
        

        
        
        print("$$$$##############$$$$$")
        
        
       

        

        
        objetivos=[]
        productos=[]
        ingredientes=[]
        dosis=[]
        dosis_unidad=[]
        application_method=1
        dosis_responsible=[]
        operators=[]
        sprayer=[]
        tractor=[]
        volumen_total=total_hectareas_data*wetting

        dosage_responsible=body['dosification_responsible']
        for el in dosage_responsible:
            dosis_responsible.append(el['id_operator'])

        asignees=body['asignees']
        for asig in asignees:
            operators.append(asig['id_operator'])
            sprayer.append(asig['id_sprayer'])
            tractor.append(asig['id_tractor'])

        if back_pump:
            application_method=2
        if other_machinery:
            application_method=3


        final_phis=[]
        for item in data_list2:
            print("$$$$##############$$$$$------------------------------------------------------------------------------*******")

            if item["id_objective"]!=0:
                objetivos.append(item["id_objective"])
            else:
                objetivos.append(item["objective_name"])



           
            
            k_filter1 = "id_objective"
            v_match1 = item["id_objective"]
            
            print("or0")
            
            dosage=0
            dosage_unit=1
            
            
            if can_cast_to_number(item["id_product"])==False:
                print("or1")
                print(item)
                index = item["products_names"].index(item["id_product"])
                dosage=item["dosages"][index]
                dosage_unit=item["id_dosage_unit"][index]
                final_phis.append(item["phis"][index])
                print("or2")
                productos.append(item["id_product"])
                ingredientes.append(item["ingredients"][index])
                dosis.append(dosage)
                dosis_unidad.append(dosage_unit)
            else:
                print("essta en plataforma el producto")
                
                
                product=item["id_product"]
                found=False
                for index, option in enumerate(item["products_ids"]):
                    if int(option)==0:
                        continue

                    

                    if int(product) == int(option):
                        found=True
                        print('esta')
                        

                   
                    elif int(product) in products:
                                
                               if products[int(option)]['chemical_compounds']==products[int(product)]['chemical_compounds']:
                                   print('buscandolo')
                                   found=True
                  

                    
                    
                    if found==True:
                        productos.append(product)
                        ingredientes.append(product)
                        dosis.append(item["dosages"][index])
                        dosis_unidad.append(item["id_dosage_unit"][index])
                        dosage=item["dosages"][index]
                        dosage_unit=item["id_dosage_unit"][index]
                        final_phis.append(item["phis"][index])
                        break
            print("or5")      
            unit=""
            unit_dosage=""
            total_product=0

            unit_hectare=""
            dosage_hectare=0
            
            
            dosage=float(dosage)
            print("or6")

            if dosage_unit == 1:
                print(" 1")
                unit=" gr"
                unit_dosage="gr/100L"
                total_product=dosage*(wetting/100)*total_hectareas_data
                if total_product>1000:
                    total_product=total_product/1000
                    unit=" Kg"
                unit_hectare="gr/Há"
                dosage_hectare=dosage*(wetting/100)
            elif dosage_unit == 9:
                print(" 1")
                unit=" gr Ingrediente Activo"
                unit_dosage="gr Ingrediente Activo/100L"
                total_product=dosage*(wetting/100)*total_hectareas_data
                if total_product>1000:
                    total_product=total_product/1000
                    unit=" Kg Ingrediente Activo"
                unit_hectare="gr Ingrediente Activo /Há"
                dosage_hectare=dosage*(wetting/100)
            elif dosage_unit == 2:
                print(" 2")
                unit=" Kg"
                unit_dosage="Kg/100L"
                total_product=dosage*(wetting/100)*total_hectareas_data
                unit_hectare="Kg/Há"
                dosage_hectare=dosage*(wetting/100)
            elif dosage_unit == 10:
                print(" 2")
                unit=" Kg Ingrediente Activo"
                unit_dosage="Kg Ingrediente Activo/100L"
                total_product=dosage*(wetting/100)*total_hectareas_data
                unit_hectare="Kg Ingrediente Activo/Há"
                dosage_hectare=dosage*(wetting/100)
            elif dosage_unit == 3:
                print(" 3")
                unit=" gr"
                unit_dosage="gr/100L"
                total_product=dosage*total_hectareas_data
                if total_product>1000:
                    total_product=total_product/1000
                    unit=" Kg"
                unit_hectare="gr/Há"
                dosage_hectare=dosage
                dosage=str(dosage/(wetting/100))
            elif dosage_unit == 4:
                print(" 4")
                unit=" Kg"
                unit_dosage="Kg/100L"
                total_product=dosage*total_hectareas_data
                
                unit_hectare="Kg/Há"
                dosage_hectare=dosage
                dosage=str(dosage/(wetting/100))
            if dosage_unit == 5:
                print(" 5")
                unit=" cc"
                unit_dosage="cc/100L"
                total_product=dosage*(wetting/100)*total_hectareas_data
                if total_product>1000:
                    total_product=total_product/1000
                    unit=" L"
                unit_hectare="cc/Há"
                dosage_hectare=dosage*(wetting/100)
            if dosage_unit == 11:
                print(" 5")
                unit=" cc Ingrediente Activo"
                unit_dosage="cc Ingrediente Activo/100L"
                total_product=dosage*(wetting/100)*total_hectareas_data
                if total_product>1000:
                    total_product=total_product/1000
                    unit=" L Ingrediente Activo"
                unit_hectare="cc Ingrediente Activo/Há"
                dosage_hectare=dosage*(wetting/100)
            elif dosage_unit == 6:
                print(" 6")
                unit=" L"
                unit_dosage="L/100L"
                total_product=dosage*(wetting/100)*total_hectareas_data
                unit_hectare="L/Há"
                dosage_hectare=dosage*(wetting/100)
            elif dosage_unit == 12:
                print(" 6")
                unit=" L Ingrediente Activo"
                unit_dosage="L Ingrediente Activo/100L"
                total_product=dosage*(wetting/100)*total_hectareas_data
                unit_hectare="L Ingrediente Activo/Há"
                dosage_hectare=dosage*(wetting/100)
            elif dosage_unit == 7:
                print(" 7")
                unit=" cc"
                unit_dosage="cc/100L"
                total_product=dosage*total_hectareas_data
                if total_product>1000:
                    total_product=total_product/1000
                    unit=" L"
                
                unit_hectare="cc/Há"
                dosage_hectare=dosage
                dosage=str(dosage/(wetting/100))
            elif dosage_unit == 8:
                print(" 8")
                unit=" L"
                unit_dosage="L/100L"
                total_product=dosage*total_hectareas_data
                unit_hectare="L/Há"
                dosage_hectare=dosage
                dosage=str(dosage/(wetting/100))
            print("cuartel 1")
            hola='{:,.2f}'.format(total_product).replace(',','*').replace('.', ',').replace('*','.').replace(',00','')
            dosage='{:,.2f}'.format(float(dosage)).replace(',','*').replace('.', ',').replace('*','.').replace(',00','')
            print("cuartel 2")
            dosage_hectare='{:,.2f}'.format(float(dosage_hectare)).replace(',','*').replace('.', ',').replace('*','.').replace(',00','')
            print("cuartel 3")
            totalXmaquinada='{:,.2f}'.format(float(total_product/n_maquinadas)).replace(',','*').replace('.', ',').replace('*','.').replace(',00','')
            
            print('-products')
            
            
            objective=""
            product_name=""
            product_chemichal=""
            if can_cast_to_number(item["id_product"])==False:
                index = item["products_names"].index(item["id_product"])
                product_name=item["id_product"]
                product_chemichal=item["ingredients"][index]
                
            else:
                print("aqui")
                product_name=products[item["id_product"]]["product_name"]
                product_chemichal=products[item["id_product"]]["chemical_compounds"]

            
            if item["id_objective"]==0:
                objective=item["objective_name"]
            else:
                print("aca")
                objective=objectives[item["id_objective"]]["objective_name"]
                print("por aca")
            
            row_data = [" ",str(product_name),str(product_chemichal),objective,str(dosage_hectare)+unit_hectare,str(dosage)+unit_dosage,hola+unit,totalXmaquinada+unit]
            print('productof///////////////')
            print(row_data)
            
            wrapped_row = [create_wrapped_paragraph(cell) for cell in row_data]
            print("fin")
           

            table_data2.append(wrapped_row)
        print('hola-footer')
        # Create a table with the data
        table2 = Table(table_data2,colWidths=[67,102, 102, 118,78,78,68, 68])
        print('hola3')
        # Add style to the table
        table_style = TableStyle([
            ('BACKGROUND', (1, 0), (-1, 0), colors.lightgreen),  # Header background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center-align all cells
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
            
            ('GRID', (1, 0), (-1, -1), 1, colors.green),  # Gridlines
            ('FONTSIZE', (0, 0), (-1, -1) , 8 )
        ])

      
       

        table2.setStyle(table_style)
        
        pdf_content.append(table2)
        pdf_content.append(Spacer(1,15))


        section6_table_data = []
        print('-----**********finalizando phis')
        print(final_phis)


        if "reentry" in body:
            section6_table_data = [
            ["Reingreso:", '{:,.1f}'.format(body["reentry"]).replace(',','*').replace('.', ',').replace('*','.').replace(',0','')+" hrs", "Carencia:",'{:,.1f}'.format(max(final_phis)).replace(',','*').replace('.', ',').replace('*','.').replace(',0','') +" días"]
            
        ]
            print(section6_table_data)

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


        par_style = getSampleStyleSheet()["Normal"]
        par_style.alignment = 0  # Align left
        print('----------2')
        par2_style = getSampleStyleSheet()["Normal"]
        par2_style.alignment = 0  # Align left
        
        par1 = Paragraph("Obligaciones", par_style)
        par2 = Paragraph("[ ]Leer la etiqueta de los productos a aplicar, cualquier duda consultar", par2_style)
        par3 = Paragraph("[ ]Usar equipos de protección personal completo", par2_style)
        par4 = Paragraph("[ ]Hacer triple lavado de envases vaciós ", par2_style)
        par5 = Paragraph("[ ]Poner bandera roja en los sectores aplicados", par2_style)
        pdf_content.append(par1)
        pdf_content.append(par2)
        pdf_content.append(par3)
        pdf_content.append(par4)
        pdf_content.append(par5)

        pdf_content.append(Spacer(1,10))
        pdf_content.append(HorizontalLine2(125))
          # Adjust the width as needed
        pdf_content.append(Spacer(1,10))
        par_style = getSampleStyleSheet()["Normal"]
        par_style.alignment = 2  # Align left
        par_style.whiteSpace = 'preserve'
        par1 = Paragraph("Nombre Aplicador:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;", par_style)
        pdf_content.append(par1)
        pdf_content.append(Spacer(1,5))
        subtitle1 = Paragraph("Orden emitida por: "+order_creator,par_style)
        
        pdf_content.append(subtitle1)

        print("creando pdf")
        # Build the PDF document
        doc.build(pdf_content)
        
        alias='ODA_'+str(application_date)+'_'+campo_data.replace(' ','-')+'_N-'+str(order_number)+'.pdf'
        print("creando pdf2")

      
        real_task_id=None
        
        if "reentry" in body :
            print("reentry")
          
            
            plots_format=str(body['id_plots']).replace('[','(').replace(']',')')

            adjacent_plot_tasks=getAdjacentPlotTasks(id_task,plots_format)
                    
            for apt in adjacent_plot_tasks:
                
                apt_id=apt['_id']
                real_task_id=apt_id
                       
                new_task_order = TaskOrderClass( application_date=application_date,application_date_end=application_date,wetting=wetting,id_company=company_id,id_task=apt_id,file_name=doc_name,order_number=order_number,plots=str(body['id_plots']),alias=alias,reentry=body["reentry"],phi=max(final_phis)
                ,objectives=str(objetivos),products=str(productos),ingredients=str(ingredientes),dosage=str(dosis),dosage_unit=str(dosis_unidad),application_method=application_method
                ,dosage_responsible=str(dosis_responsible),operators=str(operators),sprayer=str(sprayer),tractor=str(tractor),volumen_total=volumen_total,field_id=body['id_field'])

        
                db.session.add(new_task_order)
                        
                        
            db.session.commit()
        else:
            new_task_order = TaskOrderClass( application_date=application_date,application_date_end=application_date,wetting=wetting,id_company=company_id,id_task=id_task,file_name=doc_name,order_number=order_number,plots=str(body['id_plots']),alias=alias)

        
        
            db.session.add(new_task_order,real_task_id)
            db.session.commit()
        
        print('hola10')
        return(str(myuuid)+".pdf"),real_task_id
    
    except Exception as error: 
        print(error)
        return False,False
    
def formatter(valor):
            
            formated_number='{:,.2f}'.format(float(valor)).replace(',','*').replace('.', ',').replace('*','.').split(',')[0]

            return formated_number
def formatter2(valor):
            print('formatter')
            print(valor)
            if valor>9999:
                print(1)
                valor= valor/1000
                print(valor)
                values='{:,.2f}'.format(float(valor)).replace(',','*').replace('.', ',').replace('*','.').split(',')

                formated_number=values[0]
                print(values)
                print(len(values))
                print(values[1]!='00')
                
                if len(values)>=2 and values[1]!='00':
                    print(2)
                    formated_number='{:,.2f}'.format(float(valor)).replace(',','*').replace('.', ',').replace('*','.')
                return formated_number

            print(3)
            formated_number='{:,.2f}'.format(float(valor)).replace(',','*').replace('.', ',').replace('*','.').split(',')[0]

            return formated_number
def generatePurchaseOrder(body):

    try:
        print(1)
        # Create a PDF document
        user_id =  get_jwt_identity()
        user_name=getUserData(user_id)
        
        order_creator=user_name[0]["user_name"]
        myuuid = uuid.uuid4()
        doc_name = str(myuuid)+".pdf"
        doc = SimpleDocTemplate("files/"+doc_name, pagesize=letter, topMargin=10,leftMargin=10)
        print(str(myuuid)+".pdf")
        products=getTableDict("products")
        print("hol1")
        user_companies=getUserCompanies(user_id)
        print(user_companies)
        print("hol2")
        company_id=user_companies[0]["_id"]
        print("hol3")
        companies=getTableDict("company")
        company=companies[company_id]
        order_number=1
        print("hola4")
        company_purchase_orders = getCompanyPurchaseOrders(company_id)
        print('hola1233')
        print(company_purchase_orders)
        if len(company_purchase_orders)>0:
           order_number = company_purchase_orders[0]['order_number']+1
        
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
        title = Paragraph("Orden de Compra Nº "+str(order_number), title_style)
        pdf_content.append(title)
        print('----------')
        # Section 2: Subtitles (aligned to the left and in gray)
        subtitle_style = getSampleStyleSheet()["Normal"]
        subtitle_style.alignment = 0  # Align left
        subtitle_style.textColor = colors.grey
        print('----------')
        subtitle1 = Paragraph("Proveedor :"+body["provider_name"], subtitle_style)
        today_date = daytime1.now().strftime("%d-%m-%Y")  # Example: "2023 September 04"
        subtitle2 = Paragraph(f"Fecha emisión: {today_date}", subtitle_style)
        pdf_content.extend([subtitle1, Spacer(1, 5), subtitle2, Spacer(1, 5)])
        print('----------')
        pdf_content.append(Spacer(1,10))      
        pdf_content.append(HorizontalLine(550))  # Adjust the width as needed
        pdf_content.append(Spacer(1,10))
        # Section 2: Information in Two Columns
        # Load JSON data (replace this with your actual JSON data)4
        json_data = body
        
        
        # Create a table with two columns
        info_table_data = [
            ["Facturar a:", company["company_name"], "", ""],
            ["RUT:", company["rut"], "Plazo entrega:", json_data["delivery_date"]],
            ["Plazo pago:", json_data["payment_term"],"",""],
            ["Enviar a:", json_data["delivery_address"], "",""],
            ["Observaciones:",json_data["observations"],"",""]
            
        ]

        info_table = Table(info_table_data, colWidths=[100, 150, 100, 150])
        info_table_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica')])
        info_table.setStyle(info_table_style)
        pdf_content.append(info_table)
        pdf_content.append(Spacer(1,10))      
        pdf_content.append(HorizontalLine(550))  # Adjust the width as needed
        pdf_content.append(Spacer(1,10))

        # Section 3: Table with Product Names and Prices
        # Replace this with your actual product data (a list of dictionaries)
        product_data = [
            {"name": "Product 1", "price": 100},
            {"name": "Product 2", "price": 200},
            {"name": "Product 3", "price": 150}
        ]

        # Start with the headers as the first row

        print('hola-productos')
        # Add the data rows
       

        
        
       
        print("$$$$##############$$$-$$")
        

        
       
        table_data2 = [['Nombre Producto','Formato Envase','Cantidad','Precio Unitario','Precio Total']] 
        subtotal=0
        
        
        for item in body["products"]:
            format_unit={'1':'cc','2':'Lt','3':'gr','4':'Kg',}
            item["format_unit"]=format_unit[str(item['container_unit_id'])]
            
            product_total=item["number_products"]*item["container_price_clp"]
           
            subtotal=subtotal+product_total
            

            
            total_price_format =str(formatter(item["number_products"]*item["container_price_clp"]))
            container_size_format=str(formatter(item["container_size"]))
            container_price_format=str(formatter(item["container_price_clp"]))
            
            if can_cast_to_number(item["id_product"]):
                product_alternative=products[int(item["id_product"])]["product_name"]
            else:
                product_alternative=item["id_product"]

            row_data = [product_alternative,container_size_format+" "+item["format_unit"],item["number_products"],"$"+container_price_format,"$"+total_price_format]
            print(row_data)
            wrapped_row = [create_wrapped_paragraph(str(cell)) for cell in row_data]
            
            table_data2.append(wrapped_row)
        table_data2.append(["","","","Sub-Total","$"+str(formatter(subtotal))])
        table_data2.append(["","","","IVA 19%","$"+str(formatter(subtotal*0.19))])
        table_data2.append(["","","","Total","$"+str(formatter(subtotal*1.19))])
        print('hola-footer')
        # Create a table with the data
        table2 = Table(table_data2,colWidths=[140, 120, 60,100,100 ])
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
       
        pdf_content.append(Spacer(1,10))      
        pdf_content.append(HorizontalLine(550))  # Adjust the width as needed
        pdf_content.append(Spacer(1,10))

       

        # Add the total price
        #pdf_content.append(Paragraph(f"Total: ${total_price}", title_style))

        # Build the PDF document
        doc.build(pdf_content)
        alias='ODC_'+str(today_date)+'_'+body["provider_name"].replace(' ','-')+'_N-'+str(order_number)+'.pdf'

        print('hola---------')
        new_purchase_order = PurchaseOrderClass( id_company=company_id,id_quote=body['id_quote'],file_name=doc_name,order_number=order_number,alias=alias)
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
        print("holaf")
        
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
        
        today_date = daytime1.now().strftime("%d-%m-%Y")  # Example: "2023 September 04"
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
        
        for key,section in body.items():
            

            product_unit=' gr'
            if section["product_needed_unit_id"]>=5 and not (section["product_needed_unit_id"]  in (9,10)):
                print('enter 1')
                product_unit=' cc'
                if max(section["product_needed"]-section["product_stored"],0) >9999:
                    product_unit=' Lt'
                    print('enter 2')
            
            elif (max(section["product_needed"]-section["product_stored"],0) >9999):
                print('enter 3')
                product_unit=' Kg'
            print('exit 1')

            final_product=str(formatter2(max(section["product_needed"]-section["product_stored"],0)))

            product_name=""
            if can_cast_to_number(section["product_id"]):
                product_name=products[int(section["product_id"])]["product_name"]
            else:
                product_name=section["product_id"]
            
            row={"name":product_name,"price":final_product+product_unit}
            print('siguiente')
            product_data.append(row)
            for alternative in section["alternatives"]:
                print('******alternative')
                print(alternative)
                product_alternative=""
                if can_cast_to_number(alternative["product_id"]):
                    product_alternative=products[int(alternative["product_id"])]["product_name"]
                else:
                    product_alternative=section["product_id"]
                print('nombre agragado')
                product_unit=' gr'
                if alternative["product_needed_unit_id"]>=5 and not (alternative["product_needed_unit_id"]  in (9,10)):
                    print('enter 1')
                    product_unit=' cc'
                    if max(alternative["product_needed"]-alternative["product_stored"],0) >9999:
                        product_unit=' Lt'
                        print('enter 2')
                
                elif (max(alternative["product_needed"]-alternative["product_stored"],0) >9999):
                    print('enter 3')
                    product_unit=' Kg'
                print('exit 1')

                final_product=str(formatter2(max(alternative["product_needed"]-alternative["product_stored"],0)))

                product_name=""
                if can_cast_to_number(alternative["product_id"]):
                    product_name=products[int(alternative["product_id"])]["product_name"]
                else:
                    product_name=alternative["product_id"]


                row={"name":product_alternative,"price":final_product+product_unit}


                product_data.append(row)
          

        # Section 3: Table with Product Names and Prices
        # Replace this with your actual product data (a list of dictionaries)
       

        # Create a table for product data
        product_table_data = [["Producto", "Cantidad"]]
        print('listo')
        
        for product in product_data:
            product_table_data.append([product["name"], product['price']])
            

        product_table = Table(product_table_data, colWidths=[300, 80])
        pdf_content.append(product_table)

        # Add the total price
        
        

        # Build the PDF document
        doc.build(pdf_content)

       

        return(str(myuuid)+".pdf")
    except Exception as e:
        print(e) 
        return False