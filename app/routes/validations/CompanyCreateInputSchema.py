from marshmallow import Schema, fields, ValidationError
from marshmallow.validate import Length

class CompanyCreateInputSchema(Schema):
    """ /api/users - POST

    Parameters:
     - name: (str)
     - phone_region:  (str) 
     - phone_number:  (str) 
     
    """
    name = fields.Str(required=True, validate=Length(max=32))
    phone_region = fields.Str(required=False)
    phone_number = fields.Str(required=True)
