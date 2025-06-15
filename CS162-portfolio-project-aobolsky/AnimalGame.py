# Author: Andrew Obolsky
# GitHub username: aobolsky
# Date: 06/06/2025
# Description: Main Piece Class, it's subclasses, and Animal Game Class


class Piece:
    def __init__(self, color, name, direction, distance, locomotion):
        self._color = color
        self._name = name
        self._direction = direction
        self._distance = distance
        self._locomotion = locomotion

    def get_color(self):
        return self._color

    def get_name(self):
        return self._name

    def destination_is_valid(self, board, to_row, to_col):



        if not (0 <= to_row < 7 and 0 <= to_col < 7):
            return False





        destination_piece = board[to_row][to_col]
        if destination_piece is not None:
            if destination_piece.get_color() == self._color:
                return False
        return True


class Chinchilla(Piece):
    def __init__(self, color):
        super().__init__(color, "chinchilla", "diagonal", 1, "sliding")

    def can_move(self, board, from_row, from_col, to_row, to_col):
        if not self.destination_is_valid(board, to_row, to_col):
            return False
        if from_row == to_row and from_col == to_col:
            return False
        if (to_row == from_row + 1 or to_row == from_row - 1) and (to_col == from_col + 1 or to_col == from_col - 1):
            return True
        """Special movement"""
        if (to_row == from_row and (to_col == from_col + 1 or to_col == from_col - 1)) or (to_col == from_col and (to_row == from_row + 1 or to_row == from_row - 1)):
            return True
        return False


class Wombat(Piece):
    def __init__(self, color):
        super().__init__(color, "wombat", "orthogonal", 4, "jumping")

    def can_move(self, board, from_row, from_col, to_row, to_col):
        if not self.destination_is_valid(board, to_row, to_col):
            return False

        if from_row == to_row and from_col == to_col:
            return False

        if to_row == from_row and (to_col == from_col + 4 or to_col == from_col - 4):
            return True
        if to_col == from_col and (to_row == from_row + 4 or to_row == from_row - 4):
            return True
        """Special movement"""
        if (to_row == from_row + 1 or to_row == from_row - 1) and (to_col == from_col + 1 or to_col == from_col - 1):
            return True
        return False


class Emu(Piece):
    def __init__(self, color):
        super().__init__(color, "emu", "orthogonal", 3, "sliding")

    def can_move(self, board, from_row, from_col, to_row, to_col):
        if not self.destination_is_valid(board, to_row, to_col):
            return False

        if from_row == to_row and from_col == to_col:
            return False


        if from_row == to_row:
            if to_col - from_col > 3 or from_col - to_col > 3:
                return False
            if to_col > from_col:
                step = 1
            else:
                step = -1
            current = from_col + step
            while current != to_col:
                if board[from_row][current] is not None:
                    return False
                current += step
            return True

        if from_col == to_col:
            if to_row - from_row > 3 or from_row - to_row > 3:
                return False
            if to_row > from_row:
                step = 1
            else:
                step = -1
            current = from_row + step
            while current != to_row:
                if board[current][from_col] is not None:
                    return False
                current += step
            return True

        """Special movement"""
        if (to_row == from_row + 1 or to_row == from_row - 1) and (to_col == from_col + 1 or to_col == from_col - 1):
            return True

        return False


class Cuttlefish(Piece):
    def __init__(self, color):
        super().__init__(color, "cuttlefish", "diagonal", 2, "jumping")

    def can_move(self, board, from_row, from_col, to_row, to_col):
        if not self.destination_is_valid(board, to_row, to_col):
            return False

        if from_row == to_row and from_col == to_col:
            return False

        if (to_row == from_row + 2 or to_row == from_row - 2) and (to_col == from_col + 2 or to_col == from_col - 2):
            return True
        """Special movement"""
        if (to_row == from_row and (to_col == from_col + 1 or to_col == from_col - 1)) or (to_col == from_col and (to_row == from_row + 1 or to_row == from_row - 1)):
            return True
        return False


class AnimalGame:
    """Represents Animal Game"""

    def __init__(self):
        """Initialize Animal Game"""
        self._board = [[], [], [], [], [], [], []]

        self._board[0] = [None, None, None, None, None, None, None]
        self._board[1] = [None, None, None, None, None, None, None]
        self._board[2] = [None, None, None, None, None, None, None]
        self._board[3] = [None, None, None, None, None, None, None]
        self._board[4] = [None, None, None, None, None, None, None]
        self._board[5] = [None, None, None, None, None, None, None]
        self._board[6] = [None, None, None, None, None, None, None]

        self._board[0][0] = Chinchilla("Tangerine")
        self._board[0][1] = Wombat("Tangerine")
        self._board[0][2] = Emu("Tangerine")
        self._board[0][3] = Cuttlefish("Tangerine")
        self._board[0][4] = Emu("Tangerine")
        self._board[0][5] = Wombat("Tangerine")
        self._board[0][6] = Chinchilla("Tangerine")

        self._board[6][0] = Chinchilla("Amethyst")
        self._board[6][1] = Wombat("Amethyst")
        self._board[6][2] = Emu("Amethyst")
        self._board[6][3] = Cuttlefish("Amethyst")
        self._board[6][4] = Emu("Amethyst")
        self._board[6][5] = Wombat("Amethyst")
        self._board[6][6] = Chinchilla("Amethyst")

        self._game_state = "UNFINISHED"
        self._turn_color = "Tangerine"

    def get_game_state(self):
        """Returns game state"""
        return self._game_state

    def make_move(self, from_position, to_position):
        """Checks if game is still going, remaps position i.e. "b4" to column and row indexes, checks
        other conditions and sets up capture and turn order. Also finishes game."""
        if self._game_state != "UNFINISHED":
            return False


        col_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6}
        row_map = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6}



        from_col = col_map.get(from_position[0].lower())
        from_row = row_map.get(from_position[1])
        to_col = col_map.get(to_position[0].lower())
        to_row = row_map.get(to_position[1])

        if len(from_position) != 2 or len(to_position) != 2:
            return False

        if from_col is None or from_row is None or to_col is None or to_row is None:
            return False



        moving_piece = self._board[from_row][from_col]

        if moving_piece is None:
            return False

        if moving_piece.get_color() != self._turn_color:
            return False

        if not moving_piece.can_move(self._board, from_row, from_col, to_row, to_col):
            return False


        if self._board[to_row][to_col] != None:
            captured_piece = self._board[to_row][to_col]
            if captured_piece.get_name() == "cuttlefish":
                if self._turn_color == "Tangerine":
                    self._game_state = "TANGERINE_WON"
                else:
                    self._game_state = "AMETHYST_WON"

        """Move the piece"""
        self._board[to_row][to_col] = moving_piece
        """Clear position from where moving piece moved from"""
        self._board[from_row][from_col] = None



        if self._game_state == "UNFINISHED":
            if self._turn_color == "Tangerine":
                self._turn_color = "Amethyst"
            else:
                self._turn_color = "Tangerine"

        return True

    def print_board(self):
        for row in self._board:
            for piece in row:
                if piece is None:
                    print(".", end=" ")
                else:
                    print("X", end=" ")
            print()




# game = AnimalGame()
# move_result = game.make_move('c1', 'c4')
# move_result2 = game.make_move('c7', 'c4')
# move_result3 = game.make_move('d1', 'b3')
# move_result4 = game.make_move('b7', 'b3')
#
# state = game.get_game_state()
#
# print(state)
# game.print_board()
# print("Game state:", game.get_game_state())




