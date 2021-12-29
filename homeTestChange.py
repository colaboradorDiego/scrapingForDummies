import requests
import hashlib
import sys
import os
import json
from datetime import datetime
from twilio.rest import Client


def sendMessage(conArgs):
    account_sid = conArgs['api']['account']
    auth_token = conArgs['api']['token']
    twilioPhone = conArgs['phones']['twilio']
    diegoPhone = conArgs['phones']['diego']
    messaging_service_sid = conArgs['phones']['messagingService']

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="ALERTA!! CAMBIO EL MD5 DE MYH.COM.AR",
        # from_=twilioPhone,
        messaging_service_sid=messaging_service_sid,
        to=diegoPhone
    )
    print(message.sid)


def startApp(conArgs):

    # leemos el archivo md5.txt
    with open('data\md5.txt', 'r') as fHandle:
        datos = [current_place.rstrip() for current_place in fHandle.readlines()]
        pagina = datos[0]
        checksumOK = datos[1]

        response = requests.get(pagina)

        # Guardamos una copia de la pagina correcta, esto lo hacemos solo una vez
        """
        with open('data\\myh_.html', 'w') as fHandle:
            fHandle.write(str(response.text))
        """

        checksum = hashlib.sha256(str(response.text).encode('utf-8')).hexdigest()

        status = str(datetime.now())
        if checksum == checksumOK:
            status = status + " ** Todo bien\n"

        else:
            status = status + " ** Todo Mal\n"

        with open('data\status.log', 'a') as fLOG:
            fLOG.write(status)


def main(argv):
    parametros = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'twilio.ini'))
    with open(parametros, 'r') as f:
        conArgs = json.load(f)
    startApp(conArgs)


def init():
    if __name__ == '__main__':
        sys.exit(main(sys.argv))

init()




