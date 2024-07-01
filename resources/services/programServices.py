import json
from database.models.Program import TaskOrderClass,PlotTasksClass,FieldWeatherLocationsAssignClass,QuoteRowClass,QuoterProductClass,PlotClass,TaskClass,QuoterClass,QuoteClass,ProgramCompaniesClass,MarketProgramClass,ProgramClass,userClass,SpeciesClass,FieldClass,ProgramTaskClass,TaskObjectivesClass, db,auth
from sqlalchemy import  text,select
from flask import g
import jwt
import time
from sqlalchemy.orm import class_mapper
import ast
import uuid
import datetime



def getTable(table,field=None,value=None):
   
    
    try:
        
        query="""SELECT *
                FROM """+table+"""
             """
        
        if field!=None:
            query="""SELECT *
                FROM """+table+"""
                WHERE """+field+"""="""+str(value)+"""
             """

        rows=[]
        with db.engine.begin() as conn:
            result = conn.execute(text(query)).fetchall()
            for row in result:
                row_as_dict = row._mapping
                
                rows.append(dict(row_as_dict))
            return rows

    except Exception as e:
        print(e)
        return False
    
def getTableDict(table):
    table_elements=getTable(table)
    products_dict={}
    for el in table_elements:
        products_dict[el["_id"]]=el

    return products_dict


def getProductsAlt(products):
        productsAlt=[]

    

        for o_index,objective in enumerate(products):
            
            productsAlt.append([])
            for aa_index,and_alt in enumerate(objective):
                
                
                alternatives=[]
                and_alt_format='('
                for market in and_alt:
            
                    and_alt_format=and_alt_format+str(market)+","
                and_alt_format = and_alt_format[:-1]
                and_alt_format=and_alt_format+" )"
                
                
                query="""WITH RankedProducts AS (
                                    SELECT 
                                        p2._id,
                                        p2.product_name,
                                        ROW_NUMBER() OVER (PARTITION BY p2.product_name ORDER BY p2._id) AS rn
                                    FROM 
                                        products p1
                                    LEFT JOIN 
                                        products p2
                                    ON 
                                        p1.chemical_compounds = p2.chemical_compounds
                                    WHERE 
                                        p1._id IN """ + str(and_alt_format) + """
                                )
                                SELECT 
                                    _id
                                FROM 
                                    RankedProducts
                                WHERE 
                                    rn = 1;
                        
                    """
                

               
                with db.engine.begin() as conn:
                    result = conn.execute(text(query)).fetchall()
                    for row in result:
                        row_as_dict = row._mapping
                            
                        alternatives.append(row_as_dict['_id'])
                
                    
                        
                                
                productsAlt[o_index].append(alternatives)
                


        return productsAlt
    
def getMoments(id_program,start,end):
   
    
    try:
        
        query="""SELECT pt._id,wetting,id_product,dosage,dosage_parts_per_unit,id_objective
                FROM program_tasks  pt
                left join task_objectives  ta
                    on pt._id=ta.id_task
                WHERE id_program = """+ str(id_program)+"""
                
                AND (
                    (start_date <= DATE('"""+ end +"""') AND end_date >= DATE('"""+ start +"""'))
                    )
                
             """
        

        rows=[]
        with db.engine.begin() as conn:
            result = conn.execute(text(query)).fetchall()
            for row in result:
                row_as_dict = row._mapping
                
                rows.append(dict(row_as_dict))
           
            return rows
        

    except Exception as e:
        print(e)
        return False

def getUserCompanies(user):
   
    
    try:
        

        query="""SELECT c._id,c.company_name as company_name 
                    FROM user_company as  uc
                    left join company as c
                    on c._id=uc.company_id
                where uc.user_id ="""+str(user)+"""
                order by uc._id asc
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

def getUserData(user):
   
    
    try:
        

        query="""SELECT *
                from users
                where _id ="""+str(user)+"""
                
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

def verify_password(username_or_token, password):
    # first try token
    user = userClass.verify_auth_token(username_or_token)
    # then check for username and password pair
    if not user:
        user = userClass.query.filter_by(email = username_or_token).first()
        if not user or not user.verify_password(password) or user.active==False:
            return False
    g.user = user
    return True


def getPrograms(id_usuario,company_id):
    
    try:
        
        query="""SELECT p._id as _id,id_user,program_name,species_name,market_name,published,updated_at FROM programs as p
                left join species as s on p.id_species= s._id
                left join market_program as mp on p._id=mp.program_id
                left join market as m on m._id=mp.market_id
                left join program_companies as pc on p._id=pc.id_program
                WHERE p.id_user = """+ str(id_usuario)+"""
                or pc.id_company in """+ str(company_id)+"""
                ORDER BY p._id DESC

                 
                
             """
        
        
        rows=[]
        with db.engine.begin() as conn:
            result = conn.execute(text(query)).fetchall()
            
            for row in result:
                row_as_dict = row._mapping
                
                rows.append(dict(row_as_dict))
            return rows

    except Exception as e:
        print(e)
        return False
    
def getProgramsMarketFilter(id_usuario,company_id,markets):
    
    try:
        
        query="""SELECT distinct(p._id)  FROM programs as p
                left join species as s on p.id_species= s._id
                left join market_program as mp on p._id=mp.program_id
                left join program_companies as pc on p._id=pc.id_program
                WHERE (p.id_user = """+ str(id_usuario)+"""
                or pc.id_company in """+ str(company_id)+""") 
                and mp.market_id in """+ str(markets)+"""

                 
                
             """
        
        
        rows=[]
        with db.engine.begin() as conn:
            result = conn.execute(text(query)).fetchall()
            print(result)
            for row in result:
                row_as_dict = row._mapping
                print(row_as_dict)
                rows.append(dict(row_as_dict))
            return rows

    except Exception as e:
        print(e)
        return False
    

def getFields(id_company):
    
    try:
        
        
        
        results = FieldClass.query.filter_by(company_id=id_company).all()

        result_list = []
        for result in results:
            result_dict = {}
            for key, value in result.__dict__.items():
                if (not key.startswith('_')) and key not in ('latitude','longitude'):
                    result_dict[key] = value
                elif key=='_id':
                    result_dict[key] = value
            result_list.append(result_dict)

        
        return result_list

    except Exception as e:
        print(e)
        return False
    

    

def getPlots(id_field):
    
    try:
        
        
        
        results = PlotClass.query.filter_by(id_field=id_field).all()

        result_list = []
        for result in results:
            result_dict = {}
            for key, value in result.__dict__.items():
                if not key.startswith('_'):
                    result_dict[key] = value
                elif key=='_id':
                    result_dict[key] = value
            result_list.append(result_dict)
        
        return result_list

    except Exception as e:
        print(e)
        return False
    

def getProgramDetails(id_usuario,id_programa):
    
    try:
        
        query="""SELECT p._id as _id,id_species,id_user,user_name,program_name,species_name,market_id,published,updated_at FROM programs as p
                left join species as s on p.id_species= s._id
                left join market_program as mp on p._id=mp.program_id
                left join market as m on m._id=mp.market_id
                left join  users on p.id_user= users._id
                
                WHERE p._id = """+ str(id_programa)+"""
                
             """
        query_tasks="""SELECT pt._id as _id
                FROM programs as p
                left join program_tasks as pt on p._id=pt.id_program
                
                WHERE p._id = """+ str(id_programa)+"""
                order by pt.start_date asc,pt._id
             """
        
        query_companies="""SELECT pf.id_company as _id
                FROM programs as p
                left join program_companies as pf on p._id=pf.id_program
                
                
                WHERE p._id = """+ str(id_programa)+"""
                
             """
        
        
        rows=[]
        rows_tasks=[]
        rows_fields=[]
        with db.engine.begin() as conn:
            result = conn.execute(text(query)).fetchall()
            result_tasks= conn.execute(text(query_tasks)).fetchall()
            result_fields= conn.execute(text(query_companies)).fetchall()
            for row in result:
                row_as_dict = row._mapping
                
                rows.append(dict(row_as_dict))
            for row in result_tasks:
                row_as_dict = row._mapping
                
                rows_tasks.append(dict(row_as_dict))
            for row in result_fields:
                row_as_dict = row._mapping
                
                rows_fields.append(dict(row_as_dict))
        
        
        return rows,rows_fields,rows_tasks

    except Exception as e:
        print(e)
        return False
    

def getTaskDetails(id_moment):
    
    try:
        
        
        query_tasks="""SELECT pt._id as _id,id_program,id_moment_type,end_date,start_date,moment_value,wetting,observations,id_objective,id_product,dosage,dosage_parts_per_unit
                
              
                from program_tasks as pt 
                left join task_objectives as tp on pt._id=tp.id_task
                where pt._id = """+ str(id_moment)+"""
                
             """
        
        
        
        rows_tasks=[]
        with db.engine.begin() as conn:
            
            result_tasks= conn.execute(text(query_tasks)).fetchall()

            
            
            
            for row in result_tasks:
                row_as_dict = row._mapping
                
                rows_tasks.append(dict(row_as_dict))
        
        
        return rows_tasks

    except Exception as e:
        print(e)
        return False
    
def getVisitTaskDetails(id_task):
    
    try:
        
        
        query_tasks="""SELECT pt._id as _id,visit_id as id_program,2 as id_moment_type,pt.date_end as end_date,pt.date_start as start_date,Null as moment_value, wetting,observations,objectives as id_objective,products as id_product,dosage,dosage_parts_per_unit
                
              
                from visit_tasks as pt 
                left join visit_task_objectives as tp on pt._id= tp.visit_task_id
                where pt._id = """+ str(id_task)+"""
                
             """
        
        
        
        rows_tasks=[]
        with db.engine.begin() as conn:
            
            result_tasks= conn.execute(text(query_tasks)).fetchall()

            
            
            
            for row in result_tasks:
                row_as_dict = row._mapping
                
                rows_tasks.append(dict(row_as_dict))
        
        
        return rows_tasks

    except Exception as e:
        print(e)
        return False
    
def getFieldMachineryDetails(id_field):
    
    print("-----enter")
    try:
        
        query_tasks="""SELECT _id,name,model,id_machinery_type,size
                FROM machinery
                
                where id_field = """+ str(id_field)+"""
                
                
             """
        rows_tasks=[]
        with db.engine.begin() as conn:
            
            result_tasks= conn.execute(text(query_tasks)).fetchall()

            
            for row in result_tasks:
                row_as_dict = row._mapping
                
                rows_tasks.append(dict(row_as_dict))
        print(rows_tasks)
        
        return rows_tasks

    except Exception as e:
        print(e)
        return False
    
def getFieldFieldTeamDetails(id_field):
    
    try:
        
        query_tasks="""SELECT _id,name,phone_number,id_worker_type
                FROM workers
                
                where id_field = """+ str(id_field)+"""
                and id_worker_type in (3)
                
             """
        rows_tasks=[]
        with db.engine.begin() as conn:
            
            result_tasks= conn.execute(text(query_tasks)).fetchall()

            
            for row in result_tasks:
                row_as_dict = row._mapping
                
                rows_tasks.append(dict(row_as_dict))
        print(rows_tasks)
        
        return rows_tasks

    except Exception as e:
        print(e)
        return False
def getFieldAdminTeamDetails(id_field):
    
    try:
        
        
        query_tasks="""SELECT _id,name,email,phone_number,id_worker_type
                FROM workers
                
                where id_field = """+ str(id_field)+"""
                and id_worker_type in (1,2)
                
             """
        rows_tasks=[]
        with db.engine.begin() as conn:
            
            result_tasks= conn.execute(text(query_tasks)).fetchall()

            
            for row in result_tasks:
                row_as_dict = row._mapping
                
                rows_tasks.append(dict(row_as_dict))
        print(rows_tasks)
        
        return rows_tasks

    except Exception as e:
        print(e)
        return False
    
def getFieldPlotsDetails(id_field):
    
    try:
        
        
        query_tasks="""SELECT _id,name,size,id_species,variety,id_program,id_phenological_stage
                FROM plots 
                
                where id_field = """+ str(id_field)+"""
                
             """
        rows_tasks=[]
        with db.engine.begin() as conn:
            
            result_tasks= conn.execute(text(query_tasks)).fetchall()

            
            for row in result_tasks:
                row_as_dict = row._mapping
                
                rows_tasks.append(dict(row_as_dict))
        print(rows_tasks)
        
        return rows_tasks

    except Exception as e:
        print(e)
        return False
    
def getFieldMarketFilter(programs):
    
    try:
        
        
        query_tasks="""SELECT distinct(fi._id),sag_code
                FROM field as fi
				left join plots as pl on pl.id_field= fi._id
                where pl.id_program in """+ str(programs)+"""
             """
        rows_tasks=[]
        with db.engine.begin() as conn:
            
            result_tasks= conn.execute(text(query_tasks)).fetchall()

            
            for row in result_tasks:
                row_as_dict = row._mapping
                
                rows_tasks.append(dict(row_as_dict))
        print(rows_tasks)
        
        return rows_tasks

    except Exception as e:
        print(e)
        return False
    

def calculate_date_difference(date_end, application_date):
    # Convert date strings to datetime objects
    
    print(type(application_date))
    # Calculate the difference in days
    difference = (application_date-date_end).days
    
    # If date_end is higher, return 0
    if difference < 0:
        return 0
    
    return difference

def getFieldBookData(fields):
    
    try:
        
        
        query_tasks="""SELECT pl_t.status_id as id_status,ta._id,ta.date_start,ta.date_end, com.company_name,field._id as f_id,field.sag_code,field.location as locat,plot.variety,t_o._id as to_id,t_o.id_product,t_o.dosage,t_o.dosage_parts_per_unit,o.objective_name, task_orders.wetting, task_orders.application_date
FROM plot_tasks as pl_t
left join tasks as ta on pl_t.task_id= ta._id
left join program_tasks as pt on pt._id=ta.id_moment
left join plots as plot on plot._id = pl_t.plot_id
left join field as field on field._id =plot.id_field
left join task_objectives as t_o on t_o.id_task = pt._id
left join objectives as o on o._id =t_o.id_objective
left join company as com on com._id = field.company_id
left join (WITH ranked_tasks AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY id_task ORDER BY _id DESC) AS rn
    FROM task_orders
) 
SELECT *
FROM ranked_tasks
WHERE rn = 1) as task_orders on task_orders.id_task =pl_t._id 

where field._id in """+ str(fields)+"""
             """
        rows_tasks=[]
        with db.engine.begin() as conn:
            
            result_tasks= conn.execute(text(query_tasks)).fetchall()

            
            for row in result_tasks:
                row_as_dict = row._mapping
                
                rows_tasks.append(dict(row_as_dict))
        print(rows_tasks)
        
        return rows_tasks

    except Exception as e:
        print(e)
        return False
    
def getFieldGeneralDetails(id_field):
    
    try:
        
        
        query_tasks="""SELECT field_name,location,latitude,longitude,sag_code
                FROM field 
                
                where _id = """+ str(id_field)+"""
                
             """
        
        
        
        rows_tasks=[]
        with db.engine.begin() as conn:
            
            result_tasks= conn.execute(text(query_tasks)).fetchall()

            
            
            
            for row in result_tasks:
                row_as_dict = row._mapping
                
                rows_tasks.append(dict(row_as_dict))
        print(rows_tasks)
        
        return rows_tasks

    except Exception as e:
        print(e)
        return False
    
def getFieldMachinery(id_field):
    
    try:
        
        
        query_tasks="""SELECT _id,name,model,id_machinery_type
                FROM machinery  
                where id_field = """+ str(id_field)+"""
                
             """
        
        
        rows_machinery=[]
        with db.engine.begin() as conn:
            
            result_tasks= conn.execute(text(query_tasks)).fetchall()
            
            
            for row in result_tasks:
                row_as_dict = row._mapping
                
                rows_machinery.append(dict(row_as_dict))
       
        
        return rows_machinery

    except Exception as e:
        print(e)
        return False
    

def getFieldWorkers(id_field):
    
    try:
        
        
        query_tasks="""SELECT _id,name
                FROM workers  
                where id_field = """+ str(id_field)+"""
                
             """
        
        
        rows_machinery=[]
        with db.engine.begin() as conn:
            
            result_tasks= conn.execute(text(query_tasks)).fetchall()
            
            
            for row in result_tasks:
                row_as_dict = row._mapping
                
                rows_machinery.append(dict(row_as_dict))
       
        
        return rows_machinery

    except Exception as e:
        print(e)
        return False
    
def getTask(id_task):
    
    try:

        task = PlotTasksClass.query.get(id_task)
        print('///////')
        print(task.from_program)
        
        
        query_tasks="""select pt._id as _id, t.date_start,t.date_end, t.id_task_type, p.name as time_indicator, pt.status_id as id_status, 
                        t.id_company as id_company,t.id_moment as id_moment, pt.from_program
                from plot_tasks as pt
                left join tasks as t on pt.task_id = t._id
                left join plots as p on pt.plot_id = p._id

                WHERE pt._id = """+ str(id_task)+"""
                and pt.from_program = True
                
             """
        
        query_tasks2="""select pt._id as _id, t.date_start,t.date_end, t.task_type_id as id_task_type, p.name as time_indicator, pt.status_id as id_status, 
                         t._id as id_moment, pt.from_program, t.visit_id as id_program
                from plot_tasks as pt
                left join visit_tasks as t on pt.task_id = t._id
                left join plots as p on pt.plot_id = p._id

                WHERE pt._id = """+ str(id_task)+"""
                and pt.from_program = False
                
             """
        
        if task.from_program==False:
            query_tasks=query_tasks2
        
        
        
        rows_tasks=[]
        with db.engine.begin() as conn:
            
            result_tasks= conn.execute(text(query_tasks)).fetchall()

            
            
            for row in result_tasks:
                row_as_dict = row._mapping
                
                rows_tasks.append(dict(row_as_dict))
        
        
        return rows_tasks

    except Exception as e:
        print(e)
        return False
    

    
def getUserPlots(user_id):
    try:


        companies=getUserCompanies(user_id)
        print(companies)
        if len(companies)==0:
            return False
        company=companies[0]['_id']

        query_tasks="""SELECT pt.*
                FROM plots as pt
                left join field as fi  on pt.id_field=fi._id
                
                where fi.company_id = """+ str(company)+"""
                
             """
        
        
        
        rows_plots=[]
        with db.engine.begin() as conn:
            
            result_tasks= conn.execute(text(query_tasks)).fetchall()
            
            
            for row in result_tasks:
                row_as_dict = row._mapping
                
                rows_plots.append(dict(row_as_dict))
        
        
        return rows_plots

    except Exception as e:
        print(e)
        return False
    

def getUserValidPlots(user_id):
    try:


        companies=getUserCompanies(user_id)
        print(companies)
        if len(companies)==0:
            return False
        company=companies[0]['_id']

        query_tasks="""SELECT pl.*,ts.id_moment as moment_id, pt.status_id
                FROM plots as pl
                left join field as fi  on pl.id_field=fi._id
				left join plot_tasks as pt on pl._id = pt.plot_id
				left join tasks  as ts on ts._id = pt.task_id
                
                where fi.company_id = """+ str(company)+"""
                and pt.from_program = True
                and pt.status_id IS NOT NULL
                and pt.status_id != 2
                
             """
        
        
        rows_plots=[]
        with db.engine.begin() as conn:
            
            result_tasks= conn.execute(text(query_tasks)).fetchall()
            
            
            for row in result_tasks:
                row_as_dict = row._mapping
                
                rows_plots.append(dict(row_as_dict))
        
        
        return rows_plots

    except Exception as e:
        print(e)
        return False    
def createProgram(program_name,id_user,species):
    
    try:

        
        companies=getUserCompanies(id_user)
        print(companies)
        if len(companies)==0:
            return False
        company=companies[0]['_id']
        
        program = ProgramClass( program_name=program_name, id_user = id_user,id_species = species,published=False)
       
        
        db.session.add(program)
        db.session.commit()

        program_company=ProgramCompaniesClass(id_program=program._id, id_company=company)
        db.session.add(program_company)
        db.session.commit()
        return program._id
    

    except Exception as e:
        print(e)
        return False
    
def getTaskOrders(id_task):
    try:
        plot_task=PlotTasksClass.query.get(id_task)
        
        query="""
                    SELECT _id,file_name,plots
                    FROM task_orders
                    WHERE task_orders.id_task in (
                        SELECT _id 
                        FROM plot_tasks 
                        WHERE task_id = (
                            SELECT task_id 
                            FROM plot_tasks 
                            WHERE _id = """+ str(id_task)+"""
                    ))
                    order by order_number desc
                
             """
        
        
        rows=[]
        with db.engine.begin() as conn:
            result = conn.execute(text(query)).fetchall()
            for row in result:
                row_as_dict = dict(row._mapping)
                
                
                print(row_as_dict)
                if row_as_dict['plots'] != None and (plot_task.plot_id in ast.literal_eval(row_as_dict['plots'])):
                    del(row_as_dict["plots"])
                    rows.append(row_as_dict)
            return rows,plot_task.plot_id
        

    except Exception as e:
        print(e)
        return False
    
def getTaskOrdersNewFormat(id_task):
    try:
        plot_task=PlotTasksClass.query.get(id_task)
        
        query="""
                    SELECT _id,file_name,plots,time_start ,time_end ,alias
                    FROM task_orders
                    WHERE task_orders.id_task in (
                        SELECT _id 
                        FROM plot_tasks 
                        WHERE task_id = (
                            SELECT task_id 
                            FROM plot_tasks 
                            WHERE _id = """+ str(id_task)+"""
                    ))
                    order by order_number desc
                
             """
        
        
        rows=[]
        with db.engine.begin() as conn:
            result = conn.execute(text(query)).fetchall()
            for row in result:
                row_as_dict = dict(row._mapping)
                
                
                print(row_as_dict)
                if row_as_dict['plots'] != None and (plot_task.plot_id in ast.literal_eval(row_as_dict['plots'])):
                    del(row_as_dict["plots"])
                    rows.append(row_as_dict)
            return rows,plot_task.plot_id
        

    except Exception as e:
        print(e)
        return False
    
def getTaskOrdersFull(id_task):
    try:
        plot_task=PlotTasksClass.query.get(id_task)
        
        query="""
                    SELECT _id,file_name,plots
                    FROM task_orders
                    WHERE task_orders.id_task in (
                        SELECT _id 
                        FROM plot_tasks 
                        WHERE task_id = (
                            SELECT task_id 
                            FROM plot_tasks 
                            WHERE _id = """+ str(id_task)+"""
                    ))
                    order by order_number desc
                
             """
        
        
        rows=[]
        with db.engine.begin() as conn:
            result = conn.execute(text(query)).fetchall()
            for row in result:
                row_as_dict = dict(row._mapping)
                
                
                
                if row_as_dict['plots'] != None and (plot_task.plot_id in ast.literal_eval(row_as_dict['plots'])):
                    
                    rows.append(row_as_dict)
            return rows
        

    except Exception as e:
        print(e)
        return False


def getAdjacentPlotTasks(id_task,plots):
    try:
        plot_task=PlotTasksClass.query.get(id_task)
        
        query="""
                    
                    
                        SELECT *
                        FROM plot_tasks 
                        WHERE task_id = (
                            SELECT task_id 
                            FROM plot_tasks 
                            WHERE _id = """+ str(id_task)+""")
                        and plot_id in """+ str(plots)+"""
                   
                    
                
             """
        
        
        rows=[]
        with db.engine.begin() as conn:
            result = conn.execute(text(query)).fetchall()
            for row in result:
                row_as_dict = dict(row._mapping)
                
                
                print(row_as_dict)
                
                rows.append(row_as_dict)
            return rows
        

    except Exception as e:
        print(e)
        return False
    
def mailExists(email):
    try:

        
        
        query="""SELECT _id,email
                    FROM users
                    WHERE email = '"""+ str(email)+"""'
                    
                
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
def process_nested_list(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.append(process_nested_list(item))
        elif isinstance(item, str):
            # Replace "," with "." and convert to float
            result.append(float(item.replace(',', '.')))
        else:
            result.append(item)
    return result

def process_dictionary(d):
    result = {}
    for key, value in d.items():
        if isinstance(value, list):
            result[key] = [process_nested_list(value[0])]
        else:
            result[key] = value
    return result
  
def createTask(body):
    
    try:
        
        if 'end_date' not in body :
            body['end_date']=body.get('start_date')
        print("hola")

        task = ProgramTaskClass( id_program=body.get('id_program'), id_moment_type=body.get('id_moment_type'),start_date=body.get('start_date'),moment_value=body.get('moment_value'),wetting=body.get('wetting'),observations=body.get('observations'),end_date=body.get('end_date'))
        db.session.add(task)
        print(task._id)
        
       

        db.session.commit()
        print(task._id)
        for idx, objective in enumerate(body.get('objectives')):
         
          
          taskObjective=   TaskObjectivesClass(id_task=task._id, id_objective=objective,id_product=str(body.get('products')[idx]),dosage=str(process_nested_list(body.get('dosage')[idx])),dosage_parts_per_unit=str(body.get('dosage_parts_per_unit')[idx]))
          db.session.add(taskObjective)
        db.session.commit()
        return task._id
    except Exception as e:
        print(e)
        return False
    
def createField(body):
    
    try:
        
       

        field = FieldClass( company_id=body.get('id_company'), field_name=body.get('field_name'))
        db.session.add(field)
        print(field._id)
        


        db.session.commit()
        weather_locaction_assign=FieldWeatherLocationsAssignClass(field_id=field._id,weather_locations_id=1)
        db.session.add(weather_locaction_assign)
        db.session.commit()
       
        return field._id
    except Exception as e:
        print(e)
        return False
    
def updateMoment(task_id,body):
    
    try:
    
        task = ProgramTaskClass.query.get(task_id)

        if task is None:
            return False
        
        TaskObjectivesClass.query.filter_by(id_task=task._id).delete()
        

        
        task.id_program=body.get('id_program')
        task.id_moment_type=body.get('id_moment_type')
        task.start_date=body.get('start_date')
        task.moment_value=body.get('moment_value')
        task.wetting=body.get('wetting')
        task.observations=body.get('observations')
        task.end_date=body.get('end_date')


    
        for idx, objective in enumerate(body.get('objectives')):
          
          taskObjective =  TaskObjectivesClass(id_task=task._id, id_objective=objective,id_product=str(body.get('products')[idx]),dosage=str(body.get('dosage')[idx]),dosage_parts_per_unit=str(body.get('dosage_parts_per_unit')[idx]))
          db.session.add(taskObjective)
        db.session.add(task)
        db.session.commit()
        return task._id
    except Exception as e:
        print(e)
        return False
    

def updateMomentTasks(moment_id,body):
    
    try:
    
        print('Holas')

        
        
        tasks=TaskClass.query.filter_by(id_moment=moment_id)
        if tasks is None:
            return False
        
        for task in tasks:
        
            
            task.id_task_type=1
            task.date_start=body.get('start_date')
            task.date_end=body.get('end_date')

            db.session.add(task)
        db.session.commit()
        return moment_id
    except Exception as e:
        print(e)
        return False
    

    
def createTasks(program_id, body):
    try:
        program_details = body.get('program_details')

        if program_details is None:
            return False
        assigned_companies = body.get('assigned_companies')
        print("assigned companies")
        print(assigned_companies)
        query="""SELECT m._id as _id, m.id_program, m.start_date, m.end_date, t._id as id_task,t.id_company
                    FROM program_tasks as m
                    left join tasks  as t on m._id = t.id_moment
                    
                    WHERE m.id_program = """+ str(program_id)+"""
                    
                    """
        rows=[]
        with db.engine.begin() as conn:
                result = conn.execute(text(query)).fetchall()
                
                for row in result:
                    row_as_dict = row._mapping
                    
                    rows.append(dict(row_as_dict))
        print(rows)

        tasks={}
        for el in rows:   
            tasks[el['_id']]  =el
        print(tasks)    
        

        for company_id in assigned_companies:
            created = [dicc for dicc in rows if dicc['id_company'] ==company_id]
            created_tasks={}
            for el in created:
                created_tasks[el['_id']]  =el
  
 
            for moment_id,task in tasks.items():
                if 'end_date' not in task:
                    task['end_date']=task['start_date']

                if moment_id not in created_tasks:
                    task_instance = TaskClass(id_moment =moment_id,id_task_type =1,date_start=task['start_date'],date_end=task['end_date'],time_indicator='AM' ,id_status=1,id_company=company_id)
                    db.session.add(task_instance)
                    db.session.commit()
                    print('creando_task')
                    print(task_instance._id)
                    program_plots=PlotClass.query.filter_by(id_program=program_id)
                    for plot in program_plots:
                        plot_task=PlotTasksClass( plot_id=plot._id,task_id=task_instance._id,status_id=1)
                        db.session.add(plot_task)
                    db.session.commit()
                    
        db.session.commit()                       

        return True

    except Exception as e:
        print(e)
        return False
    
def updateTaskIns(task_id, body):
    try:
        

        task = PlotTasksClass.query.get(task_id)

        if task is None:
            return False
        
        batch_update=False
        if "batch_update" in body:
            batch_update=body["batch_update"]

        task_orders=getTaskOrdersFull(task_id)
        task_order=0
        print(task_orders)
        if len(task_orders)>0:
            task_order=task_orders[0]

        print("hola")
        for key,value in body.items():
            if key=="status":
              
                if batch_update and len(task_orders)>0 and task_order['plots']!=None :
                    plots=task_order['plots'].replace('[','(').replace(']',')')
                   
                    adjacent_plot_tasks=getAdjacentPlotTasks(task_id,plots)
                    print(adjacent_plot_tasks)
                    for apt in adjacent_plot_tasks:

                       
                        task = PlotTasksClass.query.get(apt['_id'])
                        task.status_id = value
                        db.session.add(task)

                else:
                    print("cambio de status")
                    task.status_id = value
                    db.session.add(task)
            #if key=="time_indicator":
            #       print("cambio de tiempo")
            #  task.time_indicator = value
            #status = body.get('status')
            #time_indicator = body.get('time_indicator')
                
        #task.status = status
        #task.time_indicator = time_indicator
        


        
        db.session.commit()

        return task._id
    

    except Exception as e:
        print(e)
        return False
    

def updateTaskOrder(to_id, body):
    try:
        

        task = TaskOrderClass.query.get(to_id)

        if task is None:
            return False
        
       
        for key,value in body.items():
            if key=="time_start":
              
                task.time_start = value
                

            if key=="time_end":
                task.time_end = value
                
            #if key=="time_indicator":
            #       print("cambio de tiempo")
            #  task.time_indicator = value
            #status = body.get('status')
            #time_indicator = body.get('time_indicator')
                
        #task.status = status
        #task.time_indicator = time_indicator
        


        db.session.add(task)
        db.session.commit()

        return task._id
    

    except Exception as e:
        print(e)
        return False
    

def updateQuotes( body):
    try:
        

        for quote in body['quotes']:
        
            updated_quote = QuoteClass.query.get(quote['quote_id'])
            updated_quote.provider_name = quote['provider_name']
            db.session.add(updated_quote)
            for row in quote['rows']:
                updated_row = QuoteRowClass.query.get(row['_id'])
                updated_row.container_size = row['container_size']
                updated_row.container_price_clp = row['container_price_clp']
                updated_row.container_unit_id = row['container_unit_id']
                updated_row.checked = row['checked']
                db.session.add(updated_row)
            
        db.session.commit()
        return True
        # Update the row fields with the new data
        for key, value in data.items():
            setattr(row, key, value)

        # Commit the changes to the database
        db.session.commit()


        task = TaskClass.query.get(task_id)

        if task is None:
            return False

        for key,value in body.items():
            if key=="status":
                print("cambio de status")
                task.id_status = value
            if key=="time_indicator":
                print("cambio de tiempo")
                task.time_indicator = value
            #status = body.get('status')
            #time_indicator = body.get('time_indicator')
                
        #task.status = status
        #task.time_indicator = time_indicator
        


        db.session.add(task)
        db.session.commit()

        return task._id
    

    except Exception as e:
        print(e)
        return False


def updateProgram(program_id, body):
    try:
        program_details = body.get('program_details')

        if program_details is None:
            return False

        program = ProgramClass.query.get(program_id)

        if program is None:
            return False

        
        MarketProgramClass.query.filter_by(program_id=program._id).delete()
        ProgramCompaniesClass.query.filter_by(id_program=program._id).delete()
 
        program.id_user = program_details.get('id_user')
        program.program_name = program_details.get('program_name')
        program.published = program_details.get('published')
        program.id_species = program_details.get('id_species')


        markets = program_details.get('markets')
        for market_id in markets:
            new_market_program = MarketProgramClass(market_id=market_id, program_id=program._id)
            db.session.add(new_market_program)

        
        assigned_companies = body.get('assigned_companies')
        for id in assigned_companies:
            program_field = ProgramCompaniesClass(id_program=program._id, id_company=id)
            db.session.add(program_field)

        db.session.add(program)
        db.session.commit()

        return program._id

    except Exception as e:
        print(e)
        return False
    

def publishProgram(id_program):
    
    try:
    
        program = ProgramClass.query.get(id_program)

        if program is None:
            return False
        
        
       
        program.published = True

        
        
    
        
        db.session.add(program)
        db.session.commit()
        return program._id
    
    except Exception as e:
        print(e)
        return False

def deleteProgram(id_program,id_user):
    
    try:
        print(id_program)
        print(id_user)
        
        program = ProgramClass.query.filter_by(_id=id_program, id_user=id_user).first()
        if program:
            db.session.delete(program)
            db.session.commit()
            return True
        
        return False

    

    except Exception as e:
        print(e)
        return False
    
def deleteTask(id_moment):
    
    try:
        


        query="""DELETE FROM tasks
                    
                    
                    WHERE id_moment = """+ str(id_moment)+"""
                    
                    """
        rows=[]
        with db.engine.begin() as conn:
                result = conn.execute(text(query))
        db.session.commit()

        task = ProgramTaskClass.query.filter_by(_id=id_moment).first()
        if task:
            for product in task.objectives:
                db.session.delete(product)
            db.session.delete(task)
            db.session.commit()
            return True
        print('hola')
        return False

    

    except Exception as e:
        print(e)
        return False
    
def create_logic():
     try:
        db.create_all()
        db.session.commit()
     except Exception as e:
        print(e)
        return False

def delete_program_tasks_plot(plot_id):
    PlotTasksClass.query.filter_by(plot_id=plot_id).delete()
    db.session.commit()


def add_program_tasks_plot(program_id,plot_id,user_id):
    
    companies=getUserCompanies(user_id)
    user_company_id=companies[0]['_id']

    
    
    query="""SELECT t.*
                from tasks as t
                left join program_tasks as pt on pt._id=id_moment
                left join programs as p on p._id=pt.id_program
                where t.id_company = """+ str(user_company_id)+"""
                and p._id="""+ str(program_id)+"""

                """
        
    rows=[]
    with db.engine.begin() as conn:
            result = conn.execute(text(query)).fetchall()
            
            for row in result:
                row_as_dict = row._mapping
               
                rows.append(dict(row_as_dict))
    
    
    for task in rows:
        plot_task=PlotTasksClass( plot_id=plot_id,task_id=task["_id"],status_id=1)
        db.session.add(plot_task)
        print(plot_task)
    db.session.commit()


def createQuoter(body,user_id):
    
    try:
        
        
        quoter=QuoterClass(id_user=user_id,id_programs=str(body.get('programs_id')), start_date=body.get('start_date'), end_date=body.get('end_date'),total_hectares=body.get('total_hectares'))
        db.session.add(quoter)
        
        
        
        db.session.commit()
        print(quoter._id)
        print("hola")

        quote = QuoteClass( id_quoter=quoter._id,provider_name='Nombre Proveedor 1')
        db.session.add(quote)
        quote2 = QuoteClass( id_quoter=quoter._id,provider_name='Nombre Proveedor 2')
        db.session.add(quote2)
        quote3 = QuoteClass( id_quoter=quoter._id,provider_name='Nombre Proveedor 3')
        db.session.add(quote3)
        quote4 = QuoteClass( id_quoter=quoter._id,provider_name='Nombre Proveedor 4')
        db.session.add(quote4)
        db.session.commit()
        row_id=0
        clusters={}
        cluster_masters={}
        
        for product in body["products"]:
            if len(product)==0:
                    continue
            if product["cluster_id"] not in cluster_masters:
                cluster_masters[product["cluster_id"]]=False
            if product["cluster_master"]==True:
                cluster_masters[product["cluster_id"]]=True
           

        n_cluster_master={}
        for product in body["products"]:
                print("producto:")
                if len(product)==0:
                    continue
                if product['cluster_id'] not in clusters:
                    cluster=uuid.uuid4()
                    clusters[product['cluster_id'] ]= cluster
                    n_cluster_master[product['cluster_id']]=0
                if cluster_masters[product['cluster_id'] ]==False:
                    product["cluster_master"]=True
                    cluster_masters[product['cluster_id'] ]=True
                if product["cluster_master"]==True:
                    
                    n_cluster_master[product['cluster_id'] ]=n_cluster_master[product['cluster_id'] ]+1
                    if  n_cluster_master[product['cluster_id'] ]>1:
                        product["cluster_master"]=False
                
                container_unit=3
                if product['product_needed_unit_id']>4:
                    container_unit=1
                
                
                print(product['product_id'])
                print(product['cluster_master'])
                print(n_cluster_master[product['cluster_id'] ])
                print(n_cluster_master)
                row_id=row_id+1
                quoter_product=QuoterProductClass(id_quoter=quoter._id,cluster_id=clusters[product['cluster_id'] ],cluster_master=product['cluster_master'],product_row_id=row_id,product_id=product['product_id'],
                                          product_needed=product['product_needed'],product_stored=product['product_stored'],product_needed_unit_id=product['product_needed_unit_id'],
                                          valid_hectares=product['valid_hectares'])
                db.session.add(quoter_product)

                quote_row=QuoteRowClass(quote_id=quote._id,product_row_id=row_id,container_size=0,container_unit_id=container_unit,container_price_clp=0,checked=False)
                db.session.add(quote_row)
                quote_row=QuoteRowClass(quote_id=quote2._id,product_row_id=row_id,container_size=0,container_unit_id=container_unit,container_price_clp=0,checked=False)
                db.session.add(quote_row)
                quote_row=QuoteRowClass(quote_id=quote3._id,product_row_id=row_id,container_size=0,container_unit_id=container_unit,container_price_clp=0,checked=False)
                db.session.add(quote_row)
                quote_row=QuoteRowClass(quote_id=quote4._id,product_row_id=row_id,container_size=0,container_unit_id=container_unit,container_price_clp=0,checked=False)
                db.session.add(quote_row)
                
                
                
        
        
        
        
        
        db.session.commit()

                    
       

        
        
        return quoter._id
    
    except Exception as e:
        print(e)
        return False
    


def getQuoterProducts(quoter_id):
    
    try:
        
 
        

        query="""SELECT *
                from quoter_products
                where id_quoter = """+ str(quoter_id)+"""
                """
        
       
        
        rows=[]
        with db.engine.begin() as conn:
            result = conn.execute(text(query)).fetchall()
            
            for row in result:
                row_as_dict = row._mapping
               
                rows.append(dict(row_as_dict))
                
            return rows

    except Exception as e:
        print(e)
        return False


def getQuoter(id_usuario,quoter_id):
    
    try:
        
 
        

        query="""SELECT q.id_programs,qs._id as quote_id,q.start_date,q.end_date,q.total_hectares, qs.provider_name,qp.product_row_id
                    ,qp.container_size,qp.container_unit_id,qp.container_price_clp,qp.checked,qp._id as row_id
                FROM quoter as q
                left join quote as qs on q._id = qs.id_quoter
                left join quote_rows as qp on qp.quote_id=qs._id
                WHERE q.id_user = """+ str(id_usuario)+"""
                AND q._id = """+ str(quoter_id)+"""
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
    

def getProviderPurchaseOrders(quote_id):
    
    try:
        
 
        

        query="""SELECT file_name,order_number,alias
        from purchase_orders
                WHERE id_quote = """+ str(quote_id)+"""
                order by order_number
                
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







def getQuoters(id_usuario):
    
    try:
        
        query="""SELECT *
                from quoter
                WHERE id_user = """+ str(id_usuario)+"""
                ORDER BY _id DESC
                
             """
        
        
        rows=[]
        with db.engine.begin() as conn:
            result = conn.execute(text(query)).fetchall()
            
            for row in result:
                row_as_dict = row._mapping
                
                rows.append(dict(row_as_dict))
            return rows

    except Exception as e:
        print(e)
        return False
    
def getFieldForecast(field):

    query="""SELECT wd.*
                from field
                left join field_weather_location_assign as fw on fw.field_id=field._id
                left join weather_day as wd on fw.weather_locations_id = wd.weather_locations_id
                WHERE field._id = """+ str(field)+"""
                and TO_DATE(date, 'YYYY-MM-DD')>=CURRENT_DATE
                order by date asc
             """
        
        
    rows=[]
    with db.engine.begin() as conn:
        result = conn.execute(text(query)).fetchall()
        print(result)
        for row in result:
            row_as_dict = row._mapping
            rows.append(dict(row_as_dict))
        return rows

    
def getCompanyFromField(id_field):

    try:
        
        query="""SELECT *
                from field
                WHERE _id = """+ str(id_field)+"""
                
             """
        
        
        rows=[]
        with db.engine.begin() as conn:
            result = conn.execute(text(query)).fetchall()
            print(result)
            for row in result:
                row_as_dict = row._mapping
                print(row_as_dict)
                rows.append(dict(row_as_dict))
            return rows

    except Exception as e:
        print(e)
        return False
    
def getTasks(id_company):
    
    try:
        
        query="""SELECT *
                from tasks
                WHERE id_company = """+ str(id_company)+"""
                
             """
        
        
        rows=[]
        with db.engine.begin() as conn:
            result = conn.execute(text(query)).fetchall()
            print(result)
            for row in result:
                row_as_dict = row._mapping
                print(row_as_dict)
                rows.append(dict(row_as_dict))
            return rows

    except Exception as e:
        print(e)
        return False
    
def getTasks2(company_id,field_id):
    
    try:

       
        
        query="""SELECT pt._id as _id, t.date_start,t.date_end, t.id_task_type, p.name as time_indicator, pt.status_id as id_status,
         t.id_company as id_company,t.id_moment as id_moment,pt.from_program
                from plot_tasks as pt
                left join tasks as t on pt.task_id = t._id
                left join plots as p on pt.plot_id = p._id

                WHERE t.id_company = """+ str(company_id)+"""
                and p.id_field = """+ str(field_id)+"""
                and pt.from_program = True
                
             """
        
        
        rows=[]
        with db.engine.begin() as conn:
            result = conn.execute(text(query)).fetchall()
           
            for row in result:
                row_as_dict = row._mapping
                
                rows.append(dict(row_as_dict))
            return rows

    except Exception as e:
        print(e)
        return False
    

def getVisitTasks(company_id,field_id):
    
    try:

       
        
        query="""SELECT pt._id as _id, t.date_start,t.date_end, t.task_type_id as id_task_type, p.name as time_indicator, pt.status_id as id_status,
        pt.from_program
                from plot_tasks as pt
                left join visit_tasks as t on pt.task_id = t._id
                left join plots as p on pt.plot_id = p._id
                left join visits as v on v._id=t.visit_id

                where p.id_field = """+ str(field_id)+"""
                and pt.from_program = False
                and v.published = True
                
                
             """
        
        
        rows=[]
        with db.engine.begin() as conn:
            result = conn.execute(text(query)).fetchall()
            print(result)
            for row in result:
                row_as_dict = row._mapping
                print(row_as_dict)
                rows.append(dict(row_as_dict))
            return rows

    except Exception as e:
        print(e)
        return False
    

def getTaskPlots(id_task):
        

    try:
        
        query="""SELECT plots._id , programs._id as id_program, programs.id_species
                    FROM programs
                    JOIN program_tasks ON programs._id = program_tasks.id_program
                    JOIN tasks ON program_tasks._id = tasks.id_moment
                    join plots on plots.id_program =programs._id
                    WHERE tasks._id = """+ str(id_task)+"""
                
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


def getTaskPlots2(id_task,from_program):
        

    try:
        
        query="""SELECT  pt.plot_id as _id, pt.task_id, p.id_program as id_program,p.id_species as id_species, p.id_field
                    FROM plot_tasks as pt
                    left join plots as p on p._id =pt.plot_id
                    WHERE task_id = (SELECT task_id FROM plot_tasks WHERE _id = """+ str(id_task)+""")
                    and pt.from_program = """+ str(from_program)+"""
                
             """
        
        
        rows=[]
        with db.engine.begin() as conn:
            result = conn.execute(text(query)).fetchall()
            for row in result:
                row_as_dict = row._mapping
                
                rows.append(dict(row_as_dict))
            return rows

    except Exception as e:
        print(e)
        return False
