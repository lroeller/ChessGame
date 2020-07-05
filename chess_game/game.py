from collections import Counter
from chess_game.board import Board
from chess_game.pieces import King, Queen, Rook, Bishop, Knight, Pawn, NonePiece


# TODO: pawn moves and captures (pawn capture diagonal only, En passant, pawn promotion),
#  Castling
class Game:

    def __init__(self):
        white_pieces = {'K': King('K', 'white'),
                        'Q': Queen('Q', 'white'),
                        'R1': Rook('R1', 'white'),
                        'R2': Rook('R2', 'white'),
                        'B1': Bishop('B1', 'white'),
                        'B2': Bishop('B2', 'white'),
                        'N1': Knight('N1', 'white'),
                        'N2': Knight('N2', 'white'),
                        'P1': Pawn('P1', 'white'),
                        'P2': Pawn('P2', 'white'),
                        'P3': Pawn('P3', 'white'),
                        'P4': Pawn('P4', 'white'),
                        'P5': Pawn('P5', 'white'),
                        'P6': Pawn('P6', 'white'),
                        'P7': Pawn('P7', 'white'),
                        'P8': Pawn('P8', 'white')
                        }
        black_pieces = {'K': King('K', 'black'),
                        'Q': Queen('Q', 'black'),
                        'R1': Rook('R1', 'black'),
                        'R2': Rook('R2', 'black'),
                        'B1': Bishop('B1', 'black'),
                        'B2': Bishop('B2', 'black'),
                        'N1': Knight('N1', 'black'),
                        'N2': Knight('N2', 'black'),
                        'P1': Pawn('P1', 'black'),
                        'P2': Pawn('P2', 'black'),
                        'P3': Pawn('P3', 'black'),
                        'P4': Pawn('P4', 'black'),
                        'P5': Pawn('P5', 'black'),
                        'P6': Pawn('P6', 'black'),
                        'P7': Pawn('P7', 'black'),
                        'P8': Pawn('P8', 'black')
                        }
        self.pieces = {'white': white_pieces,
                       'black': black_pieces}
        self.piece_count = {'white': Counter([str(i) for i in list(self.pieces['white'].values())]),
                            'black': Counter([str(i) for i in list(self.pieces['black'].values())])}

        self.turn = 'white'
        self.check = False

        self.board = Board()
        self.board.setup_pieces(self.pieces)
        self.history = []
        self.fifty_moves = 0

    def play_game(self):
        while True:

            if self.fifty_move_rule():
                print("50 moves without a piece capture or pawn move! The game ends in a draw!")
                self.board.draw_board()
                break
            elif self.threefold_repetition():
                print("Threefold repetition! The game ends in a draw!")
                self.board.draw_board()
                break
            elif self.insufficient_material():
                print("Insufficient Material! The game ends in a draw!")
                self.board.draw_board()
                break

            if self.board.in_check(self.pieces[self.turn]['K'], self.pieces[self.switch_turn()]):
                self.check = True
                if self.check_mate():
                    print("Checkmate! " + self.switch_turn().capitalize() + " won the game!")
                    self.board.draw_board()
                    break
                print(self.turn.capitalize() + " is in check!")
            else:
                self.check = False
                if self.check_mate():
                    print("Stalemate! The game ends in a draw!")
                    self.board.draw_board()
                    break

            print(self.turn.capitalize() + "'s turn:")
            self.board.draw_board()
            next_move = input("Move Piece").split(",")
            if not self.check_bounds(*[int(i) for i in next_move]):
                print("The provided coordinates are not on the chess board! Try again:")
                continue

            if not self.check_piece_color(int(next_move[0]), int(next_move[1])):
                print("You need to move your own pieces! Try again:")
                continue

            if not self.move_piece(*[int(i) for i in next_move]):
                print("Invalid move! Try again:")
                continue

            self.turn = self.switch_turn()

    def check_mate(self):
        squares = [[1 for i in range(8)] for j in range(8)]
        for piece in self.pieces[self.turn].values():
            for idx_x, file in enumerate(squares):
                for idx_y, square in enumerate(file):
                    piece_coords = self.board.get_coords(piece)
                    if self.move_piece(*piece_coords, idx_x, idx_y, dryrun=True):
                        return False

        return True

    def check_piece_color(self, x, y):
        return self.board.get_piece(x, y).color == self.turn

    @staticmethod
    def check_bounds(x_from, y_from, x_to, y_to):
        return all(x in range(0, 8) for x in [x_from, y_from, x_to, y_to])

    def fifty_move_rule(self):
        return self.fifty_moves >= 100

    def threefold_repetition(self):
        if not self.history:
            return False
        return True if self.history.count(self.history[-1]) >= 3 else False

    def insufficient_material(self):
        white = self.piece_count['white']
        black = self.piece_count['black']
        if any(white[x] > 0 for x in ['pawn', 'rook', 'queen']) | any(black[x] > 0 for x in ['pawn', 'rook', 'queen']):
            return False
        elif (white['bishop'] > 1) | (black['bishop'] > 1):
            return False
        elif (white['knight'] > 2) | (black['knight'] > 2):
            return False
        return True

    def move_piece(self, x_from, y_from, x_to, y_to, dryrun=False):
        if self.board.check_move(x_from, y_from, x_to, y_to):
            piece_capt = self.board.move_piece(x_from, y_from, x_to, y_to)
            if not isinstance(piece_capt, NonePiece):
                del self.pieces[piece_capt.color][piece_capt.ident]
                self.piece_count[piece_capt.color][str(piece_capt)] = \
                    self.piece_count[piece_capt.color][str(piece_capt)] - 1

            still_in_check = self.board.in_check(self.pieces[self.turn]['K'], self.pieces[self.switch_turn()])

            if still_in_check | dryrun:
                self.board.move_piece(x_to, y_to, x_from, y_from, piece_capt)
                if not isinstance(piece_capt, NonePiece):
                    self.pieces[piece_capt.color][piece_capt.ident] = piece_capt
                return not still_in_check
            else:
                piece_move = self.board.get_piece(x_to, y_to)
                self.add_history()
                if (not isinstance(piece_capt, NonePiece)) | isinstance(piece_move, Pawn):
                    self.fifty_moves = 0
                else:
                    self.fifty_moves += 1

            return True

        else:
            return False

    def add_history(self):
        flat_board = [repr(square) for file in self.board.game_board for square in file]
        self.history.append(', '.join(flat_board) + " " + self.turn)

    def switch_turn(self):
        if self.turn == 'white':
            return 'black'
        elif self.turn == 'black':
            return 'white'
        else:
            raise AssertionError("self.turn is neither 'black' nor 'white'")
