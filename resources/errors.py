# Custom errors

class InternalServerError(Exception):
    pass


  
errors = {
    "InternalServerError": {
        "message": "Something was wrong",
        "status": 500
    }
}