from chess_game.pieces import NonePiece


class Board:

    def __init__(self):
        self.game_board = [[NonePiece() for i in range(8)] for j in range(8)]

    def setup_pieces(self, pieces):
        self.game_board[0][0] = pieces['white']['R1']
        self.game_board[1][0] = pieces['white']['N1']
        self.game_board[2][0] = pieces['white']['B1']
        self.game_board[3][0] = pieces['white']['Q']
        self.game_board[4][0] = pieces['white']['K']
        self.game_board[5][0] = pieces['white']['B2']
        self.game_board[6][0] = pieces['white']['N2']
        self.game_board[7][0] = pieces['white']['R2']
        self.game_board[0][1] = pieces['white']['P1']
        self.game_board[1][1] = pieces['white']['P2']
        self.game_board[2][1] = pieces['white']['P3']
        self.game_board[3][1] = pieces['white']['P4']
        self.game_board[4][1] = pieces['white']['P5']
        self.game_board[5][1] = pieces['white']['P6']
        self.game_board[6][1] = pieces['white']['P7']
        self.game_board[7][1] = pieces['white']['P8']
        self.game_board[0][7] = pieces['black']['R1']
        self.game_board[1][7] = pieces['black']['N1']
        self.game_board[2][7] = pieces['black']['B1']
        self.game_board[3][7] = pieces['black']['Q']
        self.game_board[4][7] = pieces['black']['K']
        self.game_board[5][7] = pieces['black']['B2']
        self.game_board[6][7] = pieces['black']['N2']
        self.game_board[7][7] = pieces['black']['R2']
        self.game_board[0][6] = pieces['black']['P1']
        self.game_board[1][6] = pieces['black']['P2']
        self.game_board[2][6] = pieces['black']['P3']
        self.game_board[3][6] = pieces['black']['P4']
        self.game_board[4][6] = pieces['black']['P5']
        self.game_board[5][6] = pieces['black']['P6']
        self.game_board[6][6] = pieces['black']['P7']
        self.game_board[7][6] = pieces['black']['P8']

    def draw_board(self):
        for file in self.game_board:
            print(file)

    def get_piece(self, x, y):
        return self.game_board[x][y]

    def get_coords(self, piece):
        flat_board = [piece for file in self.game_board for piece in file]
        idx = flat_board.index(piece)
        return idx // 8, idx % 8

    def move_piece(self, x_from, y_from, x_to, y_to, piece_revert=None):
        piece_to = self.game_board[x_to][y_to]
        self.game_board[x_to][y_to] = self.game_board[x_from][y_from]

        if piece_revert is not None:
            self.game_board[x_from][y_from] = piece_revert
        elif isinstance(piece_to, NonePiece):
            self.game_board[x_from][y_from] = piece_to
        else:
            self.game_board[x_from][y_from] = NonePiece()

        return piece_to

    def is_legal_move(self, piece, x_from, y_from, x_to, y_to):
        x_next = x_from + ((x_to - x_from) > 0) - ((x_to - x_from) < 0)
        y_next = y_from + ((y_to - y_from) > 0) - ((y_to - y_from) < 0)

        if ((x_next == x_to) & (y_next == y_to)) | (piece.type == "knight"):
            return piece.color != self.get_piece(x_to, y_to).color
        elif not isinstance(self.get_piece(x_next, y_next), NonePiece):
            return False
        else:
            return self.is_legal_move(piece, x_next, y_next, x_to, y_to)

    def check_move(self, x_from, y_from, x_to, y_to):
        piece = self.get_piece(x_from, y_from)
        legal_piece_move = piece.is_legal_move(x_from, y_from, x_to, y_to)
        legal_board_move = self.is_legal_move(piece, x_from, y_from, x_to, y_to)
        return legal_piece_move & legal_board_move

    def in_check(self, king, pieces):
        king_coords = self.get_coords(king)

        for piece in pieces.values():
            piece_coords = self.get_coords(piece)
            if self.check_move(*piece_coords, *king_coords):
                return True

        return False
