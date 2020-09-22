from flask import request, jsonify
from app.routes.validations.errors.ValidationError import ValidationError
def handle_request_validation (schema):
    req_data = request.get_json()
    errors = schema.validate(req_data)
    error_list = []
    
    for k, v in errors.items():
      error_list.append({k: v})
    
    if len(error_list) > 0:
      raise ValidationError(expression='InputValidationError', message=error_list)