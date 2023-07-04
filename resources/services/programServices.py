import json
from database.models.Program import ProgramCompaniesClass,MarketProgramClass,ProgramClass,userClass,SpeciesClass,FieldClass,ProgramTaskClass,TaskObjectivesClass, db,auth
from sqlalchemy import  text,select
from flask import g
import jwt
import time
from sqlalchemy.orm import class_mapper
import ast


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
        
        
        query_tasks="""SELECT pt._id as _id,id_program,id_moment_type,start_date,moment_value,wetting,observations,id_objective,id_product,dosage,max_applications
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
    
        task = ProgramTaskClass( id_program=body.get('id_program'), id_moment_type=body.get('id_moment_type'),start_date=body.get('start_date'),moment_value=body.get('moment_value'),wetting=body.get('wetting'),observations=body.get('observations'))
        db.session.add(task)
        print(task._id)
        
       

        db.session.commit()
        print(task._id)
        for idx, objective in enumerate(body.get('objectives')):
         
          
          taskObjective=   TaskObjectivesClass(id_task=task._id, id_objective=objective,id_product=str(body.get('products')[idx]),dosage=str(body.get('dosage')[idx]),max_applications=str(body.get('max_applications')[idx]))
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
          
          taskObjective =  TaskObjectivesClass(id_task=task._id, id_objective=objective,id_product=str(body.get('products')[idx]),dosage=str(body.get('dosage')[idx]),max_applications=str(body.get('max_applications')[idx]))
          db.session.add(taskObjective)
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
