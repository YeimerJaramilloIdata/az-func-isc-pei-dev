import os
import logging
import requests


class Mcsft():
    def __init__(self):
        # self.__client =  os.environ.get("APP_CLIENT_ID")
        self.__client = "Salesforce"
        # self.__secret = os.environ.get('APP_CLIENT_SECRET')
        self.__secret = "oL03m8Zr4*&^"
        self.__tenant = os.environ.get('TENANT_ID')
        self.__signendpoint = os.environ.get('SIGN_IN_POLICY_ENDPOINT')
        self.__urlgraph = os.environ.get('URL_GRAPH')
        self.__issuer = os.environ.get('ISSUER')


    def get_token_signup(self):
        try:
            data = {"grant_type":"client_credentials","client_id":self.__client,"scope":"https://graph.microsoft.com/.default","client_secret":self.__secret}
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            url = "https://x.docm.co/MicroClienttest/PEIContratos/oauth2/token"

            response= requests.post(url, data, headers)
            response = response.json()

            # #logging.warning(response)
            if response.get("error") == "access_denied":
                return {
                    'ok':False,
                    'message': "algo salio mal"
                }
            #logging.warning(response)
            return {
                'ok' : True,
                "message" : response.get('access_token')
            }
            # return response
        except Exception as e:
            logging.error(e)
            return None
