from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)


user_schema = UserSchema()
