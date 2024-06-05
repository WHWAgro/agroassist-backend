import json
from database.models.Program import VisitClass,db,auth,CompanyClass,FieldClass,userClass,VisitTaskClass,VisitTaskObjectivesClass,PlotTasksClass
from sqlalchemy import  text,select
from flask import g
import jwt
import time
from sqlalchemy.orm import class_mapper
import ast
import uuid
import datetime



def createVisit(user_id,body):
    
    try:
        print(user_id)
        print(type(user_id))
        body['user_name']=userClass.query.get(user_id).user_name
        if body['company_id'] !=-1:

            body['company_name']= CompanyClass.query.get(body['company_id']).company_name
            body['company_mail']= 'None'
            body['field_name']= FieldClass.query.get(body['field_id']).field_name

        
        
        visit = VisitClass( user_id=user_id,user_name=body['user_name'],company_id=body['company_id'],company_name=body['company_name'],company_mail=body['company_mail'],field_name=body['field_name'],field_id=body['field_id'],published=False)
       
        
        db.session.add(visit)
        db.session.commit()

       
        return visit._id
    

    except Exception as e:
        print(e)
        return False
    
def updateVisit(user_id,visit_id,body):
    try:
        visit=VisitClass.query.get(visit_id)
        
        body['user_name']=userClass.query.get(user_id).user_name
        if body['company_id'] !=-1:

            body['company_name']= CompanyClass.query.get(body['company_id']).company_name
            body['company_mail']= 'None'
            body['field_name']= FieldClass.query.get(body['field_id']).field_name

        
        
        visit.user_id=user_id
        visit.user_name=body['user_name']
        visit.company_id=body['company_id']
        visit.company_name=body['company_name']
        visit.company_mail=body['company_mail']
        visit.field_name=body['field_name']
        visit.field_id=body['field_id']

        
        db.session.add(visit)
        db.session.commit()

       
        return visit._id
    

    except Exception as e:
        print(e)
        return False
    
def publishVisit(user_id,visit_id):
    try:
        visit=VisitClass.query.get(visit_id)
        
        

        
        
        visit.published=True

        db.session.add(visit)
        db.session.commit()

       
        return visit._id
    

    except Exception as e:
        print(e)
        return False
    
def deleteVisit(visit_id):
    try:
       
        #ToDo  tambien eliminar las task y objectives tasks
        VisitClass.query.filter_by(_id=visit_id).delete()


        
        
        db.session.commit()

       
        return True
    

    except Exception as e:
        print(e)
        return False



def getVisitInfo(visit_id):

    try:
       
        visit=VisitClass.query.get(visit_id)
        return visit_to_dict(visit)
    

    except Exception as e:
        print(e)
        return False

def visit_to_dict(visit):
    return {column.name: getattr(visit, column.name) for column in visit.__table__.columns}


def getVisitTasks(visit_id):

    try:
        
        tasks=VisitTaskClass.query.filter_by(visit_id=visit_id).all()
 
        visit_tasks=[]
        for visit in tasks:
            visit_tasks.append(visit._id)

       
        return visit_tasks
    

    except Exception as e:
        print(e)
        return False
    
def getVisits(user_id,companies):
    try:
        
        query="""SELECT _id,field_id,field_name,created_at as date, user_name as created_by
                FROM visits as v
                WHERE v.user_id = """+ str(user_id)+"""
                or v.company_id in """+ str(companies)+"""
                ORDER BY v._id DESC

                 
                
             """
        
        
        rows=[]
        with db.engine.begin() as conn:
            result = conn.execute(text(query)).fetchall()
            
            
            for row in result:
                row_as_dict = row._mapping
                
                rows.append(dict(row_as_dict))
            print(rows)
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


def createVisitTask(body):
    
    try:
        
        if 'end_date' not in body :
            body['end_date']=body.get('start_date')
        
        
        task=''
        if body.get('task_type_id')==1:
            print('aca')
            task = VisitTaskClass( visit_id=body.get('visit_id'), task_type_id=body.get('task_type_id'),date_start=body.get('date_start'),date_end=body.get('date_end'),plots=str(body.get('plots')),wetting=body.get('wetting'),observations=body.get('observations'))
            db.session.add(task)
        

            db.session.commit()
            print(task._id)
            
            taskObjective=   VisitTaskObjectivesClass(visit_task_id=task._id, objectives=str(body.get('objectives')),products=str(body.get('products')),dosage=str(process_nested_list(body.get('dosage'))),dosage_parts_per_unit=str(body.get('dosage_parts_per_unit')))
            db.session.add(taskObjective)
            db.session.commit()
        
    
        else:
            
            task = VisitTaskClass( visit_id=body.get('visit_id'), task_type_id=body.get('task_type_id'),date_start=body.get('date_start'),date_end=body.get('date_end'),plots=str(body.get('plots')),observations=body.get('observations'))
            db.session.add(task)
            db.session.commit()

        for plot in body.get('plots'):
            plot_task = PlotTasksClass(plot_id=plot,task_id=task._id,status_id=1,from_program=False)
            db.session.add(plot_task)
        db.session.commit()

        return task._id
    except Exception as e:
        print(e)
        return False
    

def updateVisitTask(task_id,body):
    
    try:
    
        task = VisitTaskClass.query.get(task_id)

        if task is None:
            return False
        
        VisitTaskObjectivesClass.query.filter_by(visit_task_id=task._id).delete()

        plot_tasks=PlotTasksClass.query.filter_by(task_id=task._id)

        if body.get('task_type_id')==1:
            
            
            task.task_type_id=body.get('task_type_id')
            task.date_start=body.get('date_start')
            task.date_end=body.get('date_end')
            task.wetting=body.get('wetting')
            task.observations=body.get('observations')
            task.plots=str(body.get('plots'))
            db.session.add(task)
        

            db.session.commit()
            print(task._id)
            
            taskObjective=   VisitTaskObjectivesClass(visit_task_id=task._id, objectives=str(body.get('objectives')),products=str(body.get('products')),dosage=str(process_nested_list(body.get('dosage'))),dosage_parts_per_unit=str(body.get('dosage_parts_per_unit')))
            db.session.add(taskObjective)
            db.session.commit()
        

        else:
            task.task_type_id=body.get('task_type_id')
            task.date_start=body.get('date_start')
            task.date_end=body.get('date_end')
            task.wetting=None
            task.observations=body.get('observations')
            task.plots=str(body.get('plots'))

            db.session.add(task)
            db.session.commit()
        plots=body.get('plots')
        plots_with_task=[]
        for plot_task in plot_tasks:
            if plot_task.plot_id not in plots:
                db.session.delete(plot_task)
                db.session.commit()

                continue
            plots_with_task.append(plot_task.plot_id)

        print(plots_with_task)
        for plot in plots:
            if plot not in plots_with_task:
                print(plot)
                print(plot not in plots_with_task)
                plot_task = PlotTasksClass(plot_id=plot,task_id=task._id,status_id=1,from_program=False)
                db.session.add(plot_task)
        db.session.commit()




        return task._id
    except Exception as e:
        print(e)
        return False
    
def deleteVisitTask(task_id):
    try:
       
        if task_id is None:
            return False
        
        VisitTaskObjectivesClass.query.filter_by(visit_task_id=task_id).delete()
        db.session.commit()
        PlotTasksClass.query.filter_by(task_id=task_id).delete()
        db.session.commit()
        VisitTaskClass.query.filter_by(_id=task_id).delete()
        
        

        
        
        db.session.commit()

       
        return True
    

    except Exception as e:
        print(e)
        return False


def getVisitTaskInfo(visit_task_id):
    try:
        
        query="""SELECT vt.*,vto.objectives,vto.products,vto.dosage,vto.dosage_parts_per_unit 
                FROM visit_tasks as vt
                left join visit_task_objectives as vto on vto.visit_task_id=vt._id
                WHERE vt._id = """+ str(visit_task_id)+"""
                ORDER BY vt._id DESC

                 
                
             """
        
        
        rows=[]
        with db.engine.begin() as conn:
            result = conn.execute(text(query)).fetchall()
            
            
            for row in result:
                row_as_dict = row._mapping
                
                rows.append(dict(row_as_dict))
            

            if len(rows)>0:
                return rows[0]
            return False
        
        

    except Exception as e:
        print(e)
        return False


