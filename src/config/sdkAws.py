import boto3

class SdkAws:
    _instance = None

    def __init__(self) -> None:
        if SdkAws._instance is not None:
            raise Exception("Esta clase es un singleton. Usa el método getInstance() para obtener la instancia.")
        else:
            self.session = boto3.Session()  # Crear una sesión de boto3
            SdkAws._instance = self
            print("Sesión de Boto3 creada.", SdkAws._instance)

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = SdkAws()
        return cls._instance

    def get_session(self):
        return self.session
