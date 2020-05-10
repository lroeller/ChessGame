from chess_game.pieces import NonePiece


class Board:

    def __init__(self):
        self.game_board = [[NonePiece() for i in range(8)] for j in range(8)]

    def setup_pieces(self, pieces):
        self.game_board[4][0] = pieces['white']['K']

    def draw_board(self):
        for file in self.game_board:
            print(file)

    def get_piece(self, x, y):
        return self.game_board[x][y]

    def move_piece(self, x_from, y_from, x_to, y_to):
        if not self.check_move(x_from, y_from, x_to, y_to):
            return False

        piece_to = self.game_board[x_to][y_to]
        self.game_board[x_to][y_to] = self.game_board[x_from][y_from]
        self.game_board[x_from][y_from] = piece_to

        return True

    def check_move(self, x_from, y_from, x_to, y_to):
        return self.get_piece(x_from, y_from).is_legal_move(x_from, y_from, x_to, y_to)
