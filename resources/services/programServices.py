import json
from database.models.Program import ProgramClass,userClass, db,auth
from sqlalchemy import  text,select
from flask import g
import jwt
import time



def getTable(table):
   
    
    try:
        
        query="""SELECT *
                FROM """+table+"""
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
        
        query="""SELECT p._id as _id,id_user,program_name,species_name,market_name,published FROM programs as p
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
    

def getProgramDetails(id_usuario,id_programa):
    
    try:
        
        query="""SELECT p._id as _id,id_user,program_name,species_name,market_name,published FROM programs as p
                left join species as s on p.id_species= s._id
                left join market_program as mp on p._id=mp.program_id
                left join market as m on m._id=mp.market_id
                WHERE p.id_user = """+ str(id_usuario)+"""
                AND p._id = """+ str(id_programa)+"""
                
             """
        query_tasks="""SELECT pt._id as _id,id_type,fecha_inicio,id_phenological_stage,validity_period,dosage,dosage_unit,objective,wetting,id_product
                FROM programs as p
                left join program_tasks as pt on p._id=pt.id_program
                left join task_product as tp on pt._id=tp.id_task
                WHERE p.id_user = """+ str(id_usuario)+"""
                AND p._id = """+ str(id_programa)+"""
                
             """
        
        
        rows=[]
        rows_tasks=[]
        with db.engine.begin() as conn:
            result = conn.execute(text(query)).fetchall()
            result_tasks= conn.execute(text(query_tasks)).fetchall()
            
            for row in result:
                row_as_dict = row._mapping
                
                rows.append(dict(row_as_dict))
            for row in result_tasks:
                row_as_dict = row._mapping
                
                rows_tasks.append(dict(row_as_dict))
        
        
        return rows,rows_tasks

    except Exception as e:
        print(e)
        return False
    
def createProgram(program_name,id_user):
    
    try:
    
        program = ProgramClass( program_name=program_name, id_user = id_user,published=False)
        db.session.add(program)
        db.session.commit()
        return True
    

    except Exception as e:
        print(e)
        return False
def deleteProgram(id_program,id_user):
    
    try:
        
        program = ProgramClass.query.filter_by(_id=id_program,id_user=id_user).first()

        db.session.delete(program)
        db.session.commit()
        return True
    

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
