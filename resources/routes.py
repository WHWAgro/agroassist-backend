from .controllers.editProgram import EditProgramApi
from .controllers.programSelection import ProgramSelectionApi,ProgramApi,ProgramPublishApi
from .controllers.user import CreateUserApi,LoginUserApi
from .controllers.tryc import CreationApi
from .controllers.others import FieldsListApi,TaskApi



def initialize_routes(api):
 

 
 # calendarizacion programa control fitosanitario


 api.add_resource(EditProgramApi, '/api/v1.0/program/edit')

 api.add_resource(ProgramSelectionApi, '/api/v1.0/program/selection')
 api.add_resource(ProgramPublishApi, '/api/v1.0/program/publish')


 api.add_resource(FieldsListApi, '/api/v1.0/company/fields')
 
 
 api.add_resource(ProgramApi, '/api/v1.0/program')

 api.add_resource(TaskApi, '/api/v1.0/task')
 

 api.add_resource(CreateUserApi, '/api/v1.0/user')
 api.add_resource(LoginUserApi, '/api/v1.0/login')
 api.add_resource(CreationApi, '/api/v1.0/create')
 
 


 
 
 