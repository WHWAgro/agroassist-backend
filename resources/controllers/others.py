from flask import Response, request,send_file
from flask_restful import Resource
import json
from datetime import datetime
#import pandas as pd
#from get_project_root import root_path
from resources.errors import  InternalServerError
from database.models.Program import ProgramClass,FieldClass,PlotClass,MachineryClass,WorkersClass,db
from resources.services.programServices import *
from resources.services.generatePDF import *
from flask_jwt_extended import jwt_required,get_jwt_identity,current_user
from sqlalchemy.orm import class_mapper
import pandas as pd



class OnboardingApi(Resource):
  

    @jwt_required()
    def post(self):
    
      try:
        response={}
        response['status']=200
        response['message']=0
        
        
        #print(request.files['id_file'].read().decode('utf-8')

        
        id_field=request.form['id_field']
        field_instance = FieldClass.query.get(id_field)
        print("hola")
        
        if field_instance is None: 
          response['status']=400 
          response['message']=1
          print("no existe")
        else:
           print("existe")
           file=request.files['file']
           df = pd.read_excel(file)
           df.rename(columns = {df.columns[0]:'name',df.columns[1]:'size',df.columns[2]:'id_species',df.columns[3]:'variety'}, inplace = True)
           df['id_field']=int(id_field)
           df['id_species']=1
           print(df)

           for index, row in df.iterrows():

            new_data = PlotClass(
                  id_field=row['id_field'],
                  name=row['name'],
                  size=float(str(row['size']).replace(',','.')),
                  id_species=1,
                  variety=row['variety']
                  # Add more columns as needed
              )
            print(new_data)
              # Add the new data to the database session
            db.session.add(new_data)

        # Commit the changes to the database
           db.session.commit()

        
        data={}
        data['id_field']=int(id_field)
        
        
        if response.get('status') == 200:
          response['data']=data
          return {'response': response}, 200
        
        else: 
          
          return {'response': response}, 400

      except Exception as e:
        print(e)
        response['status']=500
        response['message']=2
        return {'response': response},500

class FieldsListApi(Resource):
  

  @jwt_required()
  def get(self):
  
    try:
      response={}
      response['status']=200
      response['message']=0
      program_id=request.args.get('id_company')

      
      fields = getFields(program_id)
      
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
    
class FieldsApi(Resource):


  @jwt_required()
  def put(self):


   
        
        #TaskObjectivesClass.query.filter_by(id_task=task._id).delete()

        
        
       


    
        #for idx, objective in enumerate(body.get('objectives')):
          
          #taskObjective =  TaskObjectivesClass(id_task=task._id, id_objective=objective,id_product=str(body.get('products')[idx]),dosage=str(body.get('dosage')[idx]),dosage_parts_per_unit=str(body.get('dosage_parts_per_unit')[idx]))
          #db.session.add(taskObjective)
        #db.session.add(task)
        #db.session.commit()
  
    try:
        response={}
        response['status']=200
        response['message']=0
        data={}
        
        id_field=request.args.get('id_field')
        body = request.get_json()

        data['id_field']=id_field

        if "general" in body:
         
          field = FieldClass.query.get(id_field)
          
          if field is None: 
            response['status']=400
          else:
            field.field_name=body["general"].get('field_name')
            field.location = body["general"].get('location')
            field.latitude=body["general"].get('latitude')
            field.longitude=body["general"].get('longitude')
            db.session.add(field)
            db.session.commit()
            
            
        if "plots" in body:
          field_plots=getFieldPlotsDetails(id_field)
          if field_plots!=False: 
            id_current = [d["_id"] for d in field_plots]
            id_new =[d["_id"] for d in body["plots"]]
            
            for _id in id_current:
                if _id not in id_new:
                  PlotClass.query.filter_by(_id=_id).delete()
            
            
            for plot in body["plots"] :
                
                _id=plot['_id']
                print(_id)
                
                if _id is None:
                   if plot["id_program"]=="":
                      plot["id_program"]=None
                      
                   plot_instance = PlotClass(id_field=id_field,name =plot['name'],size=plot['size'],id_species=plot['id_species'],variety=plot['variety'],id_program=plot['id_program'])
                   db.session.add(plot_instance)
                elif _id not in id_current:
                   continue
                else:
                   plot_instance = PlotClass.query.get(_id)
          
                   if plot_instance is None: 
                    response['status']=400
                   else:
                      plot_instance.name=plot.get('name')
                      plot_instance.size = plot.get('size')
                      plot_instance.id_species=plot.get('id_species')
                      plot_instance.variety=plot.get('variety')
                      plot_instance.id_program=plot.get('id_program')
                      db.session.add(plot_instance)
            
                   
                   
            db.session.commit()
          else:
              response['status']=400

        if "admin_team" in body:
          print("admin")
          admin_workers=getFieldAdminTeamDetails(id_field)
          if admin_workers!=False: 
            id_current = [d["_id"] for d in admin_workers]
            id_new =[d["_id"] for d in body["admin_team"]]
            
            for _id in id_current:
                if _id not in id_new:
                  WorkersClass.query.filter_by(_id=_id).delete()
            
            
            for worker in body["admin_team"] :
                
                
                _id=worker['_id']
                print(_id)
                
                if _id is None:
                   print("hola")
                   worker_instance = WorkersClass(id_field=id_field,name =worker['name'],email=worker['email'],phone_number=worker['phone_number'],id_worker_type=worker['id_worker_type'])
                   db.session.add(worker_instance)
                elif _id not in id_current:
                   continue
                else:
                   worker_instance = WorkersClass.query.get(_id)
          
                   if worker_instance is None: 
                    response['status']=400
                   else:
                      worker_instance.name=worker.get('name')
                      worker_instance.email=worker.get('email')
                      worker_instance.phone_number=worker.get('phone_number')
                      worker_instance.id_worker_type=worker.get('id_worker_type')
                      db.session.add(worker_instance)     
                   
            db.session.commit()
          else:
              response['status']=400

          
        if "field_team" in body:
          print("field")
          field_workers=getFieldFieldTeamDetails(id_field)
          for f_w in body["field_team"]:
             if "_id" not in f_w:
                f_w["_id"]=None
          if field_workers!=False: 
            id_current = [d["_id"] for d in field_workers]
            id_new =[d["_id"] for d in body["field_team"]]
            
            for _id in id_current:
                if _id not in id_new:
                  WorkersClass.query.filter_by(_id=_id).delete()
            
            
            for worker in body["field_team"] :
                
                
                
                
                
                if '_id' not in worker or worker['_id'] is None:
                   _id=worker['_id']
                   print("hola")
                   worker_instance = WorkersClass(id_field=id_field,name =worker['name'],phone_number=worker['phone_number'],id_worker_type=3)
                   db.session.add(worker_instance)
                elif _id not in id_current:
                   continue
                else:
                   

                   _id=worker['_id']
                   worker_instance = WorkersClass.query.get(_id)
          
                   if worker_instance is None: 
                    response['status']=400
                   else:
                      worker_instance.name=worker.get('name')
                      worker_instance.phone_number=worker.get('phone_number')
                      db.session.add(worker_instance)     
                   
            db.session.commit()
          else:
              response['status']=400


        if "machinery" in body:
          field_machinery=getFieldMachineryDetails(id_field)
          if field_machinery!=False: 
            id_current = [d["_id"] for d in field_machinery]
            id_new =[d["_id"] for d in body["machinery"]]
            
            for _id in id_current:
                if _id not in id_new:
                  MachineryClass.query.filter_by(_id=_id).delete()
            
            
            for machine in body["machinery"] :
                
                machine_size=0
                if 'size' in machine:
                   machine_size =machine['size']
                _id=machine['_id']
                print(_id)
                
                if _id is None:
                   print("hola")
                   machine_instance = MachineryClass(id_field=id_field,name =machine['name'],model=machine['model'],id_machinery_type=machine['id_machinery_type'],size=machine_size)
                   db.session.add(machine_instance)
                elif _id not in id_current:
                   continue
                else:
                   machine_instance = MachineryClass.query.get(_id)
          
                   if machine_instance is None: 
                    response['status']=400
                   else:
                      machine_instance.name=machine.get('name')
                      machine_instance.model=machine.get('model')
                      machine_instance.id_machinery_type=machine.get('id_machinery_type')
                      machine_instance.size=machine_size
                      db.session.add(machine_instance)     
                   
            db.session.commit()
          else:
              response['status']=400

          
                        
                 
      
        
        data={'id_field':id_field}
        if response.get('status') == 200:
            response['data']=data

            return {'response': response}, 200
        
        else: 
            
            return {'response': response}, 400

    except Exception as e:
      print(e)
      response['message']=2
      response['status']=500
      return {'response': response},500
  

  @jwt_required()
  def post(self):
  
    try:
        response={}
        response['status']=200
        response['message']=0
        body = request.get_json()

        

        field = createField(body)    
      
      
        data={}
        data['id_field']=field
        response['data']=data
        
        if response.get('status') == 200:

            return {'response': response}, 200
        
        else: 
            
            return {'response': response}, 400

    except Exception as e:
      print(e)
      response['message']=2
      response['status']=500
      return {'response': response},500
    
  @jwt_required()
  def get(self):
  
    try:
        response={}
        response['status']=200
        response['message']=0
        data={}
        
        id_field=request.args.get('id_field')
        data['id_field']=id_field
        field_general=getFieldGeneralDetails(id_field)
        if len(field_general)>0: 
          data['general']=field_general[0]
        else:
           response['status']=400

        field_plots=getFieldPlotsDetails(id_field)
        if field_plots!=False: 
          data['plots']=field_plots
        else:
           response['status']=400

        field_admin_team=getFieldAdminTeamDetails(id_field)
        if field_admin_team!=False: 
          data['admin_team']=field_admin_team
        else:
           response['status']=400

        field_field_team=getFieldFieldTeamDetails(id_field)
        if field_field_team!=False: 
          data['field_team']=field_field_team
        else:
           response['status']=400

        field_machinery_team=getFieldMachineryDetails(id_field)
        if field_field_team!=False: 
          data['machinery']=field_machinery_team
        else:
           response['status']=400

      
      
       
        
        
        
        if response.get('status') == 200:
            response['data']=data

            return {'response': response}, 200
        
        else: 
            
            return {'response': response}, 400

    except Exception as e:
      print(e)
      response['message']=2
      response['status']=500
      return {'response': response},500
  

class TaskApi(Resource):
  

  @jwt_required()
  def get(self):
  
    try:
        response={}
        response['status']=200
        response['message']=0
        id_moment=request.args.get('id_moment')

        tasks=getTaskDetails(id_moment)

        
        
        dic_result = {}
        if tasks==False:
            response['status']=400
            response['message']=1
            response['data']={}
            return {'response': response}, 400
        for task in tasks:
            id = task['_id']
            products = ast.literal_eval(task['id_product'])
            dosage = ast.literal_eval(task['dosage'])
            
            dosage_parts_per_unit=ast.literal_eval(task['dosage_parts_per_unit'])
            objectives= task['id_objective']
            if id in dic_result:
                dic_result[id]["objectives"].append(objectives)
                dic_result[id]["products"].append(products)
                dic_result[id]["dosage"].append(dosage)
                
                dic_result[id]["dosage_parts_per_unit"].append(dosage_parts_per_unit)
            else:
                dic_result[id]={}
                dic_result[id]["id_program"] = task['id_program']
                dic_result[id]["id_moment_type"] = task["id_moment_type"] 
                dic_result[id]["start_date"] = str(task['start_date'])
                if 'end_date' in task:
                  dic_result[id]["end_date"] = str(task['end_date'])
                else:
                  dic_result[id]["end_date"] = str(task['start_date'])
                dic_result[id]["moment_value"] = task['moment_value']
                dic_result[id]["objectives"] = [objectives]
                dic_result[id]["products"] = [products]
                dic_result[id]["dosage"] = [dosage]
                
                dic_result[id]["dosage_parts_per_unit"]=[dosage_parts_per_unit]
                
                dic_result[id]["wetting"] = task['wetting']
                dic_result[id]["observations"] = task['observations']

        print(dic_result)



        
        data={}
        tasks_format= [{'_id': id,'id_program': dict["id_program"],'id_moment_type': dict["id_moment_type"],'start_date': dict["start_date"],'end_date': dict["end_date"],'moment_value': dict["moment_value"] ,'objectives': list(filter(None,dict["objectives"])) ,'products': list(filter(None,dict["products"])),'dosage': list(filter(None,dict["dosage"])),'dosage_parts_per_unit': list(filter(None,dict["dosage_parts_per_unit"])),'wetting': dict["wetting"],'observations':dict['observations']} for id, dict in dic_result.items()]
        
        
        if len(tasks_format)==0:
            response['status']=400
            response['message']=1
        
        else:
            task=tasks_format[0]
            data["moment_details"]=task
            
        
        

      
      


        response['data']=data
        
        if response.get('status') == 200:

            return {'response': response}, 200
        
        else: 
            
            return {'response': response}, 400

    except Exception as e:
      print(e)
      response['message']=2
      response['status']=500
      return {'response': response},500




  @jwt_required()
  def post(self):
  
    try:
        response={}
        response['status']=200
        response['message']=0
        body = request.get_json()

        products = body.get('products')

        task = createTask(body)   

        ####
        body_update={"program_details":["test"]} 
        id_program=body.get('id_program')
        user_id =  get_jwt_identity()
        

        programs,assigned_companies,tasks=getProgramDetails(user_id,id_program)

        body_update['assigned_companies']=[ d["_id"] for d in assigned_companies]
        print("body_update")
        print(body_update)
         

        create_tasks =  createTasks(id_program,body_update)
        #####
      
        data={}
        data['id_moment']=task
        response['data']=data
        
        if response.get('status') == 200:

            return {'response': response}, 200
        
        else: 
            
            return {'response': response}, 400

    except Exception as e:
      print(e)
      response['message']=2
      response['status']=500
      return {'response': response},500
    


  @jwt_required()
  def put(self):
  
    try:
        response={}
        response['status']=200
        response['message']=0
        body = request.get_json()

        

        id_moment=request.args.get('id_moment')
        task = updateTask(id_moment,body)    

      
        data={}
        data['id_moment']=task
        response['data']=data
        
        if response.get('status') == 200:

            return {'response': response}, 200
        
        else: 
            
            return {'response': response}, 400

    except Exception as e:
      print(e)
      response['message']=2
      response['status']=500
      return {'response': response},500
    

  @jwt_required()
  def delete(self):
  
    try:
      response={}
      response['status']=500
      response['status']=200
      response['message']=0
      

      
      id_moment=request.args.get('id_moment')

      
      deleted = deleteTask(id_moment)
      if deleted== False:
        response['status']=400 
        response['message']=1
      

      data={}
      response['data']=data
      
      if response.get('status') == 200:

        return {'response': response}, 200
      
      else: 
        
        return {'response': response}, 400

    except Exception as e:
      print(e)
      return {'response': response},500
    





class PlotListApi(Resource):
  

    @jwt_required()
    def get(self):
    
      try:
        response={}
        response['status']=200
        response['message']=0
        field_id=request.args.get('id_field')

        
        plots = getPlots(field_id)
        print("dsfadsfsfdf")
        
        if plots== False:
          response['status']=400 
          response['message']=1
        

        data={}
        data['plots']=plots
        response['data']=data
        
        if response.get('status') == 200:

          return {'response': response}, 200
        
        else: 
          
          return {'response': response}, 400

      except Exception as e:
        print(e)
        response['message']=2
        return {'response': response},500

class MailApi(Resource):
  

   
    def get(self):
    
      try:
        response={}
        response['status']=200
        response['message']=0
        email=request.args.get('email')

        
        exists = mailExists(email)
        
        
        if exists== False:
          response['status']=400 
          response['message']=1
        

        data={}
        data['email']=False
        if len(exists)>0:
           data['email']=True
        response['data']=data
        
        if response.get('status') == 200:

          return {'response': response}, 200
        
        else: 
          
          return {'response': response}, 400

      except Exception as e:
        print(e)
        response['message']=2
        return {'response': response},500     


class TaskOrderApi(Resource):
  

    @jwt_required()
    def post(self):
    
      try:
        response={}
        response['status']=200
        response['message']=0
        

        body = request.get_json()
        
        taskOrderFile = generateTaskOrder(body)
        
        if taskOrderFile== False:
          response['status']=400 
          response['message']=1
        
        else:

          data={}
          data['task_order']=taskOrderFile
          response['data']=data
        
        if response.get('status') == 200:

          return {'response': response}, 200
        
        else: 
          
          return {'response': response}, 400

      except Exception as e:
        print(e)
        response['message']=2
        return {'response': response},500
      
    @jwt_required()
    def get(self):
    
      try:
        response={}
        response['status']=200
        response['message']=0
        

        id_task= request.args.get('id_task')
        
        taskOrderFile = getTaskOrders(id_task)
        
        if taskOrderFile== False:
          response['status']=400 
          response['message']=1
        
        else:

          data={}
          data['task_orders']=taskOrderFile
          response['data']=data
        
        if response.get('status') == 200:

          return {'response': response}, 200
        
        else: 
          
          return {'response': response}, 400

      except Exception as e:
        print(e)
        response['message']=2
        return {'response': response},500
      

class DowloadTaskOrderApi(Resource):
  

    @jwt_required()
    def get(self):
    
      try:
        response={}
        response['status']=200
        response['message']=0
        

        
        
        
        file_path='files/'+request.args.get('file_name')
        
        
        if True:
           return send_file(file_path, as_attachment=True)
        
        else: 
          
          return {'response': response}, 400

      except Exception as e:
        print(e)
        response['message']=2
        return {'response': response},500
      

class MachineryListApi(Resource):
  

    @jwt_required()
    def get(self):
    
      try:
        response={}
        response['status']=200
        response['message']=0
        field_id=request.args.get('id_field')

        
        plots = getFieldMachinery(field_id)
        
        
        if plots== False:
          response['status']=400 
          response['message']=1
        

        data={}
        data['machinery']=plots
        response['data']=data
        
        if response.get('status') == 200:

          return {'response': response}, 200
        
        else: 
          
          return {'response': response}, 400

      except Exception as e:
        print(e)
        response['message']=2
        return {'response': response},500
      



class WorkersListApi(Resource):
  

    @jwt_required()
    def get(self):
    
      try:
        response={}
        response['status']=200
        response['message']=0
        field_id=request.args.get('id_field')

        
        plots = getFieldWorkers(field_id)
        
        
        if plots== False:
          response['status']=400 
          response['message']=1
        

        data={}
        data['workers']=plots
        response['data']=data
        
        if response.get('status') == 200:

          return {'response': response}, 200
        
        else: 
          
          return {'response': response}, 400

      except Exception as e:
        print(e)
        response['message']=2
        return {'response': response},500
      


      


class TemplatesApi(Resource):
  

    @jwt_required()
    def get(self):
    
      try:
        response={}
        response['status']=200
        response['message']=0
        

        
        
        
        file_path='files/onboarding/Agroassist_Plantilla_Onboarding.xlsx'
        
        
        
        if True:
           return send_file(file_path, as_attachment=True)
        
        else: 
          
          return {'response': response}, 400

      except Exception as e:
        print(e)
        response['message']=2
        return {'response': response},500
      

