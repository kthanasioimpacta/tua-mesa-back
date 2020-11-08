from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length

class WaitingLineCreateInputSchema(Schema):
    """ /api/users - POST

    Parameters:
     - name: (str)
     - is_priority:  (boolean) 
     
    """
    name = fields.Str(required=True, validate=Length(max=100))
    is_priority = fields.Bool(required=True)
