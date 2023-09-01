import json
from database.models.Program import PlotClass,TaskClass,QuoterClass,QuoteClass,QuoteProductClass,ProgramCompaniesClass,MarketProgramClass,ProgramClass,userClass,SpeciesClass,FieldClass,ProgramTaskClass,TaskObjectivesClass, db,auth
from sqlalchemy import  text,select
from flask import g
import jwt
import time
from sqlalchemy.orm import class_mapper
import ast
import uuid


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
    
def getMoments(id_program,start,end):
   
    
    try:
        
        query="""SELECT wetting,id_product,dosage,id_objective
                FROM program_tasks  pt
                left join task_objectives  ta
                    on pt._id=ta.id_task
                WHERE id_program = """+ str(id_program)+"""
                AND start_date >= DATE('"""+ start+"""')
                AND start_date < DATE('"""+ end+"""')
                
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
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


def getPrograms(id_usuario):
    
    try:
        
        query="""SELECT p._id as _id,id_user,program_name,species_name,market_name,published,updated_at FROM programs as p
                left join species as s on p.id_species= s._id
                left join market_program as mp on p._id=mp.program_id
                left join market as m on m._id=mp.market_id
                WHERE p.id_user = """+ str(id_usuario)+"""
                
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
                if not key.startswith('_'):
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
        
        query="""SELECT p._id as _id,id_species,id_user,program_name,species_name,market_id,published,updated_at FROM programs as p
                left join species as s on p.id_species= s._id
                left join market_program as mp on p._id=mp.program_id
                left join market as m on m._id=mp.market_id
                WHERE p.id_user = """+ str(id_usuario)+"""
                AND p._id = """+ str(id_programa)+"""
                
             """
        query_tasks="""SELECT pt._id as _id
                FROM programs as p
                left join program_tasks as pt on p._id=pt.id_program
                WHERE p.id_user = """+ str(id_usuario)+"""
                AND p._id = """+ str(id_programa)+"""
             """
        
        query_companies="""SELECT pf.id_company as _id
                FROM programs as p
                left join program_companies as pf on p._id=pf.id_program
                
                WHERE p.id_user = """+ str(id_usuario)+"""
                AND p._id = """+ str(id_programa)+"""
                
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
        
        
        query_tasks="""SELECT pt._id as _id,id_program,id_moment_type,start_date,moment_value,wetting,observations,id_objective,id_product,dosage,dosage_parts_per_unit
                FROM program_tasks as pt 
                left join task_objectives as tp on pt._id=tp.id_task
                where pt._id = """+ str(id_moment)+"""
                
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
    
def getTask(id_task):
    
    try:
        
        
        query_tasks="""SELECT t._id as _id,t.id_moment,t.id_task_type as id_task_type,t.date_start, t.date_end,t.time_indicator as time_indicator,t.status as status, id_moment_type,moment_value,wetting,observations,id_objective,id_product,dosage,dosage_parts_per_unit
                FROM program_tasks as pt 
                left join task_objectives as tp on pt._id=tp.id_task
                left join tasks t on pt._id= t.id_moment
                where t._id = """+ str(id_task)+"""
                
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
    
def createProgram(program_name,id_user,species):
    
    try:
        
        program = ProgramClass( program_name=program_name, id_user = id_user,id_species = species,published=False)
        db.session.add(program)
        db.session.commit()
        return program._id
    

    except Exception as e:
        print(e)
        return False
    
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
         
          
          taskObjective=   TaskObjectivesClass(id_task=task._id, id_objective=objective,id_product=str(body.get('products')[idx]),dosage=str(body.get('dosage')[idx]),dosage_parts_per_unit=str(body.get('dosage_parts_per_unit')[idx]))
          db.session.add(taskObjective)
        db.session.commit()
        return task._id
    except Exception as e:
        print(e)
        return False
    
def updateTask(task_id,body):
    
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


    
        for idx, objective in enumerate(body.get('objectives')):
          
          taskObjective =  TaskObjectivesClass(id_task=task._id, id_objective=objective,id_product=str(body.get('products')[idx]),dosage=str(body.get('dosage')[idx]),dosage_parts_per_unit=str(body.get('dosage_parts_per_unit')[idx]))
          db.session.add(taskObjective)
        db.session.add(task)
        db.session.commit()
        return task._id
    except Exception as e:
        print(e)
        return False
    

    
def createTasks(program_id, body):
    try:
        program_details = body.get('program_details')

        if program_details is None:
            return False
        assigned_companies = body.get('assigned_companies')
        
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
                    task_instance = TaskClass(id_moment =moment_id,id_task_type =1,date_start=task['start_date'],date_end=task['end_date'],time_indicator='08:00:00' ,id_status=1,id_company=company_id)
                    db.session.add(task_instance)

          
        db.session.commit()
                    


            

        return True

    except Exception as e:
        print(e)
        return False
    
def updateTaskIns(task_id, body):
    try:
        status = body.get('status')
        time_indicator = body.get('time_indicator')

        

        task = TaskClass.query.get(task_id)

        if task is None:
            return False

        
 
        task.status = status
        task.time_indicator = time_indicator
        


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

def createQuoter(body,user_id):
    
    try:
    
        
        quoter=QuoterClass(id_user=user_id,id_programs=str(body.get('programs_id')), start_date=body.get('start_date'), end_date=body.get('end_date'),total_hectares=body.get('total_hectares'))
        db.session.add(quoter)
        
        print(quoter._id)
        db.session.commit()
        
        
        
        
        
        for provider_quote in body.get('quotes'):
        
            quote = QuoteClass( id_quoter=quoter._id,provider_name=provider_quote['provider_name'])
            db.session.add(quote)
            db.session.commit()
            

            for product in provider_quote["products"]:
                cluster_id=uuid.uuid4()
                quote_product=QuoteProductClass(id_quote=quote._id,cluster_id=cluster_id,cluster_master=True,product_id=product['product_id'],
                                          product_needed=product['product_needed'],product_needed_unit=product['product_needed_unit'],
                                          valid_hectares=product['valid_hectares'],container_size=product['container_size'],container_cost_clp=product['container_cost_clp'],container_unit=product['container_unit'], checked=product['checked'])
                db.session.add(quote_product)
                
                
                for alternative in product['alternatives']:
                    quote_alternative=QuoteProductClass(id_quote=quote._id,cluster_id=cluster_id,cluster_master=False,product_id=alternative['product_id'],
                                          product_needed=alternative['product_needed'],product_needed_unit=product['product_needed_unit'],
                                          valid_hectares=alternative['valid_hectares'],container_size=alternative['container_size'],container_cost_clp=alternative['container_cost_clp'],container_unit=alternative['container_unit'], checked=alternative['checked'])
                    db.session.add(quote_alternative)
                    
        db.session.commit()

        
        
        return quoter._id
    
    except Exception as e:
        print(e)
        return False


def getQuoter(id_usuario,quoter_id):
    
    try:
        
 
        

        query="""SELECT q.id_programs,q.start_date,q.end_date,q.total_hectares, qs.provider_name,qp.id_quote as quote_id,qp._id as id_quote_product,qp.cluster_id,qp.cluster_master,qp.product_id,qp.product_needed,qp.product_needed_unit,qp.valid_hectares
                    ,qp.container_size,qp.container_cost_clp,qp.container_unit,qp.checked
                FROM quoter as q
                left join quote as qs on q._id = qs.id_quoter
                left join quote_product as qp on qp.id_quote=qs._id
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
                print(rows)
            return rows

    except Exception as e:
        print(e)
        return False







def getQuoters(id_usuario):
    
    try:
        
        query="""SELECT *
                from quoter
                WHERE id_user = """+ str(id_usuario)+"""
                
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
    

def getTaskPlots(id_task):
        

    try:
        
        query="""SELECT plots._id
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


    