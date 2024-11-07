import boto3

class SdkAws:

    _instance = None

    def getInstance():
        if SdkAws._instance is None:
            SdkAws
            return SdkAws._instance

        return SdkAws._instance
        

    def __init__(self) -> None:
        if SdkAws._instance is not None:
            return True
        else:
            self.createInstance()


    def createInstance():
        SdkAws._instance = boto3
        
