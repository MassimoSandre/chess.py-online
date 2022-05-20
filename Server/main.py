import socket
import random
import pickle
import time


HOST = '127.0.0.1'
PORT = 42069

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    player_1, addr_1 = s.accept()
    
    print('Player 1: ', addr_1)
    # I inform the player that he needs to wait for another player to join
    player_1.send(b'0')
    player_2, addr_2 = s.accept()
    
    print('Player 2: ', addr_2)
    # I inform the players that the game can now start
    player_1.send(b'1')
    player_2.send(b'1')
    
    # I make a random player White
    player_1_is_white = bool(random.getrandbits(1))

    # I tell both the player which color they are
    if player_1_is_white:
        player_1.send(b'white')
        player_2.send(b'black')
        player_1_turn = True
    else:
        player_1.send(b'white')
        player_2.send(b'black')
        player_1_turn = False

    white_turn = True
    finished = False

    while not finished:
        if player_1_turn:
            data_string = player_1.recv(128)
            print("ho ricevuto qualcosa")
            #time.Sleep(0.4)
            data = pickle.loads(data_string)
            if data[0] == -1:
                finished = True
            else:
                print("pic")
                #time.Sleep(0.4)
                
                player_2.send(data_string)
            
            print(data[0])
            #time.Sleep(0.4)
            if data[0]!=1:
                player_1_turn = False
        else:
            data_string = player_2.recv(128)
            print("ho ricevuto qualcosa")
            #time.Sleep(0.4)
            data = pickle.loads(data_string)
            if data[0] == -1:
                finished = True
            else:
                print("pic2")
                #time.Sleep(0.4)
                player_1.send(data_string)

            print(data[0])
            #time.Sleep(0.4)
            
            if data[0]!=1:
                player_1_turn = True

    player_1.close()
    player_2.close()


            
            