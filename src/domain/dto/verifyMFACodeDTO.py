from marshmallow import Schema, fields, validate, ValidationError


class VerifyMFACodeDTO(Schema):
    email = fields.String(required=True, validate=validate.Email())
    session = fields.String(required=True, validate=validate.Length(min=1))
    userCode = fields.String(
        required=True, 
        validate=[validate.Length(equal=6), validate.Regexp(r'^\d{6}$')]  # Asegura que tenga 6 dígitos numéricos
    )

    @staticmethod
    def createDTO( data ):
        schema = VerifyMFACodeDTO()
        try:
            result = schema.load(data)
            print("Datos válidos:", result)
            return [None, result]
        except ValidationError as err:
            print("Errores de validación:", err.messages)
            return ["Error", err.messages]