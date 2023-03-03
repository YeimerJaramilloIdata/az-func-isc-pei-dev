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
        mc = Mcsft()
        tk = mc.get_token_signup()

        if body is None:
            return func.HttpResponse(json.dumps({
                'ok':False,
                'message':"Debe de enviarle un cuerpo a la solicitud valido"
            }),status_code=404,mimetype='application/json')

        ids_metadata = body.get("idsMetadata")
        if ids_metadata is not None:
            ids_metadata = ids_metadata.split(",")

        tipo_proceso = body.get("tipoProceso")
        if tipo_proceso is not None:
            lista_tipo_proceso = ["1493", "1494"] #1493: Term sheet, 1494: LOI
            if str(tipo_proceso) not in lista_tipo_proceso:
                return func.HttpResponse(json.dumps({
                    'ok':False,
                    'message':"Debe ingresar un tipo de proceso valido"
                }),status_code=404,mimetype='application/json')
            
        periodo_gracia = body.get("periodoGracia")

        fecha_inicio_contrato = body.get("fechaInicioContrato")
        if fecha_inicio_contrato is not None:
            try:
                datetime.strptime(fecha_inicio_contrato, '%Y-%m-%d')
            except ValueError:
                return func.HttpResponse(json.dumps({
                    'ok':False,
                    'message':"Debe ingresar una fecha valida (AAAA-MM-DD)"
                }),status_code=404,mimetype='application/json')
            
        pdf = body.get("pdf")

        data = {
            "Elements": [{
                "ETId": "1",
                "ReplaceableMetaDataIds":  ids_metadata,
                "KeyMetaDataId": "441",
                "Values": [
                    {"Id": "441","Value": "111"},
                    {"Id": "87","Value": str(tipo_proceso)},
                    {"Id": "27","Value": "1140" if periodo_gracia else "1441"},
                    {"Id": "65","Value": fecha_inicio_contrato},
                    {"Id": "55","Value": f"file.pdf|||{pdf}"}
                ]
            }]
        }

        headers = {"Content-Type": "application/json",'Authorization': f"Bearer {tk.get('message')}"}
        url = "https://x.docm.co/MicroClienttest/PEIContratos/WebApi/Element/StoreSync"
        response = requests.post(url, json = data, headers = headers)
        response = response.json()

        logging.warning(response)
        return func.HttpResponse(json.dumps({
            'ok':True,
            'message':f"El proceso se ha completado correctamente"
        }),status_code=200,mimetype='application/json')
    except Exception as e:
        logging.error(e)
        return func.HttpResponse(json.dumps({
            'ok':False,
            'message':"algo salio mal por favor revisar con el area encargada"
        }),status_code=500,mimetype='application/json')
