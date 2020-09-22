from marshmallow import Schema, fields, ValidationError
from marshmallow.validate import Length

class CustomerCreateInputSchema(Schema):
    """ /api/users - POST

    Parameters:
     - name: (str)
     - phone_number:  (str) 
     - decription:  (str) 
     - email:  (str)  

     
    """
    name = fields.Str(required=True, validate=Length(max=100))
    phone_number = fields.Str(required=True)
    description = fields.Str(required=False, validate=Length(max=100))
    email = fields.Str(required=False, validate=Length(max=100))
