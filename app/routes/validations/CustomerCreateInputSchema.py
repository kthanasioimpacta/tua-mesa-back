from marshmallow import Schema, fields, validates, ValidationError, validate
from marshmallow.validate import Length, Range
import re

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


    # @validates('username')
    # def is_not_admin(self,value):
    #     if value == 'admin':
    #         raise ValidationError("Username already exists")

    # @validates('phone_region')
    # def is_valid_region(self,value):
        
    #     if not re.match(r'(\+[0-9]+\s*)', value):
    #         raise ValidationError("Invalid Phone Region Format")