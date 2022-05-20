import pygame, sys, socket, pickle, time
from pygame.locals import *
from chessboard import Chessboard
from pieces.piece import Piece
from pieces.king import King
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.queen import Queen
import default_game as default

HOST = '127.0.0.1'
PORT = 42069

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))

p = s.recv(1024)
if p == b'0':
    p = s.recv(1024)
    if p == b'1':
        print("il secondo giocatore si è connesso")
else:
    if p == b'1':
        print("connesso come secondo giocatore")

p = s.recv(1024)

if p == b'white':
    print("colore: bianco")
    player_is_white = True
else:
    print("colore: nero")
    player_is_white = False

s.setblocking(False)    
s.settimeout(2)

size = width, height = 800, 720

colors = {'white': (255,255,255), 'black': (0,0,0), 'blue': (0,0,255), 'red': (255,0,0)}

grid = (8,8)
board = Chessboard((int((width-600))/2,int((height-600)/2)+30), grid, (75,75))
board.set_colors((75, 81, 152), (151, 147, 204))

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Sandretti\'s chess')
pygame.font.init()

default.reset_board_to_default_game(board)

  

clock = pygame.time.Clock()

running = True

white_check = False
black_check = False

is_white_turn = True
turn_switching = False

promoting = False
promoting_cell = (0,0)

dragging = False
starting = 0

moved_piece = (0,0)

last_move = []

mainfont = pygame.font.SysFont('arial', 50)

win = False
lost = False

while running:
    if win or lost:
        is_white_turn = not player_is_white
    
    if player_is_white ^ is_white_turn and not lost and not win:
        try:
            data_string = s.recv(4096)
        
            data = pickle.loads(data_string)

            if data[0] == 0:
                board.move_piece(data[2], data[3])
                turn_switching = True
                moved_piece = data[2]
                last_move = [data[2], data[3]]
            elif data[0] == 1:
                board.move_piece(data[2], data[3])
                moved_piece = data[2]
                last_move = [data[2], data[3]]
            elif data[0] == 2:
                if data[1] == 0:
                    board.add_piece(data[3], Queen(not player_is_white))
                elif data[1] == 1:
                    board.add_piece(data[3], Rook(not player_is_white))
                elif data[1] == 2:
                    board.add_piece(data[3], Bishop(not player_is_white))
                elif data[1] == 3:
                    board.add_piece(data[3], Knight(not player_is_white))
                turn_switching = True
            elif data[0] == 3:
                win = True
        except:
            pass
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not(player_is_white ^ is_white_turn): 
                if promoting:
                    # check which new pieces the users has selected
                    clicked_cell = board.get_cell_by_position(event.pos, True)
                    x = (clicked_cell[0]-promoting_cell[0], clicked_cell[1]-promoting_cell[1])
                    
                    if player_is_white:
                        cell_to_update = promoting_cell
                    else:
                        cell_to_update = (7-promoting_cell[0],7)

                    promoting = False
                    if x == (0,0):
                        if not player_is_white:
                            promoting_cell = ()
                        board.add_piece(cell_to_update, Queen(board.pieces[cell_to_update[0]][cell_to_update[1]].is_white))
                        data[1] = 0
                    elif x == (1,0):
                        board.add_piece(cell_to_update, Rook(board.pieces[cell_to_update[0]][cell_to_update[1]].is_white))
                        data[1] = 1                        
                    elif x == (0,1):
                        board.add_piece(cell_to_update, Bishop(board.pieces[cell_to_update[0]][cell_to_update[1]].is_white))
                        data[1] = 2
                    elif x == (1,1):
                        board.add_piece(cell_to_update, Knight(board.pieces[cell_to_update[0]][cell_to_update[1]].is_white))
                        data[1] = 3
                    else:
                        promoting = True

                    if not promoting:
                        data[0] = 2
                        data_string = pickle.dumps(data)
                        s.send(data_string)
                else:
                    clicked_cell = board.get_cell_by_position(event.pos, player_is_white)

                    if clicked_cell != None:
                        x = board.get_piece(clicked_cell)
                        if x != None:
                            #print(not(x.is_white ^ is_white_turn))
                            if not(x.is_white ^ is_white_turn):
                                dragging = True
                                starting_cell = clicked_cell
            elif event.button == 2:
                player_is_white = not player_is_white
        
        if event.type == pygame.MOUSEBUTTONUP:
            if(dragging):
                #print(starting_cell)
                dragging = False
                release_cell = board.get_cell_by_position(event.pos, player_is_white)
                if release_cell in board.get_piece_possibile_moves(starting_cell):
                    board.move_piece(starting_cell, release_cell)
                    turn_switching = True
                    moved_piece = release_cell
                    last_move = [starting_cell, release_cell]

                    data = [0,0,starting_cell, release_cell]
                    
                    x = board.check_for_promotion(player_is_white)
                        
                    if x != None:
                        promoting = True
                        promoting_cell = x
                        data[0] = 1
                    
                    data_string = pickle.dumps(data)
                    s.send(data_string)


    # --- UPDATE ---
    if not promoting and turn_switching:
        
        if board.check_for_checkmate(player_is_white):
            lost = True
            
            data = [3,0,(0,0), (0,0)]

            data_string = pickle.dumps(data)
            s.send(data_string)
            
        is_white_turn = not is_white_turn
        #player_is_white = is_white_turn
        turn_switching = False

    # --- RENDER ---
    screen.fill(colors['black'])
    board.render(screen)

    board.render_highlighted_cells(screen, player_is_white, last_move,(40,255,40))

    if dragging:
        pr = board.get_piece_possibile_moves(starting_cell)

        board.render_possibile_moves_cells(screen, player_is_white, pr)
        
        board.render_pieces(screen, player_is_white,[starting_cell])
        board.render_dragging_piece(screen, starting_cell, pygame.mouse.get_pos())
    else:
        board.render_pieces(screen, player_is_white)

    

    if promoting:
        board.render_promoting_ui(screen, player_is_white, promoting_cell)

    if lost:
        texts = mainfont.render("You lost!", False, (255,255,255))
    elif win:
        texts = mainfont.render("You win!", False, (255,255,255))
    else:
        if player_is_white ^ is_white_turn:
            texts = mainfont.render("It's your opponent's turn", False, (255,255,255))
        else:
            texts = mainfont.render("It's your turn", False, (255,255,255))  
    offset_x = int(texts.get_rect().width/2)
    
    screen.blit(texts,(int(width/2)-offset_x, 10))

    pygame.display.update()
    clock.tick(50)


pygame.quit()
sys.exit()