from .controllers.editProgram import EditProgramApi
from .controllers.programSelection import ProgramSelectionApi,ProgramApi,ProgramPublishApi
from .controllers.user import CreateUserApi,LoginUserApi
from .controllers.tryc import CreationApi
from .controllers.others import TemplatesApi,OnboardingApi,MailApi,FieldsApi,FieldsListApi,TaskApi,PlotListApi, TaskOrderApi,DowloadTaskOrderApi,MachineryListApi,WorkersListApi
from .controllers.quoter import QuoterApi,QuoterInitApi,QuoterSelectionApi,PurchaseOrderApi,DowloadPurchaseOrderApi
from .controllers.calendar import CalendarApi,TaskInsApi,WeatherApi



def initialize_routes(api):
 

 
 # calendarizacion programa control fitosanitario


 api.add_resource(EditProgramApi, '/api/v1.0/program/edit')

 api.add_resource(ProgramSelectionApi, '/api/v1.0/program/selection')
 api.add_resource(ProgramPublishApi, '/api/v1.0/program/publish')


 api.add_resource(FieldsListApi, '/api/v1.0/company/fields')
 
 
 api.add_resource(ProgramApi, '/api/v1.0/program')

 api.add_resource(TaskApi, '/api/v1.0/moment')
 

 api.add_resource(CreateUserApi, '/api/v1.0/user')
 api.add_resource(LoginUserApi, '/api/v1.0/login')
 api.add_resource(CreationApi, '/api/v1.0/create')


 api.add_resource(QuoterInitApi, '/api/v1.0/quoter/info')
 api.add_resource(QuoterApi, '/api/v1.0/quoter')
 api.add_resource(QuoterSelectionApi, '/api/v1.0/quoter/list')
 #api.add_resource(AlternativesApi, '/api/v1.0/quoter/alternatives')


 api.add_resource(CalendarApi,'/api/v1.0/calendar/info')
 api.add_resource(TaskInsApi,'/api/v1.0/calendar/task')
 api.add_resource(WeatherApi,'/api/v1.0/calendar/forecast')

 api.add_resource(PlotListApi,'/api/v1.0/field/plot')


 api.add_resource(TaskOrderApi,'/api/v1.0/task/order')
 api.add_resource(DowloadTaskOrderApi,'/api/v1.0/task/order/download')

 api.add_resource(PurchaseOrderApi,'/api/v1.0/quoter/order')
 api.add_resource(DowloadPurchaseOrderApi,'/api/v1.0/quoter/order/download')
 api.add_resource(MachineryListApi,'/api/v1.0/field/machinery')
 api.add_resource(WorkersListApi,'/api/v1.0/field/workers')
 api.add_resource(FieldsApi,'/api/v1.0/field')

 api.add_resource(MailApi,'/api/v1.0/email/verify')


 api.add_resource(OnboardingApi,'/api/v1.0/field/plot/upload')

 api.add_resource(TemplatesApi,'/api/v1.0/templates/onboarding')

 
 
 


 
 
 