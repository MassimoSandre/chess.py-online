class Piece():
    def __init__(self, is_white):
        self.is_white = is_white
        self.is_promotable = False
        self.is_king = False

    def get_possibile_moves(self, chessboard, pos):
        return []

    def render(self, screen, pos, radius):
        pass