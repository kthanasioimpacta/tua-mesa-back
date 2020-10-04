from marshmallow import Schema, fields

class LineUpCreateInputSchema(Schema):
    """ /api/users - POST

    Parameters:
     - waiting_line_id: (str)
     - customer_id:  (int) 
     
    """
    waiting_line_id = fields.Int(required=True)
    customer_id = fields.Int(required=True)
