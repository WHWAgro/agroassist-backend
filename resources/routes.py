from .controllers.editProgram import EditProgramApi
from .controllers.programSelection import ProgramSendApi,ProgramFileApi,ProgramSelectionApi,ProgramApi,ProgramPublishApi
from .controllers.user import CreateUserApi,LoginUserApi,RecoverPasswordApi,ChangePasswordApi
from .controllers.tryc import CreationApi
from .controllers.others import TemplatesApi,OnboardingApi,MailApi,FieldsApi,FieldsListApi,TaskApi,TriggerTaskApi,PlotListApi, TaskOrderApi,TaskOrderTimeApi,DowloadTaskOrderApi,MachineryListApi,WorkersListApi
from .controllers.quoter import QuoterProductsApi,QuoterApi,QuoterInitApi,QuoterSelectionApi,PurchaseOrderApi,DowloadPurchaseOrderApi
from .controllers.calendar import CalendarApi,TaskInsApi,WeatherApi
from .controllers.fieldbook import FieldBookApi,FieldBookExportApi,FieldBookFullApi
from .controllers.visits import VisitApi,VisitListApi,VisitTaskApi,VisitPublishApi
from .controllers.company import CompanyVisibilityApi
from .controllers.additionalTasks import AdditionalTaskApi


def initialize_routes(api):
 

 
 # calendarizacion programa control fitosanitario


 api.add_resource(EditProgramApi, '/api/v1.0/program/edit')

 api.add_resource(ProgramSelectionApi, '/api/v1.0/program/selection')
 api.add_resource(ProgramPublishApi, '/api/v1.0/program/publish')




 api.add_resource(FieldsListApi, '/api/v1.0/company/fields')
 
 
 api.add_resource(ProgramApi, '/api/v1.0/program')

 api.add_resource(TaskApi, '/api/v1.0/moment')
 api.add_resource(TriggerTaskApi, '/api/v1.0/moment/trigger')
 

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
 api.add_resource(AdditionalTaskApi,'/api/v1.0/additional_task')


 api.add_resource(PlotListApi,'/api/v1.0/field/plot')


 api.add_resource(TaskOrderApi,'/api/v1.0/task/order')
 api.add_resource(TaskOrderTimeApi,'/api/v1.0/task/order/time')
 api.add_resource(DowloadTaskOrderApi,'/api/v1.0/task/order/download')

 api.add_resource(PurchaseOrderApi,'/api/v1.0/quoter/order')
 api.add_resource(DowloadPurchaseOrderApi,'/api/v1.0/quoter/order/download')
 api.add_resource(MachineryListApi,'/api/v1.0/field/machinery')
 api.add_resource(WorkersListApi,'/api/v1.0/field/workers')
 api.add_resource(FieldsApi,'/api/v1.0/field')

 api.add_resource(MailApi,'/api/v1.0/email/verify')


 api.add_resource(OnboardingApi,'/api/v1.0/field/plot/upload')

 api.add_resource(TemplatesApi,'/api/v1.0/templates/onboarding')

 
 api.add_resource(QuoterProductsApi,'/api/v1.0/quoter/products/download')

 api.add_resource(ProgramFileApi,'/api/v1.0/program/upload')
 api.add_resource(ProgramSendApi,'/api/v1.0/program/send')
 

 #fieldbook
 api.add_resource(FieldBookApi,'/api/v1.0/fieldbook/fields')
 api.add_resource(FieldBookFullApi,'/api/v1.0/fieldbook/full/download')
 api.add_resource(FieldBookExportApi,'/api/v1.0/fieldbook/export/download')

 ##visitas
 api.add_resource(VisitApi,'/api/v1.0/visit')
 api.add_resource(VisitListApi,'/api/v1.0/visit/list')
 api.add_resource(VisitTaskApi,'/api/v1.0/visit/task')
 api.add_resource(VisitPublishApi,'/api/v1.0/visit/publish')
 api.add_resource(CompanyVisibilityApi,'/api/v1.0/company/visibility')


 api.add_resource(RecoverPasswordApi,'/api/v1.0/recover_password')
 api.add_resource(ChangePasswordApi,'/api/v1.0/change_password')
 

 
 


 
 
 