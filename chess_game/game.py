from chess_game.board import Board
from chess_game.pieces import King


class Game:

    def __init__(self):
        white_pieces = {'K': King('white')}
        black_pieces = {'K': King('black')}
        self.pieces = {'white': white_pieces,
                       'black': black_pieces}

        self.board = Board()
        self.board.setup_pieces(self.pieces)
        self.board.draw_board()

    def play_game(self):
        while True:
            next_move = input("Move Piece").split(",")
            self.board.move_piece(*[int(i) for i in next_move])
            self.board.draw_board()

