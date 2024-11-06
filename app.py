from flask import jsonify
import sys

from src.initApi import InitApi

if __name__ == "__main__":

    try:
        app = InitApi.createInstanceApi()
        app.run(debug=True)
    except Exception as e:
        print(e)
        sys.exit(e)        
