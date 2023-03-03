import logging
import requests
import json

from ..src import Mcsft
from datetime import datetime

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
    except  Exception as e:
        body = None

    try:
        print(body)

        if body is None:
            return func.HttpResponse(json.dumps({
                'ok':False,
                'message':"Debe de enviarle un cuerpo a la solicitud valido"
            }),status_code=404,mimetype='application/json')
        
        ids_metadata = body.get("idsMetadata")
        if ids_metadata is not None:
            ids_metadata = ids_metadata.split(",")

        id_elemento_padre = body.get("idElementoPadre")
        if id_elemento_padre is not None:
            if not isinstance(id_elemento_padre, int):
                return func.HttpResponse(json.dumps({
                    'ok':False,
                    'message':"Debe ingresar un id de elemento padre valido"
                }),status_code=404,mimetype='application/json')

        tipo_documento = body.get("tipoDocumento")
        if tipo_documento is not None:
            if not isinstance(id_elemento_padre, int):
                return func.HttpResponse(json.dumps({
                    'ok':False,
                    'message':"Debe ingresar un tipo de documento numerico"
                }),status_code=404,mimetype='application/json')

            lista_tipo_documento = ["31", "32","33","34"] #1493: Term sheet, 1494: LOI
            if str(tipo_documento) not in lista_tipo_documento:
                return func.HttpResponse(json.dumps({
                    'ok':False,
                    'message':"Debe ingresar un tipo de documento valido"
                }),status_code=404,mimetype='application/json')
            
        nombre = body.get("nombre")
        correo = body.get("correo")
            
        mc = Mcsft()
        tk = mc.get_token_signup()

        data = {
            "Elements": [{
                "ETId": "1",
                "ReplaceableMetaDataIds":  ids_metadata,
                "KeyMetaDataId": "5",
                "ParentKeyMetaDataId":"441",
                "ParentEmbebedMetaData":"447",
                "ParentETId": id_elemento_padre, #
                "Values": [
                    {"Id": "5","Value": "0111"},#
                    {"Id": "6","Value": nombre}, #
                    {"Id": "10","Value": "Pais"}, #
                    {"Id": "7","Value": tipo_documento}, #
                    {"Id": "15","Value": correo}, #
                    {"Id": "411","Value": "111"}
                ]
            }]
        }

        headers = {
            "Content-Type": "application/json",
            'Authorization':f"Bearer {tk.get('message')}"
        }
        url = "https://x.docm.co/MicroClienttest/PEIContratos/WebApi/Element/StoreSync"
        response = requests.post(url, json = data, headers = headers)
        response = response.json()

        logging.warning(data)
        return func.HttpResponse(json.dumps({
            'ok':True,
            'message':f"El proceso se ha completado correctamente"
        }),status_code=200,mimetype='application/json')
    except  Exception as e:
        logging.error(e)
        return func.HttpResponse(json.dumps({
            'ok':False,
            'message':"algo salio mal por favor revisar con el area encargada"
        }),status_code=500,mimetype='application/json')
