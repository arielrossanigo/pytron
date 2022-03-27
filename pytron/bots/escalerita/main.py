import random

from pytron.bot import Bot, Action, Orientation

Adel = Action.Forward
Izqui = Action.Left
Derch = Action.Right

N = Orientation.North
S = Orientation.South
E = Orientation.East
O = Orientation.West


class PlayerBot(Bot):
    size = 90
    volviendo = False
    recta_inicial = 0
    giro = Derch

    def get_action(self, board):
        self.board = board
        camino = board.bots_path[self.id]
        x, y = self.xy

        siguiente = None
        if self.volviendo:
            siguiente = self.vuelve()

        elif self.toco_borde():
            siguiente = self.vuelve()

        else:
            siguiente = self.zigzag()

        if not self.chocaria(siguiente):
            return siguiente
        elif not self.chocaria(Izqui):
            siguiente = Izqui
        elif not self.chocaria(Derch):
            siguiente = Derch
        elif not self.chocaria(Adel):
            siguiente = Adel
        else:
            return siguiente  # La conch...
        return siguiente

    def vuelve(self):
        orientacion = self.board.bots_orientation[self.id]
        x, y = self.xy

        if self.inclinacion == 'ne':
            self.giro = Derch
        elif self.inclinacion == 'no':
            self.giro = Izqui
        elif self.inclinacion == 'so':
            self.giro = Derch
        elif self.inclinacion == 'se':
            self.giro = Izqui

        if not self.volviendo:
            self.volviendo = 1
            return self.giro
        elif self.volviendo == 1:
            self.volviendo = 2
            return self.giro
        elif self.volviendo == 2:
            self.volviendo = 3
            return self.giro
        elif self.volviendo == 3:
            self.volviendo = 4
            return self.zigzag()
        elif self.volviendo == 4:
            self.volviendo = 5
            return self.zigzag()
        # elif self.volviendo == 5:
        #     self.volviendo = 6
        #     return self.zigzag()
        else:
            self.volviendo = 0
            self.actualizar_inclinacion()
            return self.zigzag()

        return Izqui

    def zigzag(self):
        camino = self.board.bots_path[self.id]
        if len(camino) % 2:
            return Izqui
        else:
            return Derch

    def toco_borde(self, x=None, y=None):
        if not x or not y:
            x, y = self.xy
        return x == 1 or y == 1 or x == self.board_column_size - 1 or y == self.board_row_size - 1

    def chocaria(self, siguiente):
        delta = 2
        x, y = self.xy
        xd, yd = self.xy
        xd1, yd1 = self.xy
        if self.orientacion is N:
            if siguiente is Adel:
                y -= 1
                yd -= delta
                yd1 -= delta + 1
            elif siguiente is Derch:
                x += 1
                xd += delta
                xd1 += delta + 1
            elif siguiente is Izqui:
                x -= 1
                xd -= delta
                xd1 -= delta + 1
        if self.orientacion is O:
            if siguiente is Adel:
                x -= 1
                xd -= delta
                xd1 -= delta + 1
            elif siguiente is Derch:
                y -= 1
                yd -= delta
                yd1 -= delta + 1
            elif siguiente is Izqui:
                y += 1
                yd += delta
                yd1 += delta + 1
        if self.orientacion is S:
            if siguiente is Adel:
                y += 1
                yd += delta
                yd1 += delta + 1
            elif siguiente is Derch:
                x -= 1
                xd -= delta
                xd1 -= delta + 1
            elif siguiente is Izqui:
                x += 1
                xd += delta
                xd1 += delta + 1
        if self.orientacion is E:
            if siguiente is Adel:
                x += 1
                xd += delta
                xd1 += delta + 1
            elif siguiente is Derch:
                y += 1
                yd += delta
                yd1 += delta + 1
            elif siguiente is Izqui:
                y -= 1
                yd -= delta
                yd1 -= delta + 1
        all_positions = self.board.bots_path[self.id] + \
            list(self.board.used_positions)
        return (y, x) in all_positions or (yd, xd) in all_positions or (yd1, xd1) in all_positions \
            or self.toco_borde(xd, yd)

    @property
    def xy(self):
        camino = self.board.bots_path[self.id]
        y, x = camino[-1]
        return x, y

    @property
    def inclinacion(self):
        camino = self.board.bots_path[self.id]
        try:
            y1, x1 = camino[self.recta_inicial]
            y2, x2 = camino[self.recta_inicial+2]
            norte = y1 - y2 > 0
            oeste = x1 - x2 > 0
            if norte and oeste:
                return 'no'
            elif norte and not oeste:
                return 'ne'
            elif not norte and oeste:
                return 'so'
            elif not norte and not oeste:
                return 'se'
        except IndexError:
            return None

    def actualizar_inclinacion(self):
        init = len(self.board.bots_path[self.id])
        self.inclinacion_inicial = (init, init + 2)

    def contramano(self, action):
        if action is Derch:
            return Izqui
        else:
            return Derch

    @property
    def orientacion(self):
        return self.board.bots_orientation[self.id]
