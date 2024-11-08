# Importa SdkAws y EnvsAwsSm
from src.config import SdkAws, EnvsAwsSm
from src.domain.dto import UserRegisterDTO, UserConfirmDTO
import json

class AuthServiceProvider:
    sdk = None
    envsCognito = None

    def __init__(self, sdkProvider: SdkAws) -> None:
        self.sdk = sdkProvider
        envs_aws_sm = EnvsAwsSm()  
        self.envsCognito = envs_aws_sm.getEnvs() 
    
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
