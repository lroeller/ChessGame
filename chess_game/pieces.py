

class Piece:

    def __init__(self, color=None):
        self.color = color
        self.type = None

    def __repr__(self):
        return self.color[0] + self.type[0]

    def __str__(self):
        return self.type


class NonePiece(Piece):

    def __init__(self, color=""):
        super().__init__(color)
        self.type = "__"

    def __repr__(self):
        return "__"

    def __str__(self):
        return "Object of type 'NonePiece'"

    @staticmethod
    def is_legal_move(*_):
        return False


class King(Piece):

    def __init__(self, color=None):
        super().__init__(color)
        self.type = "King"

    @staticmethod
    def is_legal_move(x_from, y_from, x_to, y_to):
        x_dir = abs(x_from - x_to)
        y_dir = abs(y_from - y_to)
        return max(x_dir, y_dir) == 1

