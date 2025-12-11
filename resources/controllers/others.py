from flask import Response, request,send_file
from flask_restful import Resource
import json
from datetime import datetime
#import pandas as pd
#from get_project_root import root_path
from resources.errors import  InternalServerError
from database.models.Program import userClass,UserCompanyClass,ProgramClass,FieldClass,PlotClass,PlotTasksClass,MachineryClass,WorkersClass,db

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
           df = pd.read_excel(file, dtype=str)
           df.rename(columns = {df.columns[0]:'csg_code',df.columns[1]:'name',df.columns[2]:'size',df.columns[3]:'id_species',df.columns[4]:'variety'}, inplace = True)
           df['id_field']=int(id_field)
           
           print(df)

           for index, row in df.iterrows():
            id_species=1
            if row['id_species']=="Ciruelos":
               id_species=3
            if row['id_species']=="Frutillas":
               id_species=4
            if row['id_species']=="Arandanos":
               id_species=2
            if row['id_species']=="Moras":
               id_species=5
            if row['id_species']=="Frambuesas":
               id_species=6
            if row['id_species']=="Vides":
               id_species=7
            if row['id_species']=="Manzanas":
               id_species=8
            if row['id_species']=="Nogales":
               id_species=9
            if row['id_species']=="Avellanos":
               id_species=10
            if row['id_species']=="Almendros":
               id_species=11
            if row['id_species']=="Castaños":
               id_species=12
            if row['id_species']=="Duraznos":
               id_species=13
            if row['id_species']=="Kiwis":
               id_species=14

            new_data = PlotClass(
                  id_field=row['id_field'],
                  name=row['name'],
                  size=float(str(row['size']).replace(',','.')),
                  id_species=id_species,
                  variety=row['variety'],
                  csg_code=row['csg_code']
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
      user_id =  get_jwt_identity()
      
      
      

      access = UserCompanyClass.query.filter_by(user_id=user_id, company_id=program_id).first()
      if not access:
        response['status']=400
        response['message']=0
        return {'response': response}, 400
      
      fields = getFieldsWithUserAccess(program_id,access)
      
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
          print("Es general")
          
          if field is None: 
            response['status']=400
          else:
            field.field_name=body["general"].get('field_name')
            field.location = body["general"].get('location')
            field.latitude=body["general"].get('latitude')
            field.longitude=body["general"].get('longitude')
            field.sag_code=body["general"].get('sag_code')
            db.session.add(field)
            db.session.commit()
            location=updateFieldWeatherLocation(float(body["general"].get('latitude')),float(body["general"].get('longitude')),id_field)
            print(location)
            
            
        if "plots" in body:
          print("plots")
          field_plots=getFieldPlotsDetails(id_field)
          current_company=body["company_id"]
          if field_plots!=False: 
            id_current = [d["_id"] for d in field_plots]
            id_new =[d["_id"] for d in body["plots"]]
            
            for _id in id_current:
                if _id not in id_new:
                  PlotClass.query.filter_by(_id=_id).delete()
                  delete_program_tasks_plot(_id)
            
            
            for plot in body["plots"] :
                _id=None
                
                print("plot")
                if '_id' in plot:
                  _id=plot['_id']
               
                user_id =  get_jwt_identity()
                
                if _id is None:
                   print("nuevo plot")
                   if ("id_program" not in plot) or (plot["id_program"]==""):
                      plot["id_program"]=None
                   size=float(str(plot['size']).replace(',','.'))

                   if 'csg_code' in plot:
                    print('csg_code')
                    plot_instance = PlotClass(id_field=id_field,name =plot['name'],size=size,id_species=plot['id_species'],variety=plot['variety'],id_program=plot['id_program'],id_phenological_stage=plot['id_phenological_stage'],csg_code=plot['csg_code'])
                   else:
                    print('no csg_code')
                    plot_instance = PlotClass(id_field=id_field,name =plot['name'],size=size,id_species=plot['id_species'],variety=plot['variety'],id_program=plot['id_program'],id_phenological_stage=plot['id_phenological_stage'])
                   
                   db.session.add(plot_instance)
                   db.session.commit()
                   if plot["id_program"]!=None:
                    print("no hay problema willy")
                    add_program_tasks_plot(plot["id_program"],plot_instance._id,user_id,current_company)
                   
                elif _id not in id_current:
                   print("no existte")
                   continue
                else:
                   print("existe")
                   plot_instance = PlotClass.query.get(_id)
          
                   if plot_instance is None: 
                    response['status']=400
                   else:
                      size=float(str(plot['size']).replace(',','.'))
                      plot_instance.name=plot.get('name')
                      plot_instance.size = size
                      plot_instance.id_species=plot.get('id_species')
                      if 'csg_code' in plot:
                        
                        plot_instance.csg_code=plot.get('csg_code')
                      print(plot_instance.id_program)
                      print(plot.get('id_program'))
                      print("----")
                      if plot_instance.id_program != plot.get('id_program'):
                         delete_program_tasks_plot(plot_instance._id)
                         #hay que ver que pasa con las tasks ya completadas
                         add_program_tasks_plot(plot["id_program"],plot_instance._id,user_id,current_company)
                      
                      plot_instance.variety=plot.get('variety')
                      plot_instance.id_program=plot.get('id_program')
                      plot_instance.id_phenological_stage = plot.get('id_phenological_stage')
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
                   machine_size=float(str(machine_size).replace(',','.'))
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
          for plot in field_plots:
             plot["idPhenologicalStage"]=plot["id_phenological_stage"]
             del(plot["id_phenological_stage"])
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
            print("-------------chao2")
            response['data']=data

            return {'response': response}, 200
        
        else: 
            
            return {'response': response}, 400

    except Exception as e:
      print(e)
      response['message']=2
      response['status']=500
      return {'response': response},500
    

class TriggerTaskApi(Resource):
   
  @jwt_required()
  def post(self):
  
    try:
        response={}
        response['status']=200
        response['message']=0
        body = request.get_json()

        

         
        
        ####
        
        program_id=body.get('program_id')
        moment_id=body.get('moment_id')
        date_start=body.get('date_start')
        date_end=body.get('date_end')
        
        plots=body.get('plots')
        user_id =  get_jwt_identity()
        

        company_id=getUserCompanies(user_id)[0]["_id"]

        print(company_id)
        updatePlotTasksTrigger(moment_id,company_id,date_start,date_end,plots)
    
         

        ##create_tasks =  createTasks(id_program,body_update)
        #####
      
        data={}
        data['id_moment']=moment_id
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
            products_name=ast.literal_eval(task['products_name'])
            products_ingredients=ast.literal_eval(task['products_ingredients'])
            
            
            products_phis=[]
            if task['products_phis']==None:
              products_phis=replace_values_ast(products_name, task["phi"])
            else:
              products_phis=ast.literal_eval(task['products_phis'])
            objectives_name= task['objective_name']
            
            dosage_parts_per_unit=ast.literal_eval(task['dosage_parts_per_unit'])
            objectives= task['id_objective']
           
            if id in dic_result:
                dic_result[id]["objectives"].append(objectives)
                dic_result[id]["objectives_name"].append(objectives_name)
                dic_result[id]["products_name"].append(products_name)
                dic_result[id]["products_ingredients"].append(products_ingredients)
                dic_result[id]["products_phis"].append(products_phis)
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
                dic_result[id]["objectives_name"] = [objectives_name]

                dic_result[id]["products"] = [products]
                dic_result[id]["products_ingredients"] = [products_ingredients]
                dic_result[id]["products_phis"] = [products_phis]
                dic_result[id]["products_name"] = [products_name]
                dic_result[id]["dosage"] = [dosage]
                
                dic_result[id]["dosage_parts_per_unit"]=[dosage_parts_per_unit]
                
                dic_result[id]["wetting"] = task['wetting']
                dic_result[id]["reentry"] = task['reentry']
                dic_result[id]["phi"] = task['phi']
                dic_result[id]["observations"] = task['observations']
                dic_result[id]["is_repeatable"] = task['is_repeatable']
                dic_result[id]["repeat_frequency"] = task['repeat_frequency']
                dic_result[id]["repeat_unit"] = task['repeat_unit']
                if task['repeat_until'] is None:
                   dic_result[id]["repeat_until"] = None
                else:
                  dic_result[id]["repeat_until"] = str(task['repeat_until'])
                


      
        
        data={}
        tasks_format= [{'_id': id,'id_program': dict["id_program"],'id_moment_type': dict["id_moment_type"],'start_date': dict["start_date"],'end_date': dict["end_date"],'moment_value': dict["moment_value"] ,'objectives': dict["objectives"],"objectives_name":dict["objectives_name"],"products_name":dict["products_name"],"products_ingredients":dict["products_ingredients"],"products_phis":dict["products_phis"]   ,'products': list(filter(None,dict["products"])),'dosage': list(filter(None,dict["dosage"])),'dosage_parts_per_unit': list(filter(None,dict["dosage_parts_per_unit"])),'wetting': dict["wetting"],'reentry': dict["reentry"],'phi': dict["phi"],'observations':dict['observations'],"is_repeatable": dict['is_repeatable']
                ,"repeat_frequency":dict['repeat_frequency']
                ,"repeat_unit" :dict['repeat_unit']
               ,"repeat_until": dict['repeat_until']} for id, dict in dic_result.items()]
        
        
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
        print("task creada")
        print(task)

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

        if body.get('start_date') == 'None':
            body['start_date']=None
        if body.get('end_date') == 'None':
            body['end_date']=None

        if body.get('id_moment_type') == 4:
           body['start_date'] = None
           body['end_date'] = None  
        print('------******-----')
        id_moment=request.args.get('id_moment')
        moment,former_moment_type = updateMoment(id_moment,body)
        tasks = updateMomentTasks(id_moment,body,former_moment_type)


      
        data={}
        data['id_moment']=moment
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
        
        for plot in plots:
             plot["idPhenologicalStage"]=plot["id_phenological_stage"]
             del(plot["id_phenological_stage"])
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
        is_valid = validEmail(email)
        
        if exists== False:
          response['status']=400 
          response['message']=1
        

        data={}
        data['email']=4
        if len(exists)>0 and len(is_valid)>0:
           data['email']=1
        elif len(exists)==0 and len(is_valid)>0:
           data['email']=2
        elif len(exists)>0 and len(is_valid)==0:
           data['email']=3


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
        print('processing task order ------')
        taskOrderFile,new_task_id = generateTaskOrder(body)
        print("updating_taks_status")
        id_task=int(body['id_task'])
        task_updated=updateTaskIns(int(new_task_id),{'batch_update':True,'status':3})
        print(task_updated)
        print(taskOrderFile)

        print(taskOrderFile)
        if taskOrderFile== False or task_updated==False:
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
        
        taskOrderFile,current_plot = getTaskOrders(id_task)
        
           
           
        
        
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
      

class TaskOrderTimeApi(Resource):
  

    @jwt_required()
    def put(self):
    
      try:
        response={}
        response['status']=200
        response['message']=0
        

        body = request.get_json()
        to_id=request.args.get('task_order_id')
        taskOrderFile = updateTaskOrder(to_id,body)
      
        if taskOrderFile== False :
          response['status']=400 
          response['message']=1
        
        else:

          data={}
          data['task_order']=taskOrderFile
          response['data']=data
        
        if response.get('status') == 200:

          return {'response': response}, 200
        
        else: 
          response['status']=400
          
          return {'response': response}, 400

      except Exception as e:
        print(e)
        response['message']=2
        response['status']=500
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
      

