import pygame
from pieces.piece import Piece

class Rook(Piece):
    def __init__(self, is_white):
        Piece.__init__(self=self,is_white=is_white)
        if is_white:
            self.sprite = pygame.image.load('images/whiterook.png').convert_alpha()
        else:
            self.sprite = pygame.image.load('images/blackrook.png').convert_alpha()

    def get_possibile_moves(self, chessboard, pos):
        possibile_moves = []

        for i in range(pos[1]-1, -1, -1):
            if chessboard[pos[0]][i] == 0:
                possibile_moves.append((pos[0], i))
            else:
                if self.is_white ^ chessboard[pos[0]][i].is_white:
                    possibile_moves.append((pos[0], i))
                break

        for i in range(pos[1]+1, len(chessboard[pos[1]])):
            if chessboard[pos[0]][i] == 0:
                possibile_moves.append((pos[0], i))
            else:
                if self.is_white ^ chessboard[pos[0]][i].is_white:
                    possibile_moves.append((pos[0], i))
                break

        for i in range(pos[0]+1, len(chessboard)):
            if chessboard[i][pos[1]] == 0:
                possibile_moves.append((i, pos[1]))
            else:
                if self.is_white ^ chessboard[i][pos[1]].is_white:
                    possibile_moves.append((i, pos[1]))
                break

        for i in range(pos[0]-1, -1, -1):
            if chessboard[i][pos[1]] == 0:
                possibile_moves.append((i, pos[1]))
            else:
                if self.is_white ^ chessboard[i][pos[1]].is_white:
                    possibile_moves.append((i, pos[1]))
                break
        

        return possibile_moves

    def render(self, screen, pos):
        sprite_rect = self.sprite.get_rect(center=pos)
        screen.blit(self.sprite, sprite_rect)

