from .controllers.editProgram import EditProgramApi
from .controllers.programSelection import ProgramSelectionApi
from .controllers.user import CreateUserApi,LoginUserApi
from .controllers.tryc import CreationApi




def initialize_routes(api):
 

 
 # calendarizacion programa control fitosanitario


 api.add_resource(EditProgramApi, '/api/program/edit_program')

 api.add_resource(ProgramSelectionApi, '/api/program/program_selection')

 api.add_resource(CreateUserApi, '/api/create_user')


 api.add_resource(LoginUserApi, '/api/login')
 api.add_resource(CreationApi, '/api/create')
 


 
 
 