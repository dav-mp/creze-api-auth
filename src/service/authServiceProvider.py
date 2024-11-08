# Importa SdkAws y EnvsAwsSm
from src.config import SdkAws, EnvsAwsSm
from src.domain.dto import UserRegisterDTO
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
