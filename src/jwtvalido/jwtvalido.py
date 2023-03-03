import jwt
from datetime import datetime
import os


class JwtValidate:

    def valida_token_cuerpo(self, token):
        #valida estructura de token
        temp_token = "Bearer eyJ"
        tok = ""
        for i in range(0,10):
            tok = tok + token[i]
        
        if tok == temp_token:
            return True
        else:
            return False

    def jwt_validate(self, jwt_):
        if self.valida_token_cuerpo( jwt_):
            c1 = jwt_.split(' ')
            decoded = jwt.decode(c1[1], options={"verify_signature":False})
            timestamp = decoded.get('exp')
            audince = decoded.get('aud')
            dt_object = datetime.fromtimestamp(timestamp)
            currentDate = datetime.now()
            audi = os.environ.get('AUDINCE')
            if dt_object >= currentDate and audince == audi:
                return True
            else:
                return False
        else:
            return False

    


        