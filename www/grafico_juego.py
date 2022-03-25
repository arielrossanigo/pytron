
from browser import document, console, window, timer
from browser.widgets.dialog import InfoDialog

colores = ['cyan', 'red', 'yellow']

partida = [
    [[0, 0], [9, 9],   [4, 5]],
    [[0, 1], [9, 8],  [5, 5]],
    [[1, 1], [8, 8], [6, 5]],
    [[1, 2], [8, 7], [7, 5]],
    [[1, 3], [8, 6], [8, 5]],
    [[1, 4], [8, 5], [9, 5]],
    [[1, 5], [7, 5], [9, 6]],
    [[1, 6], [7, 4], [9, 7]],
]

pixel = 15
velocidad = 500
largo = 10

canvas = document['juego']
ctx = canvas.getContext('2d')


intervalo = None

for turno in partida:
    for j in turno:
        j[0] = j[0] * pixel
        j[1] = j[1] * pixel

turno = 0

def dibujar(*args):
    global turno, partida, pixel

    turno = turno + 1

    if turno >= len(partida):
        finalizar()
        return

    for pos, jugador in enumerate(partida[turno-1]):
        ctx.fillStyle = colores[pos]
        ctx.fillRect(jugador[0], jugador[1], pixel-1, pixel-1)


def finalizar():
    timer.clear_interval(intervalo)
    InfoDialog('Ganó 👇', '¡¡ República autónoma de El Silbador !! 🍻🍻')

intervalo = timer.set_interval(dibujar, velocidad)

