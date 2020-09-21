from marshmallow import Schema, fields, validates, ValidationError, validate
from marshmallow.validate import Length, Range
import re

class LineUpCreateInputSchema(Schema):
    """ /api/users - POST

    Parameters:
     - waiting_line_id: (str)
     - customer_id:  (int) 
     
    """
    waiting_line_id = fields.Int(required=True)
    customer_id = fields.Int(required=True)


    # @validates('username')
    # def is_not_admin(self,value):
    #     if value == 'admin':
    #         raise ValidationError("Username already exists")

    # @validates('phone_region')
    # def is_valid_region(self,value):
        
    #     if not re.match(r'(\+[0-9]+\s*)', value):
    #         raise ValidationError("Invalid Phone Region Format")