

class Piece:

    def __init__(self, ident, color=None):
        self.color = color
        self.ident = ident
        self.type = None

    def __repr__(self):
        return self.color[0] + self.type.capitalize()[0]

    def __str__(self):
        return self.type


class NonePiece(Piece):

    def __init__(self, ident=None, color=None):
        super().__init__(ident, color)
        self.type = "__"

    def __repr__(self):
        return "__"

    def __str__(self):
        return "Object of type 'NonePiece'"

    @staticmethod
    def is_legal_move(*_):
        return False


class King(Piece):

    def __init__(self, ident, color=None):
        super().__init__(ident, color)
        self.type = "king"

    @staticmethod
    def is_legal_move(x_from, y_from, x_to, y_to):
        x_dir = abs(x_to - x_from)
        y_dir = abs(y_to - y_from)
        return max(x_dir, y_dir) == 1


class Queen(Piece):

    def __init__(self, ident, color=None):
        super().__init__(ident, color)
        self.type = "queen"

    @staticmethod
    def is_legal_move(x_from, y_from, x_to, y_to):
        x_dir = abs(x_to - x_from)
        y_dir = abs(y_to - y_from)
        return (x_dir == y_dir) | (x_dir == 0) | (y_dir == 0)


class Rook(Piece):

    def __init__(self, ident, color=None):
        super().__init__(ident, color)
        self.type = "rook"

    @staticmethod
    def is_legal_move(x_from, y_from, x_to, y_to):
        x_dir = abs(x_to - x_from)
        y_dir = abs(y_to - y_from)
        return (x_dir == 0) | (y_dir == 0)


class Bishop(Piece):

    def __init__(self, ident, color=None):
        super().__init__(ident, color)
        self.type = "bishop"

    @staticmethod
    def is_legal_move(x_from, y_from, x_to, y_to):
        x_dir = abs(x_to - x_from)
        y_dir = abs(y_to - y_from)
        return x_dir == y_dir


class Knight(Piece):

    def __init__(self, ident, color=None):
        super().__init__(ident, color)
        self.type = "knight"

    def __repr__(self):
        return self.color[0] + "N"

    @staticmethod
    def is_legal_move(x_from, y_from, x_to, y_to):
        x_dir = abs(x_to - x_from)
        y_dir = abs(y_to - y_from)
        return ((x_dir == 2) & (y_dir == 1)) | ((y_dir == 2) & (x_dir == 1))


class Pawn(Piece):

    def __init__(self, ident, color=None):
        super().__init__(ident, color)
        self.type = "pawn"

    def is_legal_move(self, x_from, y_from, x_to, y_to):
        x_dir = x_to - x_from
        y_dir = y_to - y_from if self.color == 'white' else y_from - y_to

        first_move = (y_from == 1) if self.color == 'white' else (y_from == 6)
        y_range = range(1, 3) if first_move else range(1, 2)

        return (y_dir in y_range) & (abs(x_dir) in range(0, 2))
