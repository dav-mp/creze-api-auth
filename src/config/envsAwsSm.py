import os
from botocore.exceptions import ClientError

from src.config import SdkAws


class EnvsAwsSm:

    _sdk = SdkAws.getInstance()

    def __init__(self) -> None:
        pass

    def getEnvs(self):
        
        # TODO: Quitar os.environ[ 'EnvsCognito' ] = 'CognitoEnvs' por testing
        os.environ[ 'EnvsCognito' ] = 'CognitoEnvs'

        secret_name = os.environ[ 'EnvsCognito' ]
        region_name = "us-east-1"

        # Create a Secrets Manager client
        session = self._sdk.session
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
            print(get_secret_value_response)
            secret = get_secret_value_response['SecretString']
            return secret
        except ClientError as e:
            # For a list of exceptions thrown, see
            # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
            raise e
