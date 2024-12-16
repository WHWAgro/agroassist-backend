import json
from database.models.Program import VisitClass,db,auth,CompanyClass,FieldClass,userClass,VisitTaskClass,VisitTaskObjectivesClass,PlotTasksClass,AdditionalTaskClass,AdditionalTaskObjectivesClass
from sqlalchemy import  text,select
from flask import g
import jwt
import time
from sqlalchemy.orm import class_mapper
import ast
import uuid
import datetime

    
    









    
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


def createAdditionalTask(body,user_id):
    
    try:
        
        print(user_id)
        print(type(user_id))
        body['user_name']=userClass.query.get(user_id).user_name
        
        

        




        if 'end_date' not in body :
            body['end_date']=body.get('start_date')
        
        
        
        task=''
        rep_task=''
        if body.get('task_type_id')==1:
            print('aca')
            task = AdditionalTaskClass(  task_type_id=body.get('task_type_id'),date_start=body.get('date_start'),date_end=body.get('date_end'),plots=str(body.get('plots')),wetting=body.get('wetting'),observations=body.get('observations'),user_id=user_id,user_name=body['user_name'],company_id=body['company_id'],field_id=body['field_id'])
            db.session.add(task)


            db.session.commit()
            print(task._id)
            
            taskObjective=   AdditionalTaskObjectivesClass(additional_task_id=task._id, objectives=str(body.get('objectives')),objectives_name=str(body.get('objectives_name')),products_name=str(body.get('products_name')),products_ingredients=str(body.get('products_ingredients')),products=str(body.get('products')),dosage=str(process_nested_list(body.get('dosage'))),dosage_parts_per_unit=str(body.get('dosage_parts_per_unit')),reentry=body.get('reentry'),products_phis=str(body.get('products_phis')))
            db.session.add(taskObjective)
            db.session.commit()

            for plot in body.get('plots'):
                plot_task = PlotTasksClass(plot_id=plot,task_id=task._id,status_id=1,from_program=False,date_start=body.get('date_start'),date_end=body.get('date_end'),task_source=3)
                db.session.add(plot_task)
        
    
        else:
            
            if body.get('is_repeatable'):


                start_date = datetime.datetime.strptime(body.get('date_start'), '%Y-%m-%d')
                end_date = datetime.datetime.strptime(body.get('date_end'), '%Y-%m-%d')
                repeat_frequency = int(body.get('repeat_frequency'))
                repeat_unit = int(body.get('repeat_unit'))
                repeat_until = datetime.datetime.strptime(body.get('repeat_until'), '%Y-%m-%d')

                task = AdditionalTaskClass( repeat_frequency=repeat_frequency,repeat_unit=repeat_unit,repeat_until=repeat_until,is_repeatable=True, task_type_id=body.get('task_type_id'),date_start=start_date,date_end=end_date,plots=str(body.get('plots')),observations=body.get('observations'),user_id=user_id,user_name=body['user_name'],company_id=body['company_id'],field_id=body['field_id'])
                db.session.add(task)
                db.session.commit()
                for plot in body.get('plots'):
                    plot_task = PlotTasksClass(plot_id=plot,task_id=task._id,status_id=1,from_program=False,date_start=start_date,date_end=end_date,task_source=3)
                    db.session.add(plot_task)

                current_date = start_date
                while current_date <= repeat_until:
                    # Calculate the next date based on repeat_frequency and repeat_unit
                    if repeat_unit == 1:  # Days
                        current_date += datetime.timedelta(days=repeat_frequency)
                    elif repeat_unit == 2:  # Weeks
                        current_date += datetime.timedelta(weeks=repeat_frequency)
                   

                    # Check if the new date exceeds repeat_until
                    if current_date > repeat_until:
                        break

                    # Create a new task for the next occurrence
                    new_task = AdditionalTaskClass(
                        
                        task_type_id=body.get('task_type_id'),
                        date_start=current_date,
                        date_end=current_date + (end_date - start_date),  # Keep the same duration
                        plots=str(body.get('plots')),
                        observations=body.get('observations'),
                        main_additional_task_id=task._id,
                        repeat_frequency=repeat_frequency,
                        repeat_unit=repeat_unit,
                        repeat_until=repeat_until,
                        is_repeatable=True
                        ,user_id=user_id,
                        user_name=body['user_name'],
                        company_id=body['company_id'],
                        field_id=body['field_id']

                    )
                    db.session.add(new_task)
                    db.session.commit()

                    # Create PlotTasks for the new task
                    for plot in body.get('plots'):
                        plot_task = PlotTasksClass(
                            plot_id=plot,
                            task_id=new_task._id,
                            status_id=1,
                            from_program=False,
                            date_start=current_date,
                            date_end=current_date + (end_date - start_date),
                            task_source=3
                        )
                        db.session.add(plot_task)
                        rep_task=plot_task

                
            
            
            else:
                task = AdditionalTaskClass(  task_type_id=body.get('task_type_id'),date_start=body.get('date_start'),date_end=body.get('date_end'),plots=str(body.get('plots')),observations=body.get('observations'),user_id=user_id,user_name=body['user_name'],company_id=body['company_id'],field_id=body['field_id'])
                db.session.add(task)
                db.session.commit()
                for plot in body.get('plots'):
                    plot_task = PlotTasksClass(plot_id=plot,task_id=task._id,status_id=1,from_program=False,date_start=body.get('date_start'),date_end=body.get('date_end'),task_source=3)
                    db.session.add(plot_task)

        
        db.session.commit()

        return task._id,rep_task._id
    except Exception as e:
        print(e)
        return False


    


def updateAdditionalTask(task_id,body,user_id):
    
    try:
        body['user_name']=userClass.query.get(user_id).user_name
    
        task = AdditionalTaskClass.query.get(task_id)

        if task is None:
            return False
        
        AdditionalTaskObjectivesClass.query.filter_by(additional_task_id=task._id).delete()

        #----------------deleting repeating tasks
        repeating_tasks = AdditionalTaskClass.query.filter_by(main_additional_task_id=task_id).all()
        repeating_task_ids = [task._id for task in repeating_tasks]

        # Delete all repeating visit tasks and their associated PlotTasks
        PlotTasksClass.query.filter(
            PlotTasksClass.task_id.in_(repeating_task_ids),
            PlotTasksClass.from_program == False,
            PlotTasksClass.task_source==3
        ).delete()
      

        AdditionalTaskClass.query.filter(AdditionalTaskClass._id.in_(repeating_task_ids)).delete()

        #----------- deleting repeating tasks

        plot_tasks=PlotTasksClass.query.filter(
            PlotTasksClass.task_id==task._id,
            PlotTasksClass.from_program == False,
            PlotTasksClass.task_source==3
        ).delete()

        plots=body.get('plots')
        plots_with_task=[]
        



        if body.get('task_type_id')==1:
            
            
            task.task_type_id=body.get('task_type_id')
            task.date_start=body.get('date_start')
            task.date_end=body.get('date_end')
            task.wetting=body.get('wetting')
            task.observations=body.get('observations')
            task.plots=str(body.get('plots'))
            task.is_repeatable=False
            
            db.session.add(task)
        

            
            print(task._id)
            
            taskObjective=   AdditionalTaskObjectivesClass(additional_task_id=task._id, objectives=str(body.get('objectives')),products=str(body.get('products')),dosage=str(process_nested_list(body.get('dosage'))),dosage_parts_per_unit=str(body.get('dosage_parts_per_unit')),reentry=body.get('reentry'),products_phis=str(body.get('products_phis')))
            db.session.add(taskObjective)
            for plot in plots:
                if plot not in plots_with_task:
                    print(plot)
                    print(plot not in plots_with_task)
                    plot_task = PlotTasksClass(plot_id=plot,task_id=task._id,status_id=1,from_program=False,date_start=body.get('date_start'),date_end=body.get('date_end'),task_source=3)
                    db.session.add(plot_task)
            db.session.commit()
        

        else:

            

        
            task.task_type_id=body.get('task_type_id')
            task.date_start=body.get('date_start')
            task.date_end=body.get('date_end')
            task.wetting=None
            task.observations=body.get('observations')
            task.plots=str(body.get('plots'))
            task.is_repeatable=body.get('is_repeatable')
            task.repeat_frequency= None
            task.repeat_unit= None
            task.repeat_until= None

            
                
            for plot in plots:
                if plot not in plots_with_task:
                    print(plot)
                    print(plot not in plots_with_task)
                    plot_task = PlotTasksClass(plot_id=plot,task_id=task._id,status_id=1,from_program=False,date_start=body.get('date_start'),date_end=body.get('date_end'),task_source=3)
                    db.session.add(plot_task)
            
            if body.get('is_repeatable'):
                
                repeat_frequency = int(body.get('repeat_frequency'))
                repeat_unit = int(body.get('repeat_unit'))
                repeat_until = datetime.datetime.strptime(body.get('repeat_until'), '%Y-%m-%d')
                start_date = datetime.datetime.strptime(body.get('date_start'), '%Y-%m-%d')
                if 'end_date' not in body :
                    body['end_date']=body.get('start_date')
                end_date = datetime.datetime.strptime(body.get('date_end'), '%Y-%m-%d')
                
                task.repeat_frequency= repeat_frequency
                task.repeat_unit= repeat_unit
                task.repeat_until= repeat_until
                current_date = start_date
                while current_date <= repeat_until:
                    # Calculate the next date based on repeat_frequency and repeat_unit
                    if repeat_unit == 1:  # Days
                        current_date += datetime.timedelta(days=repeat_frequency)
                    elif repeat_unit == 2:  # Weeks
                        current_date += datetime.timedelta(weeks=repeat_frequency)
                   

                    # Check if the new date exceeds repeat_until
                    if current_date > repeat_until:
                        break

                    # Create a new task for the next occurrence
                    new_task = AdditionalTaskClass(
                        
                        task_type_id=body.get('task_type_id'),
                        date_start=current_date,
                        date_end=current_date + (end_date - start_date),  # Keep the same duration
                        plots=str(body.get('plots')),
                        observations=body.get('observations'),
                        main_additional_task_id=task._id,
                        repeat_frequency=repeat_frequency,
                        repeat_unit=repeat_unit,
                        repeat_until=repeat_until,
                        is_repeatable=True,
                        user_id=user_id,
                        user_name=body['user_name'],
                        company_id=body['company_id'],
                        field_id=body['field_id']

                    )
                    db.session.add(new_task)
                    db.session.commit()

                    # Create PlotTasks for the new task
                    for plot in body.get('plots'):
                        plot_task = PlotTasksClass(
                            plot_id=plot,
                            task_id=new_task._id,
                            status_id=1,
                            from_program=False,
                            date_start=current_date,
                            date_end=current_date + (end_date - start_date),
                            task_source=3
                        )
                        db.session.add(plot_task)
                
                
                

            db.session.add(task)
       
        
       
        db.session.commit()




        return task._id
    except Exception as e:
        print(e)
        return False
    



def getAdditionalTaskInfo(visit_task_id):
    try:
        
        query="""SELECT vt.*,vto.objectives,vto.products,vto.dosage,vto.dosage_parts_per_unit ,vto.reentry,vto.products_phis
                FROM additional_tasks as vt
                left join additional_task_objectives as vto on vto.additional_task_id=vt._id
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


