
from browser import document, console, window, timer, ajax
from browser.widgets.dialog import InfoDialog
from javascript import JSON


# speed
# size
# steps
# score_board [('nombre', score)]

partida = None
largo = None
velocidad = None
score_board = None

pixel = 10
colores = ['cyan', 'red', 'yellow', 'green',
        'white', 'salmon', 'magenta', 'gray']

canvas = document['juego']
ctx = canvas.getContext('2d')

intervalo = None

turno = 0

def dibujar(*args):
    global turno, partida, pixel

    turno = turno + 1
    if turno >= len(partida):
        finalizar()
        return
    for pos, jugador in enumerate(partida[turno-1]):
        console.log(jugador)
        ctx.fillStyle = colores[pos]
        ctx.fillRect(jugador[0], jugador[1], pixel-1, pixel-1)


def finalizar():
    global intervalo, turno, score_board

    timer.clear_interval(intervalo)
    turno = 0
    mensaje = ''
    for score in score_board:
        nombre, puntos = score
        mensaje += '{}) {} <br>'.format(puntos, nombre)
    InfoDialog('Tabla de posiciones 👇', mensaje)

    
def on_complete(req):
    global partida, largo, velocidad, score_board, intervalo, pixel

    if req.status !=200 and req.status != 0:
        InfoDialog('Sin Archivo', 'No se encontró el archivo.')
    else:
        resp = JSON.parse(req.responseText)
        partida = resp['steps']
        for turno in partida:
            for j in turno:
                j[0] = j[0] * pixel
                j[1] = j[1] * pixel
        largo = resp['size']
        velocidad = resp['speed']
        score_board = resp['score_board']
        intervalo = timer.set_interval(dibujar, velocidad)


try:
    file = document.query['file']
except KeyError:
    InfoDialog('Sin Archivo', 'Parámetro "file" no especificado.')
else:
    req = ajax.ajax()
    req.bind('complete', on_complete)
    req.open('GET', file, True)
    req.set_header('content-type', 'application/json')
    req.send()

