# Importa SdkAws y EnvsAwsSm
from src.config import SdkAws, EnvsAwsSm
from src.domain.dto import UserRegisterDTO, UserConfirmDTO, UserLoginDTO
import json

class AuthServiceProvider:
    sdk = None
    envsCognito = None

    def __init__(self, sdkProvider: SdkAws) -> None:
        self.sdk = sdkProvider
        envs_aws_sm = EnvsAwsSm()  
        self.envsCognito = envs_aws_sm.getEnvs() 

    def _getEnvsCognito( self ):
        envs = json.loads(self.envsCognito)
        return envs

    def _getCognitoClient( self ):
        session = self.sdk.get_session()
        cognitoClient = session.client('cognito-idp', region_name='us-east-1')

        return cognitoClient
    
    def userRegister(self, user: UserRegisterDTO):

        try:
            envs = json.loads(self.envsCognito)

            session = self.sdk.get_session()
            cognitoClient = session.client('cognito-idp', region_name='us-east-1')

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

        envs = json.loads(self.envsCognito)
        session = self.sdk.get_session()
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

        envs = self._getEnvsCognito()
        cognitoClient = self._getCognitoClient()

        try:
            response = cognitoClient.initiate_auth(
                ClientId=envs["CLIENT_ID"],
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': user["email"],  
                    'PASSWORD': user["password"]
                }
            )
            print(response)
            if 'ChallengeName' in response and response['ChallengeName'] == 'MFA_SETUP':
                return {
                    **self.setupMFA( response["Session"] ),
                    "message": response['ChallengeName'],
                    "session": response["Session"]
                }, 200
            # Usuario autenticado
            return response['AuthenticationResult'], 200
        except cognitoClient.exceptions.NotAuthorizedException:
            return {"error": "Invalid credentials"}, 403
        except Exception as e:
            return {"error": str(e)}, 500
        
    def setupMFA( self, session: str ):

        cognitoClient = self._getCognitoClient()

        try:
        # Inicia el proceso de configuración de MFA y obtiene el secreto TOTP
            response = cognitoClient.associate_software_token(Session=session)
            secretode = response['SecretCode']  # Este es el código secreto para configurar TOTP - QR
            return {"secretode": secretode}
        except Exception as e:
            return {"error": str(e)}, 500

