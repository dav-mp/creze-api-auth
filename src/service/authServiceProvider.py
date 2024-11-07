from src.config import SdkAws, EnvsAwsSm

class AuthServiceProvider:

    sdk = None

    def __init__(self, sdkProvider: SdkAws) -> None:

        self.sdk = sdkProvider

        pass


    def getEnvsBySdk( self ):

        envs_aws_sm = EnvsAwsSm()  
        envs = envs_aws_sm.getEnvs() 

        print('AYUDAAAAAAAA')
        print(envs)

        pass
        # self.sdk
