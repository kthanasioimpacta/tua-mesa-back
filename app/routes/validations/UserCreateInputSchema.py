from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length

class UserCreateInputSchema(Schema):
    """ /api/users - POST

    Parameters:
     - username: (str)
     - password:  (str)
     - email:  (str)
     - company_id: (int)
     - phone_number:  (str) 
     - role_id: (int) 
     
    """
    username = fields.Str(required=True, validate=Length(max=32))
    password = fields.Str(required=True)
    email = fields.Str(required=True)
    company_id = fields.Int(required=True)
    phone_number = fields.Str(required=True)
    role_id = fields.Int(required=True)

    @validates('username')
    def is_not_admin(self,value):
        if value == 'admin':
            raise ValidationError("Username already exists")
