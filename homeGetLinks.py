import requests
from bs4 import BeautifulSoup
import sys
import os
import json
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


def buscarLinkRotos(internalLinks, validos):
    for link in internalLinks:
        if link in validos:
            print('OK: ', link)

        else:
            print('Roto!!!! ', link)


def startApp(conArgs):
    # Guardamos una copia de la pagina correcta, esto lo hacemos solo una vez
    """
    with open('data\\myh.html', 'w') as fHandle:
        fHandle.write(str(response.text))
    """


    # leemos el archivo md5.txt
    validos = []
    with open('data\sitiosValidos.txt', 'r') as fHandle:
        validos = [current_place.rstrip() for current_place in fHandle.readlines()]


    internalLinks = []

    # leemos el archivo md5.txt
    with open('data\md5.txt', 'r') as fHandle:
        datos = [current_place.rstrip() for current_place in fHandle.readlines()]
        pagina = datos[0]

        response = requests.get(pagina)
        soup = BeautifulSoup(response.content, 'html.parser')

        internalLinks = [
            a.get('href') for a in soup.find_all('a')
        ]

        buscarLinkRotos(internalLinks, validos)



def main(argv):
    parametros = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'twilio.ini'))
    with open(parametros, 'r') as f:
        conArgs = json.load(f)
    startApp(conArgs)


def init():
    if __name__ == '__main__':
        sys.exit(main(sys.argv))

init()




