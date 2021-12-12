# -*- coding: utf-8 -*-
from datetime import datetime
import io
import time
import threading
from wsgiref.validate import validator
from wsgiref.simple_server import make_server

EXCHANGE_FILE = "./exchange.dat"


def update_exchange_file():
    """
    Ecrit la date dans un fichier toutes les 10 secondes
    Le fichier est créé si il n'existe pas.
    """
    print("Mise à jour du fichier")
    while True:
        with io.open(EXCHANGE_FILE, "w") as f:
            f.write(datetime.now().isoformat())
        time.sleep(10)


def simple_app(environ, start_response):
    """
    Lit le contenu du fichier et l'affiche
    """
    start_response('200 OK', [('Content-type', 'text/plain')])
    with io.open(EXCHANGE_FILE) as f:
        return [f.read().encode('utf-8')+"\n"]


if __name__ == '__main__':
    t = threading.Thread(target=update_exchange_file)
    t.start()

    httpd = make_server('', 8080, simple_app)
    print("Ecoute sur le port 8080....")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()
        t.join(timeout=1)
