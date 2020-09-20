from marshmallow import Schema, fields, validates, ValidationError, validate
from marshmallow.validate import Length, Range
import re

class WaitingLineCreateInputSchema(Schema):
    """ /api/users - POST

    Parameters:
     - name: (str)
     - company_id:  (int) 
     - is_priority:  (boolean) 
     
    """
    name = fields.Str(required=True, validate=Length(max=100))
    company_id = fields.Int(required=True)
    is_priority = fields.Bool(required=True)


    # @validates('username')
    # def is_not_admin(self,value):
    #     if value == 'admin':
    #         raise ValidationError("Username already exists")

    # @validates('phone_region')
    # def is_valid_region(self,value):
        
    #     if not re.match(r'(\+[0-9]+\s*)', value):
    #         raise ValidationError("Invalid Phone Region Format")