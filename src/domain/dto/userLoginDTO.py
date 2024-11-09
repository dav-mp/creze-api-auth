from marshmallow import Schema, fields, validate, ValidationError

class UserLoginDTO(Schema):
    password = fields.String(
        required=True, 
        validate=[
            validate.Length(min=8),
            validate.Regexp(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)',
                error="Password must contain at least one lowercase letter, one uppercase letter, and one number"
            )
        ]
    )
    email = fields.String(required=True, validate=validate.Email())

    @staticmethod
    def createDTO( data ):
        schema = UserLoginDTO()
        try:
            result = schema.load(data)
            print("Datos válidos:", result)
            return [None, result]
        except ValidationError as err:
            print("Errores de validación:", err.messages)
            return ["Error", err.messages]  

