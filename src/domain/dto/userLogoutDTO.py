from marshmallow import Schema, fields, validate, ValidationError


class UserLogoutDTO(Schema):
    session = fields.String(required=True, validate=validate.Length( min=1 ))


    @staticmethod
    def createDTO( data ):
        schema = UserLogoutDTO()
        try:
            result = schema.load(data)
            print("Datos válidos:", result)
            return [None, result]
        except ValidationError as err:
            print("Errores de validación:", err.messages)
            return ["Error", err.messages]  