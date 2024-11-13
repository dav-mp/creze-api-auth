# Importa SdkAws y EnvsAwsSm
from src.config import SdkAws, EnvsAwsSm
from src.domain.dto import UserRegisterDTO, UserConfirmDTO, UserLoginDTO, ConfirmMFADTO, VerifyMFACodeDTO, UserLogoutDTO
import json

# Clase que funciona para consumir un SDK y poder conectar con los servicios de nuestro servicio externo de auth

class AuthServiceProvider:
    sdk = None
    envsCognito = None

    # En cuanto se crea una instancia de nuestra clase obtenemos nuestra instancia de BOTO3 y obtenemos las variables de entorno que las tenemos almacenadas en AWS SM
    def __init__(self, sdkProvider: SdkAws) -> None:
        self.sdk = sdkProvider
        envs_aws_sm = EnvsAwsSm()  
        self.envsCognito = envs_aws_sm.getEnvs() 

    # Metodo privado que transforma en diccionario las variables de entorno
    def _getEnvsCognito( self ):
        envs = json.loads(self.envsCognito)
        return envs

    # Obtiene la conexion con aws cognito
    def _getCognitoClient( self ):
        session = self.sdk.get_session()
        cognitoClient = session.client('cognito-idp', region_name='us-east-1')

        return cognitoClient
    
    def userRegister(self, user: UserRegisterDTO):

        try:
            # Obtenemos variables de AWS SM
            envs = json.loads(self.envsCognito)

            # Creamos una conexion con AWS mediante credenciales
            session = self.sdk.get_session()

            # Conectamos con AWS cognito
            cognitoClient = session.client('cognito-idp', region_name='us-east-1')

            # Metodo para crear un usaruio en AWS cognito
            response = cognitoClient.sign_up(
                ClientId=envs["CLIENT_ID"],
                Username=user["email"], 
                Password=user["password"],
                UserAttributes=[
                    {'Name': 'email', 'Value': user["email"]},
                    {'Name': 'name', 'Value': user["name"]}  
                ]
            )

            return response
        except cognitoClient.exceptions.UsernameExistsException:
            return {"error": "Email already exists"}, 400
        except Exception as e:
            return {"error": str(e)}, 500
        
    def userConfirm( self, user: UserConfirmDTO ):

        # Obtenemos variables de AWS SM
        envs = json.loads(self.envsCognito)

        # Creamos una conexion con AWS mediante credenciales
        session = self.sdk.get_session()

        # Conectamos con AWS cognito
        cognitoClient = session.client('cognito-idp', region_name='us-east-1')

        try:
            response = cognitoClient.confirm_sign_up(
                ClientId=envs["CLIENT_ID"],
                Username=user["email"],
                ConfirmationCode=user["confirmationCode"]
            )
            print(response)
            return {"message": "User confirmed successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        
    def userLogin( self, user: UserLoginDTO ):

        # Obtenemos variables de AWS SM
        envs = self._getEnvsCognito()

        # Conectamos con AWS cognito
        cognitoClient = self._getCognitoClient()

        try:
            # Hace peticion para iniciar sesion de usario e iniciar proceso DE TOTP
            response = cognitoClient.initiate_auth(
                ClientId=envs["CLIENT_ID"],
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': user["email"],  
                    'PASSWORD': user["password"]
                }
            )
            # Inicia proceso de auth mediante TOTP
            if 'ChallengeName' in response and response['ChallengeName'] == 'MFA_SETUP':
                return {
                    **self.setupMFA( response["Session"] ),
                    "message": response['ChallengeName'],
                }, 200
            # Usuario autenticado
            return {
                "message": response['ChallengeName'],
                "session": response['Session']
            }, 200
        except cognitoClient.exceptions.NotAuthorizedException:
            return {"error": "Invalid credentials"}, 403
        except Exception as e:
            return {"error": str(e)}, 500
        
    def setupMFA( self, session: str ):

        # Conectamos con AWS cognito
        cognitoClient = self._getCognitoClient()

        try:
        # Inicia el proceso de configuración de MFA y obtiene el secreto TOTP
            response = cognitoClient.associate_software_token(Session=session)
            secretode = response['SecretCode']  # Este es el código secreto para configurar TOTP - QR
            return {"secretode": secretode, "session": response["Session"]}
        except Exception as e:
            return {"error": str(e)}, 500

    def confirmMFA( self, data: ConfirmMFADTO ):

        # Conectamos con AWS cognito
        cognitoClient = self._getCognitoClient()

        try:
            # Confirma el código TOTP ingresado por el usuario
            response = cognitoClient.verify_software_token(
                Session=data["session"],
                UserCode=data["userCode"]
            )
            if response['Status'] == 'SUCCESS':
                return {"message": "MFA setup complete", "response": response}, 200
            else:
                return {"error": "MFA setup failed"}, 400
        except cognitoClient.exceptions.CodeMismatchException:
            return {"error": "Invalid TOTP code"}, 403
        except Exception as e:
            return {"error": str(e)}, 500
        
    def verifyMfaCode( self, data: VerifyMFACodeDTO ):

        # Obtenemos variables de AWS SM
        envs = self._getEnvsCognito()

        # Conectamos con AWS cognito
        cognitoClient = self._getCognitoClient()

        try:
            response = cognitoClient.respond_to_auth_challenge(
                ClientId=envs["CLIENT_ID"],
                ChallengeName='SOFTWARE_TOKEN_MFA',
                Session=data["session"],
                ChallengeResponses={
                    'USERNAME': data["email"],  # Cambia esto al nombre de usuario
                    'SOFTWARE_TOKEN_MFA_CODE': data["userCode"]
                }
            )
            return response
        except cognitoClient.exceptions.NotAuthorizedException:
            return {"error": "Invalid TOTP code"}, 403
        except Exception as e:
            return {"error": str(e)}, 500
        
    def userLogout( self, session: UserLogoutDTO ):

        # Conectamos con AWS cognito
        cognitoClient = self._getCognitoClient()

        try:
            # Llamamos a global_sign_out para cerrar la sesión en Cognito
            response = cognitoClient.global_sign_out(
                AccessToken=session["session"]
            )
            return response, 200
        except cognitoClient.exceptions.NotAuthorizedException:
            return {"error": "The user is not authorized or token is invalid"}, 403
        except Exception as e:
            return {"error": str(e)}, 500

